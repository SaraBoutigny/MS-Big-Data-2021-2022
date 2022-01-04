import class_machine


machine = class_machine.machine("tp-4b01-38","sboutigny-20")

machine.execute("ssh {}@{} cat /tmp/sboutigny-20/Slave.py".format(machine.login,machine.name),20,print_out=True,return_out=False)




#print (dict_machines.values())