# APT Serviços monitora apt do servidor.

Este script feito em Python monitora o apt da maquina e informar qtos pacotes precisam ser atualizados e ser requer reboot para aplicar atualização.

## Clonando esse repositorio e configure o serviço.


- Execute o clone.

```
git clone git@github.com:mleinfelder/apt_exporter.git

```

- acesse a pasta do projeto.
```
cd apt_exporter 

```
Agora movimente os arquivos para locais necessarios


```
mv apt_exporter.py /usr/local/bin/apt_exporter.py
```

## Instruções de Uso

Siga estas instruções para construir e executar o contêiner:

1. Certifique-se de ter os pacotes instalados:  python3, pip, debian-goodies e pip flask na sua máquina.

2. Clone este repositório para obter os arquivos necessários.

3. Navegue até o diretório do projeto.


```
 sudo  apt-get install -y python3 && 
 sudo  apt-get install -y debian-goodies &&
 sudo apt-get install -y pip && 
 sudo pip install flask

```

5. Após a instalação dos requisitos acima mencionados, movimente os arquivos para locais determinados:

```
mv apt_exporter.py /usr/local/bin/apt_exporter.py
mv apt_exporter.service /etc/systemd/system/apt_exporter.service

systemctl daemon-reload
systemctl start apt_exporter.service 
systemctl enable apt_exporter.service

```

## Validação do serviços

Acesse o serviço no browser e informar nome da maquina ou endereço IPv4 ou Ipv6

http://localhost:3999/metrics

# HELP update_available Number of available updates 
# TYPE update_available gauge update_available 0 
# HELP needs_reboot Indicates whether a system reboot is needed 
# TYPE needs_reboot gauge needs_reboot 1
## 

By Márcio Felder.
