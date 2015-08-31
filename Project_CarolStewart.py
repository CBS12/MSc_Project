fa__author__ = 'CS 2160196S'

import csv
import math
'''
    method to calculate and apply linear discount
    :parameter dictionary{string:integer):nGram string/word and frequency
    :returns dictionary {string: float}: nGram string and discounted frequency
'''


def linear_discount(countDict):
    # create a dictionary of (r:nr), word frequencies: frequency of frequencies
    countD = {}
    for nr in countDict.values():
        countD[nr] = countDict.values().count(nr)
    # print countD
    # print sum(countD.values())

    discountedDict = {}
    totalR = sum(countDict.values())
    # calculate linear discount applying factor (1 - nr/sum(r)) to frequency
    for word in countDict:
        for count in countD:
            if countDict[word] == count:
                discountedDict[word] = (1 - (countD[count]) / float(totalR)) * (countDict[word])

    totalrxnr = sum(discountedDict.values())
    # calculating total of the discounted count to apportion the remainder to zero frequency words.
    for word in discountedDict:
        if discountedDict[word] == 0.0:
            discountedDict[word] = (totalR - totalrxnr) / float(countD[0])
    return discountedDict


'''
    Creating a list of ngrams
'''

def combinations(nGramsize):
    a = ['talk', 'laugh', 'filler', 'backchannel', 'talk_talk', 'talk_laugh', 'talk_filler', 'talk_backchannel',
         'laugh_laugh', 'laugh_filler',
         'laugh_backchannel', 'filler_filler', 'filler_backchannel', 'backchannel_backchannel', 'silence', 'ring',
         'end']

    statelist = []
    if nGramsize == 0:
        return None
    elif nGramsize == 1:
        return a
    elif nGramsize >= 2:
        index = 1
        for i in a:
            # noinspection PyTypeChecker
            for n in combinations(nGramsize - 1):
                newstate = i + '->' + n

                statelist.append(newstate)
                # print str.format('S%d(%d) = %s|%s    ' % (nGramsize, index, i, n))
                index += 1
        return statelist


'''
    Method to create a dictionary of probabilities for test and training data and calculating the perplexity
    :parameter string conCode; code for test conversation
    :parameter string filename; data file
    :parameter integer nGramsize; size of nGrams being evaluated
    :returns    float perplexity;
'''


