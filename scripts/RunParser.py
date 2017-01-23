# Michelle Renee Morales
# This is a script to run Google's Parsey McParseface
# Input: 2 arguments [input_file] [output_file]


# command to run Syntaxnet: echo 'sentence' | syntaxnet/demo.sh

import subprocess, re, csv, sys

file = sys.argv[1] #file to parse
outF = sys.argv[2] #file to write trees to
labels_file = sys.argv[3] #labels file
# open text file with all transcripts
with open(file) as f:
    sents = f.readlines()

# open csv with participant ids
IDS = []
labels = {}
with open(labels_file,'rb') as c:
    reader = csv.reader(c)
    for i, row in enumerate(reader):
        ID, ptsd, ptsd_value, depression, depression_value = row
        IDS.append(ID)
        labels[ID] = [ptsd, ptsd_value, depression, depression_value]

# write output to file
newF = open(outF,'w')

for i, s in enumerate(sents):
    s = re.sub('\<.*?\>', '', s.strip())
    s = re.sub('\/.*?\/', '', s.strip())
    ID = IDS[i]
    meta = '<TREE> %s\n'%ID
    s = s.replace("'",'')
    command = "echo '%s' | syntaxnet/demo.sh" %s
    output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
    newF.write(meta)
    newF.write(output)
    newF.write('</TREE>\n')
