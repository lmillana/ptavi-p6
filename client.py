#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import sys
import socket

# Cliente UDP simple.

if len(sys.argv) != 3:
    sys.exit("Usage: python3 client.py method receiver@IP:SIPport")

# Dirección IP del servidor:
try:
    METHOD = sys.argv[1].upper()
    SERVER = sys.argv[2].split('@')[0]
    IP = sys.argv[2].split('@')[1].split(':')[0]
    PORT = int(sys.argv[2].split('@')[1].split(':')[1])
except Exception:
    sys.exit("Usage: python3 client.py method receiver@IP:SIPport")


# Contenido que vamos a enviar:
LINE = METHOD + ' sip:' + SERVER + '@' + IP + ' SIP/2.0\r\n' 

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print("Enviando: " + LINE)
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
try:
    data = my_socket.recv(1024)
except ConnectionRefusedError:
    sys.exit('Connection refuses')

#Metodo de asentimiento:
message = data.decode('utf-8').split('\r\n\r\n')[0:-1]

if message == ['SIP/2.0 100 Trying', 'SIP/2.0 180 Ring', 'SIP/2.0 200 OK']:
    MESS_ACK = 'ACK sip:' + RECEPTOR + '@' + IP + ' SIP/2.0\r\n'
    print("Enviando: " + MESS_ACK)
    my_socket.send(bytes(MESS_ACK, 'utf-8') + b'\r\n')
    try:
        data = my_socket.recv(1024)
    except ConnectionRefusedError:
        sys.exit('Connection refuses')

print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
