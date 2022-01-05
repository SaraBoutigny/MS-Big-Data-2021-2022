import class_machine
import param
import datetime as dt

def deploy():
    start_time = dt.datetime.now()
    login, dict_machines = class_machine.build_machines()
    available_machines = []

    #class_machine.multi_parallel_execution(dict_machines)
    # Vérification que toutes les machines répondent
    for machine in dict_machines.values():
        if machine.ping(): available_machines.append(machine)

    # Création du dossier [login] (parallélisé)
    for machine in available_machines:
        machine.execute("ssh {}@{} mkdir /tmp/{}".format(machine.login, machine.name, machine.login), print_out=True,
                        communicate=False)

    # Attente de la fin des subprocess
    for machine in available_machines:
        machine.communicate()

    # Création du dossier "python" (parallélisé)
    for machine in available_machines:
        machine.execute("ssh {}@{} mkdir /tmp/{}/python".format(machine.login, machine.name, machine.login),
                        print_out=True, communicate=False)

    # Attente de la fin des subprocess
    for machine in available_machines:
        machine.communicate()

    # Envoi de fichiers (parallélisé)
    for machine in available_machines:
        machine.execute(r"scp {}/_slave.py {}@{}:/tmp/{}/python/".format(param.scripts_path, machine.login, machine.name,machine.login), print_out=True, timeout=100,communicate=True)
        machine.execute(r"scp {}/param.py {}@{}:/tmp/{}/python/".format(param.scripts_path, machine.login, machine.name,machine.login), print_out=True, timeout=100,communicate=True)
        machine.execute(r"scp {}/class_machine.py {}@{}:/tmp/{}/python/".format(param.scripts_path, machine.login, machine.name,machine.login), print_out=True, timeout=100,communicate=True)
        machine.execute(r"scp -r {}/param {}@{}:/tmp/{}/python".format(param.scripts_path, machine.login, machine.name, machine.login),print_out=True, timeout=100, communicate=True)

    print("Deploy time :", (dt.datetime.now() - start_time))
    pass




