import os, hashlib, importlib.util
spec=importlib.util.spec_from_file_location("ag","algorithmic_gold.py")
ag=importlib.util.module_from_spec(spec); spec.loader.exec_module(ag)
exec(open('algorithmic_gold.py').read().split('if __name__')[0])
dom=Domain("forecast", _sample, _truth, slices=("trend","flat"))
results=[]
for i in range(5):
    r=judge(candidate_trend, baseline_ewma, dom, entropy=os.urandom(32))
    results.append(r["GOLD"])
    print(f"fresh_seed_{i}: GOLD={r['GOLD']}")
holdout_entropy=hashlib.sha256(b"holdout-2026-frozen").digest()
hr=judge(candidate_trend, baseline_ewma, dom, entropy=holdout_entropy)
print(f"holdout: GOLD={hr['GOLD']}")
gate=all(results) and hr["GOLD"]
print("GATE:", gate)
