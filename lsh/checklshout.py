
"""

Author : Berk Mandiracioglu


"""


import pandas as pd

xls = pd.ExcelFile("corpus-final09.xls")

sheetX = xls.parse(1) #2 is the sheet number

files = sheetX['File']

categories = sheetX['Category']


import glob

countL = 0
countH = 0
countN = 0
countC = 0

for filename in glob.glob('doc_nes.txt'):
	with codecs.open(filename, "r",encoding='utf-8', errors='ignore') as f:
		for line in f:


tp = countC / 19
fp = (countN+countH+countL)/(19+19+38)

tn = 1-fp
fn = 1-tp


print("true positive:",tp)
print("false positive:",fp)
print("true negative:",tn)
print("false negative:",fn)