# OoC-QA — Technical Report | AI4S Tool & Platform

## Purpose and implemented product
OoC-QA is a research prototype and retrospective evidence replay for quality assessment in organ-on-a-chip brightfield microscopy. It displays recorded, group-held-out out-of-fold (OOF) scores on authentic microscopy images, applies a fixed abstention gate and offers context references in an Atlas. It does not currently infer on new uploaded images, perform human review, provide clinical advice or claim external laboratory validation.

## Data
The source is the Organ-on-a-Chip Image Dataset (Movčana et al., 2023), Zenodo DOI 10.5281/zenodo.10203721, CC BY 4.0. The historical evaluation uses 3,072 image records and six cell types with dataset GOOD/BAD labels. The 21 group_safe units are conservative acquisition/dependency proxies, not 21 independent experiments. The public candidate includes 37 intact representative micrographs identified in image manifests.

## Historical method
Pretrained EfficientNet-B0 produces global 1,280D, 3x3 patch-mean 1,280D and 3x3 patch-max 1,280D representations (3,840D in total), after aspect-preserving RGB letterboxing and ImageNet normalization. Historical fold-local StandardScaler, PCA128 (randomized, seed42) and balanced Logistic Regression (C=1, liblinear, max_iter3000, seed42) generate held-out probabilities across 21 group-safe folds. The current executable demo only replays the saved scores.

Decision: confidence = max(p_BAD, 1-p_BAD). At confidence >=0.90, AUTO-DECISION; otherwise ABSTAIN — HUMAN REVIEW. Confidence is not a calibrated probability of correctness and no human review is completed by the program.

## Frozen retrospective results

| Population | N | Coverage | ROC AUC | Balanced accuracy |
|---|---:|---:|---:|---:|
| Entire OOF | 3072 | 100% | 0.783035 | 0.711545 |
| Confidence >=0.85 | 1496 | 48.6979% | 0.864517 | 0.817850 |
| Confidence >=0.90 | 1185 | 38.5742% | 0.882119 | 0.847215 |

The selective AUC is for the retained subset only (20 groups at threshold .90). RAW_MEAN7 full OOF baseline AUC = 0.737774; the historical paired interval for PCA-versus-RAW includes zero. Statistically significant superiority has not been established. The Atlas has contextual value without demonstrated additional AUC. The shown CACO error is retrospective OOF, not a prospective external test.

## Reproduction evidence and limitations
L1: OOF numerical evaluation available via evaluate.py (PASS). L2: historical evidence replay and image/integrity checks were tested with Streamlit and a ten-test suite (PASS for the tested CPU environment). L3A: the owner independently reran 21/21 PCA/LR group-held-out fits on existing historical embeddings on 2026-10-09 using CPU; reproduction AUC = 0.783030073 versus historical 0.783034809, balanced accuracy matched at 0.711545474, and maximum absolute paired score difference was 0.000328336. See L3_CPU_REPRODUCTION_RECEIPT.md.

L3B: the full raw-image -> new EfficientNet embeddings -> 21-fold training -> OOF chain was not independently certified. The historical ~230MB embedding CSV is not part of this repository and has no confirmed public download. The exact original weight bytes were not certified. A third party **cannot rerun L3A solely from this repository at present**. The owner-run receipt has not been independently downloaded and verified by this repository audit. Neither an end-to-end reproducibility claim nor arbitrary new-image inference is made.

## How to run the audited scope
With Python 3.12 in a fresh environment: install requirements.txt, run python verify_package.py, python evaluate.py and python -m unittest discover -s tests -v, then start python -m streamlit run app/streamlit_app.py. No GPU or external model download is needed for this replay.

## Rights and scope
Original participant-owned app/evaluation source is offered under Apache-2.0 subject to the limits in LICENSE_SCOPE.md. Movčana et al. images are separately CC BY 4.0; third-party libraries and weights have their own terms. Slides, video and private integrations are not included in this repository. Commercial integrations, prospective multicenter validation, and future digital-twin connections are proposed work, not already-implemented features.

## Presentation
Video: https://www.youtube.com/watch?v=Ny-8awT0aOg (accessible by link, unlisted at report time).
Submission track: Tool & Platform.
Competition Core: https://github.com/botegalucas/ooc-qa-competition-core (private pending owner's separate publication authorization).
