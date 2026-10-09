# OoC-QA — Competition Core release candidate (PRIVATE)

Retrospective group-held-out OOF replay — not new-image inference.

This is an adaptation of the existing artifact-based demo, not a new scientific architecture.
The backend uses the frozen PCA128 + Logistic Regression OOF CSV. It never loads a neural model,
trains, regenerates embeddings, or uses labels to make its evidence decision.
Confidence is max(p_BAD,1-p_BAD), not a calibrated probability of correctness.
At confidence >=0.90 the action is AUTO-DECISION; otherwise ABSTAIN — HUMAN REVIEW.
Review is requested, not performed by this application.

## Run

Use Python 3.12. From this directory:

```sh
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python verify_package.py
python evaluate.py
python -m unittest discover -s tests -v
python -m streamlit run app/streamlit_app.py --global.developmentMode false --server.headless true --browser.gatherUsageStats false
```

The documented dependency versions were inspected in the CPU test environment. A clean independent Windows CPU installation was tested in the prior 2026-10-08 audit;
this release copy is tested again without changing frozen predictions. The metric evaluator uses only the
Python standard library and requires no paid service. Backend/Streamlit tests passed locally.
No Torch, GPU, API key, paid account or external model is required for this replay.

For a direct case use `/?case=230525_114` (AUTO), `/?case=230320_52` (ABSTAIN), or
`/?case=220606_17` (known CACO error). Disable browser automatic translation when switching
cases: it was observed retaining stale translated text. Direct fresh case URLs were verified.

## Certified results

| Confidence threshold | N | Coverage | AUC |
|---|---:|---:|---:|
| Full population | 3072 | 100% | 0.783035 |
| >=0.85 | 1496 | 48.6979% | 0.864517 |
| >=0.90 | 1185 | 38.5742% | 0.882119 |

Full-coverage Balanced Accuracy is 0.711545. There are 6 cell types and 21 conservative
dependency/acquisition proxies, not 21 proven independent biological experiments.
The retained >=0.90 subset represents 20 groups. Selective AUC is not full-population AUC.
RAW_MEAN7 AUC 0.737774 is a separate baseline. The paired PCA-vs-RAW interval includes zero;
statistical superiority has not been demonstrated. Optical QC remains complementary/experimental.

## Assets and limits

`data/OOF.csv` preserves the certified probabilities, labels, IDs and group_safe. Its SHA256 is
554d0b2b1ba1c5d29ecfcd100915f40050de5b5a93a9c127b7797bc6c30c13e3.
`data/IMAGES.csv` maps actual unmodified PNG bytes to ZIP members and hashes. There are
37 unique real images. Atlas uses existing references with query-group exclusion; missing
references are displayed as unavailable. No new retrieval or AUC gain is claimed.
CACO 220606_17 is GOOD, predicted BAD, confidence 0.9922845230250426; this is a retrospective OOF error.

Source images: Movčana et al., Organ-on-a-Chip Image Dataset, DOI 10.5281/zenodo.10203721,
https://zenodo.org/records/10203721, CC BY 4.0. Images are unchanged; retain attribution.
See provenance/DATASET_LICENSE_CERTIFICATION.md and LICENSE_INVENTORY.md.

`scientific_sources/` contains unexecuted verbatim notebook/script extracts for static review.
Cell 59 defines RGB, proportional bilinear resize plus black padding to 224, ImageNet normalization,
3x3 original-image patches, and global/patch-mean/patch-max 1280D concatenation (3840D).
Cell 122 fits scaler/PCA/LR only on each of 21 training folds (PCA randomized seed42, LR C1,
balanced, liblinear, max_iter3000, seed42). It also contains historical fusion/control code, which
is NOT the deployed replay policy. Cell 57 has a historical CUDA availability check: NOT EXECUTED.
The extracted files are text, not automatically runnable entrypoints.

Full image-to-OOF reproduction is not certified: notebook upstream state, exact frozen weight
identity/terms, complete independent environment and input orchestration require closure.
No serialized PCA/scaler/LR deployment bundle was located in AI4S_OOC. New-image inference is unavailable.

## Rights and release

PRIVATE CANDIDATE. Apache-2.0 text is included for eligible original participant-owned application/evaluation code, as delimited in LICENSE_SCOPE.md. Do not publish this directory
until the owner approves a competition-compatible license and the release blockers are closed.
Existing microscopy, pretrained extractor and libraries are preexisting work. Competition work
includes group-safe evaluation, fold-local PCA-LR OOF, evidence abstention and contextual replay;
this technical audit adds integrity tests/documentation without changing frozen science.
Commercial integrations/services/brand development are reserved separately. Essential scientific
reproduction code may not be hidden in a Commercial Core. No clinical or external-validation claim.

## Release review
See REPRODUCTION_STATUS.md for L1/L2 versus incomplete L3 and LICENSE_SCOPE.md for per-component rights. scientific_reproduction_draft/ is preserved as unexecuted candidate methodology, not a certified training pipeline. No implemented proprietary Commercial Core is claimed.
