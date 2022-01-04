import class_machine

# INITIALISATION -----------------------------------------------------------------------------------------
login, dict_machines = class_machine.build_machines()
maps = {}
def mapping(string):
    return ' 1\n'.join(string.split(' ')) + ' 1'


# Calcul d'un Map à partir d'un Split

# Récupération des splits
for machine in dict_machines.values():
    _, out, _, _ = machine.execute("ssh {}@{} cat /tmp/{}/splits/*.txt".format(machine.login,machine.name,machine.login),return_out=True,print_out=True)

    print(mapping(out))

# MAP à partir du out

