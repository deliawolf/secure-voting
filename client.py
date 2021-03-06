# Author: Marwan Nour

import socket
import json
import time
from phe import paillier

# Get Public Key from Trustee
# create a socket object
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# get local machine name
host = socket.gethostname()                           
portTrustee = 10001
# connection to hostname on the port.
clientSocket.connect((host, portTrustee))                               
# Receive no more than 1024 bytes
msg = clientSocket.recv(2000)                                
public_key = msg.decode("ascii")
clientSocket.close()

# Client needs to vote
candidates = ['Donald Trump', 'Roger Federer', 'Britney Spears', 'Ali El Deek','Steve Jobs']

print("Choose your candidates (up to 2) among the list: "  + str(candidates))

print(public_key)            

# Deserialize the public key
received_dict = json.loads(public_key)
pk = received_dict['public_key']
public_key_rec = paillier.PaillierPublicKey(n=int(pk['n']))
print(str(public_key_rec))


vote_count = 0
# choice is 0 by default so it can compute to 0 when encoded
choice = "-1"
summed_choices = 0

while(vote_count < 2):
    print("0 - Donald Trump")
    print("1 - Roger Federer")
    print("2 - Britney Spears")
    print("3 - Ali El Deek")
    print("4 - Steve Jobs")
    print("9  to exit")
    choice = int(input())
    #encode the choice
    if(choice == 9):
        break
    summed_choices += pow(10, choice)
    vote_count += 1 

print("Summed Choices:\t" + str(summed_choices))

# now we use it to encrypt the summed choices
encrypted_choices = public_key_rec.encrypt(summed_choices)

print(encrypted_choices)

# create a voting socket with a different port
voting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port_voting_server = 10002
voting_socket.connect((host, port_voting_server))
# send the encrypted choices CIPHERTEXT to voting server
voting_socket.send(str(encrypted_choices.ciphertext()).encode())
voting_socket.close()


# Create a socket to receive the winner
# Try catch
while(True):
    # put code here
    try:
        print("Connecting to trustee server...")
        winner_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        port_winner = 10004
        winner_sock.connect((host, port_winner))
        msg = winner_sock.recv(1024)
        winner_sock.close()
        # Decode Winner
        # Print Winner
        decoded_winner = msg.decode("ascii")
        print(decoded_winner)
        break

    except socket.error as e:
        #sleep here
        print("Error connecting to trustee server. Sleeping for 5 seconds")
        time.sleep(5)


