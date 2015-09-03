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

def combinations(ngramsize):
    statelist_base = ['talk', 'laugh', 'filler', 'backchannel', 'talk_talk', 'talk_laugh', 'talk_filler', 'talk_backchannel',
     'laugh_laugh', 'laugh_filler',
     'laugh_backchannel', 'filler_filler', 'filler_backchannel', 'backchannel_backchannel', 'silence', 'ring',
     'end']

    statelist = []
    if ngramsize == 0:
        return None
    elif ngramsize == 1:
        return statelist_base
    elif ngramsize >= 2:
        index = 1
        for i in statelist_base:
            # noinspection PyTypeChecker
            for n in combinations(ngramsize - 1):
                newstate = i + '->' + n

                statelist.append(newstate)
                # print str.format('S%d(%d) = %s|%s    ' % (nGramsize, index, i, n))
                index += 1
        return statelist

class Perplexity(object):

    statelist_base = ['talk', 'laugh', 'filler', 'backchannel', 'talk_talk', 'talk_laugh', 'talk_filler', 'talk_backchannel',
         'laugh_laugh', 'laugh_filler',
         'laugh_backchannel', 'filler_filler', 'filler_backchannel', 'backchannel_backchannel', 'silence', 'ring',
         'end']



    def __init__(self,ngramsize,filename):
        self.ngramsize = ngramsize
        self.filename = filename
        self.testconrange = []


    def setTestConRange(self,start,numberCons):
        self.testconrange = []
        for k in range(start, start + numberCons,1):
            self.testconrange.append(str.format("F%02d" %k))
        return self.testconrange


    '''
        Method to create a dictionary of probabilities for test and training data and calculating the perplexity
        :parameter string conCode; code for test conversations
        :parameter string filename; data file
        :parameter integer nGramsize; size of nGrams being evaluated
        :returns float perplexity;
    '''


    def readCon(self):

        statelist_Ngram =  combinations(self.ngramsize)
        f = open(self.filename, 'r')  # open the csv file
        reader = csv.reader(f)  # creates the reader object

    # listing the conversation data, separating the test from the training in the corpus
        test_cons = []
        train_cons = []
        for row in reader:
            if row[0] in self.testconrange:
                test_cons.append(row[1].strip())
            else:
                train_cons.append(row[1].strip())
        del train_cons[0]  # remove header entry
        f.close()

    # creating a list of the nGram states TODO change the format of the nGrams to (w|h)
        test_nGramlist = []
        index = 0
        if self.ngramsize == 1:
            for i in test_cons:
                test_nGramlist.append(i)
        else:
            while index < len(test_cons) - self.ngramsize + 1:
                newstate = test_cons[index]
                for i in range(1, self.ngramsize):
                    newstate += '->' + test_cons[index + i]
                test_nGramlist.append(newstate)
                index += 1
        # print test_nGramlist

        train_nGramlist = []
        index = 0
        if self.ngramsize == 1:
            for i in train_cons:
                train_nGramlist.append(i)
        else:
            while index < len(train_cons) - self.ngramsize + 1:
                train_newstate = train_cons[index]
                for i in range(1, self.ngramsize):
                    train_newstate += '->' + train_cons[index + i]
                train_nGramlist.append(train_newstate)
                index += 1

    # counting the frequency of occurences of nGrams and adding to a dictionary=====
        test_dictCountsN = {}
        index = 1
        for i in statelist_Ngram:
            test_dictCountsN[i] = test_nGramlist.count(i)
            # print str.format('N_test(%s) = %d    ' % (i, test_dictCountsN[i]))
            index += 1
        # print len(test_nGramlist)

        train_dictCountsN = {}
        index = 1
        for i in statelist_Ngram:
            train_dictCountsN[i] = train_nGramlist.count(i)
            # print str.format('N_train%d(%s) = %d    ' % (self.ngramsize, i, train_dictCountsN[i]))
            index += 1

    # calculating the estimated probability of each state==============================

        test_probDict = {} #TODO final version cut down excessive number of dictionaries
        for i in statelist_Ngram:
            test_probDict[i] = int(test_dictCountsN[i]) / float(len(test_nGramlist))
            # print str.format('P_test(%s) = %.6f    ' % (i, test_probDict[i]))
        # print sum(test_probDict.values())

        train_probDict = {}
        for i in statelist_Ngram:
            train_probDict[i] = int(train_dictCountsN[i]) / float(len(train_nGramlist))
            # print str.format('P_train%d(%s) = %.6f    ' % (self.ngramsize, i, train_probDict[i]))
            # print sum(train_probDict.values())

    # calculating the discounted probabilities of each state in the training data=========

        train_discountprobDict = {}
        train_discountedCounts = linear_discount(train_dictCountsN)
        for i in statelist_Ngram:
            train_discountprobDict[i] = int(train_discountedCounts[i]) / float(len(train_nGramlist))
            # print str.format('P*%d(%s) = %.8f    ' % (self.ngramsize, i, train_discountprobDict[i]))
        # print sum(train_discountprobDict.values())

    # calculating perplexity before linear discount============================================
        # cross_entropy = 0.0
        # for i in statelist_Ngram:
        #     if train_probDict[i] > 0:
        #         cross_entropy += (test_probDict[i] * math.log(train_probDict[i],10))
        # perplexity = round(2 ** (-1 * cross_entropy), 3)
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
        print ('Discount Perplexity = ' + str(discountperplexity))
        return discountperplexity


def Main():
    begin = raw_input("Enter the nGramsize: ")
    ngramsize = int(begin)
    any = Perplexity(ngramsize,"GenderRoleCorpusBasic.csv")
    perplexity_dict = {}
    for i in range(3):
        start = i*20 + 1
        end = i* 20 + 20
        any.setTestConRange(start,20)
        convCode = "\nF{:02d} to F{:02d}".format(start,end)
        print convCode
        # print any.readCon()
        perplexity_dict[convCode] = any.readCon()
        i += 1
    # calculate mean perplexity over a number of test cases
    mean_perplexity = sum(perplexity_dict.values())/3.0
    print '\nOverall mean_perplexity = {:.3f}'.format(mean_perplexity)

if __name__ == '__main__':
    Main()

