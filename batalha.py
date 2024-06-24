import pygame
import random
import os

# Inicialização da Pygame
pygame.init()
pygame.mixer.init()

# Configurações da tela
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Saga do Conhecimento - Batalha")

# Cores
COLORS = {
    "BRANCO": (255, 255, 255),
    "PRETO": (0, 0, 0),
    "VERDE": (0, 255, 0),
    "VERMELHO": (255, 0, 0),
    "AZUL": (0, 0, 255),
    "CINZA": (169, 169, 169),
    "CINZA_CLARO": (211, 211, 211),
    "AMARELO": (255, 255, 0)
}

# Fonte
font = pygame.font.Font(None, 36)

# Carregar e redimensionar imagens
def carregar_imagem(nome, width, height):
    img = pygame.image.load(nome).convert_alpha()
    return pygame.transform.scale(img, (width, height))

background_batalha_img = carregar_imagem("background_batalha.png", WIDTH, HEIGHT)
background_menu_img = carregar_imagem("background_menu.png", WIDTH, HEIGHT)

# Carregar músicas e sons
MUSICAS = {
    "menu": "musica_menu.mp3",
    "batalha": "musica_batalha.mp3",
    "vitoria": "som_vitoria.mp3",
    "derrota": "som_derrota.mp3"
}

# Funções de áudio
def tocar_musica(musica, loop=-1):
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play(loop)

def parar_musica():
    pygame.mixer.music.stop()

def tocar_som(som):
    efeito = pygame.mixer.Sound(som)
    efeito.play()

# Função para desenhar texto na tela
def desenhar_texto(texto, fonte, cor, superficie, x, y):
    objeto_texto = fonte.render(texto, True, cor)
    retangulo_texto = objeto_texto.get_rect(topleft=(x, y))
    superficie.blit(objeto_texto, retangulo_texto)
    return retangulo_texto  # Retornar o retângulo para detecção de clique

# Função para carregar os frames da animação
def carregar_animacao(caminho, largura_frame, altura_frame, num_frames):
    if not os.path.isfile(caminho):
        raise FileNotFoundError(f"No file '{caminho}' found in working directory '{os.getcwd()}'.")
    sprite_sheet = pygame.image.load(caminho).convert_alpha()
    frames = [pygame.transform.scale(sprite_sheet.subsurface((i * largura_frame, 0, largura_frame, altura_frame)), (200, 200)) for i in range(num_frames)]
    return frames

# Carregar animações
jogador_animacoes = {
    "idle": carregar_animacao("idle-Sheet.png", 64, 64, 4),
    "attack": carregar_animacao("Attack-01-Sheet.png", 64, 64, 8),
    "derrota": carregar_animacao("derrota_jogador-Sheet.png", 64, 64, 8)
}

inimigo_animacoes = {
    "idle": carregar_animacao("Idle-Sheet-inimigo.png", 64, 64, 4),
    "derrota": carregar_animacao("derrota_inimigo-Sheet.png", 64, 64, 8)
}

# Perguntas organizadas por nível e disciplina
perguntas_por_nivel_e_disciplina = {
    "1° Ano": {
        "Matemática": [
            {"pergunta": "Quanto é 2 + 2?", "opcoes": ["3", "4", "5", "6"], "resposta": 1},
            {"pergunta": "Quanto é 3 + 3?", "opcoes": ["5", "6", "7", "8"], "resposta": 1},
            # Mais perguntas
        ],
        "Língua Portuguesa": [
            {"pergunta": "Qual é a letra inicial da palavra 'gato'?", "opcoes": ["A", "B", "G", "D"], "resposta": 2},
            {"pergunta": "Qual é a letra inicial da palavra 'casa'?", "opcoes": ["C", "B", "G", "D"], "resposta": 0},
            # Mais perguntas
        ],
    },
    # Mais níveis e disciplinas
}

