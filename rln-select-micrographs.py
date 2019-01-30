#!/usr/bin/env python

# give a starfile with micrographs (from otf processing or anywhere esle) and a list of the files you want to keep and get a starfile with just tje ones you wanted.

import sys

###---------function: read the star file get the header, labels, and data -------------#######
def read_starfile(f):
    inhead = True
    alldata = open(f,'r').readlines()
    labelsdic = {}
    data = []
    header = []
    count = 0
    labcount = 0
    for i in alldata:
        if '_rln' in i and '#' in i:
            labelsdic[i.split('#')[0]] = labcount
            labcount+=1
        if inhead == True:
            header.append(i.strip("\n"))
            if '_rln' in i and '#' in i and  '_rln' not in alldata[count+1] and '#' not in alldata[count+1]:
                inhead = False
        else:
            if len(i.split()) > 0:
	    	data.append(i.split())
        count +=1
    
    return(labelsdic,header,data)
#---------------------------------------------------------------------------------------------#



if len(sys.argv) != 3:
    sys.exit('USAGE: rln-select-micrographs.py <starfile> <list of good files>')

(labels,header,data) = read_starfile(sys.argv[1])
list = open(sys.argv[2],'r').readlines()

output = open('selected_micrographs.star','w')
for i in header:
    output.write('{0}\n'.format(i))
count = 0
found = []
for i in data:
    if '{0}\n'.format(i[labels['_rlnMicrographName ']].split('/')[-1]) in list or i[labels['_rlnMicrographName ']].split('/')[-1] in list:
    	found.append(i[labels['_rlnMicrographName ']].split('/')[-1])
        count+=1
	output.write('{0}\n'.format('    '.join(i)))
print('\n{0} micrographs selected'.format(count))
missed_count = 0
for i in list:
	if i.replace('\n','') not in found:
		missed_count+=1
		print("didn't find {0} in the star file".format(i.replace('\n','')))
print('{0} micrographs missed'.format(missed_count))
