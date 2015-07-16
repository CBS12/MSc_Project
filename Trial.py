__author__ = 'CS 2160196S'

import csv

f = open('GenderRoleCorpusBasic.csv', 'r')#open the csv file
reader = csv.reader(f)#creates the reader object

#listing the states
conStates = []
for row in reader:
  conStates.append(row[1].strip())
del conStates[0] #remove header entry

f.close()

# states = set(conStates)
# index = 1
# for i in states:
#     print str.format('S(%d) = %s    ' %(index,i))
#     index += 1
# print '\n'
#
#
# #counting the frequency of occurences and adding to a dictionary
#
# dictStates = {}
# index = 1
# for i in states:
#     dictStates[i] = conStates.count(i)
#
#     print str.format('N(%d) = %d    ' %(index,conStates.count(i)))
#     index += 1
# print dictStates['l']
#
#
#
#
#
# #calculating the estimated probability of each
#
# totalStates = float(len(conStates))
# print totalStates
#
# dictProbs = {}
# index = 1
# for i in states:
#     dictProbs[i] = int(dictStates[i])/totalStates
#     # print dictProbs[i]
#     print str.format('E(%d) = %.4f    ' %(index, (float(dictStates[i])/totalStates)))
#     index += 1

#=======================================================================================================
#playing with NGrams

conStatesN = []
n = 2
index = 0
while index < len(conStates) - (n):
    newState = ''
    for i in range(n):
        newState += conStates[index + (i)] + '_'
    conStatesN.append(newState)
    print conStatesN[index]
    index += 1

# #listing the states
statesN = set(conStatesN)

index = 1
for i in statesN:
    print str.format('S%d(%d) = %s    ' %(n,index,i))
    index += 1
print '\n'

# #counting the frequency of occurences and adding to a dictionary

dictStatesN = {}
index = 1
for i in statesN:
    dictStatesN[i] = conStatesN.count(i)

    print str.format('N%d(%d) = %d    ' %(n,index,conStatesN.count(i)))
    index += 1



# #calculating the estimated probability of each

totalStatesN = float(len(conStatesN))
print totalStatesN

dictProbsN = {}
index = 1
for i in statesN:
    dictProbsN[i] = int(dictStatesN[i])/totalStatesN
    print str.format('E%d(%d) = %.4f    ' %(n,index, (float(dictStatesN[i])/totalStatesN)))
    index += 1
print sum(dictProbsN.values())