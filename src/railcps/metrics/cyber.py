def classification_metrics(labels: list[int], alarms: list[int]) -> dict[str, float]:
    tp=sum(1 for y,p in zip(labels,alarms) if y==1 and p==1)
    fp=sum(1 for y,p in zip(labels,alarms) if y==0 and p==1)
    fn=sum(1 for y,p in zip(labels,alarms) if y==1 and p==0)
    tn=sum(1 for y,p in zip(labels,alarms) if y==0 and p==0)
    precision=tp/(tp+fp) if tp+fp else 0.0
    recall=tp/(tp+fn) if tp+fn else 0.0
    f1=2*precision*recall/(precision+recall) if precision+recall else 0.0
    fpr=fp/(fp+tn) if fp+tn else 0.0
    return {"precision":precision,"recall":recall,"f1":f1,"false_positive_rate":fpr,"tp":tp,"fp":fp,"fn":fn,"tn":tn}
