import class_machine


# INITIALISATION -----------------------------------------------------------------------------------------
login, dict_machines = class_machine.build_machines()

def mapping(string):
    return r" 1, ".join(string.split(' ')) + ' 1'


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


# ==================================================================================================== #
#                                                MAP                                                   #
# ==================================================================================================== #



