import pygame
import random

# Inicialização da Pygame
pygame.init()
pygame.mixer.init()

# Configurações da tela
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Saga do Conhecimento - Batalha")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
CINZA = (169, 169, 169)

# Fonte
font = pygame.font.Font(None, 36)

# Carregar e redimensionar imagens
jogador_img = pygame.image.load("jogador.png").convert_alpha()
inimigo_img = pygame.image.load("inimigo.png").convert_alpha()
background_batalha_img = pygame.image.load("background_batalha.png").convert_alpha()
background_menu_img = pygame.image.load("background_menu.png").convert_alpha()
jogador_img = pygame.transform.scale(jogador_img, (200, 200))
inimigo_img = pygame.transform.scale(inimigo_img, (200, 200))
background_batalha_img = pygame.transform.scale(background_batalha_img, (WIDTH, HEIGHT))
background_menu_img = pygame.transform.scale(background_menu_img, (WIDTH, HEIGHT))

# Carregar músicas e sons
musica_menu = "musica_menu.mp3"
musica_batalha = "musica_batalha.mp3"
som_vitoria = "som_vitoria.mp3"
som_derrota = "som_derrota.mp3"

# Função para tocar música de fundo
def tocar_musica(musica):
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play(-1)  # Loop infinito

# Função para parar música
def parar_musica():
    pygame.mixer.music.stop()

# Função para tocar som de vitória ou derrota
def tocar_som(som):
    efeito = pygame.mixer.Sound(som)
    efeito.play()

# Função para desenhar texto na tela
def desenhar_texto(texto, fonte, cor, superficie, x, y):
    objeto_texto = fonte.render(texto, True, cor)
    retangulo_texto = objeto_texto.get_rect(topleft=(x, y))
    superficie.blit(objeto_texto, retangulo_texto)
    return retangulo_texto  # Retornar o retângulo para detecção de clique

# Perguntas organizadas por nível e disciplina
perguntas_por_nivel_e_disciplina = {
    "1° Ano": {
        "Matemática": [
            {"pergunta": "Quanto é 2 + 2?", "opcoes": ["3", "4", "5", "6"], "resposta": 1},
            {"pergunta": "Quanto é 3 + 3?", "opcoes": ["5", "6", "7", "8"], "resposta": 1},
            {"pergunta": "Quanto é 1 + 1?", "opcoes": ["1", "2", "3", "4"], "resposta": 1},
            {"pergunta": "Quanto é 4 - 2?", "opcoes": ["1", "2", "3", "4"], "resposta": 1},
            {"pergunta": "Quanto é 5 - 3?", "opcoes": ["1", "2", "3", "4"], "resposta": 1},
            {"pergunta": "Quanto é 7 + 1?", "opcoes": ["7", "8", "9", "10"], "resposta": 1},
            {"pergunta": "Quanto é 6 - 4?", "opcoes": ["1", "2", "3", "4"], "resposta": 1},
            {"pergunta": "Quanto é 3 + 2?", "opcoes": ["4", "5", "6", "7"], "resposta": 1},
            {"pergunta": "Quanto é 9 - 1?", "opcoes": ["7", "8", "9", "10"], "resposta": 1},
            {"pergunta": "Quanto é 10 - 5?", "opcoes": ["4", "5", "6", "7"], "resposta": 1},
        ],
        "Língua Portuguesa": [
            {"pergunta": "Qual é a letra inicial da palavra 'gato'?", "opcoes": ["A", "B", "G", "D"], "resposta": 2},
            {"pergunta": "Qual é a letra inicial da palavra 'casa'?", "opcoes": ["C", "B", "G", "D"], "resposta": 0},
            {"pergunta": "Qual é a letra inicial da palavra 'banana'?", "opcoes": ["A", "B", "G", "D"], "resposta": 1},
            {"pergunta": "Qual é a letra inicial da palavra 'dado'?", "opcoes": ["A", "B", "G", "D"], "resposta": 3},
            {"pergunta": "Qual é a letra inicial da palavra 'elefante'?", "opcoes": ["E", "B", "G", "D"], "resposta": 0},
            {"pergunta": "Qual é a letra inicial da palavra 'foca'?", "opcoes": ["A", "F", "G", "D"], "resposta": 1},
            {"pergunta": "Qual é a letra inicial da palavra 'girafa'?", "opcoes": ["A", "B", "G", "D"], "resposta": 2},
            {"pergunta": "Qual é a letra inicial da palavra 'hipopótamo'?", "opcoes": ["H", "B", "G", "D"], "resposta": 0},
            {"pergunta": "Qual é a letra inicial da palavra 'iguana'?", "opcoes": ["I", "B", "G", "D"], "resposta": 0},
            {"pergunta": "Qual é a letra inicial da palavra 'jacaré'?", "opcoes": ["J", "B", "G", "D"], "resposta": 0},
        ],
        # Adicione outras disciplinas
    },
    "2° Ano": {
        # Adicione perguntas para o 2° Ano
    },
    # Adicione outros níveis até o 9° Ano
}

