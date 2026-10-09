"""Private reproduction CANDIDATE adapted from historical notebook cell 122.
Default = input preflight. --run-oof explicitly fits CPU PCA+LR; NEVER overwrites frozen OOF.
Not scientifically rerun or approved for publication.
"""
import argparse, csv, hashlib, json
from pathlib import Path

HIST_EMB_SHA = "f9510efd5a1a73db5ce5bbc356b635f07ab9eaca8759a7bb9477a79cc5097e99"

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for part in iter(lambda: f.read(8*1024*1024), b""):
            h.update(part)
    return h.hexdigest()

def inspect(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        r = csv.DictReader(f)
        cols = r.fieldnames or []
        ids, groups = set(), set()
        for line in r:
            image_id = line.get("imageID")
            if not image_id or image_id in ids:
                raise ValueError(f"Duplicate/empty imageID: {image_id} in {path}")
            ids.add(image_id)
            if "group_safe" in cols:
                groups.add(line["group_safe"])
        return cols, ids, groups

def preflight(root, check_hash):
    emb, base = root/"efficientnet_patch_aspect_embeddings_3072.csv", root/"FINAL_DEMO_EVIDENCE_GATE_PER_IMAGE.csv"
    if not emb.is_file() or not base.is_file():
        raise FileNotFoundError("Missing embeddings or FINAL_DEMO_EVIDENCE_GATE_PER_IMAGE.csv")
    ec, ei, _ = inspect(emb)
    bc, bi, groups = inspect(base)
    features = [c for c in ec if c[:1] in ("g","m","x") and c[1:].isdigit()]
    if len(ei)!=3072 or ei!=bi or len(features)!=3840 or len(groups)!=21:
        raise ValueError("Frozen row/ID/feature/group contract violated")
    if not {"imageID","y_true","group_safe","p_raw_mean7"}.issubset(bc):
        raise ValueError("Baseline missing fields")
    result={"status":"PREFLIGHT_PASS","n":len(ei),"features":len(features),"groups":len(groups)}
    if check_hash:
        result["sha256"]=sha256(emb)
        if result["sha256"]!=HIST_EMB_SHA:
            raise ValueError("Embeddings SHA256 != original historical file")
    print(json.dumps(result,indent=2),flush=True)
    return features

def fit(root, output, feats):
    import numpy as np
    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    e=pd.read_csv(root/"efficientnet_patch_aspect_embeddings_3072.csv",dtype={"imageID":str})
    b=pd.read_csv(root/"FINAL_DEMO_EVIDENCE_GATE_PER_IMAGE.csv",dtype={"imageID":str})
    cols=["imageID","y_true","group_safe","p_raw_mean7"]
    df=b[cols].merge(e,on="imageID",how="inner",validate="one_to_one")
    y=df.y_true.astype(int).to_numpy()
    groups=df.group_safe.to_numpy()
    x=df[feats].replace([np.inf,-np.inf],np.nan).fillna(0).to_numpy(dtype=np.float32)
    oof=np.full(len(df),np.nan)
    for group in np.unique(groups):
        tr=groups!=group
        va=~tr
        sc=StandardScaler()
        xt=sc.fit_transform(x[tr]); xv=sc.transform(x[va])
        p=PCA(n_components=min(128,xt.shape[0]-1,xt.shape[1]),svd_solver="randomized",random_state=42)
        xt=p.fit_transform(xt);xv=p.transform(xv)
        model=LogisticRegression(C=1.0,class_weight="balanced",solver="liblinear",max_iter=3000,random_state=42)
        model.fit(xt,y[tr])
        oof[va]=model.predict_proba(xv)[:,1]
        print("Fold completed:",group,flush=True)
    if not np.isfinite(oof).all():
        raise RuntimeError("OOF nonfinite")
    output.parent.mkdir(parents=True,exist_ok=True)
    df[cols].assign(p_pca_embedding_cpu=oof).to_csv(output,index=False)
    print(json.dumps({"status":"REPRODUCTION_ATTEMPT_UNCERTIFIED","auc_pca":float(roc_auc_score(y,oof)),"path":str(output)}))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,required=True)
    p.add_argument("--verify-sha256",action="store_true")
    p.add_argument("--run-oof",action="store_true",help="Explicit training/reproduction opt-in")
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    feats=preflight(args.root,args.verify_sha256)
    if args.run_oof:
        if args.output is None:
            p.error("--run-oof requires a separate --output")
        historical=(args.root/"EXPERIMENT_CPU_PCA_EMBEDDING_OOF.csv").resolve()
        if args.output.resolve()==historical or args.output.exists():
            p.error("Refusing to overwrite historical or existing output")
        fit(args.root,args.output,feats)

if __name__=="__main__":
    main()
