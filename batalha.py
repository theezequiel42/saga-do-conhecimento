import pygame
import random

# Inicialização da Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
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
background_img = pygame.image.load("background.png").convert_alpha()
jogador_img = pygame.transform.scale(jogador_img, (150, 150))
inimigo_img = pygame.transform.scale(inimigo_img, (150, 150))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

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

# Inicialização das variáveis globais
saude_jogador = 100
saude_inimigo = 100
mana_jogador = 100
mana_inimigo = 100
defendendo = False
nivel_selecionado = "1° Ano"
disciplinas_selecionadas = list(perguntas_por_nivel_e_disciplina[nivel_selecionado].keys())

# Função para desenhar barras de saúde e mana
def desenhar_barras_de_saude():
    # Barra de saúde do jogador
    pygame.draw.rect(screen, VERMELHO, (20, 460, 200, 20))
    pygame.draw.rect(screen, VERDE, (20, 460, 2 * saude_jogador, 20))
    desenhar_texto(f"Jogador: {saude_jogador}/100", font, BRANCO, screen, 20, 430)

    # Barra de saúde do inimigo
    pygame.draw.rect(screen, VERMELHO, (580, 460, 200, 20))
    pygame.draw.rect(screen, VERDE, (580, 460, 2 * saude_inimigo, 20))
    desenhar_texto(f"Inimigo: {saude_inimigo}/100", font, BRANCO, screen, 580, 430)

    # Barra de mana do jogador
    pygame.draw.rect(screen, CINZA, (20, 540, 200, 20))
    pygame.draw.rect(screen, AZUL, (20, 540, 2 * mana_jogador, 20))
    desenhar_texto(f"Mana: {mana_jogador}/100", font, BRANCO, screen, 20, 510)

    # Barra de mana do inimigo
    pygame.draw.rect(screen, CINZA, (580, 540, 200, 20))
    pygame.draw.rect(screen, AZUL, (580, 540, 2 * mana_inimigo, 20))
    desenhar_texto(f"Mana: {mana_inimigo}/100", font, BRANCO, screen, 580, 510)

