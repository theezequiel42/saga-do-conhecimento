import pygame, sys
from settings import *

# Define a classe principal do jogo
class Game:
    def __init__(self):
        # Inicializa todas as funções pygame
        pygame.init()
        
        # Define as dimensões da tela do jogo
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        
        # Define o título da janela do jogo
        pygame.display.set_caption('A Saga do Conhecimento')
        
        # Cria um objeto clock para controlar o tempo do jogo
        self.clock = pygame.time.Clock()
    
    # Método principal para rodar o jogo
    def run(self):
        # Loop infinito para manter o jogo rodando
        while True:
            # Checa todos os eventos (como teclas pressionadas ou o fechamento da janela)
            for event in pygame.event.get():
                # Se o evento for de fechamento da janela
                if event.type == pygame.QUIT:
                    # Encerra o pygame
                    pygame.quit()
                    # Encerra o programa
                    sys.exit()
            
            # Preenche a tela com a cor preta
            self.screen.fill('black')
            
            # Atualiza a tela do jogo
            pygame.display.update()
            
            # Controla a taxa de frames por segundo (FPS)
            self.clock.tick(FPS)

# Ponto de entrada do programa
if __name__ == '__main__':
    # Cria uma instância da classe Game
    game = Game()
    # Chama o método run para iniciar o jogo
    game.run()