import socket
import threading

class TicTacToeClient:
    
    def __init__(self):
        
        self.board = [[" "," "," "],[" "," "," "],[" "," "," "]]
        self.turn = None
        self.you = None
        self.opponent = None
        self.winner = None
        self.game_over = False
        self.counter = 0
        self.ready = False  
        
    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        
        # Recibe el turno del servidor
        self.you = client.recv(1024).decode('utf-8')
        self.opponent = 'O' if self.you == 'X' else 'X'
        self.turn = 'X' 
        
        threading.Thread(target=self.handle_connection, args=(client,)).start()
        
    def handle_connection(self, client):
        
        while not self.game_over:
            print("1")
            data = client.recv(1024)
            if not data:
                client.close()
                break
            else:
                print("2")
                message = data.decode('utf-8')
                print("3")
                if message:
                    print("4")
                    self.ready = True
                    print("5")
                if self.ready:
                    print("6")
                    print("self.turn: ", self.turn)
                    print("self.you: ", self.you)                   
                    if self.turn == self.you:
                        print("7")
                        move = input("Enter a move (row,column): ")                
                        if self.check_valid_move(move.split(',')):
                            client.send(move.encode('utf8'))
                            self.apply_move(move.split(','), self.you)
                            self.turn = self.opponent
                            print("8")                            
                        else:
                            print("Invalid move!")
                    else: 
                        print("9")
                        data = client.recv(1024)
                        if not data:
                            print("10")
                            client.close()
                            break
                        else:
                            print("11")
                            self.apply_move(data.decode("utf-8").split(","), self.opponent)                    
                            self.turn = self.you
                         
                            if not self.game_over:
                                move = input("Enter a move (row,column): ")                
                                if self.check_valid_move(move.split(',')):
                                    client.send(move.encode('utf8'))
                                    self.apply_move(move.split(','), self.you)
                                    self.turn = self.opponent
                                else:
                                    print("Invalid move!")
                    
        client.close()
        
    

                        
    def check_valid_move(self, move):   
        if not self.is_in_range(move):
            return False
        return self.board[int(move[0])][int(move[1])] == " "
    
            
    def apply_move(self, move, player):
        if self.game_over:
            return
        else:        
            self.counter += 1 
            self.board[int(move[0])][int(move[1])] = player
            self.print_board()
            if self.counter == 9:  
                print("It's a tie!")
                exit()
            elif self.check_if_won(): 
                if self.winner == self.you:
                    print("You Winner!")
                    exit()
                elif self.winner == self.opponent:
                    print("You lose!")
                    exit()

                             
      
    
    
    def check_if_won(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0]
                self.game_over = True
                return True
            
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col]
                self.game_over = True
                return True
            
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            self.winner = self.board[0][0]
            self.game_over = True
            return True
        
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            self.winner = self.board[1][1]
            self.game_over = True
            return True
        
        return False
    
    def is_in_range(self, move):
        row, col = int(move[0]), int(move[1])
        return 0 <= row <= 2 and 0 <= col <= 2
    
    def print_board(self):        
        for row in range(3):
            print(" | ".join(self.board[row]))
            if row != 2:
                print("----------")
                
game = TicTacToeClient()
game.connect_to_game("192.168.1.107", 9999)
        
   
        
        
    
                
       
    
            
        
        
        
        
            
                       
    
    
                    
            
                    
        
                
        