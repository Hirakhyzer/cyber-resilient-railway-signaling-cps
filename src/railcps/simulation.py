from dataclasses import dataclass
import random
from railcps.physical.block import Block
from railcps.physical.track import TrackNetwork
from railcps.physical.train import Train
from railcps.physical.railway import Railway
from railcps.physical.signal import Signal
from railcps.physical.switch import Switch
from railcps.signaling.route import Route
from railcps.signaling.interlocking import Interlocking
from railcps.signaling.movement_authority import movement_authority_blocks
from railcps.cyber.telemetry import TelemetryPacket
from railcps.cyber.network import Network
from railcps.cyber.freshness import FreshnessChecker
from railcps.cyber.attacks import AttackInjector
from railcps.twin.digital_twin import RailwayDigitalTwin
from railcps.twin.uncertainty import TwinUncertainty
from railcps.twin.residuals import train_residual
from railcps.security.detector import HybridDetector
from railcps.security.trust import TrustManager
from railcps.resilience.supervisor import ResilienceSupervisor
from railcps.resilience.recovery import RecoveryTracker
from railcps.operations.dispatcher import target_speed
from railcps.safety.invariants import evaluate_safety
from railcps.metrics.cyber import classification_metrics
from railcps.metrics.operations import service_metrics
from railcps.metrics.safety import safety_metrics
from railcps.metrics.resilience import resilience_score

SCENARIOS={
    "normal": ("none", None, 0.0),
    "position_spoof": ("position_spoof", "train:T1", 180.0),
    "velocity_spoof": ("velocity_spoof", "train:T1", 12.0),
    "occupancy_spoof": ("occupancy_spoof", "occupancy:B2", 0.0),
    "replay": ("replay", "train:T1", 0.0),
    "rewritten_replay": ("rewritten_replay", "train:T1", 0.0),
    "freeze": ("freeze", "train:T1", 0.0),
    "signal_falsification": ("signal_falsification", "signal:S2", 0.0),
    "switch_falsification": ("switch_falsification", "switch:SW1", 0.0),
    "packet_loss": ("none", None, 0.0),
    "high_latency": ("none", None, 0.0),
}

@dataclass
class SimulationResult:
    scenario: str
    metrics: dict
    records: list[dict]

def build_demo() -> tuple[Railway, Interlocking]:
    track=TrackNetwork()
    for bid in ["A1","A2","J","B1","B2","C1","C2"]:
        track.add_block(Block(bid, 300.0))
    track.connect("A1","A2"); track.connect("A2","J"); track.connect("J","B1"); track.connect("B1","B2");
    track.connect("C1","C2"); track.connect("C2","J")
    rail=Railway(track)
    rail.switches["SW1"]=Switch("SW1","STRAIGHT")
    rail.signals["S2"]=Signal("S2","J","RED")
    rail.add_train(Train("T1", ["A1","A2","J","B1","B2"]))
    rail.add_train(Train("T2", ["C1","C2","J","B1","B2"], max_speed_mps=18.0))
    routes={
      "R1":Route("R1",("A2","J","B1"),(("SW1","STRAIGHT"),),frozenset({"R2"})),
      "R2":Route("R2",("C2","J","B1"),(("SW1","DIVERGE"),),frozenset({"R1"})),
    }
    return rail, Interlocking(rail,routes)

