#*******************************************************#
#Author: zhaobin Chu
#Create time: 2017-08-09
#Description: main()

import selectData
import dataAnalysis

if __name__ == '__main__':
    ssqNumber = selectData.getZJnum() #get ssq history number
    
    #L:frequent item set ,suppData:{number set: frequency} 
    L,suppData = dataAnalysis.apriori(ssqNumber,0.04)
    
    numSet = sorted(suppData.items(), \
            key = lambda p: p[1], reverse = True)
    for number in numSet:
        print number
