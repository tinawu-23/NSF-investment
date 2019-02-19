#!/usr/bin/env python3
from tqdm import tqdm

fr = open('nsf-award-data.txt','r')
awardidlst = []
for line in tqdm(fr):
	arr = line.strip('\r\n').split('\t')
	if arr[1] == 'Investigator-FirstName':
		firstname = arr[2]
		line = fr.readline()
		arr =line.strip('\r\n').split('\t')
		if arr[1] == 'Investigator-LastName':
			lastname = arr[2]
			name = (firstname+' '+lastname).lower()
			if name == "wei wang":
				awardidlst.append(arr[0])
fr.close()
print("Finished finding all authors with name weiwang.")



fr = open('nsf-award-data.txt','r')
fw = open('weiwang.txt', 'w')

for line in tqdm(fr):
	arr = line.strip('\r\n').split('\t')
	if arr[0] in awardidlst:
		fw.write(line)
fr.close()
fw.close()
print("Finished writing to weiwang.txt")



