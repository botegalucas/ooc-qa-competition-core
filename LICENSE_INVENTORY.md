# License inventory — not a grant of rights

| Component | Verified evidence | Status / outstanding action |
|---|---|---|
| Microscopy dataset and 37 unchanged images | Zenodo 10203721, existing GATE2 dataset certificate: CC BY 4.0 | PASS for source attribution; retain authors/DOI/license and no-change notice |
| Project code | Apache-2.0 LICENSE included; grant scoped to eligible original application/evaluation code in LICENSE_SCOPE.md | PARTIAL: ownership and any embedded third-party portions still require final review before public release |
| EfficientNet torchvision implementation | Public PyTorch/torchvision implementation | PARTIAL: implementation license is distinct from weight/data terms |
| EfficientNet pretrained weights | Original code uses EfficientNet_B0_Weights.DEFAULT | PARTIAL: exact frozen bundle/hash and permitted-use terms need certification |
| Streamlit / pandas / numpy / Pillow and transitive packages | Installed distribution metadata exported to logs/DEPENDENCY_LICENSES.json | PARTIAL: packaging notices and complete transitive license review before release |
| OOF tables and evaluation graphs | Existing participant-produced scientific outputs | PARTIAL until ownership/code/data release approval |
| Voice, music, fonts, 16 arts, video | Not included in this Competition Core candidate | Outside this execution; previous rights blockers remain with art/video owner |

Torchvision explicitly warns pretrained models may have separate dataset-derived terms:
https://docs.pytorch.org/vision/stable/models.html#general-information-on-pre-trained-weights
Do not infer unrestricted weight rights from the software license.
No proprietary API or paid service is required to run the supplied replay.
