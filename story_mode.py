import pygame
from config import WIDTH, HEIGHT, COLORS
from utils import carregar_imagem, desenhar_texto, desenhar_hud, desenhar_personagens, tocar_musica

def fase_zero(screen, jogador):
    tocar_musica('musica_historia.mp3')  # Garantir que a música seja tocada
    running = True
    clock = pygame.time.Clock()
    jogador_pos = [100, HEIGHT - 400]
    jogador_vel_y = 0
    jogador_no_chao = True
    altura_chao = HEIGHT - 400

    jogador.estado.update({
        "jogador_acao": "idle",
        "jogador_frame_atual": 0,
        "jogador_frame_tempo": 0
    })

    # Carregar a imagem de fundo da história
    background_historia_img = carregar_imagem("background_historia.png", WIDTH, HEIGHT)

    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            jogador.estado["jogador_acao"] = "run"
        else:
            jogador.estado["jogador_acao"] = "idle"

        if keys[pygame.K_LEFT]:
            jogador_pos[0] -= 5
        if keys[pygame.K_RIGHT]:
            jogador_pos[0] += 5
        if keys[pygame.K_SPACE] and jogador_no_chao:
            jogador_vel_y = -15
            jogador_no_chao = False

        jogador_vel_y += 1
        jogador_pos[1] += jogador_vel_y
        if jogador_pos[1] >= altura_chao:
            jogador_pos[1] = altura_chao
            jogador_vel_y = 0
            jogador_no_chao = True

        screen.blit(background_historia_img, (0, 0))
        screen.blit(jogador.jogador_animacoes[jogador.estado["jogador_acao"]][jogador.estado["jogador_frame_atual"]], jogador_pos)

        ret_sair = desenhar_texto("Sair", None, COLORS["BRANCO"], screen, WIDTH - 100, HEIGHT - 50)
        mouse_pos = pygame.mouse.get_pos()
        if ret_sair.collidepoint(mouse_pos):
            pygame.draw.rect(screen, COLORS["AMARELO"], ret_sair)
            desenhar_texto("Sair", None, COLORS["PRETO"], screen, WIDTH - 100, HEIGHT - 50)
            if pygame.mouse.get_pressed()[0]:
                running = False

        pygame.display.flip()
        clock.tick(60)

def modo_historia(screen, jogador):
    fase_zero(screen, jogador)
