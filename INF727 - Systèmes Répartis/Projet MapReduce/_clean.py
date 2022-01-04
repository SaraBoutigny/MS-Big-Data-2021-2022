import class_machine

def clean():
    timeout = 10
    login, dict_machines = class_machine.build_machines()

    for machine in dict_machines.values():
        responded = machine.ping()

        if responded:
            machine.execute("ssh {}@{} rm -R /tmp/{}".format(machine.login,machine.name,machine.login),print_out=True)
