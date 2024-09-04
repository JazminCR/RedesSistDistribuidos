#!/usr/bin/env python
# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Revisión 2014 Carlos Bederián
# Revisión 2011 Nicolás Wolovick
# Copyright 2008-2010 Natalia Bidart y Daniel Moisset
# $Id: server.py 656 2013-03-18 23:49:11Z bc $

import connection
import optparse
import socket
import sys
import threading
from constants import *
import os


class Server(object):
    """
    El servidor, que crea y atiende el socket en la dirección y puerto
    especificados donde se reciben nuevas conexiones de clientes.
    """

    def __init__(self, addr=DEFAULT_ADDR, port=DEFAULT_PORT,
                 directory=DEFAULT_DIR):
        """
        Inicializa el servidor.
        Crea un socket de servidor y lo configura.
        """        
        print("Serving %s on %s:%s." % (directory, addr, port))
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print ("Starting up server on %s port %s" % (addr, port)) 
        self.s.bind((addr, port))
        self.s.listen(MAX_THREADS)
        self.directory = directory
        self.threadLimiter = threading.BoundedSemaphore(MAX_THREADS)

    def handle_client(self, client_s):
        """
        Crea una nueva conexión y la atiende.
        """
        self.threadLimiter.acquire()
        try:
            connect = connection.Connection(client_s, self.directory)
            connect.handle()
        finally:
            self.threadLimiter.release()

    def serve(self):
        """
        Loop principal del servidor. Se acepta una conexión a la vez
        y se espera a que concluya antes de seguir.
        """
        while True:
            print ("Waiting to receive message from client")
            client, address = self.s.accept()
            print(f"The connection was established at address {address}")
            new_thread = threading.Thread(target=self.handle_client, args=(client,))
            new_thread.start()
            

def main():
    """Parsea los argumentos y lanza el server"""

    parser = optparse.OptionParser()
    parser.add_option(
        "-p", "--port",
        help="Número de puerto TCP donde escuchar", default=DEFAULT_PORT)
    parser.add_option(
        "-a", "--address",
        help="Dirección donde escuchar", default=DEFAULT_ADDR)
    parser.add_option(
        "-d", "--datadir",
        help="Directorio compartido", default=DEFAULT_DIR)

    options, args = parser.parse_args()
    if len(args) > 0:
        parser.print_help()
        sys.exit(1)
    try:
        port = int(options.port)
    except ValueError:
        sys.stderr.write(
            "Numero de puerto invalido: %s\n" % repr(options.port))
        parser.print_help()
        sys.exit(1)

    if not os.path.exists(options.datadir) :    
        print("El directorio no existe")
        return
    
    server = Server(options.address, port, options.datadir)
    server.serve()


if __name__ == '__main__':
    main()
