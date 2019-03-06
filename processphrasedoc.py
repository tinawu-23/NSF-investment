fr = open('obs5-phrasedoc.txt', 'r')
fw = open('NSF_awardtopics.txt', 'w')
fr.readline()
for line in fr:
    arr = line.strip('\r\n').split('\t')
    awardid = arr[0]
    amount = int(arr[1])
    year = int(arr[2][6:])
    topicstr = ''
    for item in arr[4].split(' '):
        pos = item.rfind(':')
        phrase = item[:pos].replace("_", " ").replace("*", "")
        topicstr += (phrase+' ')
    fw.write(topicstr+'\n')
fr.close()
