import os
import pygame
from config import WIDTH, HEIGHT, COLORS, MUSICAS
from story_mode import modo_historia
from utils import carregar_imagem, tocar_musica, parar_musica, desenhar_texto, desenhar_hud, desenhar_personagens, desenhar_barra_tempo, tocar_som
from entities import Jogador, Inimigo
from questions import perguntas_por_nivel_e_disciplina

# Função para listar arquivos no diretório de trabalho
def listar_arquivos_diretorio(diretorio):
    print(f"Listando arquivos no diretório: {diretorio}")
    for arquivo in os.listdir(diretorio):
        print(arquivo)

# Inicialização da Pygame
pygame.init()
pygame.mixer.init()

# Configurações da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Saga do Conhecimento - Batalha")

# Listar arquivos no diretório de trabalho
listar_arquivos_diretorio(os.getcwd())

# Carregar e redimensionar imagens
background_batalha_img = carregar_imagem("background_batalha.png", WIDTH, HEIGHT)
background_menu_img = carregar_imagem("background_menu.png", WIDTH, HEIGHT)

# Inicializar Jogador e Inimigo
jogador = Jogador()
inimigo = Inimigo()

# Função principal da batalha
def batalha():
    # Configurações iniciais
    jogador.reset()
    inimigo.reset()

    tocar_musica(MUSICAS["batalha"])

    # Perguntas da batalha
    perguntas = []
    for disciplina in jogador.estado["disciplinas_selecionadas"]:
        perguntas.extend(perguntas_por_nivel_e_disciplina[jogador.estado["nivel_selecionado"]][disciplina])

    # Loop principal da batalha
    while jogador.estado["batalha_ativa"]:
        # Selecionar ação do jogador
        screen.blit(background_batalha_img, (0, 0))
        desenhar_hud(screen, jogador.estado)
        desenhar_personagens(screen, jogador.jogador_animacoes, inimigo.inimigo_animacoes, jogador.estado)

        acao = jogador.selecionar_acao(screen, background_batalha_img)

        if acao == "Fugir":
            resultado = jogador.executar_acao(acao, False, 0, inimigo, screen, background_batalha_img)
            if resultado == "fugir":
                tela_inicial()  # Encerrar a função batalha e retornar ao menu inicial
                return

        # Apresentar pergunta e avaliar resposta
        pergunta, opcoes_rects = jogador.apresentar_pergunta(perguntas, screen, background_batalha_img)
        resposta_correta, tempo_resposta = jogador.avaliar_resposta(pergunta, opcoes_rects, screen, background_batalha_img)

        # Executar ação do jogador
        jogador.executar_acao(acao, resposta_correta, tempo_resposta, inimigo, screen, background_batalha_img)

        # Checar fim da batalha
        resultado = jogador.checar_fim_batalha(inimigo)
        if resultado:
            jogador.estado["batalha_ativa"] = False
            parar_musica()
            tocar_som(MUSICAS["vitoria"] if resultado == "Vitória" else MUSICAS["derrota"])
            if resultado == "Vitória":
                inimigo.mostrar_derrota(screen, background_batalha_img, jogador.estado)
            else:
                jogador.mostrar_resultado(screen, background_batalha_img, resultado)
            pygame.time.delay(3000)  # Aguarda um tempo antes de retornar ao menu inicial
            tela_inicial()
            break

        # Turno do inimigo
        inimigo.turno_inimigo(jogador, screen, background_batalha_img)

        # Checar fim da batalha
        resultado = jogador.checar_fim_batalha(inimigo)
        if resultado:
            jogador.estado["batalha_ativa"] = False
            parar_musica()
            tocar_som(MUSICAS["vitoria"] if resultado == "Vitória" else MUSICAS["derrota"])
            if resultado == "Vitória":
                inimigo.mostrar_derrota(screen, background_batalha_img, jogador.estado)
            else:
                jogador.mostrar_resultado(screen, background_batalha_img, resultado)
            pygame.time.delay(3000)  # Aguarda um tempo antes de retornar ao menu inicial
            tela_inicial()
            break

# Função para exibir a tela inicial
def tela_inicial():
    tocar_musica(MUSICAS["menu"])
    screen.blit(background_menu_img, (0, 0))
    desenhar_texto("A Saga do Conhecimento", None, COLORS["BRANCO"], screen, WIDTH // 2 - 150, HEIGHT // 2 - 100)
    opcoes_menu = ["Jogar", "Tela Cheia", "Opções", "Modo História", "Sair"]
    retangulos_menu = [desenhar_texto(opcao, None, COLORS["BRANCO"], screen, WIDTH // 2 - 50, HEIGHT // 2 + i * 50) for i, opcao in enumerate(opcoes_menu)]
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
                        tocar_musica(MUSICAS["historia"])
                        modo_historia(screen, jogador)
                    elif opcao_selecionada == 4:
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
                            tocar_musica(MUSICAS["historia"])
                            modo_historia(screen, jogador)
                        elif i == 4:
                            pygame.quit()
                            exit()
            # Atualizar a opção selecionada com base na posição do mouse
            for i, ret in enumerate(retangulos_menu):
                if ret.collidepoint(mouse_pos):
                    opcao_selecionada = i
        screen.blit(background_menu_img, (0, 0))
        desenhar_texto("A Saga do Conhecimento", None, COLORS["BRANCO"], screen, WIDTH // 2 - 150, HEIGHT // 2 - 100)
        for i, opcao in enumerate(opcoes_menu):
            cor = COLORS["PRETO"] if i == opcao_selecionada else COLORS["BRANCO"]
            if i == opcao_selecionada:
                pygame.draw.rect(screen, COLORS["AMARELO"], retangulos_menu[i])
            desenhar_texto(opcao, None, cor, screen, WIDTH // 2 - 50, HEIGHT // 2 + i * 50)
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
