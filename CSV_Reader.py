__author__ = 'Owner'

# Initialization

fileName = sys.argv[1]

# Reading the CSV files
# Acquisition of assessments, every column is a judge, every row is
# a subject.

csvFile = open(fileName,'r')
csvData = csv.reader(csvFile)

assessments = []

for subject in csvData:

    assessment = []

    for item in subject[1:]:
        assessment.append(int(item))

    assessments.append(assessment)
