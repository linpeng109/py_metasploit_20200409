from pymetasploit3.msfrpc import MsfRpcClient, MsfConsole
import time

client = MsfRpcClient(server='192.168.1.164', port=55552, username='msf', password='msf')
cid = client.consoles.console().cid

console = client.consoles.console(cid)

console.read()
console.write(command='ls -l ')

result = ''

while result == '' or console.is_busy():
    time.sleep(1)
    result = result + console.read()['data']
print(result)
# result = console.read()

console.destroy()
