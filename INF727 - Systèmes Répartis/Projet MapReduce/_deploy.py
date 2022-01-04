import class_machine
import param

def deploy():
    timeout = 10
    login, dict_machines = class_machine.build_machines()


    for machine in dict_machines.values():
        responded = machine.ping()

        if responded:
            # Création d'un dossier portant le nom de l'utilisateur sur les machines
            machine.execute("ssh {}@{} mkdir /tmp/{}".format(machine.login,machine.name,machine.login),print_out=True)

            # Copie des scripts sur les machines (création d'un dossier python + copie des scripts)
            machine.execute("ssh {}@{} mkdir /tmp/{}/python".format(machine.login, machine.name, machine.login),print_out=True)
            machine.execute(r"scp {}/*.py {}@{}:/tmp/{}/python/".format(param.scripts_path,machine.login, machine.name, machine.login), print_out=True,timeout=100)
            machine.execute(r"scp {}/*.py {}@{}:/tmp/{}/python/".format(param.scripts_path, machine.login, machine.name,machine.login), print_out=True, timeout=100)
            machine.execute(r"scp -r {}/param {}@{}:/tmp/{}/python/".format(param.scripts_path, machine.login, machine.name,machine.login), print_out=True, timeout=100)
            machine.execute(r"scp -r {}/txt_files {}@{}:/tmp/{}/python/".format(param.scripts_path, machine.login, machine.name,machine.login), print_out=True, timeout=100)

    pass




