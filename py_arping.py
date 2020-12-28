from pymetasploit3.msfrpc import MsfRpcClient

client = MsfRpcClient(server='192.168.1.164', username='msf', password='msf', port=55552)
exploit = client.modules.use(mtype='auxiliary', mname='scanner/discovery/arp_sweep')
exploit['RHOSTS'] = '192.168.1.100-200'
exploit['THREADS'] = 5
cid = client.consoles.console().cid
console = client.consoles.console(cid)
result = console.run_module_with_output(exploit)
print(result)
console.destroy()