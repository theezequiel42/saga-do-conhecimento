import pygame
from config import COLORS, WIDTH, HEIGHT
from utils import carregar_animacao, desenhar_texto, desenhar_hud, desenhar_personagens, desenhar_barra_tempo, tocar_som, parar_musica

class Jogador:
    def __init__(self):
        self.estado = {
            "saude_jogador": 100,
            "saude_inimigo": 100,
            "mana_jogador": 100,
            "mana_inimigo": 100,
            "pontos_sabedoria": 0,
            "defendendo": False,
            "nivel_selecionado": "1° Ano",
            "disciplinas_selecionadas": ["Matemática", "Língua Portuguesa"],
            "batalha_ativa": True,
            "jogador_acao": "idle",
            "jogador_frame_atual": 0,
            "jogador_frame_tempo": 0,
            "inimigo_acao": "idle",
            "inimigo_frame_atual": 0,
            "inimigo_frame_tempo": 0
        }
        self.jogador_animacoes = {
            "idle": carregar_animacao("idle-Sheet.png", 64, 64, 4),
            "run": carregar_animacao("Run-Sheet.png", 64, 64, 8),
            "attack": carregar_animacao("Attack-01-Sheet.png", 64, 64, 8),
            "derrota": carregar_animacao("derrota_jogador-Sheet.png", 64, 64, 8)
        }

    def reset(self):
        self.estado.update({
            "saude_jogador": 100,
            "saude_inimigo": 100,
            "mana_jogador": 100,
            "mana_inimigo": 100,
            "pontos_sabedoria": 0,
            "defendendo": False,
            "batalha_ativa": True,
            "jogador_acao": "idle",
            "jogador_frame_atual": 0,
            "jogador_frame_tempo": 0,
            "inimigo_acao": "idle",
            "inimigo_frame_atual": 0,
            "inimigo_frame_tempo": 0
        })

    def selecionar_acao(self, screen, background_batalha_img, inimigo):
        acoes = ["Ataque", "Magia", "Defesa", "Curar", "Fugir"]
        opcao_selecionada = 0
        opcoes_rects = []

        while True:
            mouse_pos = pygame.mouse.get_pos()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_DOWN:
                        opcao_selecionada = (opcao_selecionada + 1) % len(acoes)
                    elif evento.key == pygame.K_UP:
                        opcao_selecionada = (opcao_selecionada - 1) % len(acoes)
                    elif evento.key == pygame.K_RETURN:
                        return acoes[opcao_selecionada]
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(opcoes_rects):
                        if rect.collidepoint(evento.pos):
                            return acoes[i]

            screen.blit(background_batalha_img, (0, 0))
            desenhar_hud(screen, self.estado)
            desenhar_personagens(screen, self.jogador_animacoes, inimigo.inimigo_animacoes, self.estado)
            desenhar_texto("Escolha sua ação:", None, COLORS["BRANCO"], screen, 20, 20)

            opcoes_rects = []
            for i, acao in enumerate(acoes):
                cor = COLORS["PRETO"] if i == opcao_selecionada else COLORS["BRANCO"]
                ret = desenhar_texto(acao, None, cor, screen, 20, 60 + i * 40)
                opcoes_rects.append(ret)
                if ret.collidepoint(mouse_pos):
                    opcao_selecionada = i

            for i, rect in enumerate(opcoes_rects):
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, COLORS["AMARELO"], rect)
                    desenhar_texto(acoes[i], None, COLORS["PRETO"], screen, rect.x, rect.y)

            pygame.display.flip()

    def apresentar_pergunta(self, perguntas, screen, background_img):
        pergunta = random.choice(perguntas)
        screen.blit(background_img, (0, 0))
        desenhar_hud(screen, self.estado)
        desenhar_personagens(screen, self.jogador_animacoes, {}, self.estado)
        desenhar_texto(pergunta["pergunta"], None, COLORS["BRANCO"], screen, 20, 20)
        desenhar_barra_tempo(screen, 10, 10)

        opcoes_rects = []
        for i, opcao in enumerate(pergunta["opcoes"]):
            ret_opcao = desenhar_texto(opcao, None, COLORS["BRANCO"], screen, 20, 120 + i * 30)
            opcoes_rects.append(pygame.Rect(20, 120 + i * 30, WIDTH - 30, 30))

        pygame.display.flip()
        return pergunta, opcoes_rects

    def avaliar_resposta(self, pergunta, opcoes_rects, screen, background_img):
        tempo_inicio = pygame.time.get_ticks()
        opcao_selecionada = None
        indice_opcao_selecionada = 0

        while opcao_selecionada is None:
            tempo_atual = pygame.time.get_ticks()
            tempo_passado = (tempo_atual - tempo_inicio) / 1000
            tempo_restante = 10 - tempo_passado

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

            screen.blit(background_img, (0, 0))
            desenhar_hud(screen, self.estado)
            desenhar_personagens(screen, self.jogador_animacoes, {}, self.estado)
            desenhar_texto(pergunta["pergunta"], None, COLORS["BRANCO"], screen, 20, 20)
            for i, opcao in enumerate(pergunta["opcoes"]):
                cor = COLORS["PRETO"] if i == indice_opcao_selecionada else COLORS["BRANCO"]
                if i == indice_opcao_selecionada:
                    pygame.draw.rect(screen, COLORS["CINZA_CLARO"], opcoes_rects[i])
                desenhar_texto(opcao, None, cor, screen, 20, 120 + i * 30)
            desenhar_barra_tempo(screen, tempo_restante, 10)
            pygame.display.flip()

        tempo_total_resposta = (pygame.time.get_ticks() - tempo_inicio) / 1000
        resposta_correta = opcao_selecionada == pergunta["resposta"]

        return resposta_correta, tempo_total_resposta

    def executar_acao(self, acao, resposta_correta, tempo_resposta, inimigo, screen, background_img):
        dano = 0
        mensagem = ""
        dano_inimigo = False
        cura = 0

        if acao == "Fugir":
            self.estado["batalha_ativa"] = False
            mensagem = "Você fugiu da batalha!"
            parar_musica()
            return "fugir"
        else:
            if resposta_correta:
                if acao == "Ataque":
                    dano = 20 if tempo_resposta <= 5 else 10
                    self.estado["jogador_acao"] = "attack"
                elif acao == "Magia" and self.estado["mana_jogador"] >= 10:
                    self.estado["mana_jogador"] -= 10
                    dano = 25 if tempo_resposta <= 5 else 15
                elif acao == "Defesa":
                    self.estado["defendendo"] = True
                    mensagem = "Você se preparou para a defesa!"
                elif acao == "Curar" and self.estado["mana_jogador"] >= 15:
                    self.estado["mana_jogador"] -= 15
                    cura = 20 if tempo_resposta <= 5 else 10
                    self.estado["saude_jogador"] = min(self.estado["saude_jogador"] + cura, 100)
                    mensagem = f"Você se curou em {cura} pontos!"
                self.estado["pontos_sabedoria"] += 10
            else:
                mensagem = "Resposta errada! Nenhum dano causado!" if acao != "Defesa" else "A defesa falhou!"
                self.estado["defendendo"] = False

            if acao == "Ataque":
                for frame in self.jogador_animacoes["attack"]:
                    screen.blit(background_img, (0, 0))
                    desenhar_hud(screen, self.estado)
                    screen.blit(frame, (100, HEIGHT - 400))
                    pygame.display.flip()
                    pygame.time.delay(150)

            self.estado["saude_inimigo"] -= dano
            mensagem = f"Você causou {dano} de dano!" if dano > 0 else mensagem
            dano_inimigo = dano > 0

            screen.blit(background_img, (0, 0))
            desenhar_hud(screen, self.estado)
            desenhar_personagens(screen, self.jogador_animacoes, inimigo.inimigo_animacoes, self.estado, dano_inimigo=dano_inimigo)
            desenhar_texto(mensagem, None, COLORS["BRANCO"], screen, 20, 20)
            desenhar_texto(f"Tempo de resposta: {tempo_resposta:.2f} segundos", None, COLORS["BRANCO"], screen, 20, 60)
            pygame.display.flip()
            pygame.time.delay(3000)

    def checar_fim_batalha(self, inimigo):
        if self.estado["saude_jogador"] <= 0:
            return "Derrota"
        elif self.estado["saude_inimigo"] <= 0:
            return "Vitória"
        return None

    def mostrar_resultado(self, screen, background_img, resultado):
        screen.blit(background_img, (0, 0))
        desenhar_hud(screen, self.estado)
        desenhar_personagens(screen, self.jogador_animacoes, {}, self.estado, derrota_jogador=(resultado == "Derrota"))
        desenhar_texto(resultado, None, COLORS["BRANCO"], screen, WIDTH // 2 - 50, HEIGHT // 2)
        pygame.display.flip()

class Inimigo:
    def __init__(self):
        self.estado = {
            "saude_inimigo": 100,
            "inimigo_acao": "idle",
            "inimigo_frame_atual": 0,
            "inimigo_frame_tempo": 0
        }
        self.inimigo_animacoes = {
            "idle": carregar_animacao("Idle-Sheet-inimigo.png", 64, 64, 4),
            "attack": carregar_animacao("Attack-01-Sheet-inimigo.png", 64, 64, 8),
            "derrota": carregar_animacao("derrota_inimigo-Sheet.png", 64, 64, 8)
        }

    def reset(self):
        self.estado.update({
            "saude_inimigo": 100,
            "inimigo_acao": "idle",
            "inimigo_frame_atual": 0,
            "inimigo_frame_tempo": 0
        })

    def turno_inimigo(self, jogador, screen, background_img):
        dano = random.randint(5, 15)
        tipo_acao = random.choice(["Ataque", "Magia", "Defesa"])
        dano_jogador = False
        mensagem = ""

        if tipo_acao == "Magia" and jogador.estado["mana_inimigo"] >= 10:
            jogador.estado["mana_inimigo"] -= 10
            dano += 5
        elif tipo_acao == "Defesa":
            jogador.estado["defendendo"] = True
            mensagem = "O inimigo se preparou para a defesa!"
            dano = 0
        else:
            if jogador.estado["defendendo"]:
                dano //= 2
                jogador.estado["defendendo"] = False
                mensagem = "Defesa bem-sucedida! Dano reduzido!"

        jogador.estado["saude_jogador"] -= dano
        dano_jogador = dano > 0

        for frame in self.inimigo_animacoes["attack"]:
            screen.blit(background_img, (0, 0))
            desenhar_hud(screen, jogador.estado)
            screen.blit(frame, (980, HEIGHT - 400))
            pygame.display.flip()
            pygame.time.delay(150)

        screen.blit(background_img, (0, 0))
        desenhar_hud(screen, jogador.estado)
        desenhar_personagens(screen, jogador.jogador_animacoes, self.inimigo_animacoes, jogador.estado, dano_jogador=dano_jogador)
        desenhar_texto(f"O inimigo causou {dano} de dano!", None, COLORS["BRANCO"], screen, 20, 20)
        desenhar_texto(mensagem, None, COLORS["BRANCO"], screen, 20, 60)
        pygame.display.flip()
        pygame.time.delay(2000)

    def mostrar_derrota(self, screen, background_img, estado):
        screen.blit(background_img, (0, 0))
        desenhar_hud(screen, estado)
        desenhar_personagens(screen, {}, self.inimigo_animacoes, estado, derrota_inimigo=True)
        pygame.display.flip()
        pygame.time.delay(3000)
