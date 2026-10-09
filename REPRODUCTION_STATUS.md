# Reproduction status and boundaries

Private audited candidate, 2026-10-09. Not a published competition submission.

L1 = numerical evaluation of the included frozen OOF predictions. L2 = deterministic retrospective evidence replay, authentic image checks and application tests. L3 = independent raw-image → embeddings → fold-local fitting → OOF reproduction.

The supplied executable demo and evaluator support L1/L2. They do not infer on newly uploaded images, perform human review or implement a calibrated correctness probability. The historical model is EfficientNet-B0 global/patch aggregation → 3840D → fold-local StandardScaler/PCA128/LogisticRegression, using 21 dependency/acquisition proxy holdouts.

The `scientific_sources/` text files preserve original methodology for inspection. They are not standalone executable entrypoints. `scientific_reproduction_draft/` preserves the existing optional embeddings-to-OOF runner, not a validated full pipeline. It requires the historical 230MB embedding CSV, whose documented SHA256 is f9510efd5a1a73db5ce5bbc356b635f07ab9eaca8759a7bb9477a79cc5097e99. That file is not redistributed in this repository and no public download for it has been verified. A frozen baseline metadata CSV is provided separately in that draft. No training is executed during this audit.

Outstanding L3 items: public availability or regenerability of the feature table, standalone raw-image orchestration, exact historical extractor weight identity and terms, historical environment evidence, and an authorized independent reproduction execution. Merely supplying a public current EfficientNet weight URL does not prove equivalence to the historical bytes.

The official AI4S overview requires reproducible public code, including core sources, environment, model files/download instructions, entry scripts and input/output documentation. It lists testing, inference, evaluation **or** demo scripts; it does not explicitly mandate new-image inference or independent retraining before submission. Therefore a truthfully scoped replay can demonstrate the tool's implemented operations. It cannot certify the full scientific training claim, and eligibility or judges' interpretation cannot be guaranteed by this repository. Do not present the replay as an end-to-end image classifier.

Current package readiness is distinct from public-submission readiness. Public repository/video/report links and registration are still required and no publication has been authorized.