# Variáveis de estado do jogo
saude_jogador = 100
saude_inimigo = 100
mana_jogador = 100
mana_inimigo = 100
pontos_sabedoria = 0
defendendo = False
nivel_selecionado = "1° Ano"
disciplinas_selecionadas = list(perguntas_por_nivel_e_disciplina[nivel_selecionado].keys())
batalha_ativa = True

# Estrutura básica de quests
quests = {
    "Quest 1": {
        "descrição": "Recupere o tomo perdido na floresta",
        "completada": False
    },
    "Quest 2": {
        "descrição": "Resolva o enigma da caverna",
        "completada": False
    }
}

# Função para desenhar HUD
def desenhar_hud():
    # Barra de saúde do jogador
    pygame.draw.rect(screen, VERMELHO, (20, 600, 200, 20))
    pygame.draw.rect(screen, VERDE, (20, 600, 2 * saude_jogador, 20))
    desenhar_texto(f"Jogador: {saude_jogador}/100", font, BRANCO, screen, 20, 570)

    # Barra de saúde do inimigo
    pygame.draw.rect(screen, VERMELHO, (1060, 600, 200, 20))
    pygame.draw.rect(screen, VERDE, (1060, 600, 2 * saude_inimigo, 20))
    desenhar_texto(f"Inimigo: {saude_inimigo}/100", font, BRANCO, screen, 1060, 570)

    # Barra de mana do jogador
    pygame.draw.rect(screen, CINZA, (20, 660, 200, 20))
    pygame.draw.rect(screen, AZUL, (20, 660, 2 * mana_jogador, 20))
    desenhar_texto(f"Mana: {mana_jogador}/100", font, BRANCO, screen, 20, 630)

    # Barra de mana do inimigo
    pygame.draw.rect(screen, CINZA, (1060, 660, 200, 20))
    pygame.draw.rect(screen, AZUL, (1060, 660, 2 * mana_inimigo, 20))
    desenhar_texto(f"Mana: {mana_inimigo}/100", font, BRANCO, screen, 1060, 630)

    # Pontos de sabedoria
    desenhar_texto(f"Pontos de Sabedoria: {pontos_sabedoria}", font, BRANCO, screen, 540, 20)

