import class_machine
import param
import os

def master():

    # INITIALISATION -------------------------------------------------------------------------------------
    login, dict_machines = class_machine.build_machines()

    # PARAMETRES -----------------------------------------------------------------------------------------
    nb_splits = len(dict_machines.keys())
    file = param.file_wordcount

    # CREATION DES SPLITS ---------------------------------------------------------------------------------------------
    # Lecture du fichier
    with open(file,'r',encoding='utf-8') as f:
        lines = f.read().splitlines()

    # Création des splits
    splits = []
    number = 0
    step = int(len(lines)/nb_splits) + 1 if int(len(lines)/nb_splits) != len(lines)/nb_splits else int(len(lines)/nb_splits)

    for i in range(0,len(lines),step):
        filename = "S{}.txt".format(int(i/step))

        file = open('splits/'+filename,'w',encoding='utf-8')
        for line in lines[i:i+step]:
            file.write(line + "\n")
        file.close()

        splits.append(filename)
        number +=1


    # DEPLOIEMENT DES SPLITS -------------------------------------------------------------------------------

    # Machines sur lesquelles on va mettre les splits
    lst_machines = list(dict_machines.values())

    # Création des dossiers (parallélisé)
    for i,machine in enumerate(lst_machines):
        machine.execute("ssh {}@{} mkdir /tmp/{}/splits".format(machine.login, machine.name, machine.login),print_out=True,return_out = False,communicate=False,timeout=30)

    # Attente que les dossiers soient bien créés
    for machine in lst_machines:
        machine.communicate()

    # Envoi des splits sur les machines (parallélisé)
    for i,machine in enumerate(lst_machines):
        machine.execute(r"scp splits/{} {}@{}:/tmp/{}/splits/".format(splits[i], machine.login, machine.name,machine.login), print_out=True,communicate=False, timeout=100)

    # Attente que les envois soient terminés
    for machine in lst_machines:
        machine.communicate()
