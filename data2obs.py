vocab_directorate = {}
vocab_directorate['Directorate for Computer & Information Science & Engineering'] = 'Direct For Computer & Info Scie & Enginr'
vocab_directorate['Directorate for Social, Behavioral & Economic Sciences'] = 'Direct For Social, Behav & Economic Scie'
vocab_directorate['Directorate for Biological Sciences'] = 'Direct For Biological Sciences'
vocab_directorate['Directorate for Engineering'] = 'Direct For Engineering'    
vocab_directorate['Directorate For Engineering'] = 'Direct For Engineering'
vocab_directorate['Directorate for Geosciences'] = 'Direct For Geosciences'    
vocab_directorate['Directorate For Geosciences'] = 'Direct For Geosciences'
vocab_directorate['Office Of The Director'] = 'none'
vocab_directorate['Office Of Polar Programs'] = 'none'    
vocab_directorate['Office of Budget, Finance, & Award Management'] = 'none'
vocab_directorate['National Coordination Office'] = 'none'

vocab_division = {}
vocab_division['Office of Advanced Cyberinfrastructure (OAC)'] = 'Division of Advanced Cyberinfrastructure'
vocab_division['DIVISION OF EXPERIMENTAL & INTEG ACTIVIT'] = 'Division of Experimental & Integrative Activities'
vocab_division['Division of Integrative Organismal Sys'] = 'Division of Integrative Organismal Systems'
vocab_division['Division of Cellular Biosciences'] = 'Division of Molecular and Cellular Biosciences'
vocab_division['Division of Molecular and Cellular Bioscience'] = 'Division of Molecular and Cellular Biosciences'    
vocab_division['Division of Computer and Communication Foundations'] = 'Division of Computing and Communication Foundations'
vocab_division['Division of Behavioral and Cognitive Sci'] = 'Division of Behavioral and Cognitive Sciences'
vocab_division['Division Atmospheric & Geospace Sciences'] = 'Division of Atmospheric and Geospace Sciences'
vocab_division['Division of Civil, Mechanical, and Manufacturing Innovation'] = 'Division of Civil, Mechanical, & Manufact Inn'
vocab_division['Division of Chemical, Bioengineering, Environmental, and Transport Systems'] = 'Division of Chem, Bioeng, Env, & Transp Sys'
vocab_division['DIVISION OF EDUCATIONAL SYSTEM REFORM'] = 'Division of Educational System Reform'
vocab_division['National Center for Science and Engineering Statistics.'] = 'National Center For S&E Statistics'
vocab_division['Division of Polar Progrms'] = 'Division of Polar Programs'
vocab_division['Office of Polar Programs (OPP)'] = 'Division of Polar Programs'
vocab_directorate['CISE Information Technology Research'] = 'none'

