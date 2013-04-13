#!/usr/bin/env python
import random
import socket
import time


def simple_app():
    """Simplest possible application object"""
    return '<b>This app is officially working</b>'



s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 8079
s.bind((host, port))        # Bind to the port

print 'Starting server on', host, port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   response = r'''HTTP/1.0 200 OK
Content-Type: text/html

'''
   response += simple_app()
   c.send(response)

   c.close()