def run_simulation(scenario: str="normal", steps: int=220, dt: float=1.0, seed: int=7) -> SimulationResult:
    if scenario not in SCENARIOS: raise ValueError(f"unknown scenario {scenario}")
    rail, interlocking=build_demo()
    mode,target,magnitude=SCENARIOS[scenario]
    loss=0.22 if scenario=="packet_loss" else 0.0
    delay=2.0 if scenario=="high_latency" else 0.0
    network=Network(loss_prob=loss, base_delay_s=delay, jitter_s=0.3 if scenario=="high_latency" else 0.0, rng=random.Random(seed))
    injector=AttackInjector(mode,target,magnitude)
    freshness=FreshnessChecker(); twin=RailwayDigitalTwin(); unc=TwinUncertainty(); detector=HybridDetector(); trust=TrustManager(); supervisor=ResilienceSupervisor(); recovery=RecoveryTracker()
    for t in rail.trains.values(): twin.initialize(t)
    sequence={}; records=[]; labels=[]; alarms=[]; safety_hist=[]; restricted_steps=0
    pending_meta: dict[int, tuple[int,str]]={}
    attack_start,attack_end=55,105
    for step in range(steps):
        now=step*dt
        for tid in ["T1","T2"]:
            train=rail.trains[tid]
            if train.completed: continue
            if tid=="T1": rail.switches["SW1"].set_position("STRAIGHT")
            elif rail.track.blocks["J"].clear and rail.track.blocks["B1"].clear and rail.trains["T1"].route_index>=3:
                rail.switches["SW1"].set_position("DIVERGE")
            authority=movement_authority_blocks(train, rail, 1)
            if train.route_index == len(train.route)-1:
                authority = 1
            desired=14.0 if tid=="T1" else 12.0
            current_trust=trust.get(f"train:{tid}")
            decision=supervisor.decide(current_trust, False, False, False)
            speed=target_speed(train, authority, min(decision.speed_cap_mps, desired))
            if tid=="T2" and train.route_index==1 and rail.trains["T1"].route_index < 3:
                speed=0.0
            rail.move_train(tid,speed,dt)
            twin.predict(tid, train.route, speed, dt)
        rail.signals["S2"].aspect = "GREEN" if rail.track.blocks["J"].clear else "RED"
        safety=evaluate_safety(rail,interlocking); safety_hist.append(safety)
        sources=[]
        for tid,train in rail.trains.items():
            if train.completed: continue
            sources.append((f"train:{tid}", {"block_id":train.block_id,"position_m":train.progress_m,"speed_mps":train.speed_mps}, "train"))
        for bid,block in rail.track.blocks.items():
            sources.append((f"occupancy:{bid}", {"block_id":bid,"occupied":int(not block.clear)}, "occupancy"))
        sources.append(("signal:S2", {"aspect":rail.signals["S2"].aspect}, "signal"))
        sources.append(("switch:SW1", {"position":rail.switches["SW1"].position}, "switch"))

        for src,payload,kind in sources:
            sequence[src]=sequence.get(src,0)+1
            packet=TelemetryPacket(src,sequence[src],now,payload)
            active=attack_start <= step < attack_end
            packet=injector.apply(packet,step,active)
            label=int(active and mode!="none" and (target is None or src==target))
            if not network.send(packet,now):
                labels.append(0); alarms.append(0); continue
            pending_meta[id(packet)]=(label,kind)

        for delivered in network.receive(now):
            label,kind=pending_meta.pop(id(delivered),(0,"unknown"))
            src=delivered.source
            fresh=freshness.check(delivered)
            if kind=="train":
                tid=src.split(":",1)[1]; ts=twin.states[tid]; res=train_residual(delivered.payload,ts,unc)
                result=detector.evaluate_train(src,res,fresh)
            else:
                if kind=="occupancy":
                    bid=src.split(":",1)[1]; expected={"block_id":bid,"occupied":int(not rail.track.blocks[bid].clear)}
                elif kind=="signal": expected={"aspect":rail.signals["S2"].aspect}
                elif kind=="switch": expected={"position":rail.switches["SW1"].position}
                else: continue
                result=detector.evaluate_discrete(src,expected,delivered.payload,fresh)
            new_trust=trust.update(src,result.score)
            recovered=recovery.update(src,result.alarm)
            safety_conflict=sum(safety.values())>0
            dec=supervisor.decide(new_trust,result.alarm,safety_conflict,recovered)
            if dec.state!="NORMAL": restricted_steps += 1
            labels.append(label); alarms.append(int(result.alarm))
            if kind=="train" and src=="train:T1":
                records.append({"step":step,"time_s":now,"source":src,"alarm":result.alarm,"score":round(result.score,3),"trust":round(new_trust,3),"state":dec.state,"attack":label,"telemetry_age_s":round(max(0.0,now-delivered.timestamp),3)})
    cyber=classification_metrics(labels,alarms); ops=service_metrics(rail.trains,steps*dt); safe=safety_metrics(safety_hist)
    restriction_fraction=restricted_steps/max(1,len(labels)); res_score=resilience_score(ops["completion_ratio"],sum(safe.values()),restriction_fraction)
    metrics={**cyber,**ops,**safe,"restriction_fraction":restriction_fraction,"resilience_score":res_score}
    if records:
        metrics["mean_t1_telemetry_age_s"]=sum(r["telemetry_age_s"] for r in records)/len(records)
    else:
        metrics["mean_t1_telemetry_age_s"]=0.0
    return SimulationResult(scenario,metrics,records)