def obs1():
    paperid2numcitation = {}
    fr = open('DATA/mag-references.txt','rb')
    fr.readline()
    for line in fr:
        arr = line.strip('\r\n').split(' ')
        paperid = arr[0]
        numcitation = int(arr[2])
        paperid2numcitation[paperid] = numcitation
    fr.close()

    authoridaffid2paperidset = {}
    fr = open('DATA/mag-papers.txt','rb')
    fr.readline()
    for line in fr:
        arr = line.strip('\r\n').split(' ')
        paperid = arr[0]
        for i in range(6,len(arr)):
            _arr = arr[i].split(':')
            if _arr[0] == 'none' or _arr[2] == 'none': continue
            authoridaffid = _arr[0]+':'+_arr[2]
            if not authoridaffid in authoridaffid2paperidset:
                authoridaffid2paperidset[authoridaffid] = set()
            authoridaffid2paperidset[authoridaffid].add(paperid)
    fr.close()

    investigatorinstitution2awardspapers = {}
    awardid2amount = {}
    fr = open('DATA/match-nsf-amg.txt','rb')
    fr.readline()
    for line in fr:
        arr = line.strip('\r\n').split(' ')
        awardid = arr[0]
        amount = int(arr[3])
        awardid2amount[awardid] = amount
        for i in range(4,len(arr)):
            _arr = arr[i].split(':')
            investigatorinstitution = _arr[0]+':'+_arr[1]
            if not investigatorinstitution in investigatorinstitution2awardspapers:
                investigatorinstitution2awardspapers[investigatorinstitution] = [set(),set()]
            investigatorinstitution2awardspapers[investigatorinstitution][0].add(awardid)
            for j in range(2,len(_arr),2):
                authoridaffid = _arr[j]+':'+_arr[j+1]
                if authoridaffid in authoridaffid2paperidset:
                    for paperid in authoridaffid2paperidset[authoridaffid]:
                        investigatorinstitution2awardspapers[investigatorinstitution][1].add(paperid)
    fr.close()

    investigatorinstitution2stats = {}
    for [investigatorinstitution,[awardidset,paperidset]] in investigatorinstitution2awardspapers.items():
        numaward = len(awardidset)
        totalamount = 0
        for awardid in awardidset:
            totalamount += awardid2amount[awardid]
        numpaper = len(paperidset)
        totalcitation = 0
        for paperid in paperidset:
            totalcitation += paperid2numcitation[paperid]
        investigatorinstitution2stats[investigatorinstitution] = [numaward,totalamount,numpaper,totalcitation]
        
    fw = open('OBS/obs1.txt','w')
    fw.write('INVESTIGATOR:INSTITUTION\tNUMAWARD\tTOTALAMOUNT\tNUMPAPER\tTOTALCITATION\n')
    for [investigatorinstitution,stats] in sorted(investigatorinstitution2stats.items(),key=lambda x:x[0]):
        fw.write(investigatorinstitution+'\t'+str(stats[0])+'\t'+str(stats[1])+'\t'+str(stats[2])+'\t'+str(stats[3])+'\n')
    fw.close()

    fw = open('OBS/obs1-numaward.txt','w')
    fw.write('INVESTIGATOR:INSTITUTION\tNUMAWARD\tTOTALAMOUNT\tNUMPAPER\tTOTALCITATION\n')
    for [investigatorinstitution,stats] in sorted(investigatorinstitution2stats.items(),key=lambda x:-x[1][0]):
        fw.write(investigatorinstitution+'\t'+str(stats[0])+'\t'+str(stats[1])+'\t'+str(stats[2])+'\t'+str(stats[3])+'\n')
    fw.close()

    fw = open('OBS/obs1-totalamount.txt','w')
    fw.write('INVESTIGATOR:INSTITUTION\tNUMAWARD\tTOTALAMOUNT\tNUMPAPER\tTOTALCITATION\n')
    for [investigatorinstitution,stats] in sorted(investigatorinstitution2stats.items(),key=lambda x:-x[1][1]):
        fw.write(investigatorinstitution+'\t'+str(stats[0])+'\t'+str(stats[1])+'\t'+str(stats[2])+'\t'+str(stats[3])+'\n')
    fw.close()

    fw = open('OBS/obs1-numpaper.txt','w')
    fw.write('INVESTIGATOR:INSTITUTION\tNUMAWARD\tTOTALAMOUNT\tNUMPAPER\tTOTALCITATION\n')
    for [investigatorinstitution,stats] in sorted(investigatorinstitution2stats.items(),key=lambda x:-x[1][2]):
        fw.write(investigatorinstitution+'\t'+str(stats[0])+'\t'+str(stats[1])+'\t'+str(stats[2])+'\t'+str(stats[3])+'\n')
    fw.close()

    fw = open('OBS/obs1-totalcitation.txt','w')
    fw.write('INVESTIGATOR:INSTITUTION\tNUMAWARD\tTOTALAMOUNT\tNUMPAPER\tTOTALCITATION\n')
    for [investigatorinstitution,stats] in sorted(investigatorinstitution2stats.items(),key=lambda x:-x[1][3]):
        fw.write(investigatorinstitution+'\t'+str(stats[0])+'\t'+str(stats[1])+'\t'+str(stats[2])+'\t'+str(stats[3])+'\n')
    fw.close()

