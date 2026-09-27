from pathlib import Path
import sys,time,json,platform
import numpy as np, torch
ROOT=Path('/mnt/data/cie_core/CMFG_RL_STAGE5_FINAL10_AUDITED_v13F2')
sys.path.insert(0,str(ROOT)); sys.path.insert(0,str(ROOT/'scripts/final_design'))
from common import backbone
from src.final_design.env import FinalDesignEnv
from src.final_design.obs import ObsBuilder,ObsSpec
from src.final_design.rl import PPO,PPOConfig
b=backbone(); spec=ObsSpec(); ob=ObsBuilder(spec,b.calibration_slack_scale_h,b.median_operation_h)
ck=Path('/mnt/data/cie_ckpt/PPO_seed_1004_SELECTED.pt')
z=torch.load(ck,map_location='cpu',weights_only=False)
ag=PPO(spec,PPOConfig(),device='cpu'); ag.net.load_state_dict(z['model']); ag.net.eval()
# warm-up
we=FinalDesignEnv(b,970001,rho=.80,recovery_units=1,recovery_activation_h=.10,failure_mtbf_h=120.,recovery_mean_h=.35,split='heldout')
wd=we.next_decision(); wo=ob.build(we,wd)
for _ in range(50): ag.act_batch([wo],det=True)
lat=[]; counts={}; max_per=100
for seed in [970001,970002,970003,970004,970005]:
    e=FinalDesignEnv(b,seed,rho=.80,recovery_units=1,recovery_activation_h=.10,failure_mtbf_h=120.,recovery_mean_h=.35,split='heldout')
    d=e.next_decision(); c=0
    while d is not None and not e.done and c<max_per:
        o=ob.build(e,d)
        t=time.perf_counter_ns(); act=int(ag.act_batch([o],det=True)[0][0]); dt=(time.perf_counter_ns()-t)/1e6
        lat.append(dt)
        d,_,_,_=e.step(act,shaped=False); c+=1
    counts[str(seed)]=c
res={
 'design':'post-hoc PPO inference-only CPU timing diagnostic',
 'n_decision_states':len(lat),'heldout_seed_counts':counts,
 'ppo_mean_ms':float(np.mean(lat)),'ppo_median_ms':float(np.median(lat)),
 'ppo_p95_ms':float(np.quantile(lat,.95)),'ppo_max_ms':float(np.max(lat)),
 'python':platform.python_version(),'torch':torch.__version__,'cpu':platform.processor() or platform.machine()
}
Path('/mnt/data/PPO_INFERENCE_LATENCY_AUDIT.json').write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
