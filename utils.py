import pygame
import os
from config import COLORS, WIDTH

def carregar_imagem(nome, width, height):
    """Carrega e redimensiona uma imagem."""
    img = pygame.image.load(nome).convert_alpha()
    return pygame.transform.scale(img, (width, height))

def tocar_musica(musica, loop=-1):
    """Toca uma música."""
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play(loop)

def parar_musica():
    """Para a música atual."""
    pygame.mixer.music.stop()

def tocar_som(som):
    """Toca um efeito sonoro."""
    efeito = pygame.mixer.Sound(som)
    efeito.play()

def desenhar_texto(texto, fonte, cor, superficie, x, y):
    """Desenha um texto na tela."""
    if fonte is None:
        fonte = pygame.font.Font(None, 36)
    objeto_texto = fonte.render(texto, True, cor)
    retangulo_texto = objeto_texto.get_rect(topleft=(x, y))
    superficie.blit(objeto_texto, retangulo_texto)
    return retangulo_texto  # Retornar o retângulo para detecção de clique

def carregar_animacao(caminho, largura_frame, altura_frame, num_frames):
    """Carrega os frames de uma animação a partir de um sprite sheet."""
    if not os.path.isfile(caminho):
        raise FileNotFoundError(f"O arquivo '{caminho}' não foi encontrado no diretório '{os.getcwd()}'.")
    sprite_sheet = pygame.image.load(caminho).convert_alpha()
    frames = [pygame.transform.scale(sprite_sheet.subsurface((i * largura_frame, 0, largura_frame, altura_frame)), (200, 200)) for i in range(num_frames)]
    return frames

def desenhar_hud(screen, estado_jogo):
    """Desenha a HUD na tela."""
    # Barra de saúde do jogador
    pygame.draw.rect(screen, COLORS["VERMELHO"], (20, 600, 200, 20))
    pygame.draw.rect(screen, COLORS["VERDE"], (20, 600, 2 * estado_jogo["saude_jogador"], 20))
    desenhar_texto(f"Jogador: {estado_jogo['saude_jogador']}/100", None, COLORS["BRANCO"], screen, 20, 570)

    # Barra de saúde do inimigo
    pygame.draw.rect(screen, COLORS["VERMELHO"], (1060, 600, 200, 20))
    pygame.draw.rect(screen, COLORS["VERDE"], (1060, 600, 2 * estado_jogo["saude_inimigo"], 20))
    desenhar_texto(f"Inimigo: {estado_jogo['saude_inimigo']}/100", None, COLORS["BRANCO"], screen, 1060, 570)

    # Barra de mana do jogador
    pygame.draw.rect(screen, COLORS["CINZA"], (20, 660, 200, 20))
    pygame.draw.rect(screen, COLORS["AZUL"], (20, 660, 2 * estado_jogo["mana_jogador"], 20))
    desenhar_texto(f"Mana: {estado_jogo['mana_jogador']}/100", None, COLORS["BRANCO"], screen, 20, 630)

    # Barra de mana do inimigo
    pygame.draw.rect(screen, COLORS["CINZA"], (1060, 660, 200, 20))
    pygame.draw.rect(screen, COLORS["AZUL"], (1060, 660, 2 * estado_jogo["mana_inimigo"], 20))
    desenhar_texto(f"Mana: {estado_jogo['mana_inimigo']}/100", None, COLORS["BRANCO"], screen, 1060, 630)

    # Pontos de sabedoria
    desenhar_texto(f"Pontos de Sabedoria: {estado_jogo['pontos_sabedoria']}", None, COLORS["BRANCO"], screen, WIDTH - 320, 20)

def desenhar_personagens(screen, jogador_animacoes, inimigo_animacoes, estado_jogo, dano_jogador=False, dano_inimigo=False, derrota_jogador=False, derrota_inimigo=False):
    jogador_pos = (100, HEIGHT - 320)
    inimigo_pos = (980, HEIGHT - 320)

    # Animação do jogador
    if derrota_jogador:
        frames = jogador_animacoes["derrota"]
        frame_delay = 200
    elif estado_jogo["jogador_acao"] == "idle":
        frames = jogador_animacoes["idle"]
        frame_delay = 50
    elif estado_jogo["jogador_acao"] == "run":
        frames = jogador_animacoes["run"]
        frame_delay = 50
    elif estado_jogo["jogador_acao"] == "attack":
        frames = jogador_animacoes["attack"]
        frame_delay = 200

    screen.blit(frames[estado_jogo["jogador_frame_atual"]], jogador_pos)
    estado_jogo["jogador_frame_tempo"] += 1
    if estado_jogo["jogador_frame_tempo"] >= frame_delay:
        estado_jogo["jogador_frame_tempo"] = 0
        estado_jogo["jogador_frame_atual"] = (estado_jogo["jogador_frame_atual"] + 1) % len(frames)
        if estado_jogo["jogador_acao"] == "attack" and estado_jogo["jogador_frame_atual"] == len(frames) - 1:
            estado_jogo["jogador_acao"] = "idle"
            estado_jogo["jogador_frame_atual"] = 0

    # Animação do inimigo
    if derrota_inimigo:
        frames = inimigo_animacoes["derrota"]
        frame_delay = 200
    elif estado_jogo["inimigo_acao"] == "idle":
        frames = inimigo_animacoes["idle"]
        frame_delay = 50
    elif estado_jogo["inimigo_acao"] == "attack":
        frames = inimigo_animacoes["attack"]
        frame_delay = 200

    screen.blit(frames[estado_jogo["inimigo_frame_atual"]], inimigo_pos)
    estado_jogo["inimigo_frame_tempo"] += 1
    if estado_jogo["inimigo_frame_tempo"] >= frame_delay:
        estado_jogo["inimigo_frame_tempo"] = 0
        estado_jogo["inimigo_frame_atual"] = (estado_jogo["inimigo_frame_atual"] + 1) % len(frames)
        if estado_jogo["inimigo_acao"] == "attack" and estado_jogo["inimigo_frame_atual"] == len(frames) - 1:
            estado_jogo["inimigo_acao"] = "idle"
            estado_jogo["inimigo_frame_atual"] = 0

def desenhar_barra_tempo(screen, tempo_restante, tempo_total):
    largura_barra = int((tempo_restante / tempo_total) * 400)
    pygame.draw.rect(screen, COLORS["AZUL"], (440, 80, largura_barra, 20))
