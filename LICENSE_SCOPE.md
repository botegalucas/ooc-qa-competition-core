# Competition Core — license scope

The unmodified Apache License, Version 2.0 text is included in `LICENSE`. The project owner elects Apache-2.0 for **original participant-owned application and evaluation source code**, to the extent the owner holds the necessary rights: `app/*.py`, `src/*.py`, `evaluate.py`, `verify_package.py`, and `tests/*.py`. Third-party code portions, if any, remain governed by their respective terms.

**Not relicensed by Apache-2.0:**
- `data/images/*.png`: authentic Movčana et al. microscopy, separately licensed CC BY 4.0. Preserve attribution, source DOI, and unchanged-image notice in `provenance/DATASET_LICENSE_CERTIFICATION.md`.
- `data/*.csv`, scientific outputs and manifests: project research/data artifacts with separately documented provenance. Inclusion in the repository is not a claim that these are Apache-2.0 source code.
- `scientific_sources/*.txt`: verbatim recovered historical method extracts; their original attribution/provenance must be preserved, and their inclusion alone does not certify independent reproduction or blanket licensing.
- `scientific_reproduction_draft/*`: historical scientific draft and input data, preserved as evidence; ownership and relevant third-party terms must be confirmed before asserting a separate Apache code grant.
- Pretrained weights, PyTorch/torchvision and all third-party dependencies: each retains its own terms. Pretrained weights are not included with this replay demonstration.
- Video, slides, narration, fonts, music and conceptual artwork: **not distributed in this repository**.

The tested tool is a retrospective OOF evidence replay, not fresh-image inference. Evaluation of frozen probabilities and replay are reproducible (L1/L2). The original 21-fold experiment was executed historically, but independent raw-image-to-OOF reproduction (L3) has not been certified. Do not represent preserved notebook excerpts as a validated standalone full training pipeline.

**Commercial boundary:** Apache-2.0 permits commercial use of the code it covers without royalties. Independently developed future integrations, support, hosting, know-how and separate proprietary services can be sold but are not claimed to exist today. Trademark and third-party rights are not granted by this notice.

**Pre-publication checks still required:** confirm ownership and third-party portions of included code and scientific materials; confirm rules and complete source/data attribution; verify necessary reproduction instructions; and obtain the project owner's separate authorization to change repository visibility or submit on Kaggle. The original preparation repository remains private.
