#************************************************#
# -- coding:UTF-8 --
#Author: zhaobin Chu
#Create Time: 2017-08-09
#Description: get frequent item set by apriori algorithm

#将双色球开奖号码分离成单个号码的frozenset,方便计算单个号码的出现概率
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset, C1)

#获取概率大于minSupport的号码集合
def scanD(D,Ck,minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not ssCnt.has_key(can): ssCnt[can] = 1
                else: ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    return retList, supportData

#合并出现概率满足minSupport的号码或号码集合，方便计算更大号码集合的概率
def aprioriGen(Lk,k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1==L2:
                retList.append(Lk[i]|Lk[j])
    return retList

# 获取所有出现概率超过minSupport的单个开奖号码以及号码集合
def apriori(dataSet,minSupport=0.5):
    C1 = createC1(dataSet)
    D = map(set,dataSet)
    L1,supportData = scanD(D,C1,minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0 ):
        Ck = aprioriGen(L[k-2],k)
        Lk,supK = scanD(D,Ck,minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L,supportData

