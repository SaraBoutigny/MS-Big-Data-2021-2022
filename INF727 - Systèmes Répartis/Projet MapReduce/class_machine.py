import shlex,subprocess
import os
import param

file_machines = param.file_machines
file_login = param.file_login

class machine:
    def __init__(self, name, login):
        self.name = name
        self.login = login
        self.procs = {}

    def execute(self,command,timeout = 5, print_out = False, return_out = True, communicate = True):
        """
        Cette fonction permet d'éxecuter une commande sur la machine concernée

        Inputs :
        command : la commande à exécuter sur la machine
        timeout : temps au-delà duquel on arrête d'attendre une réponse de la machine
        print_out : affiche la sortie de la commande si True
        return_out : renvoie dans des variables la sortie si True
        communicate : attend la fin de l'exécution de la commande sur la machine distante si True
        """

        # Split de la commande unix au format demandé par Popen
        command_split = shlex.split(command)

        proc = None
        try:
            # Création du subprocess
            proc_created = True
            proc = subprocess.Popen(command_split, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)

        except:
            # En cas d'erreur de création du subprocess, cela signifie que la ligne de commande entrée n'est pas
            # reconnue -> l'erreur renvoyée est donc "unknown command"
            out = 'unknown command'
            err = 'unknown command'
            code = 1
            proc_created = False

        # Ajout du process aux subprocess en cours
        self.procs[command] = proc,timeout,print_out,return_out

        if communicate:
            return self.communicate(command)

    def communicate(self,command=""):
        out, err, code = "","",0
        procs_to_communicate = {}

        # Bloc pour savoir si on doit communicate un subprocess en particulier ou tous les subprocess en cours
        if command != "":
            procs_to_communicate[command] = self.procs[command]
        else:
            procs_to_communicate = self.procs.copy()

        # Communicate des subprocess
        for command,item in procs_to_communicate.items():
            proc = item[0]
            timeout = item[1]
            print_out = item[2]
            return_out = item[3]

            # Récupération de la sortie
            if proc != None:
                try:
                    out, err = proc.communicate(timeout=timeout)
                    out = out.decode('utf-8')[:-1]
                    err = err.decode('utf-8')[:-1]
                    code = proc.returncode

                except subprocess.TimeoutExpired:

                    proc.kill()
                    out = 'request timeout'
                    err = 'request timeout'
                    code = 1

                # Retrait du subprocess des subprocess en cours
                self.procs.pop(command)

                if print_out:
                    print('=======================================================================================')
                    print('command : ' + command)
                    print('---------------------------------------------------------------------------------------')
                    print('out : ' + out)
                    print('err : [' + str(code) + '] ' + err)
                    #print('---------------------------------------------------------------------------------------')

                if return_out:
                    return command, out, err, code


    def ping(self,print_out = False, return_out = True,timeout=5):
        command, out, err, code = self.execute("ssh {}@{} hostname".format(self.login,self.name),timeout)
        if print_out:
            if code == 0:
                print(self.name + ' : responded')
            else:
                print(self.name + ' : did not respond (' + err + ')')

        if return_out:
            return code == 0


def multi_parallel_execution(dict_machines,command,timeout = 5, print_out = False, communicate = True):
    """
    Méthode qui permet d'éxécuter plusieurs commandes en parallèle

    :param dict_machines: dictionnaire où les clés sont des noms de machine et les valeurs sont des objets machine
    :return: nothing
    """
    for name, machine in dict_machines.items():
        machine.execute(command,timeout,print_out,return_out=False,communicate=communicate)

    if communicate:
        for name, machine in dict_machines.items():
            machine.communicate()
    pass


def build_machines():
    """
    Fonction qui lit les fichiers paramètres (login et machines sur lesquelles se connecter)
    et qui renvoie le login (string), ainsi que les machines sous forme d'un dictionnaire dont la clé
    est le nom de la machine et la valeur est une instance de la classe machine
    """
    abs_path = os.path.abspath(__file__)
    if '\\' in abs_path:
        file_path = "/".join(abs_path.split('\\')[:-1]) + "/"
    else:
        file_path = "/".join(abs_path.split('/')[:-1]) + "/"

    # Récupération du login
    with open(file_path+file_login, 'r', encoding='utf-8') as f:
        login = f.read()

    # Récupération des machines
    with open(file_path+file_machines, 'r', encoding='utf-8') as f:
        machines = f.read().splitlines()

    dict_machines = {}
    for machine_name in machines:
        dict_machines[machine_name]=machine(machine_name,login)

    return login, dict_machines

