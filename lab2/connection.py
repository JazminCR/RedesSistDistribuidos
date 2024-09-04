# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

import os
import socket
from constants import *
from base64 import b64encode


class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """

    def __init__(self, socket, directory):
        """
        Inicializa los atributos de Connection
        """
        self.s = socket
        self.directory = directory
        self.connected = True
        self.status = CODE_OK

    def build_send_header(self, status):
        self.status = status
        header = f'{self.status}' + ' ' + error_messages[self.status]
        self.send(header)

    def build_send_response(self, status, message):
        self.status = status
        response = f'{self.status}' + ' ' + error_messages[self.status] + EOL + f'{message}'
        self.send(response)

    def get_file_listing(self) :
        file_list = os.listdir(self.directory)
        respuesta = ""
        for file in file_list:
            respuesta += file + EOL
        self.build_send_response(CODE_OK, respuesta)
             
    def get_metadata(self, file_name) :
        filename = f'{self.directory}/{file_name}'
        try:
            length = os.path.getsize(filename)
            self.build_send_response(CODE_OK, length)
        except FileNotFoundError:
            self.build_send_header(FILE_NOT_FOUND)
  
    def get_slice(self, file_name, offset, size) :
        try:
            filename = (f'{self.directory}/{file_name}')
            try:
                start = int(offset)
                length = int(size)
            except ValueError:
                self.build_send_header(INVALID_ARGUMENTS)
                return
            length_file = os.path.getsize(filename)

            if start < 0 or length <= 0 or start > length_file or start + length > length_file:
                self.build_send_header(BAD_OFFSET)
                return 

            file = open(filename, 'rb')
            file.seek(start)
            content = file.read(length)
            encoded_content = b64encode(content)
            decoded_content = encoded_content.decode("ascii")
            self.build_send_response(CODE_OK, decoded_content)
            file.close()

        except FileNotFoundError:
            self.build_send_header(FILE_NOT_FOUND)
    
    def close(self):
        try:
            if self.connected==True:
                print("Cerrando la conexión...")
                self.s.close()
                self.connected = False
        except socket.error as e:
            print(f"error: {e}")

    def quit(self):
        self.build_send_header(CODE_OK)
        self.close()  
        
    def send(self, message):
        """
        Envía el mensaje 'message' al cliente, seguido por el terminador de
        línea del protocolo.
        """
        message += EOL
        while message:
            bytes_sent = self.s.send(message.encode('ascii'))
            assert bytes_sent > 0
            message = message[bytes_sent:]
    
    def execute(self,command) :
        if command[0] == "get_file_listing" :
            self.get_file_listing()
        elif command[0] == "quit" :
            self.quit()
        elif command[0] == "get_metadata" :
            self.get_metadata(command[1])
        elif command[0] == "get_slice" :
            self.get_slice(command[1], command[2], command[3])
    
    def read_socket(self, buffer) :
        while not EOL in buffer:
            try:
                buffer += self.s.recv(4096).decode('ascii')
            except ConnectionError:
                self.build_send_header(INTERNAL_ERROR)
                self.close()
                return []
            except socket.error:
                self.build_send_header(INTERNAL_ERROR)
                self.close()
                return []
            except UnicodeError:
                self.build_send_header(INTERNAL_ERROR)
                self.close()
                return []

            if buffer=='':
                print("Hubo un cierre inesperado de la conexión")
                self.close()
                return []
        
        res = buffer.split(EOL)
        res = [empty_char for empty_char in res if empty_char != '']
        return res  

    def request_error(self, command):
        if len(command) > 2:
            list_file = os.listdir(self.directory)
            filenames = command[1:]
            filename = ' '.join(filenames)

            if filename in list_file:
                self.build_send_header(BAD_REQUEST)
                self.close()
                return 4

        return 0
    
    def args_error_handler(self, command):
        if (command[0] == 'get_file_listing' or command[0] == 'quit') and len(command) > 1:
            self.build_send_header(INVALID_ARGUMENTS)
            return 1
        elif command[0] == 'get_metadata' and len(command) != 2:
            request_error = self.request_error(command)

            if request_error == 0:
                self.build_send_header(INVALID_ARGUMENTS)
                return 2
            else:
                return request_error

        elif command[0] == 'get_slice':
            request_error = self.request_error(command)

            if request_error == 0 and len(command) != 4:
                self.build_send_header(INVALID_ARGUMENTS)
                return 3
            else:
                return request_error

        return 0

    def handle(self) :
        while self.connected :
            buffer = ""
            data = self.read_socket(buffer)

            if len(data) != 0:
                for command in data:
                    command = command.split(" ")

                    if command[0] in VALID_COMMANDS:
                        if self.args_error_handler(command) == 0:
                                self.execute(command)
                    elif '\n' in command[0] or '\r' in command[0]:
                        self.build_send_header(BAD_EOL)
                        self.close()
                    else:
                        self.build_send_header(INVALID_COMMAND)
   
