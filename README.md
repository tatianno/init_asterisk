# init_asterisk
Script para validar status de alguns itens no asterisk

## Configurações necessárias 

### Inserir o script ini.py no crontab e setar o intervalo de verificação

`*/3 * * * *root /< diretorio >/servicos/ini.py`

### Configurar os parametros que deseja monitorar e dados de conexão no settings.py

- Itens que serao monitorados

`
itens = ['Externaddr']
`

- Status considerados como erro

`
fail_status = ['UNKNOWN','UNREACHABLE','(null)']
`

- Dados de conexao com o manager do Asterisk

`server = '127.0.0.1'`

`port = '5038'`

`user = < usuario configurado no manager.conf >`

`secret = < senha configurada no manager.conf >`
`

- Arquivo para registro de logs

`
file_logs = '/< diretorio >/ini_asterisk.log'
`