def readCon(conCode, filename, nGramSize):
    # Final program will extract this list from the file as a set.
    statelist_base = ['talk', 'laugh', 'filler', 'backchannel', 'talk_talk', 'talk_laugh', 'talk_filler',
                      'talk_backchannel',
                      'laugh_laugh', 'laugh_filler', 'laugh_backchannel', 'filler_filler', 'filler_backchannel',
                      'backchannel_backchannel', 'silence', 'ring', 'end']

    statelist_Ngram = combinations(nGramSize)
    f = open(filename, 'r')  # open the csv file
    reader = csv.reader(f)  # creates the reader object

    # listing the conversation data, separating the test from the training in the corpus
    test_cons = []
    train_cons = []
    for row in reader:
        if row[0] == conCode:
            test_cons.append(row[1].strip())
        else:
            train_cons.append(row[1].strip())
    del train_cons[0]  # remove header entry
    f.close()

    # creating a list of the nGram states TODO change the format of the nGrams to (w|h)
    test_nGramlist = []
    index = 0
    if nGramSize == 1:
        for i in test_cons:
            test_nGramlist.append(i)
    else:
        while index < len(test_cons) - nGramSize + 1:
            newstate = test_cons[index]
            for i in range(1, nGramSize):
                newstate += '->' + test_cons[index + i]
            test_nGramlist.append(newstate)
            index += 1
    # print test_nGramlist

    train_nGramlist = []
    index = 0
    if nGramSize == 1:
        for i in train_cons:
            train_nGramlist.append(i)
    else:
        while index < len(train_cons) - nGramSize + 1:
            train_newstate = train_cons[index]
            for i in range(1, nGramSize):
                train_newstate += '->' + train_cons[index + i]
            train_nGramlist.append(train_newstate)
            index += 1

    # counting the frequency of occurences of nGrams and adding to a dictionary=====
    test_dictCountsN = {}
    index = 1
    for i in statelist_Ngram:
        test_dictCountsN[i] = test_nGramlist.count(i)
        # print str.format('N_test%s(%s) = %d    ' % (conCode, i, test_dictCountsN[i]))
        index += 1

    train_dictCountsN = {}
    index = 1
    for i in statelist_Ngram:
        train_dictCountsN[i] = train_nGramlist.count(i)
        # print str.format('N_train%d(%s) = %d    ' % (nGramSize, i, train_dictCountsN[i]))
        index += 1

    # calculating the estimated probability of each state==============================

    test_probDict = {} #TODO final version cut down excessive number of dictionaries
    for i in statelist_Ngram:
        test_probDict[i] = int(test_dictCountsN[i]) / float(len(test_nGramlist))
        # print str.format('P%s(%s) = %.6f    ' % (conCode, i, test_probDict[i]))
    # print sum(test_probDict.values())

    train_probDict = {}
    for i in statelist_Ngram:
        train_probDict[i] = int(train_dictCountsN[i]) / float(len(train_nGramlist))
        # print str.format('P%d(%s) = %.6f    ' % (nGramSize, i, train_probDict[i]))
        # print sum(train_probDict.values())

        # calculating the discounted probabilities of each state in the training data=========

    train_discountprobDict = {}
    train_discountedCounts = linear_discount(train_dictCountsN)
    for i in statelist_Ngram:
        train_discountprobDict[i] = int(train_discountedCounts[i]) / float(len(train_nGramlist))
        # print str.format('P*%d(%s) = %.6f    ' % (nGramSize, i, train_discountprobDict[i]))
    # print sum(train_discountprobDict.values())

    # calculating perplexity before linear discount============================================
    cross_entropy = 0.0
    for i in statelist_Ngram:
        if train_probDict[i] > 0:
            cross_entropy += (test_probDict[i] * math.log(train_probDict[i],10))
    perplexity = round(2 ** (-1 * cross_entropy), 3)
    # print ('Perplexity = ' + str(perplexity))

    # calculating perplexity after smoothing =================================================
    cross_entropy = 0.0
    for i in statelist_Ngram:
        if train_discountprobDict[i] > 0:
            '''
                using log base 10, use of natural log leads to an exaggerated increase in perplexity
                for increasing nGram size
             '''
            cross_entropy += (test_probDict[i] * math.log(train_discountprobDict[i], 10)) #or math.e instead
    discountperplexity = round(2 ** (-1 * cross_entropy), 3)
    # print ('Discount Perplexity = ' + str(discountperplexity))
    return discountperplexity


def listPerplexities(nGramsize, numberCons):
    """
    Input the required size of nGram and the number of test cases to be explored
    each test case (FO1 - first conversation, FO2 - second conversation, etc) is examined
    against the remainder of the corpus (ie training data) so FO1 against corpus excl FO1,
    FO2 against corpus excl FO2, etc.
    :parameter; nGramsize integer
    :parameter: numberCons integer
    :rtype : float, average perplexity
    """
    i = 1
    perplexity_dict = {}
    while i <= numberCons:
        convCode = str.format('F%02d' % i)
        perplexity_dict[convCode] = readCon(convCode, 'GenderRoleCorpusBasic.csv', nGramsize)
        i += 1
    print ("\n"+"NGram size: " + str(nGramsize))
    print perplexity_dict
    # calculate mean perplexity over a number of test cases
    return sum(perplexity_dict.values())/float(numberCons)


print ("mean perplexity: " + str(listPerplexities(1, 3)))
listPerplexities(2, 3)
listPerplexities(3, 3)
# listPerplexities(4, 1)
