"""
Usage: pip3 install -r requirements.txt
Usage: python3 lgview.py 198.51.100.0/24 65200 65001
"""
import json
import re
from netmiko import ConnectHandler
import argparse

parser = argparse.ArgumentParser("./lgview")
parser.add_argument("prefixo", help="Prefixo /24 a ser mitigado", type=str)
parser.add_argument("asn_mitigador", help="ASN responsável pela mitigação", type=int)
parser.add_argument("asn_origem", help="ASN detentor do bloco /24", type=int)
args = parser.parse_args()


def grep(texto, dado):
    linhas = texto.split('\n')
    lista = []

    for linha in linhas:
        if re.search(str(dado), linha):
            if "community" not in linha.lower():
                lista.append(linha)

    return lista


def get_data_from_lg(looking_glass_dados):
    try:
        consulta = ConnectHandler(**looking_glass_dados)
    except:
        print("Falha de autenticação no looking glass")
        return
    comando = "set cli screen-length 0" if \
        looking_glass_dados["device_type"] == "juniper_junos" else "terminal length 0"
    consulta.send_command(comando)
    commando = f"show route protocol bgp {args.prefixo}" if \
        looking_glass_dados["device_type"] == "juniper_junos" else f"show ip bgp {args.prefixo}"
    resultado = consulta.send_command(commando)
    busca = grep(resultado, args.asn_origem)
    for elemento in busca:
        if str(args.asn_mitigador) not in elemento:
            print(f"AS-PATH: \033[91m{elemento}\033[0m")
        else:
            print(f"AS-PATH:\033[92m{elemento}\033[0m")


if __name__ == '__main__':
    with open(file="looking_glass_list.json", mode="r") as looking_glass_file:
        looking_glass_json = json.load(looking_glass_file)
        print(f"Verificando Prefixo: {args.prefixo}\n")
        for looking_glass in looking_glass_json:
            print(f"Verificando looking glass: {looking_glass}")
            get_data_from_lg(looking_glass_json[looking_glass])
