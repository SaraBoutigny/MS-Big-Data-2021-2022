import class_machine
import os
import sys
import hashlib
import socket
import glob

# ==================================================================================================================== #
#                                                INITIALISATION                                                        #
# ==================================================================================================================== #
login, dict_machines = class_machine.build_machines()
lst_machines_names = list(dict_machines.keys())
host_name = socket.gethostname()
filename = sys.argv[2]

# Chemin du script
abs_path = os.path.abspath(__file__)
if '\\' in abs_path:
    file_path = "/".join(abs_path.split('\\')[:-1]) + "/"
else:
    file_path = "/".join(abs_path.split('/')[:-1]) + "/"

root_path = '/'.join(file_path.split('/')[:-2])

# Création des différents dossiers (on le fait en amont pour éviter des décalages de création qui causeraient des erreurs
# quand on enverra les shuffles)
if not os.path.exists('/tmp/{}/maps'.format(login)): os.mkdir('/tmp/{}/maps'.format(login))
if not os.path.exists('/tmp/{}/shuffles'.format(login)): os.mkdir('/tmp/{}/shuffles'.format(login))
if not os.path.exists('/tmp/{}/shuffles_received'.format(login)): os.mkdir('/tmp/{}/shuffles_received'.format(login))


# FONCTIONS ===========================================================================================================

def slave():
    # Récupération des splits
    for machine in dict_machines.values():

        # Récupération du nom du fichier txt dans le dossier splits
        _, split_name, _, _ =  machine.execute("ssh {}@{} ls /tmp/{}/splits/".format(machine.login,machine.name,machine.login),print_out=True)

        # Récupération du contenu du fichier split Sx.txt
        _, out, _, _ = machine.execute("ssh {}@{} cat /tmp/{}/splits/{}".format(machine.login,machine.name,machine.login,split_name),return_out=True,print_out=True)

        # Création du dossier maps
        machine.execute("ssh {}@{} mkdir /tmp/{}/maps".format(machine.login, machine.name, machine.login),print_out=True)

        # Création de l'unsorted map UMx.txt
        machine.execute("ssh {}@{} touch /tmp/{}/maps/{}".format(machine.login, machine.name, machine.login, split_name.replace("S","UM")),print_out=True)

        # Remplissage de l'unsorted map UMx.txt
        machine.execute('ssh {}@{} echo {} > /tmp/{}/maps/{}'.format(machine.login, machine.name, mapping(out), machine.login, split_name.replace("S","UM")),print_out=True)

        machine.execute("ssh {}@{} cat /tmp/{}/maps/{}".format(machine.login, machine.name, machine.login, split_name.replace("S","UM")),print_out=True)


# ==================================================================================================================== #
#                                                      MAP                                                             #
# ==================================================================================================================== #
def map(filename):
    map_filename = filename.split('/')[-1].replace("S","UM")

    # Création du fichier de map
    map_file = open("/tmp/{}/maps/{}".format(login,map_filename),'w')

    # Lecture du fichier split
    split_file = open(root_path+"/splits/"+filename,'r',encoding="utf-8")
    lines = split_file.read().splitlines()

    # Ecriture dans le fichier map
    for line in lines:
        words = line.split()

        for word in words:
            map_file.write(word+ " 1\n")

    map_file.close()
    split_file.close()
    pass

if sys.argv[1] == '0':

    # création du fichier map
    map(filename)

# ==================================================================================================================== #
#                                                    SHUFFLE                                                           #
# ==================================================================================================================== #

def shuffle(filename):
    map_file = open(root_path+"/maps/"+filename, 'r', encoding='utf-8')
    shuffle_files = {}

    # Création des fichiers suffle dont le nom est un nom de machine correspondant à la machine qui doit recevoir les clés
    for machine in dict_machines.values():
        file = open(root_path+"/shuffles/"+machine.name+'_from_'+host_name+".txt","w")
        shuffle_files[machine.name+'_from_'+host_name]=file

    # Hachage des clés et écriture dans le fichier shuffle de la machine à qui on devra envoyer le fichier
    for line in map_file.readline():
        hash_code = str(int.from_bytes(hashlib.sha256(line.encode('utf-8')).digest()[:8], 'little'))
        receiving_machine = lst_machines_names[int(hash_code) % len(lst_machines_names)]
        shuffle_files[receiving_machine+'_from_'+host_name].write(hash_code + "\n")

    for file in shuffle_files.values():
        file.close()

    # Envoi des shuffles aux machines respectives
    for machine in dict_machines.values():
        machine.execute("scp /tmp/{}/shuffles/{}.txt {}@{}/tmp/{}/shuffles_received/".format(login,machine.name+'_from_'+host_name,login,machine.name,login))

    pass

if sys.argv[1] == '1':

    # création des fichiers shuffle
    shuffle(filename)


# ==================================================================================================================== #
#                                                    REDUCE                                                            #
# ==================================================================================================================== #

def reduce(filename):

    pass


if sys.argv[1] == '2':

    # création des fichiers reduce
    shuffle(filename)