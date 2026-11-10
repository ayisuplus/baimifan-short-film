"""Screenshot-scoped H3 retakes. Reuse the verified provider and never auto-retry."""
import argparse
import metaso_h3_v006 as base
base.OUT=base.ROOT/'视频制作/Metaso-H3-v007';base.QUEUE=base.OUT/'执行队列.json'
base.old.OUT=base.OUT;base.old.QUEUE=base.QUEUE
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['submit','poll']);p.add_argument('--attempt');a=p.parse_args()
 if a.action=='poll':base.old.poll()
 else:base.submit(a.attempt)
