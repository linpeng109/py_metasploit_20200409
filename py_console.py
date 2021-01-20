from threading import Lock

from pymetasploit3.msfrpc import MsfRpcClient
from pymetasploit3.msfconsole import MsfRpcConsole

rpc = MsfRpcClient(server='192.168.124.10', port=55552, username='msf', password='msf')

lock = Lock()


def callback(result):
    print(result)


console = MsfRpcConsole(rpc=rpc, cb=callback)

console.lock.acquire()
console.execute('ls -l\r')
console.lock.release()

console.destroy()
