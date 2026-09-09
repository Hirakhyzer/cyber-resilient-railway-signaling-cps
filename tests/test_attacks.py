from railcps.cyber.attacks import AttackInjector
from railcps.cyber.telemetry import TelemetryPacket


def test_replay_buffer_does_not_cross_telemetry_sources():
    injector=AttackInjector(mode='replay',target='train:T1')
    train_old=TelemetryPacket('train:T1',1,0.0,{'block_id':'A1','position_m':10.0,'speed_mps':2.0})
    switch_old=TelemetryPacket('switch:SW1',1,0.0,{'position':'STRAIGHT'})
    injector.apply(train_old,0,False)
    injector.apply(switch_old,0,False)

    train_new=TelemetryPacket('train:T1',2,1.0,{'block_id':'A1','position_m':20.0,'speed_mps':3.0})
    replayed=injector.apply(train_new,1,True)

    assert replayed.source == 'train:T1'
    assert replayed.payload == train_old.payload


def test_freeze_buffer_is_scoped_to_target_source():
    injector=AttackInjector(mode='freeze',target='train:T1')
    first=TelemetryPacket('train:T1',1,0.0,{'block_id':'A1','position_m':10.0,'speed_mps':2.0})
    frozen=injector.apply(first,1,True)
    switch=TelemetryPacket('switch:SW1',1,1.0,{'position':'DIVERGE'})
    untouched=injector.apply(switch,1,True)

    assert frozen.source == 'train:T1'
    assert untouched.source == 'switch:SW1'
    assert untouched.payload['position'] == 'DIVERGE'
