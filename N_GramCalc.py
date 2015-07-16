__author__ = 'Owner'
'''
Program to read and count conversation states from .csv file.
Identifies states and calculates estimated probabilities
'''
import csv

def readFile(workfile):
    """
    method to open file and create a list of conversational states
    :param workfile: .csv file
    :return conStates[]: a list of strings representing conversational states
    """

    f = open('GenderRoleCorpusTest.csv', 'r')#open the csv file
    reader = csv.reader(f)#creates the reader object

    #listing the states
    conStates = []
    for row in reader:
        conStates.append(row[1])
    #remove header entry, TODO# Find more elegant approach
    del conStates[0]

    f.close()
    return conStates

def createNGramSet(conStates, n):
    """
    :param conStates: List of individual conversational states
    :param n: size of NGram
    :return states: a set of NGram conversational states
    TODO# add process for different values of n
    """
    #remove duplicates
    states = set(conStates)
    index = 1
    for i in states:
        print str.format('S(%d) = %s    ' %(index,i))
        index += 1
    print '\n'
    return states

def conStatesCount(states,conStates):
    """
    counting the frequency of occurences of conversational states and adding to a dictionary
    :param states: set of conversational state lists/sequences for NGram
    :param conStates: list of individual conStates
    :return dictStates:dictionary of states and counts
    """

    dictStates = {}
    index = 1
    for i in states:
        dictStates[i] = conStates.count(i)
        print str.format('N(%d) = %d    ' %(index,conStates.count(i)))
        index += 1

    return dictStates

def estProbability(states,dictStates):

    """
    calculating the estimated probability of each of the NGram states
    :param dictStates: dictionary of states and their frequency
    :return dictProbs: dictionary of states and their estimated probabilities
    """
    totalStates = float(sum(dictStates.values()))
    print totalStates

    dictProbs = {}
    index = 1
    for i in states:
        dictProbs[i] = int(dictStates[i])/totalStates
        #print dictProbs[i]
        print str.format('E(%d) = %.4f    ' %(index, (float(dictStates[i])/totalStates)))
        index += 1
    return dictProbs


readFile('GenderRoleCorpusTest')
print estProbability()