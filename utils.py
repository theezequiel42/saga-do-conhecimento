import pygame
from config import WIDTH, HEIGHT

def carregar_imagem(nome, largura, altura):
    img = pygame.image.load(nome).convert_alpha()
    return pygame.transform.scale(img, (largura, altura))

def desenhar_texto(texto, fonte, cor, surface, x, y):
    if fonte is None:
        fonte = pygame.font.Font(None, 36)
    text_surface = fonte.render(texto, True, cor)
    surface.blit(text_surface, (x, y))
    return text_surface.get_rect(topleft=(x, y))

def carregar_animacao(nome_base, largura, altura, n_frames, individual_frames=False, scale_width=None, scale_height=None):
    frames = []
    if individual_frames:
        for i in range(n_frames):
            nome = f"{nome_base}-{i:02d}.png"
            frame = carregar_imagem(nome, largura, altura)
            if scale_width and scale_height:
                frame = pygame.transform.scale(frame, (scale_width, scale_height))
            frames.append(frame)
    else:
        sprite_sheet = carregar_imagem(nome_base, largura * n_frames, altura)
        for i in range(n_frames):
            frame = sprite_sheet.subsurface(pygame.Rect(i * largura, 0, largura, altura))
            if scale_width and scale_height:
                frame = pygame.transform.scale(frame, (scale_width, scale_height))
            frames.append(frame)
    return frames

def desenhar_hud(surface, estado):
    fonte = pygame.font.Font(None, 36)
    cor = (255, 255, 255)
    
    # Desenhar barras de saúde e mana do jogador no canto inferior esquerdo
    largura_barra = 200
    altura_barra = 20

    saude_jogador_texto = f"Saúde: {estado['saude_jogador']}"
    mana_jogador_texto = f"Mana: {estado['mana_jogador']}"
    desenhar_texto(saude_jogador_texto, fonte, cor, surface, 20, HEIGHT - 80)
    desenhar_texto(mana_jogador_texto, fonte, cor, surface, 20, HEIGHT - 40)

    pygame.draw.rect(surface, (0, 0, 0), (20, HEIGHT - 60, largura_barra, altura_barra))
    pygame.draw.rect(surface, (0, 255, 0), (20, HEIGHT - 60, largura_barra * (estado['saude_jogador'] / 100), altura_barra))
    pygame.draw.rect(surface, (0, 0, 0), (20, HEIGHT - 20, largura_barra, altura_barra))
    pygame.draw.rect(surface, (0, 0, 255), (20, HEIGHT - 20, largura_barra * (estado['mana_jogador'] / 100), altura_barra))

    # Desenhar barras de saúde e mana do inimigo no canto inferior direito
    saude_inimigo_texto = f"Saúde: {estado['saude_inimigo']}"
    mana_inimigo_texto = f"Mana: {estado['mana_inimigo']}"
    desenhar_texto(saude_inimigo_texto, fonte, cor, surface, WIDTH - 220, HEIGHT - 80)
    desenhar_texto(mana_inimigo_texto, fonte, cor, surface, WIDTH - 220, HEIGHT - 40)

    pygame.draw.rect(surface, (0, 0, 0), (WIDTH - 220, HEIGHT - 60, largura_barra, altura_barra))
    pygame.draw.rect(surface, (0, 255, 0), (WIDTH - 220, HEIGHT - 60, largura_barra * (estado['saude_inimigo'] / 100), altura_barra))
    pygame.draw.rect(surface, (0, 0, 0), (WIDTH - 220, HEIGHT - 20, largura_barra, altura_barra))
    pygame.draw.rect(surface, (0, 0, 255), (WIDTH - 220, HEIGHT - 20, largura_barra * (estado['mana_inimigo'] / 100), altura_barra))

def desenhar_barra_tempo(surface, tempo_restante, tempo_total):
    largura = 400
    altura = 20
    x = (surface.get_width() - largura) // 2
    y = 20
    pygame.draw.rect(surface, (255, 0, 0), (x, y, largura, altura))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, largura * (tempo_restante / tempo_total), altura))

def desenhar_personagens(surface, jogador_animacoes, inimigo_animacoes, estado, dano_inimigo=False, dano_jogador=False):
    jogador_acao = estado["jogador_acao"]
    jogador_frame_atual = estado["jogador_frame_atual"]

    inimigo_acao = estado["inimigo_acao"]
    inimigo_frame_atual = estado["inimigo_frame_atual"]

    jogador_frames = jogador_animacoes.get(jogador_acao, jogador_animacoes["idle"])
    inimigo_frames = inimigo_animacoes.get(inimigo_acao, inimigo_animacoes["idle"])

    jogador_frame = jogador_frames[jogador_frame_atual]
    inimigo_frame = inimigo_frames[inimigo_frame_atual]

    surface.blit(jogador_frame, (100, 300))
    surface.blit(inimigo_frame, (980, 300))

def tocar_som(nome):
    som = pygame.mixer.Sound(nome)
    som.play()

def parar_musica():
    pygame.mixer.music.stop()

def tocar_musica(nome):
    pygame.mixer.music.load(nome)
    pygame.mixer.music.play(-1)
