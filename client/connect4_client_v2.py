
#from signal import sigpending
import pygame
from connect4_board_v2 import *
import socket
import threading
import pickle
from PIL import Image,ImageSequence
import tkinter
from tkinter import messagebox
import sys
import os
#from  connect4_read_v2 import Game



os.environ["SDL_VIDEODRIVER"] = "dummy"
# game variables 
sending_data = None
your_turn = None
connection_lock = False
screen_x = 910
screen_y = 700
game = None
run = True
mainloopcontrol = True

disconnection_message = None
disconnected = False
#initlize pygame
pygame.init()

#host and port 

# write the servers ip adress between the '' 
host = ''
port = 2340


def connection_error(gotdisconnected = False,error = None):
    root = tkinter.Tk()
    root.geometry("300x200")
    root.wm_withdraw()
    if not gotdisconnected and error == None :
        messagebox.showerror("connection error", "Couldn't connect to the server!")
    else : 
         messagebox.showerror("connection error", error)
    root.mainloop() 
    pygame.quit()
 
#create a client socket and connect to the host
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try :
    client.connect((host,port))
except : 
    connection_error()
    



screen = pygame.display.set_mode((screen_x,screen_y))
pygame.display.set_caption('Connect4')

#clock object
clock = pygame.time.Clock()

#games icon
#Icon = board.resource_path('img/icon.png')
programIcon = pygame.image.load('img/icon.png')
pygame.display.set_icon(programIcon)

#create an instance of Board class imported from connect4_read_v2
board = Board(screen , screen_x,screen_y)



def pilImageToSurface(  pilImage):
    try : 
        mode, size, data = pilImage.mode, pilImage.size, pilImage.tobytes()
        return pygame.image.fromstring(data, size, mode).convert_alpha()
    except: 
        return None
    #Opens a gif, splits it into frames , convert them to pygame surface and add them to the returning list
def loadGIF(filename):
    try : 
        pilImage = Image.open(filename)
        frames = []
        if pilImage.format == 'GIF' and pilImage.is_animated:
            for frame in ImageSequence.Iterator(pilImage):
                pygameImage = pilImageToSurface(frame.convert('RGBA'))
                frames.append(pygameImage)
        else:
            frames.append(pilImageToSurface(pilImage))
        return frames
    except : 
        return None

# recive data from the server
def client_recive():
    #globalize the variables 
    global your_turn
    global board
    global second
    global game 
    global mainloopcontrol
    global disconnection_message,disconnected
    counter = 0
    #always checks for new data
    while True : 
        try : 
            global game
            #loads the reciving object
            game_data = client.recv(1024)
            try:
                game = pickle.loads(game_data)
            except: 
                print('no object recived')
                game = None

            #checks if the object was recived successfuly
            try : 
                if game_data.decode() == 'Opponent has disconnected': 
                    print(game_data.decode())
                    mainloopcontrol = False
                    
                else : 
                    pass
                   # disconnection_message = game_data.decode()
                    #disconnected = True
                    #print(game_data.decode())
                    
            except:
                print('object recived')
            if game == None : 
                pygame.quit()
                game.running = False
                client.close()
                break

            #checks if the second player is in and checks if anymove has been done
            elif game.ready : 
                for i in board.table_sample: 
                    counter += i.count(0)
                #if no move was done ....
                if counter == 35:
                    your_turn = True
                    game.player = 'yellow'

                #draws the other clients  move on the screen 
                else: 
                    if game.col != None : 
                        board.move(int(game.col),game.player)
                        if game.turn == 'True' and board.valid_move : 
                                your_turn = True 
                                if game.player == 'red':
                                    game.player = 'yellow'
                                elif game.player == 'yellow': 
                                    game.player = 'red'   
        except socket.error as error : 
            game.running = False
            pygame.quit()
            client.close()

            break 
    

#run client_recive at the same time as rest of the program 
recive_thread = threading.Thread(target=client_recive,)
recive_thread.start()




#display the waiting message if only one client connected otherwise draw the main gameboard
def redrawWindow(game):
    try: 
        global connection_lock
        board.screen.fill(pygame.Color('blue'))
        print(game.connected())
        connection_lock = False

        if not game.connected():
            board.start()
        else :
            connection_lock = True
            board.game_board()
    except: 
        return


def main_func():
    #globalize the variables 
    global connection_lock
    global board
    global your_turn
    global sending_data
    global second
    global game
    global mainloopcontrol
    global run 
    global col
    global screen
    pygame.init()
    #returns the game frameList 
    gif_add =board.resource_path('img/waiting_v2_1.gif')
    #print(pygame.display.get_init(),'2323423')
    gifFrameList = loadGIF('img/waiting_v2_1.gif')
    currentFrame = 0


    
    #cheks if the game object was recived from the server without any error ....
    if game == None : 
        pygame.quit()
        print('hello')
    elif game != None  : 
        game = game
        if game.error == None : 
            redrawWindow(game)



            #game main loop 
            while hasattr(game,'running') and game.running :
                clock.tick(20)
                pygame.display.update()
                #if the second client connected shows the turn viewer otherwise displays the waiting gif
                if hasattr(game,'ready') :
                    if game.ready :
                        board.turn_viewer_text(your_turn,game.player)  
                    else: 
                        board.screen.blit(gifFrameList[currentFrame], (0,0))
                        currentFrame = (currentFrame + 1) % len(gifFrameList)
                    #updates the first clients screen 
                    if not connection_lock and game.ready:
                        board.game_board()
                        connection_lock = True
                

                #checks all the events
                for event in pygame.event.get():
                    #close the window and stop the connection
                    if event.type == pygame.QUIT: 
                        if game != None : 
                            run = False
                            mainloopcontrol = False
                            pygame.quit()
                            client.close()
                    #if it was the players turn and a valid key was recived the move will be drawn and data will be sent to the server
                    if  event.type == pygame.KEYDOWN and your_turn: 
                        if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                            col = 1
                            board.move(col,game.player)
                        if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                            col = 2
                            board.move(col,game.player)
                        if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                            col = 3
                            board.move(col,game.player)
                        if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                            col = 4
                            board.move(col,game.player)
                        if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                            col = 5
                            board.move(col,game.player)
                        if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                            col = 6
                            board.move(col,game.player)
                        if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                            col = 7
                            board.move(col,game.player)
                  
                        #if a valid key was pressed , data will be sent to the server in form a string byte
                      
                         
                        sending_data = '{}-{}-{}-{}'.format(board.row_counter,col,game.player,your_turn)
                        print('sending: ' ,sending_data)
                        client.send(sending_data.encode('utf-8'))
                        #if movement was valid , change the players  and set the current players turn to false
                        if board.valid_move :
                            your_turn = False
                            if game.player == 'red':
                                game.player = 'yellow'
                            elif game.player == 'yellow': 
                                game.player = 'red'
                    
                        
#start menu runs until the screen is tapped 
def menu_screen():
    global run
    tap_to_play_add =board.resource_path('img/tap_to_play.png')

    while run:
        clock.tick(60)
        tap_to_play= pygame.image.load('img/tap_to_play.png')
        tap_to_play = pygame.transform.scale(tap_to_play,(910,750))
        board.screen.blit(tap_to_play, (0,0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main_func()


while mainloopcontrol:

    
    menu_screen()
                




    
