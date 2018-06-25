import sys
import socket
import Adafruit_DHT
import time
import logging

logging.basicConfig( filename = '/server/logs/server.log',level = logging.DEBUG,format = '%(asctime)s - %(levelname)s: %(message)s',datefmt = '%m/%d/%Y %I:%M:%S %p' )

host = ''
port = 5000                # Reserve a port for your service.
logging.info("Restarted")

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
        s.bind((host,port))      # Bind to the port
        s.listen(2)              # Now wait for client connection.
        logging.info("Listening in {0}".format(port))
        c, addr = s.accept()     # Establish connection with client.
        c.send("Accepted\n")
        client_name = c.recv(1024)
        if client_name[:-1] != "Movil Pepe":
            logging.error("Connection try from {0} {1}".format(client_name[:-1],addr))
            s.close()
            break
        logging.warning("Connected to {0} {1}".format(client_name[:-1],addr))

        while True:
            humidity, temperature = Adafruit_DHT.read_retry(11,4,delay_seconds=5)
            if humidity > 100:
                humidity = "-"
                temperature = "-"
            var = str(temperature)+"/"+str(humidity)+"\n"
            c.send(var)
            ack = c.recv(1024)
            if ack!="ack": break
            time.sleep(5)

        logging.warning("Disconnected {0} {1}".format(client_name[:-1],addr))
        s.close()
        time.sleep(10)
        
    except socket.error as msg:
        s.close()
        logging.error(msg)
        time.sleep(60)