def plot_obs1():
    import matplotlib.pyplot as plt

    stats = []
    fr = open('OBS/obs1.txt','rb')
    fr.readline()
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        stats.append([int(arr[1]),int(arr[2]),int(arr[3]),int(arr[4])])
    fr.close()

    fw = open('OBS/obs1-numawardpaper-freq.txt','w')

    # obs1-numaward-freq

    value2freq = {}
    for item in stats:
        value = item[0]
        if not value in value2freq:
            value2freq[value] = 0
        value2freq[value] += 1
    value_freq = sorted(value2freq.items(),key=lambda x:x[0])
    values = [item[0] for item in value_freq]
    freqs = [item[1] for item in value_freq]

    fw.write('NUMAWARD\tFREQ\n')
    for [value,freq] in value_freq:
        fw.write(str(value)+'\t'+str(freq)+'\n')
    fw.write('\n')

    plt.figure(figsize=(6,4))
    plt.loglog(values,freqs,'-ok',markersize=2.5)
    plt.xlabel('Number of awards: $x$')
    plt.ylabel('Number of (investigator, institution) that have $x$ awards')
    plt.savefig('OBS/obs1-numaward-freq.pdf')

    # obs1-numpaper-freq

    value2freq = {}
    for item in stats:
        value = item[2]
        if not value in value2freq:
            value2freq[value] = 0
        value2freq[value] += 1
    value_freq = sorted(value2freq.items(),key=lambda x:x[0])
    values = [item[0] for item in value_freq]
    freqs = [item[1] for item in value_freq]

    fw.write('NUMPAPER\tFREQ\n')
    for [value,freq] in value_freq:
        fw.write(str(value)+'\t'+str(freq)+'\n')
    fw.write('\n')

    plt.figure(figsize=(6,4))
    plt.loglog(values,freqs,'-ok',markersize=2.5)
    plt.xlabel('Number of papers: $x$')
    plt.ylabel('Number of (investigator, institution) that have $x$ papers')
    plt.savefig('OBS/obs1-numpaper-freq.pdf')

    fw.close()

    # obs1-numaward-numpaper

    xyset = set()
    for item in stats:
        xyset.add(str(item[0])+' '+str(item[2]))
    xs,ys = [],[]
    for xy in xyset:
        arr = xy.split(' ')
        x,y = int(arr[0]),int(arr[1])
        if x < 10 or y < 10: continue
        xs.append(x)
        ys.append(y)

    plt.figure(figsize=(6,4))
    plt.loglog(xs,ys,'ok',alpha=0.5,markersize=1)
    plt.xlabel('Number of awards')
    plt.ylabel('Number of papers')
    plt.savefig('OBS/obs1-numaward-numpaper.pdf')

    # obs1-numaward-totalcitation

    xyset = set()
    for item in stats:
        xyset.add(str(item[0])+' '+str(item[3]))
    xs,ys = [],[]
    for xy in xyset:
        arr = xy.split(' ')
        x,y = int(arr[0]),int(arr[1])
        if x < 10 or y < 10: continue
        xs.append(x)
        ys.append(y)

    plt.figure(figsize=(6,4))
    plt.loglog(xs,ys,'ok',alpha=0.5,markersize=1)
    plt.xlabel('Number of awards')
    plt.ylabel('Total citation count')
    plt.savefig('OBS/obs1-numaward-totalcitation.pdf')

    # obs1-totalamount-numpaper

    xyset = set()
    for item in stats:
        xyset.add(str(item[1])+' '+str(item[2]))
    xs,ys = [],[]
    for xy in xyset:
        arr = xy.split(' ')
        x,y = int(arr[0]),int(arr[1])
        if x < 10 or y < 10: continue
        xs.append(x)
        ys.append(y)

    plt.figure(figsize=(6,4))
    plt.loglog(xs,ys,'ok',alpha=0.5,markersize=1)
    plt.xlabel('Total award amount')
    plt.ylabel('Number of papers')
    plt.savefig('OBS/obs1-totalamount-numpaper.pdf')

    # obs1-totalamount-totalcitation

    xyset = set()
    for item in stats:
        xyset.add(str(item[1])+' '+str(item[3]))
    xs,ys = [],[]
    for xy in xyset:
        arr = xy.split(' ')
        x,y = int(arr[0]),int(arr[1])
        if x < 10 or y < 10: continue
        xs.append(x)
        ys.append(y)

    plt.figure(figsize=(6,4))
    plt.loglog(xs,ys,'ok',alpha=0.5,markersize=1)
    plt.xlabel('Total award amount')
    plt.ylabel('Total citation count')
    plt.savefig('OBS/obs1-totalamount-totalcitation.pdf')

def obs2():
    import numpy as np

    effectiveyear2awardstats = {}
    fr = open('DATA/match-nsf-mag.txt','rb')
    fr.readline()
    for line in fr:
        arr = line.strip('\r\n').split(' ')
        year = int(arr[1])
        amount = int(arr[3])
        if not year in effectiveyear2awardstats:
            effectiveyear2awardstats[year] = [0,0]
        effectiveyear2awardstats[year][0] += 1
        effectiveyear2awardstats[year][1] += amount
    fr.close()

    fw = open('OBS/obs2.txt','w')
    fw.write('EFFECTIVEYEAR\tNUMAWARD\tTOTALAMOUNT\tAMOUNTPERAWARD\n')
    for [year,[numaward,totalamount]] in sorted(effectiveyear2awardstats.items(),key=lambda x:x[0]):
        fw.write(str(year)+'\t'+str(numaward)+'\t'+str(totalamount)+'\t'+str(np.round(1.*totalamount/numaward,2))+'\n')
    fw.close()

def plot_obs2():
    import matplotlib.pyplot as plt

    stats = []
    fr = open('OBS/obs2.txt','rb')
    fr.readline()
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        stats.append([int(arr[0]),int(arr[1]),int(arr[2]),float(arr[3])])
    fr.close()
    stats = stats[:-2]

    # obs2-year-numaward

    xs = [item[0] for item in stats]
    ys = [item[1] for item in stats]

    plt.figure(figsize=(6,4))
    plt.plot(xs,ys,'-ok',markersize=2.5)
    plt.xlabel('Award effective year')
    plt.ylabel('Number of awards')
    plt.savefig('OBS/obs2-year-numaward.pdf')

    # obs2-year-totalamount

    xs = [item[0] for item in stats]
    ys = [item[2] for item in stats]

    plt.figure(figsize=(6,4))
    plt.plot(xs,ys,'-ok',markersize=2.5)
    plt.ticklabel_format(axis='y',style='sci',scilimits=(-2,2))
    plt.xlabel('Award effective year')
    plt.ylabel('Total award amount')
    plt.savefig('OBS/obs2-year-totalamount.pdf')

    # obs2-year-amountperaward

    xs = [item[0] for item in stats]
    ys = [item[3] for item in stats]

    plt.figure(figsize=(6,4))
    plt.plot(xs,ys,'-ok',markersize=2.5)
    plt.ticklabel_format(axis='y',style='sci',scilimits=(-2,2))
    plt.xlabel('Award effective year')
    plt.ylabel('Average amount per award')
    plt.savefig('OBS/obs2-year-amountperaward.pdf')

