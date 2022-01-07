import class_machine
import param
import os
import sys

# ============================================================================================================ #
#                                             INITIALISATION                                                   #
# ============================================================================================================ #
print_out = False
login, dict_machines = class_machine.build_machines()
master_machine = list(dict_machines.values())[0]
dict_machines.pop(list(dict_machines.keys())[0])

# Paramètres
nb_splits = len(dict_machines.keys())
file = f"/tmp/{login}/python/txt_files/" + param.file_wordcount.split('/')[-1]

# Création du dossier wordcount sur la machine master (on y trouvera les résultats)
if not os.path.exists(f"/tmp/{login}/wordcount"):os.mkdir(f"/tmp/{login}/wordcount")
if not os.path.exists(f"/tmp/{login}/splits_to_send"):os.mkdir(f"/tmp/{login}/splits_to_send")

# ============================================================================================================ #
#                                                  SPLITS                                                      #
# ============================================================================================================ #


# Lecture du fichier texte (input du wordcount)
with open(file,'r',encoding='utf-8') as f:
    lines = f.read().splitlines()

# Création des splits
splits = []
step = int(len(lines)/nb_splits)

for i in range(0,len(lines),step):
    filename = "S{}.txt".format(int(i/step))

    file = open(f'/tmp/{login}/splits_to_send/'+filename,'w',encoding='utf-8')

    if (i+step)/step==len(dict_machines.values()):
        for line in lines[i:]:
            file.write(line + "\n")
        splits.append(filename)
        break
    else:
        for line in lines[i:i+step]:
            file.write(line + "\n")
    file.close()

    splits.append(filename)


time = class_machine.timer();time.start()

# Création des dossiers splits (parallélisé)
class_machine.multi_parallel_execution(dict_machines,
                                       command="ssh {1}@{2} mkdir /tmp/{1}/splits",
                                       command_param={"{1}": [machine.login for machine in dict_machines.values()],
                                                      "{2}": [machine.name for machine in dict_machines.values()]},
                                       timeout=20, print_out=print_out, communicate=True)

# Déploiement des splits (parallélisé)
class_machine.multi_parallel_execution(dict_machines,
                                       command="scp /tmp/{2}/splits_to_send/{1} {2}@{3}:/tmp/{2}/splits/",
                                       command_param={"{1}": splits,
                                                      "{2}": [machine.login for machine in dict_machines.values()],
                                                      "{3}": [machine.name for machine in dict_machines.values()]},
                                       timeout=20, print_out=print_out, communicate=True)

sys.stdout.write(f"Split time : {time.end()}\n")

# ============================================================================================================ #
#                                             LANCEMENT DU MAP                                                 #
# ============================================================================================================ #
time = class_machine.timer(); time.start()

# Exécution du slave pour convertir les splits en map
class_machine.multi_parallel_execution(dict_machines,
                                       command="ssh {1}@{2} python3 /tmp/{1}/python/_slave.py 0 S{3}.txt",
                                       command_param={"{1}": [machine.login for machine in dict_machines.values()],
                                                      "{2}": [machine.name for machine in dict_machines.values()],
                                                      "{3}": list(range(0,len(dict_machines.values())))},
                                       timeout=20, print_out=print_out, communicate=True)
sys.stdout.write (f"Mapping time : {time.end()}\n")

# ============================================================================================================ #
#                                             LANCEMENT DU SHUFFLE                                             #
# ============================================================================================================ #
time = class_machine.timer(); time.start()

# Exécution du slave pour convertir les map en shuffle
class_machine.multi_parallel_execution(dict_machines,
                                       command="ssh {1}@{2} python3 /tmp/{1}/python/_slave.py 1 UM{3}.txt",
                                       command_param={"{1}": [machine.login for machine in dict_machines.values()],
                                                      "{2}": [machine.name for machine in dict_machines.values()],
                                                      "{3}": list(range(0, len(dict_machines.values())))},
                                       timeout=20, print_out=print_out, communicate=True)
sys.stdout.write(f"Shuffle time : {time.end()}\n")

# ============================================================================================================ #
#                                             LANCEMENT DU REDUCE                                              #
# ============================================================================================================ #
time = class_machine.timer();time.start()

# Exécution du slave pour convertir les splits en map
class_machine.multi_parallel_execution(dict_machines,
                                       command="ssh {1}@{2} python3 /tmp/{1}/python/_slave.py 2",
                                       command_param={"{1}": [machine.login for machine in dict_machines.values()],
                                                      "{2}": [machine.name for machine in dict_machines.values()]},
                                       timeout=20, print_out=print_out, communicate=True)
sys.stdout.write(f"Reduce time : {time.end()}\n")

# ============================================================================================================ #
#                                               FINAL WORDCOUNT                                                #
# ============================================================================================================ #
time = class_machine.timer();time.start()

master_machine.execute(f"ssh {login}@{master_machine.name} python3 /tmp/{login}/python/_slave.py 3",timeout=30,print_out=print_out)

sys.stdout.write(f"Wordcount final time : {time.end()}\n")

# Affichage des résultats
master_machine.execute(f"ssh {login}@{master_machine.name} ls -al /tmp/{login}/wordcount", timeout=500,print_out=True)

