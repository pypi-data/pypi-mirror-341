#!/usr/bin/env python3
import sys,os
sys.path.append(os.path.dirname(__file__))

def mtgeCFS(amt=10**6,wac=0.07,wam=360,fq=12,lkppy=0,flg=0,vamort=1,debugTF=False,**optx):
	'''return mortgage cashflows via amt, wac, wam, fq, ...etc.
	'''
	import pandas as pd
	import numpy as np
	from xux64 import col_cfpmt
	from xux64 import np2ct2,np2ct,v2ct2,v2ct,vs2ct,vs2ct
	#- assign inputs
	cpn=optx.pop("cpn",wac)
	bln=optx.pop("bln",wam)
	waml=wam+1

	#- allocate cfs memory
	m=22
	mx=np.zeros(m*waml).reshape(m,waml)
	mx[18]=wac/fq
	mx[19]=cpn/fq
	mx[20]=vamort
	if 'np2ct' in locals():
		nx=[np2ct(x) for x in mx]
	else:
		nx=mx

	#- run c-function
	nx += [lkppy,bln,flg]
	cfs = col_cfpmt(wam,amt,*nx)

	#- allocate cfs to dataframe
	colx=["rvm","svt","perf_bal","new_def","fcl","sch_am","exp_am",\
	"vol_prepay","am_def","act_am","exp_int","lost_int","act_int",\
	"prin_recov","prin_loss","adb","mdr","mpr","vwac","vcpn","vamort","xadj"]
	cfs=pd.DataFrame(mx.T,columns=colx)

	#- prepare returned loan-info 
	cfsnames=",".join(cfs.columns)
	lx=['wac','cpn','amt','wam','bln','lkppy','fq','flg','cfsnames']
	li={x:y for x,y in locals().items() if x in lx}

	if debugTF:
		sys.stderr.write("{}\n".format(cfs[["perf_bal","act_am","act_int","vcpn"]].head()) )
	li.update(CFS=cfs)
	return li

if __name__ == '__main__':
	ret=mtgeCFS()
	CFS=ret.pop('CFS',[])
	print(ret)
	print(CFS)