def obs3():
    authoridaffid2paperidset = {}
    paperid2yearcite = {}
    fr = open('DATA/mag-papers.txt','rb')
    fr.readline()
    for line in fr:
        arr = line.strip('\r\n').split(' ')
        paperid = arr[0]
        year = int(arr[1])
        cite = int(arr[5])
        for i in range(6,len(arr)):
            _arr = arr[i].split(':')
            if _arr[0] == 'none' or _arr[2] == 'none': continue
            authoridaffid = _arr[0]+':'+_arr[2]
            if not authoridaffid in authoridaffid2paperidset:
                authoridaffid2paperidset[authoridaffid] = set()
            authoridaffid2paperidset[authoridaffid].add(paperid)
        paperid2yearcite[paperid] = [year,cite]
    fr.close()

    fws = []
    for ext in range(4):
        fw = open('OBS/obs3-ext'+str(ext)+'y.txt','w')
        fw.write('AWARDID EFFECTIVE EXPIRATION AMOUNT FIRSTPI NUMPAPER NUMCITATION\n')        
        fws.append(fw)
    fr = open('DATA/match-nsf-mag.txt','rb')
    fr.readline()
    for line in fr:
        arr = line.strip('\r\n').split(' ')
        s = arr[0]+' '+arr[1]+' '+arr[2]+' '+arr[3]
        _arr = arr[4].split(':')
        s += ' '+_arr[0]+':'+_arr[1]
        effectiveyear = int(arr[1])
        expirationyear = int(arr[2])
        authoridaffidset = set()
        for i in range(4,len(arr)):
            _arr = arr[i].split(':')
            for j in range(2,len(_arr),2):
                authoridaffid = _arr[j]+':'+_arr[j+1]
                authoridaffidset.add(authoridaffid)
        paperidset = set()
        for authoridaffid in authoridaffidset:
            if not authoridaffid in authoridaffid2paperidset: continue
            for paperid in authoridaffid2paperidset[authoridaffid]:
                paperidset.add(paperid)
        for ext in range(4):
            numpaper,numcitation = 0,0
            for paperid in paperidset:
                year,cite = paperid2yearcite[paperid]
                if year >= effectiveyear and year <= expirationyear+ext:
                    numpaper += 1
                    numcitation += cite
            fws[ext].write(s+' '+str(numpaper)+' '+str(numcitation)+'\n')
    fr.close()
    for fw in fws:
        fw.close()

