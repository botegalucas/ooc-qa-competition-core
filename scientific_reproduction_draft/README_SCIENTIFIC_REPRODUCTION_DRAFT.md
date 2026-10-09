# OoC-QA scientific reproduction package — PRIVATE DRAFT, NOT RELEASED

**Purpose:** Document and provide a prospective offline reproduction path for the frozen PCA128 + Logistic Regression OOF scientific experiment **from the previously generated 3840-dimensional EfficientNet embeddings**. This is *not* new-image inference. It is not a complete raw-image-to-embedding production pipeline.

## Evidence vs untested code
- Certified: frozen 3072-image OOF CSV, 21 conservative proxy groups, exact historical artifact hashes and metrics from CPU replay, real microscopy source DOI 10.5281/zenodo.10203721.
- Certified: checkpoint and final embeddings show numerical equivalence within 1e-5 in user-executed CPU comparison on Lightning, despite different byte-level hashes.
- Created in this private draft: `scientific_oof.py`, independently syntax-compiled and `--help` invoked with exit code 0 on Windows Python3.12. **It has NOT been run on the 230MB embedding file or retrained/tested across all 21 folds.**
- Source `../scientific_sources/NOTEBOOK_CELL_122.txt` is preserved verbatim as documentary evidence. Our script reimplements its OOF PCA/LR section while excluding the historical rank-fusion experiments; compare any outputs by imageID, not row order.
- `../scientific_sources/NOTEBOOK_CELL_57.txt` and `NOTEBOOK_CELL_59.txt` preserve the original extractor logic, but depend on original notebook state. They are not a standalone raw-image extractor.
- `FINAL_DEMO_EVIDENCE_GATE_PER_IMAGE.csv` is a frozen source table; **its columns y_true and group_safe are used only to train/evaluate held-out folds, never as image features**.

## Scientific inputs
Place these TWO preexisting files in one input directory (historically Lightning `/teamspace/studios/this_studio/AI4S_OOC`):
1. `efficientnet_patch_aspect_embeddings_3072.csv` — 230489482 bytes; SHA256 `f9510efd5a1a73db5ce5bbc356b635f07ab9eaca8759a7bb9477a79cc5097e99` (preserved on Lightning; not included in this small draft).
2. `FINAL_DEMO_EVIDENCE_GATE_PER_IMAGE.csv` — frozen 3072-line metadata, copied into this private draft.

Recommended source code environment (based on installed **2026-10-08 Lightning metadata**, not independently established as historical original creation environment):
- Python 3.12 (test environment; historical Python version not confirmed)
- numpy 1.26.4, pandas 2.1.4, scipy 1.11.4, scikit-learn 1.3.2
- torch 2.8.0+cu128, torchvision 0.23.0+cu128, Pillow 11.3.0 are **not needed for embeddings-to-OOF**; they are upstream extractor dependencies and the CUDA tag does not mean GPU is needed for this CPU classifier.
- Use an isolated environment, install these CPU evaluator versions according to platform. Do not confuse demo requirements (pandas2.3.3/numpy2.5.3) with scientific environment versions.

## Safe default: preflight only (no training)
```shell
python scientific_oof.py --root /teamspace/studios/this_studio/AI4S_OOC --verify-sha256
```
This scans CSV row IDs/headers and optionally validates SHA256. It requires both inputs in ROOT. It does not import torch, load a model, or train anything.

## OPTIONAL CPU experiment reproduction — NOT EXECUTED / NOT AUTHORIZED IN THIS AUDIT
```shell
python scientific_oof.py --root /teamspace/studios/this_studio/AI4S_OOC --run-oof --output /path/to/NEW_SEPARATE_AUDIT_DIR/candidate_pca_oof.csv
```
`--run-oof` performs the 21 PCA/LR fits, so it is an experiment and **must not be run merely to package the submission**. If separately authorized, use a new output path and compare resulting predictions by imageID with the frozen `EXPERIMENT_CPU_PCA_EMBEDDING_OOF.csv`. The script must not overwrite historical files. Full performance/reproducibility cannot be asserted before it is run and evaluated.

## Raw-image chain (not packaged as standalone execution)
Zenodo public raw images (~6.71GB local ZIP historically present) -> RGB -> 3x3 original patches -> proportional bilinear 224 px + black padding -> ImageNet normalize -> frozen torchvision EfficientNet-B0 IMAGENET1K_V1 (classifier Identity) -> 1280 global, 1280 patch-mean, 1280 patch-max embeddings. Historical weight file SHA256 not recorded. Pretrained weight URL was confirmed from current torchvision 0.23.0 source, but cannot be asserted as the exact historical model bytes.

## Release/rights guard
**PRIVATE.** No public license selected or applied. User approved Apache-2.0 only as possible license for independently owned Competition Core code pending verification. Dataset CC BY4.0 source authors/DOI, pretrained weights, dependencies and all upstream notices need proper treatment. Public sharing can authorize commercial reuse of disclosed code; it does not make a sales agreement with judges or sponsors. Do not publish or submit without owner's explicit separate instruction.

## Outcome
This is a documentation + code packaging improvement, not a passed independent Level3 scientific reproduction. Level1/Level2 remain PASS, Level3 PARTIAL, rights PARTIAL. No new measurements made.

## Packaging correction (2026-10-09)
The original GitHub inventory omitted the baseline input and referenced absent source_excerpts paths. This candidate includes the unchanged baseline metadata input and points to ../scientific_sources/. The 230MB embeddings remain absent; full reproduction is NOT certified.