# Variáveis de estado do jogo
estado_jogo = {
    "saude_jogador": 100,
    "saude_inimigo": 100,
    "mana_jogador": 100,
    "mana_inimigo": 100,
    "pontos_sabedoria": 0,
    "defendendo": False,
    "nivel_selecionado": "1° Ano",
    "disciplinas_selecionadas": list(perguntas_por_nivel_e_disciplina["1° Ano"].keys()),
    "batalha_ativa": True,
    "jogador_acao": "idle",
    "jogador_frame_atual": 0,
    "jogador_frame_tempo": 0,
    "inimigo_frame_atual": 0,
    "inimigo_frame_tempo": 0
}

# Função para desenhar HUD
def desenhar_hud():
    # Barra de saúde do jogador
    pygame.draw.rect(screen, COLORS["VERMELHO"], (20, 600, 200, 20))
    pygame.draw.rect(screen, COLORS["VERDE"], (20, 600, 2 * estado_jogo["saude_jogador"], 20))
    desenhar_texto(f"Jogador: {estado_jogo['saude_jogador']}/100", font, COLORS["BRANCO"], screen, 20, 570)

    # Barra de saúde do inimigo
    pygame.draw.rect(screen, COLORS["VERMELHO"], (1060, 600, 200, 20))
    pygame.draw.rect(screen, COLORS["VERDE"], (1060, 600, 2 * estado_jogo["saude_inimigo"], 20))
    desenhar_texto(f"Inimigo: {estado_jogo['saude_inimigo']}/100", font, COLORS["BRANCO"], screen, 1060, 570)

    # Barra de mana do jogador
    pygame.draw.rect(screen, COLORS["CINZA"], (20, 660, 200, 20))
    pygame.draw.rect(screen, COLORS["AZUL"], (20, 660, 2 * estado_jogo["mana_jogador"], 20))
    desenhar_texto(f"Mana: {estado_jogo['mana_jogador']}/100", font, COLORS["BRANCO"], screen, 20, 630)

    # Barra de mana do inimigo
    pygame.draw.rect(screen, COLORS["CINZA"], (1060, 660, 200, 20))
    pygame.draw.rect(screen, COLORS["AZUL"], (1060, 660, 2 * estado_jogo["mana_inimigo"], 20))
    desenhar_texto(f"Mana: {estado_jogo['mana_inimigo']}/100", font, COLORS["BRANCO"], screen, 1060, 630)

    # Pontos de sabedoria
    desenhar_texto(f"Pontos de Sabedoria: {estado_jogo['pontos_sabedoria']}", font, COLORS["BRANCO"], screen, WIDTH - 320, 20)

# Função para desenhar personagens
def desenhar_personagens(dano_jogador=False, dano_inimigo=False, derrota_jogador=False, derrota_inimigo=False):
    jogador_pos = (100, 300)
    inimigo_pos = (980, 300)

    # Animação do jogador
    if derrota_jogador:
        frames = jogador_animacoes["derrota"]
        frame_delay = 200
    elif estado_jogo["jogador_acao"] == "idle":
        frames = jogador_animacoes["idle"]
        frame_delay = 300
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
    else:
        frames = inimigo_animacoes["idle"]
        frame_delay = 300

    screen.blit(frames[estado_jogo["inimigo_frame_atual"]], inimigo_pos)
    estado_jogo["inimigo_frame_tempo"] += 1
    if estado_jogo["inimigo_frame_tempo"] >= frame_delay:
        estado_jogo["inimigo_frame_tempo"] = 0
        estado_jogo["inimigo_frame_atual"] = (estado_jogo["inimigo_frame_atual"] + 1) % len(frames)

# Função para desenhar barra de tempo
def desenhar_barra_tempo(tempo_restante, tempo_total):
    largura_barra = int((tempo_restante / tempo_total) * 400)
    pygame.draw.rect(screen, COLORS["AZUL"], (440, 80, largura_barra, 20))