def plot_obs3():
    import matplotlib.pyplot as plt

    colors = ['r','y','b','g','c','m']

    lst_stats = []
    for ext in range(4):
        stats = []
        fr = open('OBS/obs3-ext'+str(ext)+'y.txt','rb')
        fr.readline()
        for line in fr:
            arr = line.strip('\r\n').split(' ')
            stats.append([int(arr[1]),int(arr[2]),int(arr[3]),int(arr[5]),int(arr[6])])
        fr.close()
        lst_stats.append(stats)

    # obs3-numpaper-freq-ext

    lst_value2freq = []
    for ext in range(4):
        value2freq = {}
        for item in lst_stats[ext]:
            value = item[3]
            if not value in value2freq:
                value2freq[value] = 0
            value2freq[value] += 1
        value_freq = sorted(value2freq.items(),key=lambda x:x[0])
        values = [item[0] for item in value_freq]
        freqs = [item[1] for item in value_freq]
        lst_value2freq.append([values,freqs])

    legendlabels = []
    legendlabels.append('Year: ${Publish}_{paper} \in [{Effective}_{award},{Expiration}_{award}]$')    
    for ext in range(1,4):
        legendlabels.append('Year: ${Publish}_{paper} \in [{Effective}_{award},{Expiration}_{award}+'+str(ext)+']$')

    plt.figure(figsize=(6,4))
    plt.loglog(lst_value2freq[0][0],lst_value2freq[0][1],'-o'+colors[0],markersize=1)
    for ext in range(1,4):
        plt.plot(lst_value2freq[ext][0],lst_value2freq[ext][1],'-o'+colors[ext],markersize=1)
    plt.legend(legendlabels,fontsize=8,loc='lower left')
    plt.xlabel('Number of papers: $x$')
    plt.ylabel('Number of awards that produce $x$ papers')
    plt.savefig('OBS/obs3-numpaper-freq-ext.pdf')

    # obs3-numpaper-freq-decade

    decade2value2freq = {}
    for item in lst_stats[0]:
        year = item[0]
        decade = int(year/10)
        if not decade in decade2value2freq:
            decade2value2freq[decade] = {}
        value = item[3]
        if not value in decade2value2freq[decade]:
            decade2value2freq[decade][value] = 0
        decade2value2freq[decade][value] += 1
    decade_value2freq = []
    for [decade,value2freq] in sorted(decade2value2freq.items(),key=lambda x:x[0]):
        value_freq = sorted(value2freq.items(),key=lambda x:x[0])
        values = [item[0] for item in value_freq]
        freqs = [item[1] for item in value_freq]
        decade_value2freq.append([decade,[values,freqs]])
    decade_value2freq = decade_value2freq[:-1]

    legendlabels = []
    legendlabels.append('${Effective}_{award}$: '+str(decade_value2freq[0][0])+'0--'+str(decade_value2freq[0][0])+'9')    
    for i in range(1,len(decade_value2freq)):
        legendlabels.append('${Effective}_{award}$: '+str(decade_value2freq[i][0])+'0--'+str(decade_value2freq[i][0])+'9')

    plt.figure(figsize=(6,4))
    plt.loglog(decade_value2freq[0][1][0],decade_value2freq[0][1][1],'-o'+colors[0],markersize=1)
    for i in range(1,len(decade_value2freq)):
        plt.plot(decade_value2freq[i][1][0],decade_value2freq[i][1][1],'-o'+colors[i],markersize=1)
    plt.legend(legendlabels,fontsize=10,loc='lower left')
    plt.xlabel('Number of papers: $x$')
    plt.ylabel('Number of awards that produce $x$ papers')
    plt.savefig('OBS/obs3-numpaper-freq-decade.pdf')

    # obs3-amount-numpaper-decade

    decade2points = {}
    for item in lst_stats[0]:
        year = item[0]
        decade = int(year/10)
        if not decade in decade2points:
            decade2points[decade] = []
        if item[2] == 0 or item[3] == 0: continue
        decade2points[decade].append([item[2],item[3]])
    decade_points = sorted(decade2points.items(),key=lambda x:x[0])

    legendlabels = []
    legendlabels.append('${Effective}_{award}$: '+str(decade_points[0][0])+'0--'+str(decade_points[0][0])+'9')    
    for i in range(1,len(decade_points)):
        legendlabels.append('${Effective}_{award}$: '+str(decade_points[i][0])+'0--'+str(decade_points[i][0])+'9')

    plt.figure(figsize=(6,4))
    xyset = set()
    for [x,y] in decade_points[0][1]:
        xyset.add(str(x)+' '+str(y))
    xs,ys = [],[]
    for xy in xyset:
        arr = xy.split(' ')
        x,y = int(arr[0]),int(arr[1])
        if x < 10 or y < 10: continue
        xs.append(x)
        ys.append(y)
    plt.loglog(xs,ys,'o'+colors[0],alpha=0.6,markersize=0.6)
    for i in range(1,len(decade_points)):
        xyset = set()
        for [x,y] in decade_points[i][1]:
            xyset.add(str(x)+' '+str(y))
        xs,ys = [],[]
        for xy in xyset:
            arr = xy.split(' ')
            x,y = int(arr[0]),int(arr[1])
            if x < 10 or y < 10: continue
            xs.append(x)
            ys.append(y)
        plt.plot(xs,ys,'o'+colors[i],alpha=0.6,markersize=0.6)
    plt.legend(legendlabels,fontsize=6,ncol=3)
    plt.xlabel('Award amount')
    plt.ylabel('Number of papers')
    plt.savefig('OBS/obs3-amount-numpaper-decade.pdf')

    # obs3-amount-numcitation-decade

    decade2points = {}
    for item in lst_stats[0]:
        year = item[0]
        decade = int(year/10)
        if not decade in decade2points:
            decade2points[decade] = []
        if item[2] == 0 or item[4] == 0: continue
        decade2points[decade].append([item[2],item[4]])
    decade_points = sorted(decade2points.items(),key=lambda x:x[0])

    legendlabels = []
    legendlabels.append('${Effective}_{award}$: '+str(decade_points[0][0])+'0--'+str(decade_points[0][0])+'9')    
    for i in range(1,len(decade_points)):
        legendlabels.append('${Effective}_{award}$: '+str(decade_points[i][0])+'0--'+str(decade_points[i][0])+'9')

    plt.figure(figsize=(6,4))
    xyset = set()
    for [x,y] in decade_points[0][1]:
        xyset.add(str(x)+' '+str(y))
    xs,ys = [],[]
    for xy in xyset:
        arr = xy.split(' ')
        x,y = int(arr[0]),int(arr[1])
        if x < 10 or y < 10: continue
        xs.append(x)
        ys.append(y)
    plt.loglog(xs,ys,'o'+colors[0],alpha=0.6,markersize=0.6)
    for i in range(1,len(decade_points)):
        xyset = set()
        for [x,y] in decade_points[i][1]:
            xyset.add(str(x)+' '+str(y))
        xs,ys = [],[]
        for xy in xyset:
            arr = xy.split(' ')
            x,y = int(arr[0]),int(arr[1])
            if x < 10 or y < 10: continue
            xs.append(x)
            ys.append(y)
        plt.plot(xs,ys,'o'+colors[i],alpha=0.6,markersize=0.6)
    plt.legend(legendlabels,fontsize=6,ncol=3)
    plt.xlabel('Award amount')
    plt.ylabel('Number of citations')
    plt.savefig('OBS/obs3-amount-numcitation-decade.pdf')

