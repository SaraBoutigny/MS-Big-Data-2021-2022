file = "txt_files/forestier_mayotte.txt"

with open(file,'r',encoding='utf-8') as f:
    lines = f.read().splitlines()


words = []
for line in lines:
    lst_temp = line.split(' ')

    for word in lst_temp:
        if word !='':
            words.append(word)


print (words)