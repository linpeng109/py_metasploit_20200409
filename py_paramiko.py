import paramiko


def ssh2(ip, username, password, cmd):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(ip, 22, username=username, password=password, timeout=5)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read())
        print('%s OK\n' % (ip))
        ssh.close()
    except:
        print('%s Error\n' % (ip))

if __name__ == '__main__':
    # ssh2('192.168.1.164', 'linpeng109', 'stars2020', 'ls -l')
    ssh2('192.168.1.164', 'linpeng109', 'stars2020', 'nmap -sV 192.168.1.115')