# Função para desenhar personagens
def desenhar_personagens(dano_jogador=False, dano_inimigo=False):
    if dano_jogador:
        for _ in range(3):  # Piscar 3 vezes
            screen.blit(jogador_img, (50, 250))
            pygame.display.flip()
            pygame.time.delay(100)
            jogador_img_mod = jogador_img.copy()
            jogador_img_mod.fill((255, 0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(jogador_img_mod, (50, 250))
            pygame.display.flip()
            pygame.time.delay(100)
    else:
        screen.blit(jogador_img, (50, 250))

    if dano_inimigo:
        for _ in range(3):  # Piscar 3 vezes
            screen.blit(inimigo_img, (600, 250))
            pygame.display.flip()
            pygame.time.delay(100)
            inimigo_img_mod = inimigo_img.copy()
            inimigo_img_mod.fill((255, 0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(inimigo_img_mod, (600, 250))
            pygame.display.flip()
            pygame.time.delay(100)
    else:
        screen.blit(inimigo_img, (600, 250))

# Função para desenhar barra de tempo
def desenhar_barra_tempo(tempo_restante, tempo_total):
    largura_barra = int((tempo_restante / tempo_total) * 400)
    pygame.draw.rect(screen, AZUL, (200, 80, largura_barra, 20))

# Função para selecionar nível e disciplina
def selecionar_nivel_e_disciplina():
    global nivel_selecionado, disciplinas_selecionadas
    screen.blit(background_img, (0, 0))
    desenhar_texto("Selecione o Nível:", font, BRANCO, screen, 20, 20)
    niveis = ["1° Ano", "2° Ano", "3° Ano", "4° Ano", "5° Ano", "6° Ano", "7° Ano", "8° Ano", "9° Ano"]
    retangulos_niveis = []
    for i, nivel in enumerate(niveis):
        retangulo = desenhar_texto(f"{i+1}. {nivel}", font, BRANCO, screen, 20, 60 + i * 40)
        retangulos_niveis.append(retangulo)
    pygame.display.flip()

    nivel_selecionado = None
    while nivel_selecionado is None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, ret in enumerate(retangulos_niveis):
                    if ret.collidepoint(evento.pos):
                        nivel_selecionado = niveis[i]
    screen.blit(background_img, (0, 0))
    desenhar_texto("Selecione a Disciplina:", font, BRANCO, screen, 20, 20)
    disciplinas = ["Matemática", "Língua Portuguesa", "Ciências", "História", "Geografia", "Educação Física", "Inglês", "Arte"]
    retangulos_disciplinas = []
    for i, disciplina in enumerate(disciplinas):
        retangulo = desenhar_texto(f"{i+1}. {disciplina}", font, BRANCO, screen, 20, 60 + i * 40)
        retangulos_disciplinas.append(retangulo)
    ret_voltar = desenhar_texto("Voltar ao Início", font, BRANCO, screen, WIDTH - 200, HEIGHT - 50)
    pygame.display.flip()

    disciplinas_selecionadas = []
    while not disciplinas_selecionadas:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if ret_voltar.collidepoint(evento.pos):
                    tela_inicial()
                    return
                for i, ret in enumerate(retangulos_disciplinas):
                    if ret.collidepoint(evento.pos):
                        disciplinas_selecionadas.append(disciplinas[i])
    return nivel_selecionado, disciplinas_selecionadas

# Função para selecionar ação
def selecionar_acao():
    screen.blit(background_img, (0, 0))
    desenhar_barras_de_saude()
    desenhar_personagens()
    desenhar_texto("Escolha sua ação:", font, BRANCO, screen, 20, 20)
    ret_ataque = desenhar_texto("Pressione 1 para Ataque", font, BRANCO, screen, 20, 60)
    ret_magia = desenhar_texto("Pressione 2 para Magia", font, BRANCO, screen, 20, 100)
    ret_defesa = desenhar_texto("Pressione 3 para Defesa", font, BRANCO, screen, 20, 140)
    ret_fugir = desenhar_texto("Pressione 4 para Fugir", font, BRANCO, screen, 20, 180)
    pygame.display.flip()

    acao_selecionada = None
    while acao_selecionada is None:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    acao_selecionada = "Ataque"
                elif evento.key == pygame.K_2:
                    acao_selecionada = "Magia"
                elif evento.key == pygame.K_3:
                    acao_selecionada = "Defesa"
                elif evento.key == pygame.K_4:
                    acao_selecionada = "Fugir"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if ret_ataque.collidepoint(evento.pos):
                    acao_selecionada = "Ataque"
                elif ret_magia.collidepoint(evento.pos):
                    acao_selecionada = "Magia"
                elif ret_defesa.collidepoint(evento.pos):
                    acao_selecionada = "Defesa"
                elif ret_fugir.collidepoint(evento.pos):
                    acao_selecionada = "Fugir"
    return acao_selecionada

# Função para apresentar pergunta
def apresentar_pergunta(perguntas, tempo_total):
    pergunta = random.choice(perguntas)
    screen.blit(background_img, (0, 0))
    desenhar_barras_de_saude()
    desenhar_personagens()
    desenhar_texto(pergunta["pergunta"], font, BRANCO, screen, 20, 20)
    desenhar_barra_tempo(tempo_total, tempo_total)

    opcoes_rects = []
    for i, opcao in enumerate(pergunta["opcoes"]):
        ret_opcao = desenhar_texto(f"Pressione {i+1} para {opcao}", font, BRANCO, screen, 20, 120 + i * 40)
        opcoes_rects.append(ret_opcao)
    pygame.display.flip()
    return pergunta, opcoes_rects

# Função para avaliar resposta
def avaliar_resposta(pergunta, opcoes_rects, tempo_total):
    tempo_inicio = pygame.time.get_ticks()
    opcao_selecionada = None

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
                if evento.key == pygame.K_1:
                    opcao_selecionada = 0
                elif evento.key == pygame.K_2:
                    opcao_selecionada = 1
                elif evento.key == pygame.K_3:
                    opcao_selecionada = 2
                elif evento.key == pygame.K_4:
                    opcao_selecionada = 3
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(opcoes_rects):
                    if rect.collidepoint(evento.pos):
                        opcao_selecionada = i

        # Atualizar cronômetro na tela
        screen.blit(background_img, (0, 0))
        desenhar_barras_de_saude()
        desenhar_personagens()
        desenhar_texto(pergunta["pergunta"], font, BRANCO, screen, 20, 20)
        for i, opcao in enumerate(pergunta["opcoes"]):
            desenhar_texto(f"Pressione {i+1} para {opcao}", font, BRANCO, screen, 20, 120 + i * 40)
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
    global saude_inimigo, defendendo, mana_jogador, batalha_ativa
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
        else:
            if acao == "Defesa":
                defendendo = False
                mensagem = "A defesa falhou!"
            else:
                mensagem = "Resposta errada! Nenhum dano causado!"

        saude_inimigo -= dano
        mensagem = f"Você causou {dano} de dano!" if dano > 0 else mensagem
        dano_inimigo = True if dano > 0 else False

    screen.blit(background_img, (0, 0))
    desenhar_barras_de_saude()
    desenhar_personagens(dano_inimigo=dano_inimigo)
    desenhar_texto(mensagem, font, BRANCO, screen, 20, 20)
    desenhar_texto(f"Tempo de resposta: {tempo_resposta:.2f} segundos", font, BRANCO, screen, 20, 60)
    pygame.display.flip()
    pygame.time.delay(3000)

# Função para turno do inimigo
def turno_inimigo():
    global saude_jogador, defendendo, mana_inimigo
    dano = random.randint(5, 15)
    tipo_acao = random.choice(["Ataque", "Magia"])
    dano_jogador = False

    if tipo_acao == "Magia" and mana_inimigo >= 10:
        mana_inimigo -= 10
        dano += 5  # Magia causa mais dano

    if defendendo:
        dano //= 2  # Reduzir dano pela metade se o jogador estiver defendendo
        defendendo = False  # Resetar estado de defesa após reduzir dano
        mensagem = "Defesa bem-sucedida! Dano reduzido!"
    else:
        mensagem = ""

    saude_jogador -= dano
    dano_jogador = True if dano > 0 else False

    screen.blit(background_img, (0, 0))
    desenhar_barras_de_saude()
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
    screen.blit(background_img, (0, 0))
    desenhar_texto("A Saga do Conhecimento", font, BRANCO, screen, WIDTH // 2 - 150, HEIGHT // 2 - 100)
    ret_jogar = desenhar_texto("Jogar", font, BRANCO, screen, WIDTH // 2 - 50, HEIGHT // 2)
    ret_opcoes = desenhar_texto("Opções", font, BRANCO, screen, WIDTH // 2 - 50, HEIGHT // 2 + 50)
    pygame.display.flip()

    jogando = False
    while not jogando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if ret_jogar.collidepoint(evento.pos):
                    jogando = True
                elif ret_opcoes.collidepoint(evento.pos):
                    selecionar_nivel_e_disciplina()
                    jogando = True

# Função principal da batalha
def batalha():
    global nivel_selecionado, disciplinas_selecionadas, batalha_ativa
    tela_inicial()

    # Usar o primeiro ano e todas as disciplinas por padrão, se não forem selecionados
    if not nivel_selecionado:
        nivel_selecionado = "1° Ano"
    if not disciplinas_selecionadas:
        disciplinas_selecionadas = list(perguntas_por_nivel_e_disciplina[nivel_selecionado].keys())

    perguntas = []
    for disciplina in disciplinas_selecionadas:
        perguntas.extend(perguntas_por_nivel_e_disciplina[nivel_selecionado][disciplina])

    screen.blit(background_img, (0, 0))
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
            break
        pergunta, opcoes_rects = apresentar_pergunta(perguntas, tempo_total_pergunta)
        resposta_correta, tempo_resposta = avaliar_resposta(pergunta, opcoes_rects, tempo_total_pergunta)
        executar_acao(acao, resposta_correta, tempo_resposta)
        resultado = checar_fim_batalha()
        if resultado:
            batalha_ativa = False
            screen.blit(background_img, (0, 0))
            desenhar_barras_de_saude()
            desenhar_personagens()
            desenhar_texto(resultado, font, BRANCO, screen, WIDTH // 2 - 50, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(3000)
        else:
            turno_inimigo()
            resultado = checar_fim_batalha()
            if resultado:
                batalha_ativa = False
                screen.blit(background_img, (0, 0))
                desenhar_barras_de_saude()
                desenhar_personagens()
                desenhar_texto(resultado, font, BRANCO, screen, WIDTH // 2 - 50, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(3000)

# Iniciar a batalha
batalha()
pygame.quit()