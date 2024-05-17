import socket
import threading

class TicTacToeServer:
    
    def __init__(self):
        self.games = []
        
    def host_game(self, host, port):
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(2)
        
        while True:  
            game = []
            while len(game) < 2:
                client, addr = server.accept()
                game.append(client)
               
                client.send(('X' if len(game) == 1 else 'O').encode('utf-8'))
                threading.Thread(target=self.handle_connection, args=(client, game)).start()
            self.games.append(game)
           
            for player in game:
                player.send("El juego puede comenzar".encode('utf-8'))
        
    def handle_connection(self, client, game):
        
        while True:
            data = client.recv(1024)
            if not data:
                client.close()
                break
            else:
                for player in game:
                    if player != client:
                        player.send(data)
                    
        client.close()

game = TicTacToeServer()
game.host_game("192.168.1.107", 9999)
