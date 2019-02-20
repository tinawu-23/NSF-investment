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
		if arr[1] == 'Institution-Name':
			institution = arr[2].strip().lower()
			nameid = "{}**{}".format(name,institution)
			if not nameid in name2donation:
				name2donation[nameid] = {}
				name2donation[nameid]['AwardAmount'] = int(awardamount)
			else:
				name2donation[nameid]['AwardAmount'] += int(awardamount)

	fr.close()
	#print(name2donation)

	print("Finished loading nameid (author name + institution name)-> award amount.")
	
	# MAG dataset
	# Author ID: {Papaer IDs}
	uid2pid = {}
	fr = open('/afs/crc.nd.edu/group/dmsquare/vol1/data/MicrosoftAcademicGraph/PaperAuthorAffiliations.txt','r')
	# fr = open('testfile/test2.txt','r')
	for line in tqdm(fr):
		arr = line.strip('\r\n').split('\t')
		pid,uid,institution = arr[0],arr[1],arr[4]
		institution = institution.strip().lower()
		if not uid in uid2pid:
			uid2pid[uid] = []
			uid2pid[uid].append("")
			uid2pid[uid].append(set())
		uid2pid[uid][0] = institution
		uid2pid[uid][1].add(pid)
	
	fr.close()
	print("Finished loading author id -> institution & paper ids.")

	# MAG dataset
	# if the name in Authors.txt also appeared in NSF dataset, add to name2uid table, update name2donation table
	# Author Name: {Author IDs}
	# Author ID -> paper IDs from uid2pid
	# counts total publication for each author
	name2uid = {}
	nameiddict = {}
	fr = open('/afs/crc.nd.edu/group/dmsquare/vol1/data/MicrosoftAcademicGraph/Authors.txt','r')
	# fr = open('testfile/test3.txt','r')
	for line in tqdm(fr):
		arr = line.strip('\r\n').split('\t')
		uid,name = arr[0],arr[1]
		if uid in uid2pid:
			institution = uid2pid[uid][0]
			papercnt = len(uid2pid[uid][1])
			nameid = "{}**{}".format(name, institution)
		else:
			continue

		if nameid in name2donation:
			if not nameid in name2uid:
				name2uid[nameid] = set()
				nameiddict[nameid] = {}
				nameiddict[nameid]['awardamount'] = name2donation[nameid]['AwardAmount']
				nameiddict[nameid]['uid'] = set()
				nameiddict[nameid]['papercnt'] = 0
			name2uid[nameid].add(uid)
			nameiddict[nameid]['uid'].add(uid)
			nameiddict[nameid]['papercnt'] += papercnt
	fr.close()
	print("Finished loading nameid (author name+institution) -> author ids + institution -> paper ids (paper cnts)")

	#print(nameiddict)

	# write nameid, awardamount and papercnt to file
	fw = open('authorawardpapercnt.txt','w')

	for name, prop in nameiddict.items():
		try:
			fw.write("{},{},{}\n".format(name, prop['awardamount'], prop['papercnt']))
		except:
			continue
	fw.close()

	# plt.scatter(awardamounts, papercounts)
	# plt.loglog(awardamounts, papercounts)
	# plt.show()

if __name__ == '__main__':
	name_award_papercnt()