# Função para selecionar nível e disciplina
def selecionar_nivel_e_disciplina():
    screen.blit(background_menu_img, (0, 0))
    desenhar_texto("Selecione o Nível:", font, COLORS["BRANCO"], screen, 20, 20)
    niveis = ["1° Ano", "2° Ano", "3° Ano", "4° Ano", "5° Ano", "6° Ano", "7° Ano", "8° Ano", "9° Ano"]
    retangulos_niveis = [desenhar_texto(f"{i+1}. {nivel}", font, COLORS["BRANCO"], screen, 20, 60 + i * 40) for i, nivel in enumerate(niveis)]
    ret_voltar_nivel = desenhar_texto("Voltar ao Início", font, COLORS["BRANCO"], screen, WIDTH - 200, HEIGHT - 50)
    pygame.display.flip()

    opcao_selecionada = 0
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % (len(retangulos_niveis) + 1)
                elif evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % (len(retangulos_niveis) + 1)
                elif evento.key == pygame.K_RETURN:
                    if opcao_selecionada < len(niveis):
                        estado_jogo["nivel_selecionado"] = niveis[opcao_selecionada]
                        estado_jogo["disciplinas_selecionadas"] = list(perguntas_por_nivel_e_disciplina[estado_jogo["nivel_selecionado"]].keys())
                        selecionar_disciplina()
                        return
                    else:
                        tela_inicial()
                        return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if ret_voltar_nivel.collidepoint(evento.pos):
                    tela_inicial()
                    return
                for i, ret in enumerate(retangulos_niveis):
                    if ret.collidepoint(evento.pos):
                        estado_jogo["nivel_selecionado"] = niveis[i]
                        estado_jogo["disciplinas_selecionadas"] = list(perguntas_por_nivel_e_disciplina[estado_jogo["nivel_selecionado"]].keys())
                        selecionar_disciplina()
                        return
            for i, ret in enumerate(retangulos_niveis):
                if ret.collidepoint(mouse_pos):
                    opcao_selecionada = i
            if ret_voltar_nivel.collidepoint(mouse_pos):
                opcao_selecionada = len(niveis)
        screen.blit(background_menu_img, (0, 0))
        desenhar_texto("Selecione o Nível:", font, COLORS["BRANCO"], screen, 20, 20)
        for i, nivel in enumerate(niveis):
            cor = COLORS["PRETO"] if i == opcao_selecionada else COLORS["BRANCO"]
            if i == opcao_selecionada:
                pygame.draw.rect(screen, COLORS["AMARELO"], retangulos_niveis[i])
            desenhar_texto(f"{i+1}. {nivel}", font, cor, screen, 20, 60 + i * 40)
        cor = COLORS["PRETO"] if opcao_selecionada == len(niveis) else COLORS["BRANCO"]
        if opcao_selecionada == len(niveis):
            pygame.draw.rect(screen, COLORS["AMARELO"], ret_voltar_nivel)
        desenhar_texto("Voltar ao Início", font, cor, screen, WIDTH - 200, HEIGHT - 50)
        pygame.display.flip()

