__author__ = 'CS 2160196S'

import csv
import sys

# def readFile(workfile):
#


f = open('GenderRoleCorpusBasic.csv', 'r')#open the csv file
reader = csv.reader(f)#creates the reader object

#listing the states
conStates = []
for row in reader:
  conStates.append(row[1])
del conStates[0] #remove header entry

f.close()

states = set(conStates)
index = 1
for i in states:
    print str.format('S(%d) = %s    ' %(index,i))
    index += 1
print '\n'
#counting the frequency of occurences and adding to a dictionary

dictStates = {}
index = 1
for i in states:
    dictStates[i] = conStates.count(i)

    print str.format('N(%d) = %d    ' %(index,conStates.count(i)))
    index += 1
print dictStates['l']
#calculating the estimated probability of each

totalStates = float(len(conStates))
print totalStates

dictProbs = {}
index = 1
for i in states:
    dictProbs[i] = int(dictStates[i])/totalStates
    #print dictProbs[i]
    print str.format('E(%d) = %.4f    ' %(index, (float(dictStates[i])/totalStates)))
    index += 1


