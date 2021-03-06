import class_machine
import param


def deploy():
    print("*** DEPLOYING...")
    time = class_machine.timer();time.start()

    login, dict_machines = class_machine.build_machines(ping_before=True)
    master_machine = list(dict_machines.values())[0]
    print_out=False


    # Création du dossier <login> dans chaque machine en mode parallélisé
    class_machine.multi_parallel_execution(dict_machines,
                                           command="ssh {1}@{2} mkdir /tmp/{1}",
                                           command_param={"{1}":[machine.login for machine in dict_machines.values()],
                                                          "{2}":[machine.name for machine in dict_machines.values()]},
                                           timeout=20,print_out=print_out,communicate=True)

    # Création du dossier /tmp/<login>/python sur chaque machine en mode parallélisé
    class_machine.multi_parallel_execution(dict_machines,
                                           command="ssh {1}@{2} mkdir /tmp/{1}/python",
                                           command_param={"{1}": [machine.login for machine in dict_machines.values()],
                                                          "{2}": [machine.name for machine in dict_machines.values()]},
                                           timeout=20, print_out=print_out, communicate=True)

    # Transfert des scripts pythons nécessaires au fonctionnement du slave dans le dossier /tmp/<login>/python/ de chaque machine
    for file in ["_slave.py","param.py","class_machine.py"]:
        class_machine.multi_parallel_execution(dict_machines,
                                               command="scp {1}/{4} {2}@{3}:/tmp/{2}/python/",
                                               command_param={"{1}": [param.scripts_path]*len(dict_machines.values()),
                                                              "{2}": [machine.login for machine in dict_machines.values()],
                                                              "{3}": [machine.name for machine in dict_machines.values()],
                                                              "{4}": [file]*len(dict_machines.values())},
                                               timeout=20, print_out=print_out, communicate=True)

    # Transfert du dossier param dans /tmp/<login>/python
    class_machine.multi_parallel_execution(dict_machines,
                                           command=r"scp -r {1}/param {2}@{3}:/tmp/{2}/python/",
                                           command_param={
                                               "{1}": [param.scripts_path]*len(dict_machines.values()),
                                               "{2}": [machine.login for machine in dict_machines.values()],
                                               "{3}": [machine.name for machine in dict_machines.values()]},
                                           timeout=20, print_out=print_out, communicate=True)

    print("Deploy :", str(time.end()) + ")")

    # Envoi du master et du fichier texte sur la première machine
    master_machine.execute(f"ssh {login}@{master_machine.name} mkdir /tmp/{login}/python/txt_files/",timeout=20,print_out=print_out,return_out=False,communicate=True)
    master_machine.execute(f"scp {param.file_wordcount} {login}@{master_machine.name}:/tmp/{login}/python/txt_files/",timeout=20,print_out=print_out,return_out=False,communicate=True)
    master_machine.execute(f"scp {param.scripts_path}/_master.py {login}@{master_machine.name}:/tmp/{login}/python/",timeout=20,print_out=print_out,return_out=False,communicate=True)


    pass