def selecionar_disciplina():
    screen.blit(background_menu_img, (0, 0))
    desenhar_texto("Selecione a Disciplina:", font, COLORS["BRANCO"], screen, 20, 20)
    disciplinas = ["Todas as Disciplinas"] + list(perguntas_por_nivel_e_disciplina[estado_jogo["nivel_selecionado"]].keys())
    retangulos_disciplinas = [desenhar_texto(f"{i+1}. {disciplina}", font, COLORS["BRANCO"], screen, 20, 60 + i * 40) for i, disciplina in enumerate(disciplinas)]
    ret_voltar_disciplina = desenhar_texto("Voltar ao Nível", font, COLORS["BRANCO"], screen, WIDTH - 200, HEIGHT - 50)
    pygame.display.flip()

    opcao_selecionada = 0
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % (len(retangulos_disciplinas) + 1)
                elif evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % (len(retangulos_disciplinas) + 1)
                elif evento.key == pygame.K_RETURN:
                    if opcao_selecionada < len(disciplinas) - 1:
                        estado_jogo["disciplinas_selecionadas"] = [disciplinas[opcao_selecionada]]
                    elif opcao_selecionada == 0:
                        estado_jogo["disciplinas_selecionadas"] = list(perguntas_por_nivel_e_disciplina[estado_jogo["nivel_selecionado"]].keys())
                    else:
                        selecionar_nivel_e_disciplina()
                        return
                    return
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if ret_voltar_disciplina.collidepoint(evento.pos):
                    selecionar_nivel_e_disciplina()
                    return
                for i, ret in enumerate(retangulos_disciplinas):
                    if ret.collidepoint(evento.pos):
                        if i == 0:
                            estado_jogo["disciplinas_selecionadas"] = list(perguntas_por_nivel_e_disciplina[estado_jogo["nivel_selecionado"]].keys())
                        else:
                            estado_jogo["disciplinas_selecionadas"] = [disciplinas[i]]
                        return
            for i, ret in enumerate(retangulos_disciplinas):
                if ret.collidepoint(mouse_pos):
                    opcao_selecionada = i
            if ret_voltar_disciplina.collidepoint(mouse_pos):
                opcao_selecionada = len(disciplinas)
        screen.blit(background_menu_img, (0, 0))
        desenhar_texto("Selecione a Disciplina:", font, COLORS["BRANCO"], screen, 20, 20)
        for i, disciplina in enumerate(disciplinas):
            cor = COLORS["PRETO"] if i == opcao_selecionada else COLORS["BRANCO"]
            if i == opcao_selecionada:
                pygame.draw.rect(screen, COLORS["AMARELO"], retangulos_disciplinas[i])
            desenhar_texto(f"{i+1}. {disciplina}", font, cor, screen, 20, 60 + i * 40)
        cor = COLORS["PRETO"] if opcao_selecionada == len(disciplinas) else COLORS["BRANCO"]
        if opcao_selecionada == len(disciplinas):
            pygame.draw.rect(screen, COLORS["AMARELO"], ret_voltar_disciplina)
        desenhar_texto("Voltar ao Nível", font, cor, screen, WIDTH - 200, HEIGHT - 50)
        pygame.display.flip()

# Função para selecionar ação
def selecionar_acao():
    screen.blit(background_batalha_img, (0, 0))
    desenhar_hud()
    desenhar_personagens()
    desenhar_texto("Escolha sua ação:", font, COLORS["BRANCO"], screen, 20, 20)
    acoes = ["Ataque", "Magia", "Defesa", "Curar", "Fugir"]
    retangulos_acoes = [desenhar_texto(acao, font, COLORS["BRANCO"], screen, 20, 60 + i * 40) for i, acao in enumerate(acoes)]
    pygame.display.flip()

    acao_selecionada = None
    opcao_selecionada = 0

    while acao_selecionada is None:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % len(retangulos_acoes)
                elif evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % len(retangulos_acoes)
                elif evento.key == pygame.K_RETURN:
                    acao_selecionada = acoes[opcao_selecionada]
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, ret in enumerate(retangulos_acoes):
                    if ret.collidepoint(evento.pos):
                        acao_selecionada = acoes[i]
            for i, ret in enumerate(retangulos_acoes):
                if ret.collidepoint(mouse_pos):
                    opcao_selecionada = i

        screen.blit(background_batalha_img, (0, 0))
        desenhar_hud()
        desenhar_personagens()
        desenhar_texto("Escolha sua ação:", font, COLORS["BRANCO"], screen, 20, 20)
        for i, (texto, ret) in enumerate(zip(acoes, retangulos_acoes)):
            cor = COLORS["PRETO"] if i == opcao_selecionada else COLORS["BRANCO"]
            if i == opcao_selecionada:
                pygame.draw.rect(screen, COLORS["AMARELO"], ret)
            desenhar_texto(texto, font, cor, screen, 20, 60 + i * 40)
        pygame.display.flip()

    return acao_selecionada

