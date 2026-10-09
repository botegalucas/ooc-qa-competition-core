"""Recalculate only existing OOF metrics; no training or inference."""
from src.frozen_backend import audit_sources,read_csv
import json
def auc(rs):
 vals=sorted(rs,key=lambda r:float(r['p_pca_embedding_cpu']));pos=sum(int(r['y_true']) for r in vals);rank=0;i=0
 while i<len(vals):
  j=i+1
  while j<len(vals) and float(vals[j]['p_pca_embedding_cpu'])==float(vals[i]['p_pca_embedding_cpu']):j+=1
  rank+=sum(int(r['y_true']) for r in vals[i:j])*(i+1+j)/2;i=j
 return (rank-pos*(pos+1)/2)/(pos*(len(vals)-pos))
def metrics():
 audit_sources();rs=read_csv('OOF.csv');out=[]
 for t in [.5,.85,.9]:
  kept=[r for r in rs if max(float(r['p_pca_embedding_cpu']),1-float(r['p_pca_embedding_cpu']))>=t]
  ok=lambda r:int(float(r['p_pca_embedding_cpu'])>=.5)==int(r['y_true'])
  ba=sum(sum(ok(r) for r in kept if int(r['y_true'])==c)/sum(int(r['y_true'])==c for r in kept) for c in [0,1])/2
  out.append({'threshold':t,'N':len(kept),'coverage':len(kept)/len(rs),'AUC':auc(kept),'BA':ba,'accuracy':sum(ok(r) for r in kept)/len(kept),'groups':len({r['group_safe'] for r in kept})})
 return out
if __name__=='__main__':print(json.dumps(metrics(),indent=2))
