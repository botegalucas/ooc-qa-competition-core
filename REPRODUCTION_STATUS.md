# Reproduction status and boundaries

Private audited candidate, 2026-10-09. Not a published competition submission.

L1 = numerical evaluation of the included frozen OOF predictions. L2 = deterministic retrospective evidence replay, authentic image checks and application tests. L3 = independent raw-image → embeddings → fold-local fitting → OOF reproduction.

The supplied executable demo and evaluator support L1/L2. They do not infer on newly uploaded images, perform human review or implement a calibrated correctness probability. The historical model is EfficientNet-B0 global/patch aggregation → 3840D → fold-local StandardScaler/PCA128/LogisticRegression, using 21 dependency/acquisition proxy holdouts.

The `scientific_sources/` text files preserve original methodology for inspection. They are not standalone executable entrypoints. `scientific_reproduction_draft/` preserves the existing optional embeddings-to-OOF runner, not a validated full pipeline. It requires the historical 230MB embedding CSV, whose documented SHA256 is f9510efd5a1a73db5ce5bbc356b635f07ab9eaca8759a7bb9477a79cc5097e99. That file is not redistributed in this repository and no public download for it has been verified. A frozen baseline metadata CSV is provided separately in that draft. No training is executed during this audit.

Outstanding L3 items: public availability or regenerability of the feature table, standalone raw-image orchestration, exact historical extractor weight identity and terms, historical environment evidence, and an independently accessible, verifiable execution receipt for the now completed CPU 21-fold reproduction. Merely supplying a public current EfficientNet weight URL does not prove equivalence to the historical bytes.

The official AI4S overview requires reproducible public code, including core sources, environment, model files/download instructions, entry scripts and input/output documentation. It lists testing, inference, evaluation **or** demo scripts; it does not explicitly mandate new-image inference or independent retraining before submission. Therefore a truthfully scoped replay can demonstrate the tool's implemented operations. It cannot certify the full scientific training claim, and eligibility or judges' interpretation cannot be guaranteed by this repository. Do not present the replay as an end-to-end image classifier.

Current package readiness is distinct from public-submission readiness. Public repository/video/report links and registration are still required and no publication has been authorized.


## Independent CPU fold reproduction — 2026-10-09 (user-run receipt)

After restoration of the recorded CPU environment (NumPy 1.26.4, SciPy 1.11.4, scikit-learn 1.3.2, pandas 2.1.4), the project owner ran a separate CPU script in Lightning AI. The supplied execution log records **21/21 held-out groups completed**, using historical 3072 × 3840 embeddings, fold-local StandardScaler, randomized PCA128 (seed 42), and LogisticRegression(C=1, class_weight=balanced, solver=liblinear, max_iter=3000, seed 42). No GPU was used.

Original ROC AUC = **0.7830348090571139**; independent training ROC AUC = **0.7830300734238412**; absolute delta = **4.735633272634487e-06**. Both balanced accuracies = **0.7115454739184996**. Mean absolute delta of 3072 paired probabilities = **1.1221038143983599e-05**; maximum = **0.000328335631321619**; none exceeds 0.001. This is strong numerical agreement, not byte-identical reproducibility.

Input SHA256: embedding CSV `f9510efd5a1a73db5ce5bbc356b635f07ab9eaca8759a7bb9477a79cc5097e99`; metadata `b5dc8c63a00d82c16c064da7a72b743164abf819abcbe5299d7deb3f391bbbc0`; historical OOF `554d0b2b1ba1c5d29ecfcd100915f40050de5b5a93a9c127b7797bc6c30c13e3`.

Original user-run artifacts (not included here): `/teamspace/studios/this_studio/AI4S_OOC/L3_REPRO_CPU_20261009_201808/`, including `L3_REPRO_REPORT.json`, `OOF_INDEPENDENT_COMPARISON.csv` and `INPUT_HASHES.json`. **This text records the owner-provided output; the three output files were not independently fetched or checked in this GitHub update.** Do not confuse this with full raw-microscopy-to-OOF reproduction.

Status: **L1 PASS; L2 PASS in tested environment; L3A (existing embeddings → 21-fold fitting → OOF) PASS by execution receipt; L3B (raw images → independently regenerated embeddings → OOF) PARTIAL**. The 230MB historical feature CSV is not publicly distributed or linked at the time of this update. Users cannot independently repeat L3A from the GitHub candidate alone until feature access or regeneration is documented and supplied.
