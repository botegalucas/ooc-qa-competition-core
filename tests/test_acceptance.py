import unittest
from pathlib import Path
from src.frozen_backend import audit_sources,image_evidence,read_csv
from evaluate import metrics
class Acceptance(unittest.TestCase):
 def test_integrity(self):self.assertEqual(audit_sources()['groups'],21)
 def test_auto(self):self.assertEqual(image_evidence('230316_24')['decision'],'AUTO-DECISION')
 def test_abstain(self):self.assertEqual(image_evidence('230320_52')['decision'],'ABSTAIN — HUMAN REVIEW')
 def test_caco(self):
  e=image_evidence('220606_17');self.assertEqual((e['label'],e['prediction']),('GOOD','BAD'));self.assertAlmostEqual(e['confidence'],.9922845230250426,12)
 def test_atlas(self):
  checked=0
  for r in read_csv('IMAGES.csv'):
   if r['role']!='QUERY':continue
   e=image_evidence(r['imageID'])
   for ref in e['atlas'].values():
    if ref:self.assertNotEqual(ref['group'],e['group']);self.assertTrue(Path(ref['asset']).exists());checked+=1
  self.assertEqual(checked,23)
 def test_missing_reference(self):self.assertIsNone(image_evidence('230316_24')['atlas']['GOOD'])
 def test_invalid_id(self):
  for ID in ['no_such_ID','../bad','']:
   with self.assertRaises(ValueError):image_evidence(ID)
 def test_metrics(self):
  for r,n,v in zip(metrics(),[3072,1496,1185],[.7830348090571139,.8645171382562686,.8821188560050255]):self.assertEqual(r['N'],n);self.assertAlmostEqual(r['AUC'],v,12)
 def test_decision_uses_no_labels(self):
  # Test the actual evidence function with shuffled labels and retained probability.
  import src.frozen_backend as b
  original=b.read_csv
  def changed(name):
   rows=original(name)
   if name=='OOF.csv':
    for r in rows:r['y_true']=str(1-int(r['y_true']))
   return rows
  before=image_evidence('220606_17');b.read_csv=changed
  try:self.assertEqual(before['decision'],image_evidence('220606_17')['decision'])
  finally:b.read_csv=original
 def test_streamlit_init_cases_restart(self):
  from streamlit.testing.v1 import AppTest
  app=AppTest.from_file('app/streamlit_app.py',default_timeout=30).run();self.assertFalse(app.exception)
  for ID in ['230316_24','230320_52','220606_17']:
   app.selectbox[0].select(ID).run();self.assertFalse(app.exception);e=image_evidence(ID)
   self.assertEqual(app.metric[0].value,e['prediction']);self.assertEqual(app.metric[2].value,e['decision'])
  app.text_input[0].set_value('unknown').run();self.assertTrue(app.error);self.assertFalse(app.exception)
  app=AppTest.from_file('app/streamlit_app.py',default_timeout=30).run();self.assertFalse(app.exception)
if __name__=='__main__':unittest.main(verbosity=2)