# Função para apresentar pergunta
def apresentar_pergunta(perguntas, tempo_total):
    pergunta = random.choice(perguntas)
    screen.blit(background_batalha_img, (0, 0))
    desenhar_hud()
    desenhar_personagens()
    desenhar_texto(pergunta["pergunta"], font, COLORS["BRANCO"], screen, 20, 20)
    desenhar_barra_tempo(tempo_total, tempo_total)

    opcoes_rects = []
    for i, opcao in enumerate(pergunta["opcoes"]):
        ret_opcao = desenhar_texto(opcao, font, COLORS["BRANCO"], screen, 20, 120 + i * 30)  # Ajuste a distância entre as opções
        opcoes_rects.append(pygame.Rect(20, 120 + i * 30, WIDTH - 30, 30))  # Aumente a altura da área clicável

    pygame.display.flip()
    return pergunta, opcoes_rects


# Função para avaliar resposta
def avaliar_resposta(pergunta, opcoes_rects, tempo_total):
    tempo_inicio = pygame.time.get_ticks()
    opcao_selecionada = None
    indice_opcao_selecionada = 0

    while opcao_selecionada is None:
        tempo_atual = pygame.time.get_ticks()
        tempo_passado = (tempo_atual - tempo_inicio) / 1000
        tempo_restante = tempo_total - tempo_passado

        if tempo_restante <= 0:
            break

        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    indice_opcao_selecionada = (indice_opcao_selecionada + 1) % len(opcoes_rects)
                elif evento.key == pygame.K_UP:
                    indice_opcao_selecionada = (indice_opcao_selecionada - 1) % len(opcoes_rects)
                elif evento.key == pygame.K_RETURN:
                    opcao_selecionada = indice_opcao_selecionada
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(opcoes_rects):
                    if rect.collidepoint(evento.pos):
                        opcao_selecionada = i
            for i, rect in enumerate(opcoes_rects):
                if rect.collidepoint(mouse_pos):
                    indice_opcao_selecionada = i

        # Atualizar cronômetro na tela
        screen.blit(background_batalha_img, (0, 0))
        desenhar_hud()
        desenhar_personagens()
        desenhar_texto(pergunta["pergunta"], font, COLORS["BRANCO"], screen, 20, 20)
        for i, opcao in enumerate(pergunta["opcoes"]):
            cor = COLORS["PRETO"] if i == indice_opcao_selecionada else COLORS["BRANCO"]
            if i == indice_opcao_selecionada:
                pygame.draw.rect(screen, COLORS["CINZA_CLARO"], opcoes_rects[i])
            desenhar_texto(opcao, font, cor, screen, 20, 120 + i * 30)
        desenhar_barra_tempo(tempo_restante, tempo_total)
        pygame.display.flip()

    tempo_total_resposta = (pygame.time.get_ticks() - tempo_inicio) / 1000

    resposta_correta = opcao_selecionada == pergunta["resposta"]

    return resposta_correta, tempo_total_resposta

# Função para executar ação
def executar_acao(acao, resposta_correta, tempo_resposta):
    global estado_jogo
    dano = 0
    mensagem = ""
    dano_inimigo = False
    cura = 0

    if acao == "Fugir":
        estado_jogo["batalha_ativa"] = False
        mensagem = "Você fugiu da batalha!"
    else:
        if resposta_correta:
            if acao == "Ataque":
                dano = 20 if tempo_resposta <= 5 else 10
                estado_jogo["jogador_acao"] = "attack"
            elif acao == "Magia" and estado_jogo["mana_jogador"] >= 10:
                estado_jogo["mana_jogador"] -= 10
                dano = 25 if tempo_resposta <= 5 else 15
            elif acao == "Defesa":
                estado_jogo["defendendo"] = True
                mensagem = "Você se preparou para a defesa!"
            elif acao == "Curar" and estado_jogo["mana_jogador"] >= 15:
                estado_jogo["mana_jogador"] -= 15
                cura = 20 if tempo_resposta <= 5 else 10
                estado_jogo["saude_jogador"] = min(estado_jogo["saude_jogador"] + cura, 100)
                mensagem = f"Você se curou em {cura} pontos!"
            estado_jogo["pontos_sabedoria"] += 10
        else:
            mensagem = "Resposta errada! Nenhum dano causado!" if acao != "Defesa" else "A defesa falhou!"
            estado_jogo["defendendo"] = False

        if acao == "Ataque":
            for frame in jogador_animacoes["attack"]:
                screen.blit(background_batalha_img, (0, 0))
                desenhar_hud()
                screen.blit(frame, (100, 300))
                pygame.display.flip()
                pygame.time.delay(150)

        estado_jogo["saude_inimigo"] -= dano
        mensagem = f"Você causou {dano} de dano!" if dano > 0 else mensagem
        dano_inimigo = dano > 0

        screen.blit(background_batalha_img, (0, 0))
        desenhar_hud()
        desenhar_personagens(dano_inimigo=dano_inimigo)
        desenhar_texto(mensagem, font, COLORS["BRANCO"], screen, 20, 20)
        desenhar_texto(f"Tempo de resposta: {tempo_resposta:.2f} segundos", font, COLORS["BRANCO"], screen, 20, 60)
        pygame.display.flip()
        pygame.time.delay(3000)

