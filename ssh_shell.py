import argparse
import logging
import paramiko
import re
import sys
import time

class ssh_to_client:
	def __init__(self,creds):
		self.username = creds.username
		self.hostname = creds.hostname
		self.password = creds.password
		self.port = creds.port

	def __delete__(self, client):
		logging.info(f'Closing the conection to client {self.hostname}')
		client.close()

	def create_ssh_connection(self):
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		logging.info(f'Trying to connect to {self.hostname} with credentials {self.username}/{self.password} on port {self.port}')
		client.connect(hostname=self.hostname, username=self.username, password=self.password, port=self.port)
		logging.info('Connection established')
		return client

	def invoke_interactive_ssh_shell(self):
		client = self.create_ssh_connection()
		logging.info('Invoking ssh shell')
		sh = client.invoke_shell()
		a = sys.stdout.encoding
		ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
		cmd = 'uname -a'
		while True:
			if cmd == 'exit':
				logging.info('Exiting the shell')
				break
			else:
				logging.info(f'Executing command {cmd}')
				sh.send(cmd+'\n')
			while True:
				time.sleep(1)
				if sh.recv_ready():
					std_out = sh.recv(9999)
					std_out = std_out.decode(a)
					logging.info(f'Result for execution : {ansi_escape.sub('', std_out)}')
					print(ansi_escape.sub('', std_out))
				else:
					break
			cmd = input('>').strip('\n')

if __name__ == '__main__':
	logging.basicConfig(filename='shh_to_the_client.log', filemode='w' ,level=logging.INFO)
	parser_obj = argparse.ArgumentParser("Establish SSH connection to a client",  usage="%(prog)s [-h] -ho HOSTNAME -u USERNAME -p PASSWORD [-pn PORT]")
	parser_obj.add_argument('-ht', '--hostname', dest='hostname', required=True,  help='Hostname of the client', metavar='')
	parser_obj.add_argument('-u', '--username', dest='username', type=str, required=True,  help='Username with which to login to the client', metavar='')
	parser_obj.add_argument('-p', '--password', dest='password', type=str, required=True,  help='Password with which to login to the client', metavar='')
	parser_obj.add_argument('-pt', '--port', dest='port', type=int, default=22,  help='Port number of the client', metavar='')
	creds = parser_obj.parse_args()
	ssh_obj = ssh_to_client(creds)
	ssh_obj.invoke_interactive_ssh_shell()
