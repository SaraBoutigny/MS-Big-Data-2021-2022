import class_machine
import param
import _slave

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
    splits = {}
    number = 0
    last_i = 0
    step = int(len(lines)/nb_splits) + 1 if int(len(lines)/nb_splits) != len(lines)/nb_splits else int(len(lines)/nb_splits)

    for i in range(0,len(lines),step):
        splits["S{}.txt".format(number)]=lines[i:i+step]
        number +=1

    # Machine sur laquelle on va mettre les splits
    lst_machines = list(dict_machines.values())


    # DEPLOIEMENT DES SPLITS -------------------------------------------------------------------------------

    # Création des fichiers sur une machine

    for i,(key,value) in enumerate(splits.items()):
        machine = lst_machines[i]
        # Création du dossier splits
        machine.execute("ssh {}@{} mkdir /tmp/{}/splits".format(machine.login, machine.name, machine.login),print_out=True,return_out = False,communicate=False)

        # Création des splits
        machine.execute("ssh {}@{} touch /tmp/{}/splits/{}".format(machine.login,machine.name,machine.login,key),return_out = False,communicate=False)

        # Remplissage des splits
        machine.execute("ssh {}@{} echo {} > /tmp/{}/splits/{}".format(machine.login, machine.name,' '.join(value), machine.login,key),print_out=True,return_out = False, communicate = False)

    for machine in lst_machines:
        machine.communicate()

    # Execution de la phase de map sur toutes les machines
    _slave.slave()