import class_machine
import param
import os

print(param.file_wordcount, os.path.getsize(param.file_wordcount) )
time = class_machine.timer();time.start()
file = param.file_wordcount

with open(file, 'r', encoding='utf-8') as f:
    lines = f.read().splitlines()
    
dico = {}

for line in lines:
    words = line.split()
    
    for word in words:
        if word in dico:
            dico[word] += 1
        else:
            dico[word] = 1

with open('classic_wordcount/wordcount.txt', 'w') as f:
    for cle, valeur in dico.items():
        f.write(cle + " " + str(valeur) + "\n")

print("Classic wordcount time :", time.end())
