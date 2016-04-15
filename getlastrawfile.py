import base64
import getpass
import os
import socket
import sys
import traceback
from paramiko.py3compat import input

import paramiko
def getlastrawfile(putlocation,ka2):

    UseGSSAPI = True             # enable GSS-API / SSPI authentication
    DoGSSAPIKeyExchange = True
    port = 22

  


    if ka2:
        hostname = '192.168.0.228'
    else:
        hostname = '192.168.0.208'

    username = 'operator'

    p = 'xxxxxx'

    # now, connect and use paramiko Client to negotiate SSH2 across the connection
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    client.connect(hostname, port, username, p)

    stdin, stdout, stderr = client.exec_command('ls -rt /usr/iris_data/product_raw/')

    lsout = stdout.readlines()

    filetoget = str(lsout[-1].strip('\n'))
    print filetoget

    sftp_client = client.open_sftp()
    sftp_client.get('/usr/iris_data/product_raw/'+filetoget,putlocation+'/'+filetoget)

    sftp_client.close()
    client.close()
    return 0


