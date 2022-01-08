import class_machine
import os
import sys
import hashlib
import socket
import pandas as pd
import numpy as np

# ==================================================================================================================== #
#                                                INITIALISATION                                                        #
# ==================================================================================================================== #
login, dict_machines = class_machine.build_machines()
master_machine = list(dict_machines.values())[0]
dict_machines.pop(list(dict_machines.keys())[0])
lst_machines_names = list(dict_machines.keys())
host_name = socket.gethostname()
filename = sys.argv[2] if len (sys.argv) > 2 else ""

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
if not os.path.exists('/tmp/{}/partial_wordcount'.format(login)): os.mkdir('/tmp/{}/partial_wordcount'.format(login))

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
    nb_machines_shuffle = len(dict_machines.keys())
    map_file = open(root_path+"/maps/"+filename, 'r', encoding='utf-8')
    shuffle_files = {}
    dict_dataframes = {}

    for line in map_file.readlines():
        word = line.split()[0]
        hash_code = int.from_bytes(hashlib.sha256(word.encode('utf-8')).digest()[:4], 'little')
        receiving_machine = lst_machines_names[hash_code % nb_machines_shuffle]

        if receiving_machine+'_from_'+host_name not in dict_dataframes.keys():
            dict_dataframes[receiving_machine+'_from_'+host_name] = {}
            dict_dataframes[receiving_machine + '_from_' + host_name]["word"] = []

        dict_dataframes[receiving_machine+'_from_'+host_name]["word"] += [word]

    # Conversion en dataframe et sauvegarde au format pickle
    for filename, data in dict_dataframes.items():
        df = pd.DataFrame(data)
        df.to_pickle("/tmp/{}/shuffles/{}.pkl".format(login,filename))

    # Envoi des shuffles aux machines respectives
    for machine in dict_machines.values():
        machine.execute(f"scp /tmp/{login}/shuffles/{machine.name+'_from_'+host_name}.pkl {login}@{machine.name}:/tmp/{login}/shuffles_received/",30,return_out=False,communicate=True)


if sys.argv[1] == '1':

    # création des fichiers shuffle
    shuffle(filename)


# ==================================================================================================================== #
#                                                    REDUCE                                                            #
# ==================================================================================================================== #

def reduce():

    # Ouverture des pickles dans le dossier /tmp/<login>/shuffles_received et concaténation en un unique dataframe
    df_all = pd.DataFrame()

    if len(os.listdir(f"/tmp/{login}/shuffles_received")):
        for filename in os.listdir(f"/tmp/{login}/shuffles_received"):
            df = pd.read_pickle(f"/tmp/{login}/shuffles_received/{filename}")

            df_all = pd.concat([df_all,df])

        # Comptage des mots
        df_all = df_all.groupby(['word']).size()

        # Sauvegarde du fichier au format pickle
        df_all.to_pickle("/tmp/{}/partial_wordcount/{}.pkl".format(login, host_name))

        # Envoi du fichier au master
        dict_machines[host_name].execute(f"scp /tmp/{login}/partial_wordcount/{host_name}.pkl {login}@{master_machine.name}:/tmp/{login}/wordcount/",30, return_out=False, communicate=True)


if sys.argv[1] == '2':

    # création des fichiers reduce
    reduce()


# ==================================================================================================================== #
#                                        WORDCOUNT FINAL (SUR LE MASTER)                                               #
# ==================================================================================================================== #

if sys.argv[1] == '3':

    # Ouverture des pickles dans le dossier /tmp/<login>/wordcount et concaténation en un unique dataframe
    df_all = pd.DataFrame()

    if len(os.listdir(f"/tmp/{login}/wordcount")):
        for filename in os.listdir(f"/tmp/{login}/wordcount"):
            df = pd.read_pickle(f"/tmp/{login}/wordcount/{filename}")
            if df_all.empty:
                df_all = df.copy()
            else:
                df_all = pd.concat([df_all,df])

        # Comptage des mots
        df_all.sort_index(axis=0,inplace=True)
        df_all = df_all.reset_index()
        df_all.columns = ['word','count']
        df_all['count'] = df_all['count'].astype('int64')


        # Sauvegarde du wordcount au format txt
        file = open(f"/tmp/{login}/wordcount/_wordcount.txt", 'w')
        file.write(df_all.to_string())
        file.close()