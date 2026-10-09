"""Adapted existing demonstration: frozen PCA-LR replay only."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import streamlit as st
from src.frozen_backend import audit_sources,demo_cases,image_evidence,REPLAY_NOTICE
st.set_page_config(page_title='OoC-QA — PCA OOF replay',layout='wide')
audit_sources();st.title('OoC-QA · Evidence before decisions');st.warning(REPLAY_NOTICE)
st.caption('3,072 images · 6 cell types · 21 conservative dependency/acquisition proxies. No external or clinical validation.')
demo,validation,limits=st.tabs(['Real microscopy & evidence','Frozen validation','Limits & provenance'])
with demo:
 options=[r['imageID'] for r in demo_cases()]+['220606_17']
 requested=st.query_params.get('case',options[0])
 ID=st.selectbox('Certified real query / known retrospective error',options,index=options.index(requested) if requested in options else 0)
 ev=image_evidence(ID)
 left,right=st.columns([1.5,1])
 with left:st.image(ev['asset'],caption=ID+' · real dataset image',use_container_width=True)
 with right:
  st.metric('Predicted state',ev['prediction']);st.metric('Confidence',f"{ev['confidence']:.10f}");st.metric('Evidence action',ev['decision'])
  st.caption('Ground truth (retrospective audit only): '+ev['label']);st.caption('Confidence is not a calibrated probability of correctness. Human review requested, not performed.')
 st.subheader('Visual Reference Atlas — contextual evidence only')
 cols=st.columns(2)
 for col,kind in zip(cols,['GOOD','BAD']):
  with col:
   ref=ev['atlas'][kind]
   if ref is None:st.info(kind+' reference unavailable')
   else:
    st.image(ref['asset'],caption=kind+' dataset label · '+ref['imageID'],use_container_width=True);st.caption('Reference group: '+ref['group']+' · excluded query group: '+ev['group'])
 st.caption('Microscopy: Movčana et al., DOI 10.5281/zenodo.10203721, CC BY 4.0. No AUC gain or causal explanation attributed to Atlas.')
 custom=st.text_input('Inspect an OOF ID')
 if custom:
  try:st.json(image_evidence(custom))
  except ValueError as e:st.error(str(e))
with validation:
 st.metric('PCA-LR AUC — 100% coverage','0.783035');st.metric('Balanced Accuracy — 100% coverage','0.711545')
 st.table([{'threshold':.5,'coverage':'100%','AUC':.783035},{'threshold':.85,'coverage':'48.6979%','AUC':.864517},{'threshold':.9,'coverage':'38.5742%','AUC':.882119}])
 st.caption('RAW_MEAN7 baseline AUC 0.737774. Paired PCA−RAW confidence interval includes zero. Selective metrics apply only to retained subsets; .90 is the fixed operational gate.')
with limits:
 st.write('Frozen 3840D embeddings → fold-local StandardScaler/PCA128/Logistic Regression. No serialized deployment model is supplied. This application reads saved OOF probabilities; it does not infer new images.')
 st.write('Optical QC is experimental secondary evidence and is not added to this confidence gate. External multi-laboratory pilot validation remains proposed.')
