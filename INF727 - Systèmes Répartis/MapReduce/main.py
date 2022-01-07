import param
import _clean
import _deploy
import _master
import os

"""param.file_machines = "param/machines20.txt"
for file in ['D:/txt_files/CC-MAIN-20170322212949-00140-ip-10-233-31-227.ec2.internal.warc.wet','D:/txt_files/random_generated_1Go.txt','D:/txt_files/random_generated_3Go.txt','D:/txt_files/random_generated_5Go.txt','D:/txt_files/random_generated_6Go.txt']:
    param.file_wordcount = file
    print(param.file_wordcount, os.path.getsize(param.file_wordcount) )
    _deploy.deploy()
    _master.master()
    _clean.clean()"""

param.file_machines = "param/machines10.txt"
for file in ['D:/txt_files/CC-MAIN-20170322212949-00140-ip-10-233-31-227.ec2.internal.warc.wet','D:/txt_files/random_generated_1Go.txt','D:/txt_files/random_generated_3Go.txt','D:/txt_files/random_generated_5Go.txt','D:/txt_files/random_generated_6Go.txt']:
    param.file_wordcount = file
    print(param.file_wordcount, os.path.getsize(param.file_wordcount) )
    _deploy.deploy()
    _master.master()
    _clean.clean()

param.file_machines = "param/machines15.txt"
for file in ['D:/txt_files/CC-MAIN-20170322212949-00140-ip-10-233-31-227.ec2.internal.warc.wet','D:/txt_files/random_generated_1Go.txt','D:/txt_files/random_generated_3Go.txt','D:/txt_files/random_generated_5Go.txt','D:/txt_files/random_generated_6Go.txt']:
    param.file_wordcount = file
    print(param.file_wordcount, os.path.getsize(param.file_wordcount) )
    _deploy.deploy()
    _master.master()
    _clean.clean()

param.file_machines = "param/machines7.txt"
for file in ['D:/txt_files/CC-MAIN-20170322212949-00140-ip-10-233-31-227.ec2.internal.warc.wet','D:/txt_files/random_generated_1Go.txt','D:/txt_files/random_generated_3Go.txt','D:/txt_files/random_generated_5Go.txt','D:/txt_files/random_generated_6Go.txt']:
    param.file_wordcount = file
    print(param.file_wordcount, os.path.getsize(param.file_wordcount) )
    _deploy.deploy()
    _master.master()
    _clean.clean()

param.file_machines = "param/machines4.txt"
for file in ['D:/txt_files/CC-MAIN-20170322212949-00140-ip-10-233-31-227.ec2.internal.warc.wet','D:/txt_files/random_generated_1Go.txt','D:/txt_files/random_generated_3Go.txt','D:/txt_files/random_generated_5Go.txt','D:/txt_files/random_generated_6Go.txt']:
    param.file_wordcount = file
    print(param.file_wordcount, os.path.getsize(param.file_wordcount) )
    _deploy.deploy()
    _master.master()
    _clean.clean()
