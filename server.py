#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple.
"""
import sys
import socketserver
import os

if len(sys.argv) != 4:
    sys.exit("Usage: python3 server.py IP port audio_file")

try:
    IP = sys.argv[1]
    PORT = int(sys.argv[2])
    FICH = sys.argv[3]

    if not os.path.exists(FICH):
        sys.exit("Usage: python server.py IP port audio_file")

except Exception:
    sys.exit("Usage: python3 server.py IP  port audio_file")


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class.
    """
    METHODS = ['INVITE', 'ACK', 'BYE']

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            text = self.rfile.read()
            line = self.rfile.read()

            method = text.decode('utf-8').split(' ')[0]
            print("Hemos recibido tu peticion:", method, '\r\n\r\n')

            if not method in self.METHODS:
                self.wfile.write(b'SIP/2.0 405 Method Not Allowed\r\n\r\n')

            elif method == 'INVITE':
                to_send = b"SIP/2.0 100 Trying\r\n\r\n"
                to_send += b"SIP/2.0 180 Ring\r\n\r\n"
                to_send += b"SIP/2.0 200 OK\r\n\r\n"
                self.wfile.write(to_send)

            elif method == 'ACK':
            # aEjecutar es un string con lo que se ha de ejecutar en la shell
                aEjecutar = ('./mp32rtp -i 127.0.0.1 -p 23032 < ' + FICH)
                print ("Vamos a ejecutar", aEjecutar)
                os.system(aEjecutar)

            elif method == 'BYE':
                self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')

            else:
                self.wfile.write(b'SIP/2.0 400 Bad Request\r\n\r\n')

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((IP, PORT), EchoHandler)
    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