# Função para desenhar personagens
def desenhar_personagens(dano_jogador=False, dano_inimigo=False):
    if dano_jogador:
        for _ in range(3):  # Piscar 3 vezes
            screen.blit(jogador_img, (100, 250))
            pygame.display.flip()
            pygame.time.delay(100)
            jogador_img_mod = jogador_img.copy()
            jogador_img_mod.fill((255, 0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(jogador_img_mod, (100, 250))
            pygame.display.flip()
            pygame.time.delay(100)
    else:
        screen.blit(jogador_img, (100, 250))

    if dano_inimigo:
        for _ in range(3):  # Piscar 3 vezes
            screen.blit(inimigo_img, (980, 250))
            pygame.display.flip()
            pygame.time.delay(100)
            inimigo_img_mod = inimigo_img.copy()
            inimigo_img_mod.fill((255, 0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(inimigo_img_mod, (980, 250))
            pygame.display.flip()
            pygame.time.delay(100)
    else:
        screen.blit(inimigo_img, (980, 250))

# Função para desenhar barra de tempo
def desenhar_barra_tempo(tempo_restante, tempo_total):
    largura_barra = int((tempo_restante / tempo_total) * 400)
    pygame.draw.rect(screen, AZUL, (440, 80, largura_barra, 20))

# Função para selecionar nível e disciplina
def selecionar_nivel_e_disciplina():
    global nivel_selecionado, disciplinas_selecionadas
    screen.blit(background_menu_img, (0, 0))
    desenhar_texto("Selecione o Nível:", font, BRANCO, screen, 20, 20)
    niveis = ["1° Ano", "2° Ano", "3° Ano", "4° Ano", "5° Ano", "6° Ano", "7° Ano", "8° Ano", "9° Ano"]
    retangulos_niveis = []
    for i, nivel in enumerate(niveis):
        retangulo = desenhar_texto(f"{i+1}. {nivel}", font, BRANCO, screen, 20, 60 + i * 40)
        retangulos_niveis.append(retangulo)
    ret_voltar_nivel = desenhar_texto("Voltar ao Início", font, BRANCO, screen, WIDTH - 200, HEIGHT - 50)
    pygame.display.flip()

    opcao_selecionada = 0
    while True:
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
                        nivel_selecionado = niveis[opcao_selecionada]
                        disciplinas_selecionadas = list(perguntas_por_nivel_e_disciplina[nivel_selecionado].keys())
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
                        nivel_selecionado = niveis[i]
                        disciplinas_selecionadas = list(perguntas_por_nivel_e_disciplina[nivel_selecionado].keys())
                        selecionar_disciplina()
                        return
        screen.blit(background_menu_img, (0, 0))
        desenhar_texto("Selecione o Nível:", font, BRANCO, screen, 20, 20)
        for i, nivel in enumerate(niveis):
            cor = VERDE if i == opcao_selecionada else BRANCO
            desenhar_texto(f"{i+1}. {nivel}", font, cor, screen, 20, 60 + i * 40)
        cor = VERDE if opcao_selecionada == len(niveis) else BRANCO
        desenhar_texto("Voltar ao Início", font, cor, screen, WIDTH - 200, HEIGHT - 50)
        pygame.display.flip()

def selecionar_disciplina():
    global disciplinas_selecionadas
    screen.blit(background_menu_img, (0, 0))
    desenhar_texto("Selecione a Disciplina:", font, BRANCO, screen, 20, 20)
    disciplinas = ["Todas as Disciplinas"] + list(perguntas_por_nivel_e_disciplina[nivel_selecionado].keys())
    retangulos_disciplinas = []
    for i, disciplina in enumerate(disciplinas):
        retangulo = desenhar_texto(f"{i+1}. {disciplina}", font, BRANCO, screen, 20, 60 + i * 40)
        retangulos_disciplinas.append(retangulo)
    ret_voltar_disciplina = desenhar_texto("Voltar ao Nível", font, BRANCO, screen, WIDTH - 200, HEIGHT - 50)
    pygame.display.flip()

    opcao_selecionada = 0
    while True:
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
                        disciplinas_selecionadas = [disciplinas[opcao_selecionada]]
                    elif opcao_selecionada == 0:
                        disciplinas_selecionadas = list(perguntas_por_nivel_e_disciplina[nivel_selecionado].keys())
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
                            disciplinas_selecionadas = list(perguntas_por_nivel_e_disciplina[nivel_selecionado].keys())
                        else:
                            disciplinas_selecionadas = [disciplinas[i]]
                        return
        screen.blit(background_menu_img, (0, 0))
        desenhar_texto("Selecione a Disciplina:", font, BRANCO, screen, 20, 20)
        for i, disciplina in enumerate(disciplinas):
            cor = VERDE if i == opcao_selecionada else BRANCO
            desenhar_texto(f"{i+1}. {disciplina}", font, cor, screen, 20, 60 + i * 40)
        cor = VERDE if opcao_selecionada == len(disciplinas) else BRANCO
        desenhar_texto("Voltar ao Nível", font, cor, screen, WIDTH - 200, HEIGHT - 50)
        pygame.display.flip()

# Função para selecionar ação
def selecionar_acao():
    screen.blit(background_batalha_img, (0, 0))
    desenhar_hud()
    desenhar_personagens()
    desenhar_texto("Escolha sua ação:", font, BRANCO, screen, 20, 20)
    ret_ataque = desenhar_texto("Ataque", font, BRANCO, screen, 20, 60)
    ret_magia = desenhar_texto("Magia", font, BRANCO, screen, 20, 100)
    ret_defesa = desenhar_texto("Defesa", font, BRANCO, screen, 20, 140)
    ret_fugir = desenhar_texto("Fugir", font, BRANCO, screen, 20, 180)
    pygame.display.flip()

    acao_selecionada = None
    opcao_selecionada = 0
    retangulos_acoes = [ret_ataque, ret_magia, ret_defesa, ret_fugir]

    while acao_selecionada is None:
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
                    acao_selecionada = ["Ataque", "Magia", "Defesa", "Fugir"][opcao_selecionada]
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, ret in enumerate(retangulos_acoes):
                    if ret.collidepoint(evento.pos):
                        acao_selecionada = ["Ataque", "Magia", "Defesa", "Fugir"][i]

        screen.blit(background_batalha_img, (0, 0))
        desenhar_hud()
        desenhar_personagens()
        desenhar_texto("Escolha sua ação:", font, BRANCO, screen, 20, 20)
        for i, (texto, ret) in enumerate(zip(["Ataque", "Magia", "Defesa", "Fugir"], retangulos_acoes)):
            cor = VERDE if i == opcao_selecionada else BRANCO
            desenhar_texto(texto, font, cor, screen, 20, 60 + i * 40)
        pygame.display.flip()

    return acao_selecionada

# Função para apresentar pergunta
def apresentar_pergunta(perguntas, tempo_total):
    pergunta = random.choice(perguntas)
    screen.blit(background_batalha_img, (0, 0))
    desenhar_hud()
    desenhar_personagens()
    desenhar_texto(pergunta["pergunta"], font, BRANCO, screen, 20, 20)
    desenhar_barra_tempo(tempo_total, tempo_total)

    opcoes_rects = []
    for i, opcao in enumerate(pergunta["opcoes"]):
        ret_opcao = desenhar_texto(opcao, font, BRANCO, screen, 20, 120 + i * 40)
        opcoes_rects.append(ret_opcao)
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

        # Atualizar cronômetro na tela
        screen.blit(background_batalha_img, (0, 0))
        desenhar_hud()
        desenhar_personagens()
        desenhar_texto(pergunta["pergunta"], font, BRANCO, screen, 20, 20)
        for i, opcao in enumerate(pergunta["opcoes"]):
            cor = VERDE if i == indice_opcao_selecionada else BRANCO
            desenhar_texto(opcao, font, cor, screen, 20, 120 + i * 40)
        desenhar_barra_tempo(tempo_restante, tempo_total)
        pygame.display.flip()

    tempo_total_resposta = (pygame.time.get_ticks() - tempo_inicio) / 1000

    if opcao_selecionada == pergunta["resposta"]:
        resposta_correta = True
    else:
        resposta_correta = False

    return resposta_correta, tempo_total_resposta

# Função para executar ação
def executar_acao(acao, resposta_correta, tempo_resposta):
    global saude_inimigo, defendendo, mana_jogador, batalha_ativa, pontos_sabedoria
    dano = 0
    mensagem = ""
    dano_inimigo = False

    if acao == "Fugir":
        batalha_ativa = False
        mensagem = "Você fugiu da batalha!"
    else:
        if resposta_correta:
            if acao == "Ataque":
                if tempo_resposta <= 5:
                    dano = 20
                else:
                    dano = 10
            elif acao == "Magia":
                if mana_jogador >= 10:
                    mana_jogador -= 10
                    if tempo_resposta <= 5:
                        dano = 25
                    else:
                        dano = 15
                else:
                    mensagem = "Mana insuficiente!"
            elif acao == "Defesa":
                defendendo = True
                mensagem = "Você se preparou para a defesa!"
            pontos_sabedoria += 10
        else:
            if acao == "Defesa":
                defendendo = False
                mensagem = "A defesa falhou!"
            else:
                mensagem = "Resposta errada! Nenhum dano causado!"

        saude_inimigo -= dano
        mensagem = f"Você causou {dano} de dano!" if dano > 0 else mensagem
        dano_inimigo = True if dano > 0 else False

    screen.blit(background_batalha_img, (0, 0))
    desenhar_hud()
    desenhar_personagens(dano_inimigo=dano_inimigo)
    desenhar_texto(mensagem, font, BRANCO, screen, 20, 20)
    desenhar_texto(f"Tempo de resposta: {tempo_resposta:.2f} segundos", font, BRANCO, screen, 20, 60)
    pygame.display.flip()
    pygame.time.delay(3000)

# Função para turno do inimigo
def turno_inimigo():
    global saude_jogador, defendendo, mana_inimigo
    dano = random.randint(5, 15)
    tipo_acao = random.choice(["Ataque", "Magia", "Defesa"])
    dano_jogador = False
    mensagem = ""

    if tipo_acao == "Magia" and mana_inimigo >= 10:
        mana_inimigo -= 10
        dano += 5  # Magia causa mais dano
    elif tipo_acao == "Defesa":
        defendendo = True
        mensagem = "O inimigo se preparou para a defesa!"
        dano = 0  # Sem dano durante a defesa
    else:
        if defendendo:
            dano //= 2  # Reduzir dano pela metade se o jogador estiver defendendo
            defendendo = False  # Resetar estado de defesa após reduzir dano
            mensagem = "Defesa bem-sucedida! Dano reduzido!"
        else:
            mensagem = ""

    saude_jogador -= dano
    dano_jogador = True if dano > 0 else False

    screen.blit(background_batalha_img, (0, 0))
    desenhar_hud()
    desenhar_personagens(dano_jogador=dano_jogador)
    desenhar_texto(f"O inimigo causou {dano} de dano!", font, BRANCO, screen, 20, 20)
    desenhar_texto(mensagem, font, BRANCO, screen, 20, 60)
    pygame.display.flip()
    pygame.time.delay(2000)

# Função para checar fim da batalha
def checar_fim_batalha():
    if saude_jogador <= 0:
        return "Derrota"
    elif saude_inimigo <= 0:
        return "Vitória"
    return None

# Função para exibir a tela inicial
def tela_inicial():
    tocar_musica(musica_menu)
    screen.blit(background_menu_img, (0, 0))
    desenhar_texto("A Saga do Conhecimento", font, BRANCO, screen, WIDTH // 2 - 150, HEIGHT // 2 - 100)
    opcoes_menu = ["Jogar", "Tela Cheia", "Opções", "Sair"]
    retangulos_menu = []
    for i, opcao in enumerate(opcoes_menu):
        retangulo = desenhar_texto(opcao, font, BRANCO, screen, WIDTH // 2 - 50, HEIGHT // 2 + i * 50)
        retangulos_menu.append(retangulo)
    pygame.display.flip()

    jogando = False
    opcao_selecionada = 0

    while not jogando:
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
        screen.blit(background_menu_img, (0, 0))
        desenhar_texto("A Saga do Conhecimento", font, BRANCO, screen, WIDTH // 2 - 150, HEIGHT // 2 - 100)
        for i, opcao in enumerate(opcoes_menu):
            cor = VERDE if i == opcao_selecionada else BRANCO
            desenhar_texto(opcao, font, cor, screen, WIDTH // 2 - 50, HEIGHT // 2 + i * 50)
        pygame.display.flip()

# Função para definir o modo de jogo
def definir_modo_jogo(tela_cheia):
    global screen, background_batalha_img, background_menu_img
    if tela_cheia:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background_batalha_img = pygame.transform.scale(pygame.image.load("background_batalha.png").convert_alpha(), (WIDTH, HEIGHT))
    background_menu_img = pygame.transform.scale(pygame.image.load("background_menu.png").convert_alpha(), (WIDTH, HEIGHT))

# Função principal da batalha
def batalha():
    tocar_musica(musica_batalha)
    global saude_jogador, saude_inimigo, mana_jogador, mana_inimigo, pontos_sabedoria, nivel_selecionado, disciplinas_selecionadas, batalha_ativa

    perguntas = []
    for disciplina in disciplinas_selecionadas:
        perguntas.extend(perguntas_por_nivel_e_disciplina[nivel_selecionado][disciplina])

    screen.blit(background_batalha_img, (0, 0))
    desenhar_texto(f"Nível: {nivel_selecionado}", font, BRANCO, screen, 20, 20)
    desenhar_texto(f"Disciplinas: {', '.join(disciplinas_selecionadas)}", font, BRANCO, screen, 20, 60)
    pygame.display.flip()
    pygame.time.delay(2000)

    batalha_ativa = True
    tempo_total_pergunta = 10  # Tempo total para responder a pergunta em segundos
    while batalha_ativa:
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
            batalha_ativa = False
            parar_musica()
            tocar_som(som_vitoria if resultado == "Vitória" else som_derrota)
            screen.blit(background_batalha_img, (0, 0))
            desenhar_hud()
            desenhar_personagens()
            desenhar_texto(resultado, font, BRANCO, screen, WIDTH // 2 - 50, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(3000)
            tela_inicial()
        else:
            turno_inimigo()
            resultado = checar_fim_batalha()
            if resultado:
                batalha_ativa = False
                parar_musica()
                tocar_som(som_vitoria if resultado == "Vitória" else som_derrota)
                screen.blit(background_batalha_img, (0, 0))
                desenhar_hud()
                desenhar_personagens()
                desenhar_texto(resultado, font, BRANCO, screen, WIDTH // 2 - 50, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(3000)
                tela_inicial()

    # Resetar estados do jogador e inimigo
    saude_jogador = 100
    saude_inimigo = 100
    mana_jogador = 100
    mana_inimigo = 100
    pontos_sabedoria = 0
    nivel_selecionado = "1° Ano"
    disciplinas_selecionadas = list(perguntas_por_nivel_e_disciplina[nivel_selecionado].keys())

# Iniciar a tela inicial
tela_inicial()
pygame.quit()
