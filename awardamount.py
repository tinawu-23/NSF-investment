#!/usr/bin/env python3
from tqdm import tqdm
from multiprocessing import Pool
import matplotlib.pyplot as plt

def name_award_papercnt():
	# NSF dataset
	# Author Name: $ received 
	name2donation = {}
	fr = open('/afs/crc.nd.edu/group/dmsquare/vol2/ywu6/cleaned-data/nsf-award-data.txt','r')
	# fr = open('testfile/test1.txt','r')	
	while True:
		line = fr.readline()
		if line == None or line == '': break
		arr = line.strip('\r\n').split('\t')
		if arr[1] == 'AwardAmount':
			awardamount = arr[2]
		if arr[1] == 'Investigator-FirstName':
			firstname = arr[2]
			line = fr.readline()
			arr =line.strip('\r\n').split('\t')
			if arr[1] == 'Investigator-LastName':
				lastname = arr[2]
				name = (firstname+' '+lastname).lower()
				if not name in name2donation:
					name2donation[name] = {}
					name2donation[name]['AwardAmount'] = int(awardamount)
				else:
					name2donation[name]['AwardAmount'] += int(awardamount)
	fr.close()
	print("Finished loading author name -> award amount.")
	
	# MAG dataset
	# Author ID: {Papaer IDs}
	uid2pid = {}
	fr = open('/afs/crc.nd.edu/group/dmsquare/vol1/data/MicrosoftAcademicGraph/PaperAuthorAffiliations.txt','r')
	# fr = open('testfile/test2.txt','r')
	for line in tqdm(fr):
		arr = line.strip('\r\n').split('\t')
		pid,uid = arr[0],arr[1]
		if not uid in uid2pid:
			uid2pid[uid] = set()
		uid2pid[uid].add(pid)
	
	fr.close()
	print("Finished loading author id -> paper ids.")

	# MAG dataset
	# if the name in Authors.txt also appeared in NSF dataset, add to name2uid table, update name2donation table
	# Author Name: {Author IDs}
	# Author ID -> paper IDs from uid2pid
	# counts total publication for each author
	name2uid = {}
	fr = open('/afs/crc.nd.edu/group/dmsquare/vol1/data/MicrosoftAcademicGraph/Authors.txt','r')
	# fr = open('testfile/test3.txt','r')
	for line in tqdm(fr):
		arr = line.strip('\r\n').split('\t')
		uid,name = arr[0],arr[1]
		if name in name2donation:
			if not name in name2uid:
				name2uid[name] = set()
				name2donation[name]['uid'] = set()
				name2donation[name]['papercnt'] = 0
			name2uid[name].add(uid)
			name2donation[name]['uid'].add(uid)
			if uid in uid2pid:
				name2donation[name]['papercnt'] += len(uid2pid[uid])
	fr.close()
	print("Finished loading author name -> author ids -> paper ids (paper cnts)")

	# print(name2donation)

	awardamounts = []
	papercounts = []

	fw = open('authorawardpapercnt.txt','w')

	for name, prop in name2donation.items():
		try:
			papercounts.append(prop['papercnt'])
			awardamounts.append(prop['AwardAmount'])
			fw.write("{},{},{}\n".format(name, prop['AwardAmount'], prop['papercnt']))
		except:
			continue
	fw.close()

	# plt.scatter(awardamounts, papercounts)
	plt.loglog(awardamounts, papercounts)
	plt.show()

if __name__ == '__main__':
	name_award_papercnt()
