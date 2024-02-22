#import the neccessery modules 
import socket 
import threading
from connect4_read_v2  import Game
import pickle





#create the socket object
server = '92.39.14.26'
host = socket.gethostbyname(server)
port = 2340
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))

# wait for reciving a connection 
server.listen(2)

# status
clients = []
colors = []
last_player = None

#send message to all the clients 
def to_all(message):
    
    for client in clients :
        client.send(message)


#send message to all the clients except the cleint sender
def broadcast(message,client_ip):
    for client in clients : 
        if client != client_ip: 

            client.send(pickle.dumps(message))

#recives data from a client and store them into game object and send the object to the other clients
def client_handler(client,game):
    while True: 
        try : 
            if client in clients : 
                message = client.recv(1024)
                #decode the recived byteobject to string and then a list 
                data = message.decode('utf-8').split('-')
                #change the game objects values to the new recived values
                game.row_counter = data[0]
                game.col = data[1]
                game.player=data[2]
                game.turn = data[3]
                #sending the object over to all the client except the sender one
                broadcast(game,client)
                print(colors,clients)

        #checks for the error and disconnect the client
        except socket.error as e : 
            print(e,colors,clients)
            index = clients.index(client)
            clients.remove(clients[index])
            client.close()
            color = colors[index]
            colors.remove(color)
            print(colors,clients)	    
#recives data from a client and store them into game object and send the object to the other clients
#recives data from a client and store them into game object and send the object to the other clients
def client_handler(client,game):
    while True: 
        try : 
            if client in clients : 
                message = client.recv(1024)
                #decode the recived byteobject to string and then a list 
                data = message.decode('utf-8').split('-')
                #change the game objects values to the new recived values
                game.row_counter = data[0]
                game.col = data[1]
                game.player=data[2]
                game.turn = data[3]
                #sending the object over to all the client except the sender one
                broadcast(game,client)

            

        #checks for the error and disconnect the client
        except socket.error as e : 
            print(e)
            index = clients.index(client)
            clients.remove(clients[index])
            client.close()
            color = colors[index]
            colors.remove(color)
            print(colors,clients)
            to_all('Opponent has disconnected'.encode('utf-8'))
            if len(colors) == 1 : 
                game.row_counter = None
                game.col = None
                game.player='yellow'
                game.turn = None
            elif len(colors) == 0 : 
                            game.row_counter = None
                            game.col = None
                            game.player='yellow'
                            game.turn = None
                            game.ready = False	        
                            
            #accept 2 connections 
def recive_connection(): 
    global last_player
    #initilize the game object
    game = Game()
    #always checks for the connection requests
    while True :
        #if less then 2 clients connected ....
        if len(colors) <= 2:
            print('running and waiting for the connections')
        #accept the connection and store the socket and the adress into client , adress variable 
        client,address = server.accept()
        #if more than 2 clients connected ... 
        if len(colors) >= 2:
            game.error  = f"Connection overflow. Max amount is {2}"
            print(colors)
            continue
    
        else:
            print(f'connection is stablished with {str(address)}')
   
        clients.append(client)  
        if len(clients) == 1: 
            color = 'red'
            last_player = 'red'
            game.running = True
            colors.append(color)
        elif len(clients)==2: 
            color = 'yellow'
            last_player = 'yellow' 
            colors.append(color)

        if len(colors)== 2 : 
            game.ready = True
  
        to_all(pickle.dumps(game))

  
        thread = threading.Thread(target=client_handler,args=(client,game,))
        thread.start()






if __name__ == '__main__': 
    recive_connection()