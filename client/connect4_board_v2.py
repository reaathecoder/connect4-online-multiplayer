#import the required modules 
import pygame
from PIL import Image,ImageSequence
import sys 
import os 
#initialize the pygame object
pygame.init()


class Board:
    
    #board class atteributes
    def __init__(self,screen,screen_x,screen_y):
     
        self.screen =  screen
        #print(pygame.display.get_init())
        
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.table_sample = [[0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0]]
        self.player='yellow'
        self.ready = False
        self.circle_list = []
        self.table = []
        self.winner = False
        self.cols = 7
        self.rows = 5
        self.running = False
        self.row_counter = None
        self.valid_move = None
        self.player_num = 0
        self.big_font = pygame.font.SysFont('Arial',45,bold=True)
        self.font = pygame.font.SysFont('Arial',32)

 #store path with pyinstaller while conversion to exe

    


    #convert Pil image to pygame surface
    
    def pilImageToSurface(self , pilImage):
        try:
            mode, size, data = pilImage.mode, pilImage.size, pilImage.tobytes()
            return pygame.image.fromstring(data, size, mode).convert_alpha()
        except: 
            return None
    #Opens a gif, splits it into frames , convert them to pygame surface and add them to the returning list
    def loadGIF(self , filename):
        try:

            screen = self.screen
            pilImage = Image.open(filename)
            frames = []
            if pilImage.format == 'GIF' and pilImage.is_animated:
                for frame in ImageSequence.Iterator(pilImage):
                    if self.pilImageToSurface(frame.convert('RGB')) == None :
                        pygameImage = self.pilImageToSurface(frame.convert('RGBA'))
                        frames.append(pygameImage)
            else:
                frames.append(self.pilImageToSurface(pilImage))
            return frames
        except:
            return None

    def resource_path(self,relative_path):
        try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    #display the waiting menu 
    def start(self): 
            waiting_add =self.resource_path('img/waiting_v2_1.gif')
            img = pygame.image.load(waiting_add)
            self.screen.blit(img, (0,0))
   
    #draws the main game board
    def game_board(self,table_x = 910 , table_y= 600):
        
                self.screen.fill(pygame.Color('blue'))
                for row in range((table_y//5)//2,table_y,table_y//5):
                    for col in range((table_x//7)//2,table_x,table_x//7):
                        pygame.draw.circle(self.screen,pygame.Color(8,8,8),(col,row), ((table_x//7)//2)-10)
                        self.circle_list.append(pygame.draw.circle(self.screen,pygame.Color(8,8,8),(col,row), ((table_x//7)//2)-10))
                    pygame.draw.rect(self.screen,pygame.Color('black'),[0,600,table_x,100])
                for i in range(0,len(self.circle_list),7):
                    self.table.append(self.circle_list[i:i+7])
                self.table=self.table[::-1]
                return self.table

    #display the winners name on the screen 
    def show_winner(self,The_winner):
        self.winner = True
        if The_winner == 'yellow':
            yellow_add =self.resource_path('img/yellow.png')
            winner_banner = pygame.image.load(yellow_add)
            self.screen.blit(winner_banner,(0,0))
        elif The_winner == 'red':
            red_add =self.resource_path('img/red.png')
            winner_banner = pygame.image.load(red_add)
            self.screen.blit(winner_banner,(0,0))
       
    #display the players turn      
    def turn_viewer_text(self,turn,redOryellow,table_x=910):
                if not self.winner :
                    text_turn = self.font.render(redOryellow , True , pygame.Color(redOryellow))
                    text_viewer = self.font.render("'s turn",True,pygame.Color('white'))
                    pygame.draw.rect(self.screen,pygame.Color(0,0,0),[0,600,table_x,100])
                    self.screen.blit(text_turn,(self.screen_x//2-40,650)) if redOryellow == 'red' else self.screen.blit(text_turn,(self.screen_x//2-75,650))
                    self.screen.blit(text_viewer,(self.screen_x//2,650))

    #check for the winner 
    def winner_check(self,row_counter,col):
        latest_move = self.table_sample[row_counter][col]
        for each_col_num in range(self.cols-3) : 
            for each_row_num in range(self.rows):
                if self.table_sample[each_row_num][each_col_num] ==  self.table_sample[each_row_num][each_col_num+1] ==  self.table_sample[each_row_num][each_col_num+2] ==  self.table_sample[each_row_num][each_col_num+3] == latest_move :
                    self.show_winner(latest_move)
 
        for each_row_num in range(self.rows-3) : 
            for each_col_num in range(self.cols):
                if self.table_sample[each_row_num][each_col_num] ==  self.table_sample[each_row_num+1][each_col_num] ==  self.table_sample[each_row_num+2][each_col_num] ==  self.table_sample[each_row_num+3][each_col_num] == latest_move :
                    self.show_winner(latest_move)
 
        for each_col_num in range(self.cols-3) : 
            for each_row_num in range(self.rows-3):
                if self.table_sample[each_row_num][each_col_num] ==  self.table_sample[each_row_num+1][each_col_num+1] ==  self.table_sample[each_row_num+2][each_col_num+2] ==  self.table_sample[each_row_num+3][each_col_num+3] == latest_move :
                    self.show_winner(latest_move)


        for each_col_num in range(self.cols) : 
            for each_row_num in range(self.rows-3):
                if self.table_sample[each_row_num][each_col_num] ==  self.table_sample[each_row_num+1][each_col_num-1] ==  self.table_sample[each_row_num+2][each_col_num-2] ==  self.table_sample[each_row_num+3][each_col_num-3] == latest_move :
                    self.show_winner(latest_move)

    #draw the new move on the screen 
    def move(self,col,redOryellow,table_x = 910): 
        self.row_counter = 0
        if not self.winner :
            while self.row_counter < 4 and self.table_sample[self.row_counter][col-1]!=0:
                    self.row_counter+=1   
            if self.table_sample[self.row_counter][col-1] == 0:
                pygame.draw.circle(self.screen,pygame.Color(redOryellow),self.table[self.row_counter][col-1].center, ((table_x//7)//2)-10)
                self.table_sample[self.row_counter][col-1] = redOryellow
                self.valid_move = True
                self.winner_check(self.row_counter,col-1)

                return self.row_counter , col-1
            else:
                self.valid_move=False
            
            
