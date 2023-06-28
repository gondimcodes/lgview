#!/usr/bin/env python3
'''
lgview is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
#
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
#
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

Precisa do pacote: python3-netmiko
'''
import os
import sys
import re
from netmiko import ConnectHandler

__author__ = 'Marcelo Gondim'
__version__= 1.0
__datebegin__= "25/06/2023"
#########################################################################
routeviews = {
    "device_type": "cisco_xe",
    "host": "route-views.routeviews.org",
    "username": "rviews",
    "password": ""
}

ix_sp = {
    "device_type": "cisco_ios_telnet",
    "host": "lg.sp.ptt.br",
}

ix_rj = {
    "device_type": "cisco_ios_telnet",
    "host": "lg.rj.ix.br",
}

ix_ce = {
    "device_type": "cisco_ios_telnet",
    "host": "lg.ce.ix.br",
}

at_t = {
    "device_type": "cisco_ios_telnet",
    "host": "route-server.ip.att.net",
    "username": "rviews",
    "password": "rviews"
}

internexa = {
    "device_type": "juniper_junos",
    "host": "177.84.161.226",
    "username": "bgp_view",
    "password": "bgp_view"
}

algar = {
    "device_type": "juniper_junos",
    "host": "201.48.0.2",
    "username": "rviews",
    "password": "rviews"
}

#########################################################################

try:
   prefixo = sys.argv[1]
   asn_mitigacao = sys.argv[2]
   asn_prefixo = sys.argv[3]
except:
   print("Parametros faltando! Precisa passar o prefixo IPv4 /24 mitigado, o ASN mitigador e o ASN do prefixo mitigado.")
   print("Ex.: ./lgview.py 192.168.0.0/24 65000 65001")
   exit(0)


def grep(texto, dado):
    linhas = texto.split('\n')
    lista = []

    for linha in linhas:
        if re.search(dado, linha):
           if "community" not in linha.lower():
              lista.append(linha)

    return lista

os.system('cls' if os.name == 'nt' else 'clear')
titulo = "LGVIEW - Lista prefixos nos Looking Glass para troubleshooting de Mitigacao DDoS - %s - v%s - %s" % (__author__, __version__,__datebegin__)
print("#"*126)
print("    %s" %(titulo))
print("#"*126)
print("Verificando Prefixo: " + prefixo + "\n")
#########################################################################

print("Checando LG: route-views.routeviews.org")
consulta = ConnectHandler(**routeviews)
consulta.send_command('terminal length 0')
resultado = consulta.send_command('show ip bgp ' + prefixo)

busca = grep(resultado, asn_prefixo)

for elemento in busca:
   if asn_mitigacao not in elemento:
      print('AS-PATH: ' + '\033[91m' + elemento + '\033[0m')
   else:
      print('AS-PATH: ' + '\033[92m' + elemento + '\033[0m')


#########################################################################

print("Checando LG: IX-SP")
consulta = ConnectHandler(**ix_sp)
consulta.send_command('terminal length 0')
resultado = consulta.send_command('show ip bgp ' + prefixo)

busca = grep(resultado, asn_prefixo)

for elemento in busca:
   if asn_mitigacao not in elemento:
      print('AS-PATH: ' + '\033[91m' + elemento + '\033[0m')
   else:
      print('AS-PATH: ' + '\033[92m' + elemento + '\033[0m')

#########################################################################

print("Checando LG: IX-RJ")
consulta = ConnectHandler(**ix_rj)
consulta.send_command('terminal length 0')
resultado = consulta.send_command('show ip bgp ' + prefixo)

busca = grep(resultado, asn_prefixo)

for elemento in busca:
   if asn_mitigacao not in elemento:
      print('AS-PATH: ' + '\033[91m' + elemento + '\033[0m')
   else:
      print('AS-PATH: ' + '\033[92m' + elemento + '\033[0m')

#########################################################################

print("Checando LG: IX-CE")
consulta = ConnectHandler(**ix_ce)
consulta.send_command('terminal length 0')
resultado = consulta.send_command('show ip bgp ' + prefixo)

busca = grep(resultado, asn_prefixo)

for elemento in busca:
   if asn_mitigacao not in elemento:
      print('AS-PATH: ' + '\033[91m' + elemento + '\033[0m')
   else:
      print('AS-PATH: ' + '\033[92m' + elemento + '\033[0m')

#########################################################################

print("Checando LG: AT&T")
consulta = ConnectHandler(**at_t)
consulta.send_command('set cli screen-length 0')
resultado = consulta.send_command('show route protocol bgp ' + prefixo)

busca = grep(resultado, asn_prefixo)

for elemento in busca:
   if asn_mitigacao not in elemento:
      print('AS-PATH: ' + '\033[91m' + elemento + '\033[0m')
   else:
      print('AS-PATH: ' + '\033[92m' + elemento + '\033[0m')

#########################################################################

print("Checando LG: Internexa")
consulta = ConnectHandler(**internexa)
consulta.send_command('set cli screen-length 0')
resultado = consulta.send_command('show route protocol bgp ' + prefixo)

busca = grep(resultado, asn_prefixo)

for elemento in busca:
   if asn_mitigacao not in elemento:
      print('AS-PATH: ' + '\033[91m' + elemento + '\033[0m')
   else:
      print('AS-PATH: ' + '\033[92m' + elemento + '\033[0m')

#########################################################################

print("Checando LG: Algar")
consulta = ConnectHandler(**algar)
consulta.send_command('set cli screen-length 0')
resultado = consulta.send_command('show route protocol bgp ' + prefixo)

busca = grep(resultado, asn_prefixo)

for elemento in busca:
   if asn_mitigacao not in elemento:
      print('AS-PATH: ' + '\033[91m' + elemento + '\033[0m')
   else:
      print('AS-PATH: ' + '\033[92m' + elemento + '\033[0m')

#########################################################################
