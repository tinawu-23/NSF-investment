import pandas as pd

collist = ['awardid', 'AwardTitle',
           'AwardEffectiveDate', 'AwardExpirationDate', 'AwardAmount', 'MinAmdLetterDate', 'IsHistoricalAward', 'Institution-Name', 'Institution-StateCode', 'Institution-StateName', 'Institution-CountryFlag', 'AwardAmountRangeCategory', 'MinAmdLetterDateEpoch', 'AwardEffectiveDateEpoch']
df = pd.DataFrame(columns = collist)
previd = " "
rownum = -1
with open('data.txt') as f:
    for line in f:
        awardid = line.split()[0]
        if awardid != previd:
            rownum += 1
            df.loc[rownum] = [0 for n in range(14)]
            df.iloc[rownum][0] = awardid
            previd = awardid
        print(line.split()[1].strip())
        if (line.split()[1].strip() == "AwardID"):
            continue
        else:
            colid = line.split()[1].strip()
            if colid in collist:
                df.at[rownum, colid] = line.split()[2:]

print(df)