def obs4():
    import numpy as np
    
    directorate2division2numamount = {}
    decade2directorate2division2numamount = {}
    directorate2decade2division2numamount = {}
    fr = open('DATA/nsf-awards.txt','rb')
    fr.readline()
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        amount = int(arr[1])        
        decade = arr[2][6:9]
        directorate = arr[6]
        division = arr[7]
        if 'Direct' in division: continue
        if directorate in vocab_directorate:
            directorate = vocab_directorate[directorate]
        division = division.replace('Div ','Division ')
        division = division.replace('Divn ','Division ')        
        division = division.replace(' Of ',' of ').replace(' On ',' on ')
        if division in vocab_division:
            division = vocab_division[division]
        if directorate == 'none' or division == 'none': continue

        if not directorate in directorate2division2numamount:
            directorate2division2numamount[directorate] = [0,0,{}]
        directorate2division2numamount[directorate][0] += 1
        directorate2division2numamount[directorate][1] += amount
        if not division in directorate2division2numamount[directorate][2]:
            directorate2division2numamount[directorate][2][division] = [0,0]
        directorate2division2numamount[directorate][2][division][0] += 1
        directorate2division2numamount[directorate][2][division][1] += amount

        if not decade in decade2directorate2division2numamount:
            decade2directorate2division2numamount[decade] = {}
        if not directorate in decade2directorate2division2numamount[decade]:
            decade2directorate2division2numamount[decade][directorate] = [0,0,{}]
        decade2directorate2division2numamount[decade][directorate][0] += 1
        decade2directorate2division2numamount[decade][directorate][1] += amount
        if not division in decade2directorate2division2numamount[decade][directorate][2]:
            decade2directorate2division2numamount[decade][directorate][2][division] = [0,0]
        decade2directorate2division2numamount[decade][directorate][2][division][0] += 1
        decade2directorate2division2numamount[decade][directorate][2][division][1] += amount

        if not directorate in directorate2decade2division2numamount:
            directorate2decade2division2numamount[directorate] = {}
        if not decade in directorate2decade2division2numamount[directorate]:
            directorate2decade2division2numamount[directorate][decade] = [0,0,{}]
        directorate2decade2division2numamount[directorate][decade][0] += 1
        directorate2decade2division2numamount[directorate][decade][1] += amount
        if not division in directorate2decade2division2numamount[directorate][decade][2]:
            directorate2decade2division2numamount[directorate][decade][2][division] = [0,0]
        directorate2decade2division2numamount[directorate][decade][2][division][0] += 1
        directorate2decade2division2numamount[directorate][decade][2][division][1] += amount
    fr.close()

    # obs4-directorate-division

    fw = open('OBS/obs4-directorate-division.txt','w')
    for [directorate,[totalnum,totalamount,division2numamount]] in sorted(directorate2division2numamount.items(),key=lambda x:x[0]):
        fw.write('=> DIRECTORATE'+'\t'+directorate+'\n\n')
        fw.write('DIVISION\tNUMAWARD\tAWARDAMOUNT\tPCT_NUMAWARD\tPCT_AWARDAMOUNT\n')
        for [division,[num,amount]] in sorted(division2numamount.items(),key=lambda x:x[0]):
            pctnum = np.round(100.*num/totalnum,2)
            pctamount = np.round(100.*amount/totalamount,2)
            fw.write(division+'\t'+str(num)+'\t'+str(amount)+'\t'+str(pctnum)+'\t'+str(pctamount)+'\n')
        fw.write('total'+'\t'+str(totalnum)+'\t'+str(totalamount)+'\t'+str(np.round(1.*totalamount/totalnum,2))+'\n')
        fw.write('\n')
    fw.close()

    # obs4-directorate-decade

    fw = open('OBS/obs4-directorate-decade.txt','w')
    for [decade,directorate2division2numamount] in sorted(decade2directorate2division2numamount.items(),key=lambda x:x[0]):
        fw.write(str(decade)+'0--'+str(decade)+'9'+'\n\n')
        fw.write('DIRECTORATE\tNUMAWARD\tAWARDAMOUNT\tPCT_NUMAWARD\tPCT_AWARDAMOUNT\n')
        totalnum,totalamount = 0,0
        for [directorate,[num,amount,division2numamount]] in directorate2division2numamount.items():
            totalnum += num
            totalamount += amount
        for [directorate,[num,amount,division2numamount]] in sorted(directorate2division2numamount.items(),key=lambda x:x[0]):
            pctnum = np.round(100.*num/totalnum,2)
            pctamount = np.round(100.*amount/totalamount,2)
            fw.write(directorate+'\t'+str(num)+'\t'+str(amount)+'\t'+str(pctnum)+'\t'+str(pctamount)+'\n')
        fw.write('total'+'\t'+str(totalnum)+'\t'+str(totalamount)+'\t'+str(np.round(1.*totalamount/totalnum,2))+'\n')
        fw.write('\n')
    fw.close()

    # obs4-division-decade

    fw = open('OBS/obs4-division-decade.txt','w')
    for [directorate,decade2division2numamount] in sorted(directorate2decade2division2numamount.items(),key=lambda x:x[0]):
        fw.write('=> DIRECTORATE'+'\t'+directorate+'\n\n')
        for [decade,[num,amount,division2numamount]] in sorted(decade2division2numamount.items(),key=lambda x:x[0]):
            fw.write(str(decade)+'0--'+str(decade)+'9'+'\n\n')
            fw.write('DIVISION\tNUMAWARD\tAWARDAMOUNT\tPCT_NUMAWARD\tPCT_AWARDAMOUNT\n')
            totalnum,totalamount = 0,0
            for [division,[num,amount]] in division2numamount.items():
                totalnum += num
                totalamount += amount
            for [division,[num,amount]] in sorted(division2numamount.items(),key=lambda x:x[0]):
                pctnum = np.round(100.*num/totalnum,2)
                pctamount = np.round(100.*amount/totalamount,2)
                fw.write(division+'\t'+str(num)+'\t'+str(amount)+'\t'+str(pctnum)+'\t'+str(pctamount)+'\n')
            fw.write('total'+'\t'+str(totalnum)+'\t'+str(totalamount)+'\t'+str(np.round(1.*totalamount/totalnum,2))+'\n')
            fw.write('\n')
    fw.close()

