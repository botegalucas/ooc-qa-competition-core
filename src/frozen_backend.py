"""Minimal adaptation of the existing frozen artifact replay. No model execution."""
import csv,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OOF_SHA='554d0b2b1ba1c5d29ecfcd100915f40050de5b5a93a9c127b7797bc6c30c13e3'
REPLAY_NOTICE='Retrospective group-held-out OOF replay — not new-image inference.'
def read_csv(name):
 with (ROOT/'data'/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def audit_sources():
 p=ROOT/'data/OOF.csv'
 if hashlib.sha256(p.read_bytes()).hexdigest()!=OOF_SHA:raise ValueError('OOF hash mismatch')
 rows=read_csv('OOF.csv')
 if len(rows)!=3072 or len({r['imageID'] for r in rows})!=3072 or len({r['group_safe'] for r in rows})!=21:raise ValueError('Population/group contract failed')
 for r in rows:
  if not math.isfinite(float(r['p_pca_embedding_cpu'])) or not 0<=float(r['p_pca_embedding_cpu'])<=1:raise ValueError('Probability contract failed')
 for r in read_csv('IMAGES.csv'):
  if hashlib.sha256(image_path(r['imageID']).read_bytes()).hexdigest()!=r['sha256']:raise ValueError('Image hash mismatch')
 return {'status':'PASS','N':len(rows),'groups':21,'new_image_inference':False}
def image_path(image_id):
 if not image_id or Path(image_id).name!=image_id or any(x in image_id for x in ['..','/','\\']):raise ValueError('Invalid image ID')
 return ROOT/'data/images'/(image_id+'.png')
def demo_cases():return [r for r in read_csv('IMAGES.csv') if r['role']=='QUERY']
def image_evidence(image_id):
 matches=[r for r in read_csv('OOF.csv') if r['imageID']==image_id]
 if len(matches)!=1:raise ValueError('Unknown/non-unique ID')
 r=matches[0];p=float(r['p_pca_embedding_cpu']);conf=max(p,1-p)
 refs={}
 for kind in ['GOOD','BAD']:
  rr=[v for v in read_csv('IMAGES.csv') if v['query_imageID']==image_id and v['role']=='ATLAS_'+kind]
  if not rr:refs[kind]=None;continue
  if len(rr)!=1 or rr[0]['oof_group']==r['group_safe']:raise ValueError('Reference exclusion failed')
  v=rr[0];refs[kind]={'imageID':v['imageID'],'label':v['label'],'group':v['oof_group'],'asset':str(image_path(v['imageID'])),'source':v['zip_member']}
 return {'imageID':image_id,'model':'PCA128 + Logistic Regression','p_BAD':p,'confidence':conf,'prediction':'BAD' if p>=.5 else 'GOOD','decision':'AUTO-DECISION' if conf>=.9 else 'ABSTAIN — HUMAN REVIEW','label':'BAD' if int(r['y_true']) else 'GOOD','group':r['group_safe'],'atlas':refs,'asset':str(image_path(image_id)) if image_path(image_id).exists() else None,'new_inference':False,'label_used_for_decision':False}
