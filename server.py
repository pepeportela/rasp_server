import sys
import socket
import Adafruit_DHT
import time
import logging

logging.basicConfig( filename = '/server/logs/server.log',level = logging.DEBUG,format = '%(asctime)s - %(levelname)s: %(message)s',datefmt = '%m/%d/%Y %I:%M:%S %p' )

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
host = ''
port = 5000                # Reserve a port for your service.
logging.info(port)
s.bind((host,port))        # Bind to the port
s.listen(1)                 # Now wait for client connection.

while True:
    c, addr = s.accept()     # Establish connection with client.
    logging.warning("Connected to {0}".format(addr))
    
    humidity, temperature = Adafruit_DHT.read_retry(11,4,delay_seconds=5)
    var = str(temperature)+"/"+str(humidity)
    c.send(var)
    time.sleep(5)
