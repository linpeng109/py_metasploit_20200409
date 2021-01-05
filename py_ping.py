from pymetasploit3.msfrpc import MsfRpcClient
from pymetasploit3.msfconsole import MsfRpcConsole
from threading import Timer, Lock

client = MsfRpcClient(server='127.0.0.1', port=55553, password='msf')
lock = Lock()
sts = 'Not Find And Not Release'
def cb(d):
    print('reading....')
    result = d['data']
    print(result)
    #print(d)
    print('done!\n\n')
    if result.find(sts) != -1:
        lock.release() 

console = MsfRpcConsole(rpc=client, cb=cb)

lock.acquire()
sts = 'Nmap done:'
console.execute('db_nmap -Pn -A 10.10.0.50')
lock.acquire()
sts = 'address'
console.execute('hosts')
exit()