def obs5a():
    import nltk

    data = [] # AWARDID,AMOUNT,EFFECTIVEDATE,EXPIRATIONDATE,TITLE,ABSTRACT
    fr = open('DATA/nsf-awards.txt','r')
    fr.readline()
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        directorate = arr[6]
        division = arr[7]
        if 'Direct' in division: continue
        if directorate in vocab_directorate:
            directorate = vocab_directorate[directorate]
        division = division.replace('Div ','Division ')
        division = division.replace('Divn ','Division ')        
        division = division.replace(' Of ',' of ').replace(' On ',' on ')
        if division in vocab_division:
            division = vocab_division[division]
        if directorate == 'none' or division == 'none': continue
        if not directorate == 'Direct For Computer & Info Scie & Enginr': continue
        if not division == 'Division of Information & Intelligent Systems': continue
        if arr[4] == 'none' or arr[5] == 'none': continue
        data.append(arr[:6])
    fr.close()

    fw = open('OBS/obs5-postagdoc.txt','w')
    fw.write('AWARDID\tAMOUNT\tEFFECTIVEDATE\tEXPIRATIONDATE\tPOSTAGDOC\n')
    for item in data:
        title = item[4]
        abstract = item[5]
        doc = title+'. '+abstract
        doc = doc.replace('(Computer and Information Science)','')
        doc = doc.replace('<br>',' ')
        doc = doc.replace('<br/>',' ')

        _doc = ''
        for word in doc.split(' '):
            if word == '': continue
            _doc += ' '+word
        doc = _doc[1:]

        _doc = ''
        for token in nltk.word_tokenize(doc):
            _doc += ' '+token
        doc = _doc[1:]

        _doc = ''
        for (elem,tag) in nltk.pos_tag(nltk.Text(doc.split(' '))):
            if elem in ['e.g.','i.e']:
                _doc += ' '+elem+':'+'IN'
            elif '[' in elem:
                _doc += ' '+elem+':'+'('
            elif ']' in elem:
                _doc += ' '+elem+':'+')'
            elif elem == 'and/or':
                _doc += ' '+elem+':'+'CC'
            else:
                _doc += ' '+elem+':'+tag
        doc = _doc[1:]

        s = ''
        for i in range(4): s += '\t'+item[i]
        s += '\t'+doc
        fw.write(s[1:]+'\n')
    fw.close()

