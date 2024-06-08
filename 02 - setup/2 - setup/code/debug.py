import pygame  # Importa o módulo pygame
pygame.init()  # Inicializa todas as funções pygame

# Define a fonte padrão para o texto de depuração
font = pygame.font.Font(None, 30)

# Função de depuração que exibe informações na tela
def debug(info, y=10, x=10):
    display_surface = pygame.display.get_surface()  # Obtém a superfície de exibição principal onde o jogo é desenhado
    debug_surf = font.render(str(info), True, 'White')  # Renderiza o texto de depuração na cor branca
    debug_rect = debug_surf.get_rect(topleft=(x, y))  # Cria um retângulo ao redor do texto na posição (x, y)
    pygame.draw.rect(display_surface, 'Black', debug_rect)  # Desenha um retângulo preto no fundo para o texto
    display_surface.blit(debug_surf, debug_rect)  # Desenha o texto de depuração na superfície de exibição