# Função para turno do inimigo
def turno_inimigo():
    global estado_jogo
    dano = random.randint(5, 15)
    tipo_acao = random.choice(["Ataque", "Magia", "Defesa"])
    dano_jogador = False
    mensagem = ""

    if tipo_acao == "Magia" and estado_jogo["mana_inimigo"] >= 10:
        estado_jogo["mana_inimigo"] -= 10
        dano += 5
    elif tipo_acao == "Defesa":
        estado_jogo["defendendo"] = True
        mensagem = "O inimigo se preparou para a defesa!"
        dano = 0
    else:
        if estado_jogo["defendendo"]:
            dano //= 2
            estado_jogo["defendendo"] = False
            mensagem = "Defesa bem-sucedida! Dano reduzido!"

    estado_jogo["saude_jogador"] -= dano
    dano_jogador = dano > 0

    screen.blit(background_batalha_img, (0, 0))
    desenhar_hud()
    desenhar_personagens(dano_jogador=dano_jogador)
    desenhar_texto(f"O inimigo causou {dano} de dano!", font, COLORS["BRANCO"], screen, 20, 20)
    desenhar_texto(mensagem, font, COLORS["BRANCO"], screen, 20, 60)
    pygame.display.flip()
    pygame.time.delay(2000)

# Função para checar fim da batalha
def checar_fim_batalha():
    if estado_jogo["saude_jogador"] <= 0:
        return "Derrota"
    elif estado_jogo["saude_inimigo"] <= 0:
        return "Vitória"
    return None