def obs5b():
    # pattern: JJ* {{NN+ VBG}*|NN}* NN
    phrase2awardidset = {}
    awardid2yearamount = {}

    fw = open('OBS/obs5-phrasedoc.txt','w')
    fw.write('AWARDID\tAMOUNT\tEFFECTIVEDATE\tEXPIRATIONDATE\tPHRASEDOC\n')    
    fr = open('OBS/obs5-postagdoc.txt','r')
    fr.readline()
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        awardid = arr[0]
        amount = int(arr[1])
        year = int(arr[2][6:])
        awardid2yearamount[awardid] = [year,amount]
        doc = []
        for item in arr[4].split(' '):
            pos = item.find(':')
            doc.append([item[:pos],item[pos+1:]])
        phraseset = set()
        n = len(doc)
        i = n-1
        while i >= 0:
            if doc[i][1].startswith('NN'):
                tail = i
                i -= 1
                while i >= 0:
                    if i >= 1 and doc[i][1] == 'VBG' and doc[i-1][1].startswith('NN'):
                        i -= 2
                    elif doc[i][1].startswith('NN'):
                        i -= 1
                    else:
                        break
                while i >= 0:
                    if doc[i][1] == 'JJ':
                        i -= 1
                    else:
                        break
                head = i+1
                phrase,postag = '',''
                for j in range(head,tail+1):
                    phrase += '_'+doc[j][0]
                    postag += '_'+doc[j][1]
                phrase = phrase[1:].lower()
                phraseset.add(phrase+':'+postag[1:])
                if not phrase in phrase2awardidset:
                    phrase2awardidset[phrase] = set()
                phrase2awardidset[phrase].add(awardid)
                i -= 1
            else:
                i -= 1
        phrasedoc = ''
        for phrase in sorted(phraseset):
            phrasedoc += ' '+phrase
        s = ''
        for i in range(4): s += '\t'+arr[i]
        s += '\t'+phrasedoc[1:]
        fw.write(s[1:]+'\n')
    fr.close()
    fw.close()

    phrase2year2numamount = {}
    for [phrase,awardidset] in phrase2awardidset.items():
        totalnum,totalamount = 0,0
        year2numamount = {}
        for awardid in awardidset:
            [year,amount] = awardid2yearamount[awardid]
            totalnum += 1
            totalamount += amount
            if not year in year2numamount:
                year2numamount[year] = [0,0]
            year2numamount[year][0] += 1
            year2numamount[year][1] += amount
        phrase2year2numamount[phrase] = [totalnum,totalamount,year2numamount]
    
    fw = open('OBS/obs5-phraseyearawardnum.txt','w')
    fw.write('RANK PHRASE NUMAWARD YEAR_NUMAWARD\n')
    rank = 0
    for [phrase,[totalnum,totalamount,year2numamount]] in sorted(phrase2year2numamount.items(),key=lambda x:-x[1][0]):
        if totalnum < 5: break
        rank += 1
        s = ''
        for [year,[num,amount]] in sorted(year2numamount.items(),key=lambda x:x[0]):
            s += ' '+str(year)+'('+str(num)+')'
        fw.write(str(rank)+' '+phrase+' '+str(totalnum)+s+'\n')
    fw.close()
    fw = open('OBS/obs5-phraseyearawardamount.txt','w')
    fw.write('RANK PHRASE AWARDAMOUNT YEAR_AWARDAMOUNT\n')
    rank = 0
    for [phrase,[totalnum,totalamount,year2numamount]] in sorted(phrase2year2numamount.items(),key=lambda x:-x[1][1]):
        if totalnum < 5: break        
        rank += 1
        s = ''
        for [year,[num,amount]] in sorted(year2numamount.items(),key=lambda x:x[0]):
            s += ' '+str(year)+'('+str(amount)+')'
        fw.write(str(rank)+' '+phrase+' '+str(totalamount)+s+'\n')
    fw.close()

def obs5c():
    topics = [['expert_system'], \
            ['anomaly_detection','event_detection','automatic_detection', \
                'change_detection','intrusion_detection','threat_detection'], \
            ['social_media','social_network'], \
            ['neural_network'], \
            ['formal_method','formal_model','formal_analysis','formal_theory'], \
            ['knowledge_base']]
    ntopic = len(topics)
    topicnames = [topics[i][0] for i in range(ntopic)]
    awardidsets = [set() for i in range(ntopic)]
    awardid2yearamount = {}

    fr = open('OBS/obs5-phrasedoc.txt','r')
    fr.readline()
    for line in fr:
        arr = line.strip('\r\n').split('\t')
        awardid = arr[0]
        amount = int(arr[1])
        year = int(arr[2][6:])
        awardid2yearamount[awardid] = [year,amount]
        for item in arr[4].split(' '):
            pos = item.rfind(':')
            phrase = item[:pos]
            for i in range(ntopic):
                for _phrase in topics[i]:
                    if _phrase in phrase:
                        awardidsets[i].add(awardid)
    fr.close()

    year2numamount = {}
    for i in range(ntopic):
        for awardid in awardidsets[i]:
            [year,amount] = awardid2yearamount[awardid]
            if not year in year2numamount:
                year2numamount[year] = [[0,0] for i in range(ntopic)]
            year2numamount[year][i][0] += 1
            year2numamount[year][i][1] += amount

    fw = open('OBS/obs5-cise-topics.txt','w')
    s = 'YEAR'
    for topicname in topicnames:
        s += '\t'+topicname
    fw.write(s+'\n')
    for [year,numamounts] in sorted(year2numamount.items(),key=lambda x:x[0]):
        s = str(year)
        for i in range(ntopic):
            s += '\t'+str(numamounts[i][0])
        fw.write(s+'\n')
    fw.write('\n')
    s = 'YEAR'
    for topicname in topicnames:
        s += '\t'+topicname
    fw.write(s+'\n')
    for [year,numamounts] in sorted(year2numamount.items(),key=lambda x:x[0]):
        s = str(year)
        for i in range(ntopic):
            s += '\t'+str(numamounts[i][1])
        fw.write(s+'\n')
    fw.close()

if __name__ == '__main__':

    ### Python 2.7 ###

#    obs1()
    plot_obs1()

#    obs2()
#    plot_obs2()

#    obs3()
#    plot_obs3()

#    obs4()

    ### Python 3.6 ###

#    obs5a()
#    obs5b()
#    obs5c()

