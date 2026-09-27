from pathlib import Path
import sys, time, json, platform
import numpy as np
import torch, scipy
ROOT=Path('/mnt/data/cie_core/CMFG_RL_STAGE5_FINAL10_AUDITED_v13F2')
sys.path.insert(0,str(ROOT)); sys.path.insert(0,str(ROOT/'scripts/final_design'))
from common import backbone
from src.final_design.env import FinalDesignEnv
from src.final_design.obs import ObsBuilder,ObsSpec
from src.final_design.rl import PPO,PPOConfig
from src.final_design.baselines import B6RollingHorizon,B6Config
b=backbone(); spec=ObsSpec(); ob=ObsBuilder(spec,b.calibration_slack_scale_h,b.median_operation_h)
ck=Path('/mnt/data/cie_ckpt/PPO_seed_1004_SELECTED.pt')
z=torch.load(ck,map_location='cpu',weights_only=False)
ag=PPO(spec,PPOConfig(),device='cpu'); ag.net.load_state_dict(z['model']); ag.net.eval()
pol=B6RollingHorizon(B6Config(2,25,5.0,.05))
# deterministic warm-up on first held-out decision
we=FinalDesignEnv(b,970001,rho=.80,recovery_units=1,recovery_activation_h=.10,failure_mtbf_h=120.,recovery_mean_h=.35,split='heldout')
wd=we.next_decision(); wo=ob.build(we,wd)
for _ in range(20): ag.act_batch([wo],det=True)
ppo=[]; b6=[]; n=0; seed_counts={}
for seed in [970001,970002,970003,970004,970005]:
    e=FinalDesignEnv(b,seed,rho=.80,recovery_units=1,recovery_activation_h=.10,failure_mtbf_h=120.,recovery_mean_h=.35,split='heldout')
    d=e.next_decision(); c=0
    while d is not None and not e.done and n<100:
        o=ob.build(e,d)
        # time PPO on the exact current state
        t=time.perf_counter(); act=int(ag.act_batch([o],det=True)[0][0]); ppo.append(time.perf_counter()-t)
        # time B6 on the same state; do not use its action for the trajectory
        t=time.perf_counter(); _a,m=pol.select(e,d); b6.append(time.perf_counter()-t)
        d,_,_,_=e.step(act,shaped=False); n+=1; c+=1
    seed_counts[str(seed)]=c
    if n>=100: break
res={
 'design':'post-hoc matched-state computational diagnostic',
 'n_decision_states':n,
 'heldout_seed_counts':seed_counts,
 'ppo_median_ms':float(np.median(ppo)*1000),
 'ppo_p95_ms':float(np.quantile(ppo,.95)*1000),
 'ppo_mean_ms':float(np.mean(ppo)*1000),
 'b6_median_ms':float(np.median(b6)*1000),
 'b6_p95_ms':float(np.quantile(b6,.95)*1000),
 'b6_mean_ms':float(np.mean(b6)*1000),
 'speed_ratio_median_b6_over_ppo':float(np.median(b6)/np.median(ppo)),
 'python':platform.python_version(),'torch':torch.__version__,'scipy':scipy.__version__,
 'cpu':platform.processor() or platform.machine()
}
Path('/mnt/data/PPO_B6_MATCHED_LATENCY_AUDIT.json').write_text(json.dumps(res,indent=2))
print(json.dumps(res,indent=2))
