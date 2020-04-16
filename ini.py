#!/usr/bin/python3
import settings
import socket
import os
import logging

#dados para criacao de log
logging.basicConfig(
  filename= settings.file_logs, level=logging.DEBUG,
  format='%(asctime)s %(levelname)s %(funcName)s => %(message)s'
)
itens = settings.itens
fail_status = settings.fail_status

logging.debug('paramethers: item={}, status={}'.format(' - ', 'init'))

def settings2dict(response, div=':'):
  response = response.strip().split(div)
  for item in itens:
    if item in response:
      for status in fail_status:
        if status in response[1]:
          return {item : status}

def peers2dict(response, div=':'):
  response = response.strip("").split(div)
  for item in itens:
    if item in response:
      for status in fail_status:
        if status in response:
          return {item : status}

def command2manager(command):
  tcp.send (bytes('Action: Command\n','utf-8'))
  tcp.send (bytes('command: '+ command + '\n\n','utf-8'))
  data_recv =  tcp.recv(2048).decode('utf-8')
  while ("END COMMAND" not in data_recv):
    data_recv = data_recv + tcp.recv(2048).decode('utf-8')
  return data_recv

def asterisk_restart(item):
  logging.debug('paramethers: item={}, status={}'.format(item, 'fail'))
  os.system('/etc/init.d/asterisk restart')
  status = os.system('ps aux | grep /usr/bin/asterisk | wc -l')
  if status == '0':
    logging.debug('paramethers: item={}, status={}'.format('restart', status))
  else:
    logging.debug('paramethers: item={}, status={}'.format('restart', status))

#definindo variaveis
HOST = settings.server     # Endereco IP do Servidor
PORT = int(settings.port)            # Porta que o Servidor esta                      

#abre conexao tcp com o servidor Asterisk
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

#Autenticação no manager
tcp.send (bytes('Action: Login\n','utf-8'))
tcp.send (bytes('UserName: ' + settings.user + '\n','utf-8'))
tcp.send (bytes('Secret: ' + settings.secret + '\n\n','utf-8'))

##comandos
settings = command2manager('sip show settings')
peers = command2manager('sip show peers')
iax = command2manager('iax2 show peers')

#tratando convertendo retorno das requisicoes em listas
responses_settings = settings.strip().split("\n")
responses_peers = peers.strip().split("\n")
responses_iax = iax.strip().split("\n")

#quebrando o retorno em listas
settings_list = [settings2dict(response) for response in responses_settings if settings2dict(response) != None]
peers_list = [peers2dict(response,' ') for response in responses_peers if peers2dict(response,' ') != None]
iax_list = [peers2dict(response,' ') for response in responses_iax if peers2dict(response,' ') != None]

#inicio da tratativa dos retornos
if len(settings_list) > 0:
  asterisk_restart('sip settings')
elif len(peers_list) > 0:
  asterisk_restart('sip peers')
elif len(iax_list) > 0:
  asterisk_restart('iax peers')

#encerrando conexao
tcp.send (bytes('Action: Logoff\n','utf-8'))
tcp.close()

