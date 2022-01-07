import _clean
import _deploy
import class_machine


# Déploiement des scripts et fichiers paramètres sur toutes les machines distantes
_deploy.deploy()

# Création des objets machines et séparation du master
login, dict_machines = class_machine.build_machines(ping_before=True)
master_machine = list(dict_machines.values())[0]

# Lancement du master
master_machine.execute(f"ssh {login}@{master_machine.name} python3 /tmp/{login}/python/_master.py", print_out=True,timeout=400)

# Effacement de toutes les données crées sur les machines distantes
_clean.clean()