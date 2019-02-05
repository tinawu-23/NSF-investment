#!/usr/bin/env python3
import pandas as pd
from tqdm import tqdm
import time

awarddict = {}
totnames = 0
with open('nsf-award-data.txt') as f:
	for line in tqdm(f):
		if line.split()[1].strip() == "Investigator-FirstName":
			totnames += 1
			awarddict[line.split()[0]] = {}
			namedict = {}
			namedict['firstname'] = line.split('Investigator-FirstName')[-1].strip()
			awarddict[line.split()[0]] = namedict
			l = next(f)
			namedict['lastname'] = l.split('Investigator-LastName')[-1].strip()

fncnt,lncnt = 0,0
for award, value in awarddict.items():
	if '.' in value['firstname']:
		fncnt += 1
	if '.' in value['lastname']:
		lncnt += 1

print("\nShortened First Names: "+str(fncnt))
print("Shortened Last Names: "+str(lncnt))
print("Total Names: "+str(totnames))
print()
print("Shortened First Name Ratio: "+str(round((fncnt/totnames),4)*100)+"%")
print("Shortened Last Name Ratio: "+ '%.2f' % (round(lncnt/totnames, 4)*100) + "%")
