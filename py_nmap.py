from pymetasploit3.msfrpc import MsfRpcClient

client = MsfRpcClient(server='192.168.1.119', username='msf', password='msf', port=55552)
cid = client.consoles.console().cid
console = client.consoles.console(cid)
exploit = client.modules.use(mtype='auxiliary', mname='scanner/portscan/tcp')
exploit['RHOSTS'] = '192.168.1.186'
exploit['THREADS'] = 10
exploit['TIMEOUT'] = 5
result = console.run_module_with_output(exploit)
console.destroy()

print(result)
