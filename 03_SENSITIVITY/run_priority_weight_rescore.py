from pathlib import Path
import sys,json,torch,numpy as np,pandas as pd
ROOT=Path('/mnt/data/r1c_core/core/CMFG_RL_STAGE5_FINAL10_AUDITED_v13F2');sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'scripts/final_design'))
from common import backbone
from src.final_design.env import FinalDesignEnv
from src.final_design.obs import ObsBuilder,ObsSpec
from src.final_design.rl import PPO,PPOConfig
GATE=Path('/mnt/data/r1c_gate'); ALPHAS=(0.25,0.5,1.0)
class DEnv(FinalDesignEnv):
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw); self.tb=0.;self.tp=0.;self.tr=0.;self.tlb=0.;self.tlp=0.
    def _accrue_time_cost(self,new_t):
        old=self.now
        for j in self.jobs.values():
            if j.arrival>old or j.done: continue
            a=max(old,j.due); b=max(a,new_t)
            if b>a:
                dt=b-a; self.tb+=dt; self.tp+=dt*j.priority
        return super()._accrue_time_cost(new_t)
    def _td(self,j):
        rt=0.;rc=0.;st=j.op_index
        if j.status=='PROCESSING':
            end=self._active_execution_end(j)
            if end is not None:
                rt+=max(0.,end-self.now)
                if j.current_provider is not None: rc+=self.direct_cost(j,j.current_provider,'regular')
                st=j.op_index+1
        for oi in range(st,len(j.route)):
            op=j.route[oi]; fs=list(self._feasible_for_template_op(j.template,op))
            if fs:
                q=min(fs,key=lambda p:self.service_h(j,p));rt+=self.service_h(j,q);rc+=self.direct_cost(j,q,'regular')
        already=max(0.,self.now-j.due); opt=max(0.,self.now+rt-j.due); add=max(0.,opt-already)
        return rc,add,add*j.priority
    def _terminalize(self):
        if not self.done:
            self.tr=self.tlb=self.tlp=0.
            for j in self.jobs.values():
                if j.arrival<=self.horizon and not j.done:
                    a,b,c=self._td(j);self.tr+=a;self.tlb+=b;self.tlp+=c
        return super()._terminalize()
    def score(self,alpha):
        arr=max(1,len([j for j in self.jobs.values() if j.arrival<=self.horizon]))
        fixed=self.ledger.service+self.ledger.switch+self.ledger.recovery+self.ledger.restart
        return (fixed+self.tb+alpha*self.tp+self.tr+self.tlb+alpha*self.tlp)/arr
b=backbone();ob=ObsBuilder(ObsSpec(),b.calibration_slack_scale_h,b.median_operation_h);ag=PPO(ObsSpec(),PPOConfig(),'cpu');z=torch.load(GATE/'PPO_seed_1004_SELECTED.pt',map_location='cpu',weights_only=False);ag.net.load_state_dict(z['model']);ag.net.eval()
rows=[]
for i,seed in enumerate(range(970001,970051),1):
    e=DEnv(b,seed,rho=.80,recovery_units=1,recovery_activation_h=.10,failure_mtbf_h=120.,recovery_mean_h=.35,split='heldout');d=e.next_decision()
    while d is not None and not e.done:
        act=int(ag.act_batch([ob.build(e,d)],det=True)[0][0]);d,_,_,_=e.step(act,shaped=False)
    native=e.metrics()['cost_per_arrived']; assert abs(native-e.score(.5))<1e-8,(seed,native,e.score(.5))
    rows.append({'seed':seed,'completion':e.metrics()['completion_fraction'],**{f'cost_alpha_{a}':e.score(a) for a in ALPHAS}})
    if i%10==0: print(i,flush=True)
out=Path('/mnt/data/r1c_priority_ppo');out.mkdir(exist_ok=True);df=pd.DataFrame(rows);df.to_csv(out/'PPO1004_PRIORITY_WEIGHT_ROWS.csv',index=False)
base=df['cost_alpha_0.5']
s=[]
for a in ALPHAS:
    x=df[f'cost_alpha_{a}']; pct=(x-base)/base*100
    s.append({'alpha':a,'mean_cost':x.mean(),'median_cost':x.median(),'mean_change_vs_alpha0.5_pct':pct.mean(),'median_change_vs_alpha0.5_pct':pct.median(),'completion_mean':df.completion.mean(),'n':len(df)})
pd.DataFrame(s).to_csv(out/'PPO1004_PRIORITY_WEIGHT_SUMMARY.csv',index=False);print(pd.DataFrame(s).to_string(index=False))
