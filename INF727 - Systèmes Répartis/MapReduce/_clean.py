import class_machine
import os

def clean():
    print ("*** CLEANING...")
    timeout = 10
    login, dict_machines = class_machine.build_machines()
    print_out = False

    # Suppression des splits sur la machine locale
    for file in os.listdir("splits"):
        os.remove("splits/"+file)

    # Suppression des dossiers /tmp/<login> sur les machines distantes
    class_machine.multi_parallel_execution(dict_machines,
                                           command="ssh {1}@{2} rm -R /tmp/{1}",
                                           command_param={"{1}": [machine.login for machine in dict_machines.values()],
                                                          "{2}": [machine.name for machine in dict_machines.values()]},
                                           timeout=20, print_out=print_out, communicate=True)