# Função principal da batalha
def batalha():
    estado_jogo.update({
        "saude_jogador": 100, "saude_inimigo": 100, "mana_jogador": 100, "mana_inimigo": 100, "pontos_sabedoria": 0
    })

    tocar_musica(MUSICAS["batalha"])

    perguntas = []
    for disciplina in estado_jogo["disciplinas_selecionadas"]:
        perguntas.extend(perguntas_por_nivel_e_disciplina[estado_jogo["nivel_selecionado"]][disciplina])

    screen.blit(background_batalha_img, (0, 0))
    desenhar_texto(f"Nível: {estado_jogo['nivel_selecionado']}", font, COLORS["BRANCO"], screen, 20, 20)
    desenhar_texto(f"Disciplinas: {', '.join(estado_jogo['disciplinas_selecionadas'])}", font, COLORS["BRANCO"], screen, 20, 60)
    pygame.display.flip()
    pygame.time.delay(2000)

    estado_jogo["batalha_ativa"] = True
    tempo_total_pergunta = 10
    while estado_jogo["batalha_ativa"]:
        acao = selecionar_acao()
        if acao == "Fugir":
            executar_acao(acao, False, 0)
            tela_inicial()
            break
        pergunta, opcoes_rects = apresentar_pergunta(perguntas, tempo_total_pergunta)
        resposta_correta, tempo_resposta = avaliar_resposta(pergunta, opcoes_rects, tempo_total_pergunta)
        executar_acao(acao, resposta_correta, tempo_resposta)
        resultado = checar_fim_batalha()
        if resultado:
            estado_jogo["batalha_ativa"] = False
            parar_musica()
            tocar_som(MUSICAS["vitoria"] if resultado == "Vitória" else MUSICAS["derrota"])
            screen.blit(background_batalha_img, (0, 0))
            desenhar_hud()
            desenhar_personagens(derrota_jogador=(resultado=="Derrota"), derrota_inimigo=(resultado=="Vitória"))
            desenhar_texto(resultado, font, COLORS["BRANCO"], screen, WIDTH // 2 - 50, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(3000)
            tela_inicial()
        else:
            turno_inimigo()
            resultado = checar_fim_batalha()
            if resultado:
                estado_jogo["batalha_ativa"] = False
                parar_musica()
                tocar_som(MUSICAS["vitoria"] if resultado == "Vitória" else MUSICAS["derrota"])
                screen.blit(background_batalha_img, (0, 0))
                desenhar_hud()
                desenhar_personagens(derrota_jogador=(resultado=="Derrota"), derrota_inimigo=(resultado=="Vitória"))
                desenhar_texto(resultado, font, COLORS["BRANCO"], screen, WIDTH // 2 - 50, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(3000)
                tela_inicial()

# Função para exibir a tela inicial
def tela_inicial():
    tocar_musica(MUSICAS["menu"])
    screen.blit(background_menu_img, (0, 0))
    desenhar_texto("A Saga do Conhecimento", font, COLORS["BRANCO"], screen, WIDTH // 2 - 150, HEIGHT // 2 - 100)
    opcoes_menu = ["Jogar", "Tela Cheia", "Opções", "Sair"]
    retangulos_menu = [desenhar_texto(opcao, font, COLORS["BRANCO"], screen, WIDTH // 2 - 50, HEIGHT // 2 + i * 50) for i, opcao in enumerate(opcoes_menu)]
    pygame.display.flip()

    jogando = False
    opcao_selecionada = 0

    while not jogando:
        mouse_pos = pygame.mouse.get_pos()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_DOWN:
                    opcao_selecionada = (opcao_selecionada + 1) % len(retangulos_menu)
                elif evento.key == pygame.K_UP:
                    opcao_selecionada = (opcao_selecionada - 1) % len(retangulos_menu)
                elif evento.key == pygame.K_RETURN:
                    if opcao_selecionada == 0:
                        jogando = True
                        batalha()
                    elif opcao_selecionada == 1:
                        definir_modo_jogo(True)
                        tela_inicial()
                    elif opcao_selecionada == 2:
                        selecionar_nivel_e_disciplina()
                    elif opcao_selecionada == 3:
                        pygame.quit()
                        exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, ret in enumerate(retangulos_menu):
                    if ret.collidepoint(evento.pos):
                        if i == 0:
                            jogando = True
                            batalha()
                        elif i == 1:
                            definir_modo_jogo(True)
                            tela_inicial()
                        elif i == 2:
                            selecionar_nivel_e_disciplina()
                        elif i == 3:
                            pygame.quit()
                            exit()
            for i, ret in enumerate(retangulos_menu):
                if ret.collidepoint(mouse_pos):
                    opcao_selecionada = i
        screen.blit(background_menu_img, (0, 0))
        desenhar_texto("A Saga do Conhecimento", font, COLORS["BRANCO"], screen, WIDTH // 2 - 150, HEIGHT // 2 - 100)
        for i, opcao in enumerate(opcoes_menu):
            cor = COLORS["PRETO"] if i == opcao_selecionada else COLORS["BRANCO"]
            if i == opcao_selecionada:
                pygame.draw.rect(screen, COLORS["AMARELO"], ret)
            desenhar_texto(opcao, font, cor, screen, WIDTH // 2 - 50, HEIGHT // 2 + i * 50)
        pygame.display.flip()

# Função para definir o modo de jogo
def definir_modo_jogo(tela_cheia):
    global screen, background_batalha_img, background_menu_img
    if tela_cheia:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background_batalha_img = carregar_imagem("background_batalha.png", WIDTH, HEIGHT)
    background_menu_img = carregar_imagem("background_menu.png", WIDTH, HEIGHT)

# Iniciar a tela inicial
tela_inicial()
pygame.quit()
