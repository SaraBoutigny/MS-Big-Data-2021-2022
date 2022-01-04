import shlex,subprocess
import sys

login="sboutigny-20"
lst_machines = ["41","42"]

def unix_cmd(command,timer=5, print_out = True):

    command_split = shlex.split(command)
    try:
        proc_created = True
        proc = subprocess.Popen(command_split,stdin=subprocess.PIPE, stdout = subprocess.PIPE,stderr = subprocess.PIPE)

    except:
        out = 'unknown command'
        err = 'unknown command'
        code = 1
        proc_created = False

    if proc_created:
        try:
            out, err = proc.communicate(timeout=timer)
            out = out.decode('utf-8')
            err = err.decode('utf-8')
            code = proc.returncode

        except subprocess.TimeoutExpired:

            proc.kill()
            out = 'request timeout'
            err = 'request timeout'
            code = 1


    if print_out:
        print('=======================================================================================')
        print(command)
        print(out[:-2])
        print('---------------------------------------------------------------------------------------')

    return command, out, err, code

#ssh("mkdir -p /tmp/"+login)
#scp("./main.py", "/tmp/"+login)
#ssh("ls /tmp/"+login)
#unix_cmd("ssh sboutigny-20@tp-4b01-42 ls -al /tmp/",5)