import pygame
import random
import os

# Inicialização da Pygame e dos módulos de som
pygame.init()
pygame.mixer.init()

# Configurações da tela
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Saga do Conhecimento - Batalha")

# Definição das cores
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

# Configuração da fonte
font = pygame.font.Font(None, 36)

# Função para carregar e redimensionar imagens
def carregar_imagem(nome, largura, altura):
    """
    Carrega uma imagem, converte para o formato apropriado e redimensiona.
    
    Args:
    nome (str): Caminho do arquivo da imagem.
    largura (int): Largura desejada da imagem.
    altura (int): Altura desejada da imagem.

    Returns:
    pygame.Surface: Imagem carregada e redimensionada.
    """
    img = pygame.image.load(nome).convert_alpha()
    return pygame.transform.scale(img, (largura, altura))

# Carregando imagens de fundo
background_batalha_img = carregar_imagem("background_batalha.png", WIDTH, HEIGHT)
background_menu_img = carregar_imagem("background_menu.png", WIDTH, HEIGHT)

# Carregando músicas e sons
MUSICAS = {
    "menu": "musica_menu.mp3",
    "batalha": "musica_batalha.mp3",
    "vitoria": "som_vitoria.mp3",
    "derrota": "som_derrota.mp3"
}

# Funções de áudio
def tocar_musica(musica, loop=-1):
    """
    Reproduz uma música em loop.

    Args:
    musica (str): Caminho do arquivo da música.
    loop (int): Quantidade de vezes que a música deve ser reproduzida. -1 para loop infinito.
    """
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play(loop)

def parar_musica():
    """Para a música atualmente em reprodução."""
    pygame.mixer.music.stop()

def tocar_som(som):
    """
    Reproduz um efeito sonoro.

    Args:
    som (str): Caminho do arquivo de som.
    """
    efeito = pygame.mixer.Sound(som)
    efeito.play()

# Função para desenhar texto na tela
def desenhar_texto(texto, fonte, cor, superficie, x, y):
    """
    Desenha texto na tela.

    Args:
    texto (str): Texto a ser desenhado.
    fonte (pygame.font.Font): Fonte do texto.
    cor (tuple): Cor do texto.
    superficie (pygame.Surface): Superfície onde o texto será desenhado.
    x (int): Posição x do texto.
    y (int): Posição y do texto.

    Returns:
    pygame.Rect: Retângulo do texto desenhado.
    """
    objeto_texto = fonte.render(texto, True, cor)
    retangulo_texto = objeto_texto.get_rect(topleft=(x, y))
    superficie.blit(objeto_texto, retangulo_texto)
    return retangulo_texto  # Retorna o retângulo para detecção de clique

# Função para carregar os frames da animação
def carregar_animacao(caminho, largura_frame, altura_frame, num_frames):
    """
    Carrega uma animação de uma sprite sheet.

    Args:
    caminho (str): Caminho da sprite sheet.
    largura_frame (int): Largura de cada frame.
    altura_frame (int): Altura de cada frame.
    num_frames (int): Número de frames na animação.

    Returns:
    list: Lista de frames da animação.
    """
    if not os.path.isfile(caminho):
        raise FileNotFoundError(f"Arquivo '{caminho}' não encontrado no diretório '{os.getcwd()}'.")
    sprite_sheet = pygame.image.load(caminho).convert_alpha()
    frames = [
        pygame.transform.scale(
            sprite_sheet.subsurface((i * largura_frame, 0, largura_frame, altura_frame)),
            (200, 200)
        ) for i in range(num_frames)
    ]
    return frames

# Carregando animações do jogador
jogador_animacoes = {
    "idle": carregar_animacao("idle-Sheet.png", 64, 64, 4),
    "attack": carregar_animacao("Attack-01-Sheet.png", 64, 64, 8),
    "derrota": carregar_animacao("derrota_jogador-Sheet.png", 64, 64, 8)
}

# Carregando animações do inimigo
inimigo_animacoes = {
    "idle": carregar_animacao("Idle-Sheet-inimigo.png", 64, 64, 4),
    "derrota": carregar_animacao("derrota_inimigo-Sheet.png", 64, 64, 8)
}


perguntas_por_nivel_e_disciplina = {
    "1° Ano": {
        "Matemática": [
            {"pergunta": "Quanto é 2 + 2?", "opcoes": ["3", "4", "5", "6"], "resposta": 1},
            {"pergunta": "Quanto é 3 + 3?", "opcoes": ["5", "6", "7", "8"], "resposta": 1},
            {"pergunta": "Quanto é 1 + 1?", "opcoes": ["1", "2", "3", "4"], "resposta": 1},
            {"pergunta": "Quanto é 4 - 1?", "opcoes": ["2", "3", "4", "5"], "resposta": 1},
            {"pergunta": "Quanto é 5 - 2?", "opcoes": ["2", "3", "4", "5"], "resposta": 1},
            {"pergunta": "Quanto é 6 + 1?", "opcoes": ["6", "7", "8", "9"], "resposta": 1},
            {"pergunta": "Quanto é 3 - 1?", "opcoes": ["1", "2", "3", "4"], "resposta": 1},
            {"pergunta": "Quanto é 7 - 5?", "opcoes": ["1", "2", "3", "4"], "resposta": 1},
            {"pergunta": "Quanto é 9 - 3?", "opcoes": ["5", "6", "7", "8"], "resposta": 1},
            {"pergunta": "Quanto é 8 + 1?", "opcoes": ["8", "9", "10", "11"], "resposta": 1},
        ],
        "Língua Portuguesa": [
            {"pergunta": "Qual é a letra inicial da palavra 'gato'?", "opcoes": ["A", "B", "G", "D"], "resposta": 2},
            {"pergunta": "Qual é a letra inicial da palavra 'casa'?", "opcoes": ["C", "B", "G", "D"], "resposta": 0},
            {"pergunta": "Qual é a última letra da palavra 'cavalo'?", "opcoes": ["A", "O", "V", "L"], "resposta": 1},
            {"pergunta": "Qual a letra inicial da palavra 'livro'?", "opcoes": ["L", "I", "V", "R"], "resposta": 0},
            {"pergunta": "Qual a letra inicial da palavra 'escola'?", "opcoes": ["E", "S", "C", "L"], "resposta": 0},
            {"pergunta": "Qual a última letra da palavra 'elefante'?", "opcoes": ["E", "T", "N", "F"], "resposta": 0},
            {"pergunta": "Qual a letra inicial da palavra 'menino'?", "opcoes": ["M", "E", "N", "I"], "resposta": 0},
            {"pergunta": "Qual a última letra da palavra 'borboleta'?", "opcoes": ["A", "E", "T", "L"], "resposta": 0},
            {"pergunta": "Qual a letra inicial da palavra 'girafa'?", "opcoes": ["G", "I", "R", "A"], "resposta": 0},
            {"pergunta": "Qual a letra inicial da palavra 'árvore'?", "opcoes": ["Á", "R", "V", "O"], "resposta": 0},
        ],
        "Ciências": [
            {"pergunta": "Qual desses animais pode voar?", "opcoes": ["Cachorro", "Gato", "Pássaro", "Peixe"], "resposta": 2},
            {"pergunta": "Qual parte da planta é responsável pela fotossíntese?", "opcoes": ["Raiz", "Folha", "Flor", "Semente"], "resposta": 1},
            {"pergunta": "Qual destes animais é um mamífero?", "opcoes": ["Cobra", "Gato", "Sapo", "Galinha"], "resposta": 1},
            {"pergunta": "Qual parte da planta absorve água?", "opcoes": ["Folha", "Raiz", "Flor", "Semente"], "resposta": 1},
            {"pergunta": "Qual destes é um inseto?", "opcoes": ["Peixe", "Sapo", "Borboleta", "Cachorro"], "resposta": 2},
            {"pergunta": "O que a vaca nos dá?", "opcoes": ["Leite", "Ovos", "Carne", "Lã"], "resposta": 0},
            {"pergunta": "Qual desses é um animal doméstico?", "opcoes": ["Leão", "Tigre", "Gato", "Elefante"], "resposta": 2},
            {"pergunta": "Qual é o estado da água em temperatura ambiente?", "opcoes": ["Sólido", "Líquido", "Gasoso", "Plasma"], "resposta": 1},
            {"pergunta": "Qual é o órgão responsável pela respiração?", "opcoes": ["Coração", "Pulmão", "Fígado", "Estômago"], "resposta": 1},
            {"pergunta": "Qual destes é um corpo celeste?", "opcoes": ["Árvore", "Montanha", "Sol", "Rio"], "resposta": 2},
        ],
        "História": [
            {"pergunta": "Quem foi o primeiro presidente do Brasil?", "opcoes": ["Getúlio Vargas", "Juscelino Kubitschek", "Deodoro da Fonseca", "Dom Pedro II"], "resposta": 2},
            {"pergunta": "Em que ano o Brasil foi descoberto?", "opcoes": ["1492", "1500", "1600", "1700"], "resposta": 1},
            {"pergunta": "Quem descobriu o Brasil?", "opcoes": ["Cristóvão Colombo", "Pedro Álvares Cabral", "Vasco da Gama", "Fernão de Magalhães"], "resposta": 1},
            {"pergunta": "O que eram as capitanias hereditárias?", "opcoes": ["Divisões administrativas no Brasil Colônia", "Tipos de plantações", "Grupos de indígenas", "Territórios na África"], "resposta": 0},
            {"pergunta": "Quem proclamou a independência do Brasil?", "opcoes": ["Dom Pedro I", "Dom Pedro II", "Tiradentes", "Deodoro da Fonseca"], "resposta": 0},
            {"pergunta": "Quem foi Tiradentes?", "opcoes": ["Um pintor", "Um médico", "Um dentista e herói da Inconfidência Mineira", "Um presidente"], "resposta": 2},
            {"pergunta": "O que é uma aldeia indígena?", "opcoes": ["Um grupo de animais", "Um grupo de casas onde vivem indígenas", "Uma cidade grande", "Um tipo de planta"], "resposta": 1},
            {"pergunta": "O que é uma bandeira?", "opcoes": ["Um símbolo de um país", "Uma planta", "Um animal", "Uma montanha"], "resposta": 0},
            {"pergunta": "O que é um museu?", "opcoes": ["Um lugar onde se guardam objetos históricos", "Uma escola", "Um hospital", "Um parque"], "resposta": 0},
            {"pergunta": "Quem foi Zumbi dos Palmares?", "opcoes": ["Um líder indígena", "Um líder dos escravos", "Um presidente", "Um artista"], "resposta": 1},
        ],
        "Geografia": [
            {"pergunta": "Qual é o maior continente?", "opcoes": ["África", "América", "Ásia", "Europa"], "resposta": 2},
            {"pergunta": "Qual é o menor continente?", "opcoes": ["África", "Oceania", "Antártica", "Europa"], "resposta": 1},
            {"pergunta": "Qual é o maior oceano?", "opcoes": ["Atlântico", "Pacífico", "Índico", "Ártico"], "resposta": 1},
            {"pergunta": "Qual país tem a maior população?", "opcoes": ["Estados Unidos", "Índia", "Brasil", "China"], "resposta": 3},
            {"pergunta": "Qual é o maior país da América do Sul?", "opcoes": ["Argentina", "Brasil", "Chile", "Peru"], "resposta": 1},
            {"pergunta": "Qual desses é um rio brasileiro?", "opcoes": ["Nilo", "Amazonas", "Mississipi", "Danúbio"], "resposta": 1},
            {"pergunta": "Qual é a capital do Brasil?", "opcoes": ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador"], "resposta": 2},
            {"pergunta": "Qual é o maior país do mundo?", "opcoes": ["Estados Unidos", "China", "Rússia", "Canadá"], "resposta": 2},
            {"pergunta": "Qual continente está localizado o Brasil?", "opcoes": ["América do Sul", "América do Norte", "Europa", "África"], "resposta": 0},
            {"pergunta": "Qual é o nome do maior deserto do mundo?", "opcoes": ["Sahara", "Atacama", "Gobi", "Kalahari"], "resposta": 0},
        ],
        "Computação": [
            {"pergunta": "Qual dispositivo usamos para digitar?", "opcoes": ["Mouse", "Teclado", "Monitor", "Impressora"], "resposta": 1},
            {"pergunta": "Qual parte do computador mostra as imagens?", "opcoes": ["Mouse", "Teclado", "Monitor", "CPU"], "resposta": 2},
            {"pergunta": "Qual parte do computador armazena informações?", "opcoes": ["Monitor", "Teclado", "Mouse", "HD"], "resposta": 3},
            {"pergunta": "Qual desses é um navegador de internet?", "opcoes": ["Windows", "Word", "Chrome", "Excel"], "resposta": 2},
            {"pergunta": "O que significa a sigla 'CPU'?", "opcoes": ["Central Processing Unit", "Computer Personal Unit", "Central Personal Unit", "Computer Processing Unit"], "resposta": 0},
            {"pergunta": "Qual desses é um sistema operacional?", "opcoes": ["Microsoft Word", "Google Chrome", "Windows", "Excel"], "resposta": 2},
            {"pergunta": "O que é um software?", "opcoes": ["Um programa de computador", "Um hardware", "Um periférico", "Um sistema operacional"], "resposta": 0},
            {"pergunta": "Qual desses dispositivos é de entrada?", "opcoes": ["Monitor", "Impressora", "Teclado", "CPU"], "resposta": 2},
            {"pergunta": "Para que serve o mouse?", "opcoes": ["Digitar", "Selecionar itens na tela", "Armazenar dados", "Exibir imagens"], "resposta": 1},
            {"pergunta": "O que é um vírus de computador?", "opcoes": ["Um hardware", "Um software malicioso", "Um sistema operacional", "Um navegador"], "resposta": 1},
        ],
        "Arte": [
            {"pergunta": "Qual destas é uma cor primária?", "opcoes": ["Verde", "Amarelo", "Roxo", "Laranja"], "resposta": 1},
            {"pergunta": "Qual destes é um material usado para desenhar?", "opcoes": ["Papel", "Lápis", "Tesoura", "Cola"], "resposta": 1},
            {"pergunta": "Qual destes é um artista famoso?", "opcoes": ["Leonardo da Vinci", "Isaac Newton", "Albert Einstein", "Galileu Galilei"], "resposta": 0},
            {"pergunta": "Qual destes é um estilo de dança?", "opcoes": ["Ballet", "Cálculo", "Geometria", "Física"], "resposta": 0},
            {"pergunta": "Qual destes é um instrumento musical?", "opcoes": ["Violino", "Bola", "Livro", "Computador"], "resposta": 0},
            {"pergunta": "O que usamos para pintar?", "opcoes": ["Pincel", "Cola", "Tesoura", "Borracha"], "resposta": 0},
            {"pergunta": "Qual destes é um gênero musical?", "opcoes": ["Rock", "Física", "Matemática", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destas é uma técnica de pintura?", "opcoes": ["Aquarela", "Biologia", "História", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destes é um famoso pintor?", "opcoes": ["Van Gogh", "Einstein", "Newton", "Edison"], "resposta": 0},
            {"pergunta": "Qual destas é uma forma de arte?", "opcoes": ["Escultura", "Cálculo", "Análise", "Pesquisa"], "resposta": 0},
        ]
    },
    "2° Ano": {
        "Matemática": [
            {"pergunta": "Quanto é 4 + 2?", "opcoes": ["6", "7", "8", "9"], "resposta": 0},
            {"pergunta": "Quanto é 5 - 3?", "opcoes": ["1", "2", "3", "4"], "resposta": 1},
            {"pergunta": "Quanto é 3 + 5?", "opcoes": ["7", "8", "9", "10"], "resposta": 1},
            {"pergunta": "Quanto é 10 - 7?", "opcoes": ["2", "3", "4", "5"], "resposta": 1},
            {"pergunta": "Quanto é 6 + 3?", "opcoes": ["8", "9", "10", "11"], "resposta": 1},
            {"pergunta": "Quanto é 8 - 4?", "opcoes": ["2", "3", "4", "5"], "resposta": 2},
            {"pergunta": "Quanto é 7 + 2?", "opcoes": ["8", "9", "10", "11"], "resposta": 1},
            {"pergunta": "Quanto é 5 + 4?", "opcoes": ["8", "9", "10", "11"], "resposta": 1},
            {"pergunta": "Quanto é 9 - 5?", "opcoes": ["3", "4", "5", "6"], "resposta": 1},
            {"pergunta": "Quanto é 6 + 2?", "opcoes": ["7", "8", "9", "10"], "resposta": 1},
        ],
        "Língua Portuguesa": [
            {"pergunta": "Qual é a última letra da palavra 'pato'?", "opcoes": ["A", "O", "T", "P"], "resposta": 1},
            {"pergunta": "Qual palavra rima com 'bola'?", "opcoes": ["Casa", "Gato", "Escola", "Mola"], "resposta": 3},
            {"pergunta": "Qual é o plural de 'cão'?", "opcoes": ["Cães", "Cãos", "Cãeses", "Cãozes"], "resposta": 0},
            {"pergunta": "Qual palavra é um verbo?", "opcoes": ["Correr", "Rápido", "Feliz", "Grande"], "resposta": 0},
            {"pergunta": "Qual destas palavras é um substantivo?", "opcoes": ["Amor", "Bonito", "Rápido", "Feliz"], "resposta": 0},
            {"pergunta": "Qual é o feminino de 'menino'?", "opcoes": ["Menina", "Menino", "Menine", "Menin"], "resposta": 0},
            {"pergunta": "Qual destas palavras é um adjetivo?", "opcoes": ["Grande", "Casa", "Livro", "Mesa"], "resposta": 0},
            {"pergunta": "Qual é o verbo da frase 'Eu corro todos os dias'?", "opcoes": ["Eu", "Corro", "Todos", "Dias"], "resposta": 1},
            {"pergunta": "Qual destas palavras é um pronome?", "opcoes": ["Ele", "Bonito", "Mesa", "Correr"], "resposta": 0},
            {"pergunta": "Qual é o diminutivo de 'cão'?", "opcoes": ["Cãozinho", "Cãos", "Cãezinho", "Cãinho"], "resposta": 0},
        ],
        "Ciências": [
            {"pergunta": "Qual destes é um planeta?", "opcoes": ["Sol", "Lua", "Terra", "Estrela"], "resposta": 2},
            {"pergunta": "O que os peixes usam para respirar?", "opcoes": ["Pulmões", "Brânquias", "Asas", "Narinas"], "resposta": 1},
            {"pergunta": "Qual destes animais é um mamífero?", "opcoes": ["Cobra", "Gato", "Sapo", "Galinha"], "resposta": 1},
            {"pergunta": "Qual parte da planta absorve água?", "opcoes": ["Folha", "Raiz", "Flor", "Semente"], "resposta": 1},
            {"pergunta": "Qual destes é um inseto?", "opcoes": ["Peixe", "Sapo", "Borboleta", "Cachorro"], "resposta": 2},
            {"pergunta": "O que a vaca nos dá?", "opcoes": ["Leite", "Ovos", "Carne", "Lã"], "resposta": 0},
            {"pergunta": "Qual desses é um animal doméstico?", "opcoes": ["Leão", "Tigre", "Gato", "Elefante"], "resposta": 2},
            {"pergunta": "Qual é o estado da água em temperatura ambiente?", "opcoes": ["Sólido", "Líquido", "Gasoso", "Plasma"], "resposta": 1},
            {"pergunta": "Qual é o órgão responsável pela respiração?", "opcoes": ["Coração", "Pulmão", "Fígado", "Estômago"], "resposta": 1},
            {"pergunta": "Qual destes é um corpo celeste?", "opcoes": ["Árvore", "Montanha", "Sol", "Rio"], "resposta": 2},
        ],
        "História": [
            {"pergunta": "Quem foi Tiradentes?", "opcoes": ["Um pintor", "Um médico", "Um dentista e herói da Inconfidência Mineira", "Um presidente"], "resposta": 2},
            {"pergunta": "O que é uma aldeia indígena?", "opcoes": ["Um grupo de animais", "Um grupo de casas onde vivem indígenas", "Uma cidade grande", "Um tipo de planta"], "resposta": 1},
            {"pergunta": "O que é uma bandeira?", "opcoes": ["Um símbolo de um país", "Uma planta", "Um animal", "Uma montanha"], "resposta": 0},
            {"pergunta": "O que é um museu?", "opcoes": ["Um lugar onde se guardam objetos históricos", "Uma escola", "Um hospital", "Um parque"], "resposta": 0},
            {"pergunta": "Quem foi Zumbi dos Palmares?", "opcoes": ["Um líder indígena", "Um líder dos escravos", "Um presidente", "Um artista"], "resposta": 1},
            {"pergunta": "Quem foi o primeiro presidente do Brasil?", "opcoes": ["Getúlio Vargas", "Juscelino Kubitschek", "Deodoro da Fonseca", "Dom Pedro II"], "resposta": 2},
            {"pergunta": "Em que ano o Brasil foi descoberto?", "opcoes": ["1492", "1500", "1600", "1700"], "resposta": 1},
            {"pergunta": "Quem descobriu o Brasil?", "opcoes": ["Cristóvão Colombo", "Pedro Álvares Cabral", "Vasco da Gama", "Fernão de Magalhães"], "resposta": 1},
            {"pergunta": "O que eram as capitanias hereditárias?", "opcoes": ["Divisões administrativas no Brasil Colônia", "Tipos de plantações", "Grupos de indígenas", "Territórios na África"], "resposta": 0},
            {"pergunta": "Quem proclamou a independência do Brasil?", "opcoes": ["Dom Pedro I", "Dom Pedro II", "Tiradentes", "Deodoro da Fonseca"], "resposta": 0},
        ],
        "Geografia": [
            {"pergunta": "Qual é o maior oceano?", "opcoes": ["Atlântico", "Pacífico", "Índico", "Ártico"], "resposta": 1},
            {"pergunta": "Qual país tem a maior população?", "opcoes": ["Estados Unidos", "Índia", "Brasil", "China"], "resposta": 3},
            {"pergunta": "Qual é o maior país da América do Sul?", "opcoes": ["Argentina", "Brasil", "Chile", "Peru"], "resposta": 1},
            {"pergunta": "Qual desses é um rio brasileiro?", "opcoes": ["Nilo", "Amazonas", "Mississipi", "Danúbio"], "resposta": 1},
            {"pergunta": "Qual é a capital do Brasil?", "opcoes": ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador"], "resposta": 2},
            {"pergunta": "Qual é o maior país do mundo?", "opcoes": ["Estados Unidos", "China", "Rússia", "Canadá"], "resposta": 2},
            {"pergunta": "Qual continente está localizado o Brasil?", "opcoes": ["América do Sul", "América do Norte", "Europa", "África"], "resposta": 0},
            {"pergunta": "Qual é o nome do maior deserto do mundo?", "opcoes": ["Sahara", "Atacama", "Gobi", "Kalahari"], "resposta": 0},
            {"pergunta": "Qual é o menor continente?", "opcoes": ["África", "Oceania", "Antártica", "Europa"], "resposta": 1},
            {"pergunta": "Qual é o maior continente?", "opcoes": ["África", "América", "Ásia", "Europa"], "resposta": 2},
        ],
        "Computação": [
            {"pergunta": "Qual parte do computador armazena informações?", "opcoes": ["Monitor", "Teclado", "Mouse", "HD"], "resposta": 3},
            {"pergunta": "Qual desses é um navegador de internet?", "opcoes": ["Windows", "Word", "Chrome", "Excel"], "resposta": 2},
            {"pergunta": "O que significa a sigla 'CPU'?", "opcoes": ["Central Processing Unit", "Computer Personal Unit", "Central Personal Unit", "Computer Processing Unit"], "resposta": 0},
            {"pergunta": "Qual desses é um sistema operacional?", "opcoes": ["Microsoft Word", "Google Chrome", "Windows", "Excel"], "resposta": 2},
            {"pergunta": "O que é um software?", "opcoes": ["Um programa de computador", "Um hardware", "Um periférico", "Um sistema operacional"], "resposta": 0},
            {"pergunta": "Qual desses dispositivos é de entrada?", "opcoes": ["Monitor", "Impressora", "Teclado", "CPU"], "resposta": 2},
            {"pergunta": "Para que serve o mouse?", "opcoes": ["Digitar", "Selecionar itens na tela", "Armazenar dados", "Exibir imagens"], "resposta": 1},
            {"pergunta": "O que é um vírus de computador?", "opcoes": ["Um hardware", "Um software malicioso", "Um sistema operacional", "Um navegador"], "resposta": 1},
            {"pergunta": "Qual dispositivo usamos para digitar?", "opcoes": ["Mouse", "Teclado", "Monitor", "Impressora"], "resposta": 1},
            {"pergunta": "Qual parte do computador mostra as imagens?", "opcoes": ["Mouse", "Teclado", "Monitor", "CPU"], "resposta": 2},
        ],
        "Arte": [
            {"pergunta": "Qual destas é uma cor primária?", "opcoes": ["Verde", "Amarelo", "Roxo", "Laranja"], "resposta": 1},
            {"pergunta": "Qual destes é um material usado para desenhar?", "opcoes": ["Papel", "Lápis", "Tesoura", "Cola"], "resposta": 1},
            {"pergunta": "Qual destes é um artista famoso?", "opcoes": ["Leonardo da Vinci", "Isaac Newton", "Albert Einstein", "Galileu Galilei"], "resposta": 0},
            {"pergunta": "Qual destes é um estilo de dança?", "opcoes": ["Ballet", "Cálculo", "Geometria", "Física"], "resposta": 0},
            {"pergunta": "Qual destes é um instrumento musical?", "opcoes": ["Violino", "Bola", "Livro", "Computador"], "resposta": 0},
            {"pergunta": "O que usamos para pintar?", "opcoes": ["Pincel", "Cola", "Tesoura", "Borracha"], "resposta": 0},
            {"pergunta": "Qual destes é um gênero musical?", "opcoes": ["Rock", "Física", "Matemática", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destas é uma técnica de pintura?", "opcoes": ["Aquarela", "Biologia", "História", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destes é um famoso pintor?", "opcoes": ["Van Gogh", "Einstein", "Newton", "Edison"], "resposta": 0},
            {"pergunta": "Qual destas é uma forma de arte?", "opcoes": ["Escultura", "Cálculo", "Análise", "Pesquisa"], "resposta": 0},
        ]
    },
    "3° Ano": {
        "Matemática": [
            {"pergunta": "Quanto é 7 + 3?", "opcoes": ["10", "11", "12", "13"], "resposta": 0},
            {"pergunta": "Quanto é 10 - 4?", "opcoes": ["5", "6", "7", "8"], "resposta": 1},
            {"pergunta": "Quanto é 8 + 2?", "opcoes": ["9", "10", "11", "12"], "resposta": 1},
            {"pergunta": "Quanto é 15 - 6?", "opcoes": ["7", "8", "9", "10"], "resposta": 2},
            {"pergunta": "Quanto é 9 + 4?", "opcoes": ["11", "12", "13", "14"], "resposta": 2},
            {"pergunta": "Quanto é 12 - 7?", "opcoes": ["4", "5", "6", "7"], "resposta": 1},
            {"pergunta": "Quanto é 11 + 2?", "opcoes": ["12", "13", "14", "15"], "resposta": 1},
            {"pergunta": "Quanto é 13 - 5?", "opcoes": ["7", "8", "9", "10"], "resposta": 1},
            {"pergunta": "Quanto é 14 + 1?", "opcoes": ["14", "15", "16", "17"], "resposta": 1},
            {"pergunta": "Quanto é 16 - 8?", "opcoes": ["6", "7", "8", "9"], "resposta": 2},
        ],
        "Língua Portuguesa": [
            {"pergunta": "Qual é o plural de 'cão'?", "opcoes": ["Cães", "Cãos", "Cãeses", "Cãozes"], "resposta": 0},
            {"pergunta": "Qual palavra é um verbo?", "opcoes": ["Correr", "Rápido", "Feliz", "Grande"], "resposta": 0},
            {"pergunta": "Qual destas palavras é um substantivo?", "opcoes": ["Amor", "Bonito", "Rápido", "Feliz"], "resposta": 0},
            {"pergunta": "Qual é o feminino de 'menino'?", "opcoes": ["Menina", "Menino", "Menine", "Menin"], "resposta": 0},
            {"pergunta": "Qual destas palavras é um adjetivo?", "opcoes": ["Grande", "Casa", "Livro", "Mesa"], "resposta": 0},
            {"pergunta": "Qual é o verbo da frase 'Eu corro todos os dias'?", "opcoes": ["Eu", "Corro", "Todos", "Dias"], "resposta": 1},
            {"pergunta": "Qual destas palavras é um pronome?", "opcoes": ["Ele", "Bonito", "Mesa", "Correr"], "resposta": 0},
            {"pergunta": "Qual é o diminutivo de 'cão'?", "opcoes": ["Cãozinho", "Cãos", "Cãezinho", "Cãinho"], "resposta": 0},
            {"pergunta": "Qual é o plural de 'flor'?", "opcoes": ["Flores", "Flor", "Flors", "Florzinhas"], "resposta": 0},
            {"pergunta": "Qual destas palavras é um advérbio?", "opcoes": ["Rápido", "Correr", "Mesa", "Sempre"], "resposta": 3},
        ],
        "Ciências": [
            {"pergunta": "Qual destes animais é um mamífero?", "opcoes": ["Cobra", "Sapo", "Gato", "Galinha"], "resposta": 2},
            {"pergunta": "Qual parte da planta absorve água?", "opcoes": ["Folha", "Caule", "Raiz", "Flor"], "resposta": 2},
            {"pergunta": "Qual destes é um inseto?", "opcoes": ["Peixe", "Sapo", "Borboleta", "Cachorro"], "resposta": 2},
            {"pergunta": "O que a vaca nos dá?", "opcoes": ["Leite", "Ovos", "Carne", "Lã"], "resposta": 0},
            {"pergunta": "Qual desses é um animal doméstico?", "opcoes": ["Leão", "Tigre", "Gato", "Elefante"], "resposta": 2},
            {"pergunta": "Qual é o estado da água em temperatura ambiente?", "opcoes": ["Sólido", "Líquido", "Gasoso", "Plasma"], "resposta": 1},
            {"pergunta": "Qual é o órgão responsável pela respiração?", "opcoes": ["Coração", "Pulmão", "Fígado", "Estômago"], "resposta": 1},
            {"pergunta": "Qual destes é um corpo celeste?", "opcoes": ["Árvore", "Montanha", "Sol", "Rio"], "resposta": 2},
            {"pergunta": "O que é fotossíntese?", "opcoes": ["Processo de digestão", "Processo de respiração", "Processo de produção de alimento nas plantas", "Processo de circulação sanguínea"], "resposta": 2},
            {"pergunta": "Qual é o maior planeta do sistema solar?", "opcoes": ["Terra", "Marte", "Júpiter", "Saturno"], "resposta": 2},
        ],
        "História": [
            {"pergunta": "Quem descobriu o Brasil?", "opcoes": ["Cristóvão Colombo", "Pedro Álvares Cabral", "Vasco da Gama", "Fernão de Magalhães"], "resposta": 1},
            {"pergunta": "O que eram as capitanias hereditárias?", "opcoes": ["Divisões administrativas no Brasil Colônia", "Tipos de plantações", "Grupos de indígenas", "Territórios na África"], "resposta": 0},
            {"pergunta": "Quem proclamou a independência do Brasil?", "opcoes": ["Dom Pedro I", "Dom Pedro II", "Tiradentes", "Deodoro da Fonseca"], "resposta": 0},
            {"pergunta": "Quem foi Tiradentes?", "opcoes": ["Um pintor", "Um médico", "Um dentista e herói da Inconfidência Mineira", "Um presidente"], "resposta": 2},
            {"pergunta": "O que é uma aldeia indígena?", "opcoes": ["Um grupo de animais", "Um grupo de casas onde vivem indígenas", "Uma cidade grande", "Um tipo de planta"], "resposta": 1},
            {"pergunta": "O que é uma bandeira?", "opcoes": ["Um símbolo de um país", "Uma planta", "Um animal", "Uma montanha"], "resposta": 0},
            {"pergunta": "O que é um museu?", "opcoes": ["Um lugar onde se guardam objetos históricos", "Uma escola", "Um hospital", "Um parque"], "resposta": 0},
            {"pergunta": "Quem foi Zumbi dos Palmares?", "opcoes": ["Um líder indígena", "Um líder dos escravos", "Um presidente", "Um artista"], "resposta": 1},
            {"pergunta": "Quem foi o primeiro presidente do Brasil?", "opcoes": ["Getúlio Vargas", "Juscelino Kubitschek", "Deodoro da Fonseca", "Dom Pedro II"], "resposta": 2},
            {"pergunta": "Em que ano o Brasil foi descoberto?", "opcoes": ["1492", "1500", "1600", "1700"], "resposta": 1},
        ],
        "Geografia": [
            {"pergunta": "Qual é o maior país da América do Sul?", "opcoes": ["Argentina", "Brasil", "Chile", "Peru"], "resposta": 1},
            {"pergunta": "Qual desses é um rio brasileiro?", "opcoes": ["Nilo", "Amazonas", "Mississipi", "Danúbio"], "resposta": 1},
            {"pergunta": "Qual é a capital do Brasil?", "opcoes": ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador"], "resposta": 2},
            {"pergunta": "Qual é o maior país do mundo?", "opcoes": ["Estados Unidos", "China", "Rússia", "Canadá"], "resposta": 2},
            {"pergunta": "Qual continente está localizado o Brasil?", "opcoes": ["América do Sul", "América do Norte", "Europa", "África"], "resposta": 0},
            {"pergunta": "Qual é o nome do maior deserto do mundo?", "opcoes": ["Sahara", "Atacama", "Gobi", "Kalahari"], "resposta": 0},
            {"pergunta": "Qual é o menor continente?", "opcoes": ["África", "Oceania", "Antártica", "Europa"], "resposta": 1},
            {"pergunta": "Qual é o maior continente?", "opcoes": ["África", "América", "Ásia", "Europa"], "resposta": 2},
            {"pergunta": "Qual é o maior oceano?", "opcoes": ["Atlântico", "Pacífico", "Índico", "Ártico"], "resposta": 1},
            {"pergunta": "Qual país tem a maior população?", "opcoes": ["Estados Unidos", "Índia", "Brasil", "China"], "resposta": 3},
        ],
        "Computação": [
            {"pergunta": "O que é um software?", "opcoes": ["Um programa de computador", "Um hardware", "Um periférico", "Um sistema operacional"], "resposta": 0},
            {"pergunta": "Qual desses dispositivos é de entrada?", "opcoes": ["Monitor", "Impressora", "Teclado", "CPU"], "resposta": 2},
            {"pergunta": "Para que serve o mouse?", "opcoes": ["Digitar", "Selecionar itens na tela", "Armazenar dados", "Exibir imagens"], "resposta": 1},
            {"pergunta": "O que é um vírus de computador?", "opcoes": ["Um hardware", "Um software malicioso", "Um sistema operacional", "Um navegador"], "resposta": 1},
            {"pergunta": "Qual dispositivo usamos para digitar?", "opcoes": ["Mouse", "Teclado", "Monitor", "Impressora"], "resposta": 1},
            {"pergunta": "Qual parte do computador mostra as imagens?", "opcoes": ["Mouse", "Teclado", "Monitor", "CPU"], "resposta": 2},
            {"pergunta": "Qual parte do computador armazena informações?", "opcoes": ["Monitor", "Teclado", "Mouse", "HD"], "resposta": 3},
            {"pergunta": "Qual desses é um navegador de internet?", "opcoes": ["Windows", "Word", "Chrome", "Excel"], "resposta": 2},
            {"pergunta": "O que significa a sigla 'CPU'?", "opcoes": ["Central Processing Unit", "Computer Personal Unit", "Central Personal Unit", "Computer Processing Unit"], "resposta": 0},
            {"pergunta": "Qual desses é um sistema operacional?", "opcoes": ["Microsoft Word", "Google Chrome", "Windows", "Excel"], "resposta": 2},
        ],
        "Arte": [
            {"pergunta": "Qual destas é uma cor primária?", "opcoes": ["Verde", "Amarelo", "Roxo", "Laranja"], "resposta": 1},
            {"pergunta": "Qual destes é um material usado para desenhar?", "opcoes": ["Papel", "Lápis", "Tesoura", "Cola"], "resposta": 1},
            {"pergunta": "Qual destes é um artista famoso?", "opcoes": ["Leonardo da Vinci", "Isaac Newton", "Albert Einstein", "Galileu Galilei"], "resposta": 0},
            {"pergunta": "Qual destes é um estilo de dança?", "opcoes": ["Ballet", "Cálculo", "Geometria", "Física"], "resposta": 0},
            {"pergunta": "Qual destes é um instrumento musical?", "opcoes": ["Violino", "Bola", "Livro", "Computador"], "resposta": 0},
            {"pergunta": "O que usamos para pintar?", "opcoes": ["Pincel", "Cola", "Tesoura", "Borracha"], "resposta": 0},
            {"pergunta": "Qual destes é um gênero musical?", "opcoes": ["Rock", "Física", "Matemática", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destas é uma técnica de pintura?", "opcoes": ["Aquarela", "Biologia", "História", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destes é um famoso pintor?", "opcoes": ["Van Gogh", "Einstein", "Newton", "Edison"], "resposta": 0},
            {"pergunta": "Qual destas é uma forma de arte?", "opcoes": ["Escultura", "Cálculo", "Análise", "Pesquisa"], "resposta": 0},
        ]
    },
    "4° Ano": {
        "Matemática": [
            {"pergunta": "Quanto é 12 + 8?", "opcoes": ["20", "21", "22", "23"], "resposta": 0},
            {"pergunta": "Quanto é 15 - 7?", "opcoes": ["7", "8", "9", "10"], "resposta": 1},
            {"pergunta": "Quanto é 7 x 3?", "opcoes": ["20", "21", "22", "23"], "resposta": 1},
            {"pergunta": "Quanto é 24 ÷ 6?", "opcoes": ["3", "4", "5", "6"], "resposta": 1},
            {"pergunta": "Quanto é 10 + 15?", "opcoes": ["24", "25", "26", "27"], "resposta": 1},
            {"pergunta": "Quanto é 30 - 12?", "opcoes": ["17", "18", "19", "20"], "resposta": 1},
            {"pergunta": "Quanto é 5 x 5?", "opcoes": ["20", "25", "30", "35"], "resposta": 1},
            {"pergunta": "Quanto é 40 ÷ 8?", "opcoes": ["4", "5", "6", "7"], "resposta": 0},
            {"pergunta": "Quanto é 18 + 7?", "opcoes": ["24", "25", "26", "27"], "resposta": 1},
            {"pergunta": "Quanto é 25 - 9?", "opcoes": ["15", "16", "17", "18"], "resposta": 2},
        ],
        "Língua Portuguesa": [
            {"pergunta": "Qual é o antônimo de 'feliz'?", "opcoes": ["Triste", "Contente", "Alegre", "Satisfeito"], "resposta": 0},
            {"pergunta": "Qual é o plural de 'flor'?", "opcoes": ["Flores", "Flor", "Flors", "Florzinhas"], "resposta": 0},
            {"pergunta": "Qual destas palavras é um advérbio?", "opcoes": ["Rápido", "Correr", "Mesa", "Sempre"], "resposta": 3},
            {"pergunta": "Qual é o sujeito da frase 'O gato dorme no sofá'?", "opcoes": ["Gato", "Dorme", "No", "Sofá"], "resposta": 0},
            {"pergunta": "Qual é o feminino de 'ator'?", "opcoes": ["Atora", "Atoriza", "Atoriz", "Atriz"], "resposta": 3},
            {"pergunta": "Qual é o verbo da frase 'Ela canta bem'?", "opcoes": ["Ela", "Canta", "Bem", "Cantar"], "resposta": 1},
            {"pergunta": "Qual destas palavras é um substantivo abstrato?", "opcoes": ["Amor", "Mesa", "Cadeira", "Livro"], "resposta": 0},
            {"pergunta": "Qual é a forma diminutiva de 'casa'?", "opcoes": ["Casinha", "Casa", "Casão", "Casoca"], "resposta": 0},
            {"pergunta": "Qual destas palavras é um adjetivo?", "opcoes": ["Alto", "Mesa", "Correr", "Livro"], "resposta": 0},
            {"pergunta": "Qual é o coletivo de 'abelha'?", "opcoes": ["Abelharada", "Abelhal", "Enxame", "Colmeia"], "resposta": 2},
        ],
        "Ciências": [
            {"pergunta": "Qual é o maior planeta do sistema solar?", "opcoes": ["Terra", "Marte", "Júpiter", "Saturno"], "resposta": 2},
            {"pergunta": "Qual parte da planta realiza a fotossíntese?", "opcoes": ["Raiz", "Caule", "Folha", "Flor"], "resposta": 2},
            {"pergunta": "Qual destes animais é um anfíbio?", "opcoes": ["Sapo", "Cachorro", "Gato", "Leão"], "resposta": 0},
            {"pergunta": "Qual destes animais é uma ave?", "opcoes": ["Cachorro", "Gato", "Papagaio", "Leão"], "resposta": 2},
            {"pergunta": "O que é um ecossistema?", "opcoes": ["Um grupo de animais", "Uma comunidade de seres vivos interagindo com o meio ambiente", "Uma árvore", "Um rio"], "resposta": 1},
            {"pergunta": "O que é um herbívoro?", "opcoes": ["Um animal que come carne", "Um animal que come plantas", "Um animal que come tudo", "Um animal que não come"], "resposta": 1},
            {"pergunta": "Qual é a função do coração?", "opcoes": ["Respirar", "Bombear sangue", "Digestão", "Mover o corpo"], "resposta": 1},
            {"pergunta": "Qual destes é um exemplo de cadeia alimentar?", "opcoes": ["Planta -> Herbívoro -> Carnívoro", "Planta -> Carnívoro -> Herbívoro", "Herbívoro -> Planta -> Carnívoro", "Carnívoro -> Herbívoro -> Planta"], "resposta": 0},
            {"pergunta": "Qual é o estado físico da água a 100°C?", "opcoes": ["Sólido", "Líquido", "Gasoso", "Plasma"], "resposta": 2},
            {"pergunta": "Qual é a função do pulmão?", "opcoes": ["Digestão", "Respiração", "Circulação", "Locomoção"], "resposta": 1},
        ],
        "História": [
            {"pergunta": "Quem proclamou a independência do Brasil?", "opcoes": ["Dom Pedro I", "Dom Pedro II", "Tiradentes", "Deodoro da Fonseca"], "resposta": 0},
            {"pergunta": "Quem foi Tiradentes?", "opcoes": ["Um pintor", "Um médico", "Um dentista e herói da Inconfidência Mineira", "Um presidente"], "resposta": 2},
            {"pergunta": "O que é uma aldeia indígena?", "opcoes": ["Um grupo de animais", "Um grupo de casas onde vivem indígenas", "Uma cidade grande", "Um tipo de planta"], "resposta": 1},
            {"pergunta": "O que é uma bandeira?", "opcoes": ["Um símbolo de um país", "Uma planta", "Um animal", "Uma montanha"], "resposta": 0},
            {"pergunta": "O que é um museu?", "opcoes": ["Um lugar onde se guardam objetos históricos", "Uma escola", "Um hospital", "Um parque"], "resposta": 0},
            {"pergunta": "Quem foi Zumbi dos Palmares?", "opcoes": ["Um líder indígena", "Um líder dos escravos", "Um presidente", "Um artista"], "resposta": 1},
            {"pergunta": "Quem foi o primeiro presidente do Brasil?", "opcoes": ["Getúlio Vargas", "Juscelino Kubitschek", "Deodoro da Fonseca", "Dom Pedro II"], "resposta": 2},
            {"pergunta": "Em que ano o Brasil foi descoberto?", "opcoes": ["1492", "1500", "1600", "1700"], "resposta": 1},
            {"pergunta": "Quem descobriu o Brasil?", "opcoes": ["Cristóvão Colombo", "Pedro Álvares Cabral", "Vasco da Gama", "Fernão de Magalhães"], "resposta": 1},
            {"pergunta": "O que eram as capitanias hereditárias?", "opcoes": ["Divisões administrativas no Brasil Colônia", "Tipos de plantações", "Grupos de indígenas", "Territórios na África"], "resposta": 0},
        ],
        "Geografia": [
            {"pergunta": "Qual é o maior país da América do Sul?", "opcoes": ["Argentina", "Brasil", "Chile", "Peru"], "resposta": 1},
            {"pergunta": "Qual desses é um rio brasileiro?", "opcoes": ["Nilo", "Amazonas", "Mississipi", "Danúbio"], "resposta": 1},
            {"pergunta": "Qual é a capital do Brasil?", "opcoes": ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador"], "resposta": 2},
            {"pergunta": "Qual é o maior país do mundo?", "opcoes": ["Estados Unidos", "China", "Rússia", "Canadá"], "resposta": 2},
            {"pergunta": "Qual continente está localizado o Brasil?", "opcoes": ["América do Sul", "América do Norte", "Europa", "África"], "resposta": 0},
            {"pergunta": "Qual é o nome do maior deserto do mundo?", "opcoes": ["Sahara", "Atacama", "Gobi", "Kalahari"], "resposta": 0},
            {"pergunta": "Qual é o menor continente?", "opcoes": ["África", "Oceania", "Antártica", "Europa"], "resposta": 1},
            {"pergunta": "Qual é o maior continente?", "opcoes": ["África", "América", "Ásia", "Europa"], "resposta": 2},
            {"pergunta": "Qual é o maior oceano?", "opcoes": ["Atlântico", "Pacífico", "Índico", "Ártico"], "resposta": 1},
            {"pergunta": "Qual país tem a maior população?", "opcoes": ["Estados Unidos", "Índia", "Brasil", "China"], "resposta": 3},
        ],
        "Computação": [
            {"pergunta": "O que é um software?", "opcoes": ["Um programa de computador", "Um hardware", "Um periférico", "Um sistema operacional"], "resposta": 0},
            {"pergunta": "Qual desses dispositivos é de entrada?", "opcoes": ["Monitor", "Impressora", "Teclado", "CPU"], "resposta": 2},
            {"pergunta": "Para que serve o mouse?", "opcoes": ["Digitar", "Selecionar itens na tela", "Armazenar dados", "Exibir imagens"], "resposta": 1},
            {"pergunta": "O que é um vírus de computador?", "opcoes": ["Um hardware", "Um software malicioso", "Um sistema operacional", "Um navegador"], "resposta": 1},
            {"pergunta": "Qual dispositivo usamos para digitar?", "opcoes": ["Mouse", "Teclado", "Monitor", "Impressora"], "resposta": 1},
            {"pergunta": "Qual parte do computador mostra as imagens?", "opcoes": ["Mouse", "Teclado", "Monitor", "CPU"], "resposta": 2},
            {"pergunta": "Qual parte do computador armazena informações?", "opcoes": ["Monitor", "Teclado", "Mouse", "HD"], "resposta": 3},
            {"pergunta": "Qual desses é um navegador de internet?", "opcoes": ["Windows", "Word", "Chrome", "Excel"], "resposta": 2},
            {"pergunta": "O que significa a sigla 'CPU'?", "opcoes": ["Central Processing Unit", "Computer Personal Unit", "Central Personal Unit", "Computer Processing Unit"], "resposta": 0},
            {"pergunta": "Qual desses é um sistema operacional?", "opcoes": ["Microsoft Word", "Google Chrome", "Windows", "Excel"], "resposta": 2},
        ],
        "Arte": [
            {"pergunta": "Qual destas é uma cor primária?", "opcoes": ["Verde", "Amarelo", "Roxo", "Laranja"], "resposta": 1},
            {"pergunta": "Qual destes é um material usado para desenhar?", "opcoes": ["Papel", "Lápis", "Tesoura", "Cola"], "resposta": 1},
            {"pergunta": "Qual destes é um artista famoso?", "opcoes": ["Leonardo da Vinci", "Isaac Newton", "Albert Einstein", "Galileu Galilei"], "resposta": 0},
            {"pergunta": "Qual destes é um estilo de dança?", "opcoes": ["Ballet", "Cálculo", "Geometria", "Física"], "resposta": 0},
            {"pergunta": "Qual destes é um instrumento musical?", "opcoes": ["Violino", "Bola", "Livro", "Computador"], "resposta": 0},
            {"pergunta": "O que usamos para pintar?", "opcoes": ["Pincel", "Cola", "Tesoura", "Borracha"], "resposta": 0},
            {"pergunta": "Qual destes é um gênero musical?", "opcoes": ["Rock", "Física", "Matemática", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destas é uma técnica de pintura?", "opcoes": ["Aquarela", "Biologia", "História", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destes é um famoso pintor?", "opcoes": ["Van Gogh", "Einstein", "Newton", "Edison"], "resposta": 0},
            {"pergunta": "Qual destas é uma forma de arte?", "opcoes": ["Escultura", "Cálculo", "Análise", "Pesquisa"], "resposta": 0},
        ]
    },
    # Continuar preenchendo para os anos 5° ao 9°
    "5° Ano": {
        "Matemática": [
            {"pergunta": "Quanto é 12 + 8?", "opcoes": ["20", "21", "22", "23"], "resposta": 0},
            {"pergunta": "Quanto é 15 - 7?", "opcoes": ["7", "8", "9", "10"], "resposta": 1},
            {"pergunta": "Quanto é 7 x 3?", "opcoes": ["20", "21", "22", "23"], "resposta": 1},
            {"pergunta": "Quanto é 24 ÷ 6?", "opcoes": ["3", "4", "5", "6"], "resposta": 1},
            {"pergunta": "Quanto é 10 + 15?", "opcoes": ["24", "25", "26", "27"], "resposta": 1},
            {"pergunta": "Quanto é 30 - 12?", "opcoes": ["17", "18", "19", "20"], "resposta": 1},
            {"pergunta": "Quanto é 5 x 5?", "opcoes": ["20", "25", "30", "35"], "resposta": 1},
            {"pergunta": "Quanto é 40 ÷ 8?", "opcoes": ["4", "5", "6", "7"], "resposta": 0},
            {"pergunta": "Quanto é 18 + 7?", "opcoes": ["24", "25", "26", "27"], "resposta": 1},
            {"pergunta": "Quanto é 25 - 9?", "opcoes": ["15", "16", "17", "18"], "resposta": 2},
        ],
        "Língua Portuguesa": [
            {"pergunta": "Qual é o antônimo de 'feliz'?", "opcoes": ["Triste", "Contente", "Alegre", "Satisfeito"], "resposta": 0},
            {"pergunta": "Qual é o plural de 'flor'?", "opcoes": ["Flores", "Flor", "Flors", "Florzinhas"], "resposta": 0},
            {"pergunta": "Qual destas palavras é um advérbio?", "opcoes": ["Rápido", "Correr", "Mesa", "Sempre"], "resposta": 3},
            {"pergunta": "Qual é o sujeito da frase 'O gato dorme no sofá'?", "opcoes": ["Gato", "Dorme", "No", "Sofá"], "resposta": 0},
            {"pergunta": "Qual é o feminino de 'ator'?", "opcoes": ["Atora", "Atoriza", "Atoriz", "Atriz"], "resposta": 3},
            {"pergunta": "Qual é o verbo da frase 'Ela canta bem'?", "opcoes": ["Ela", "Canta", "Bem", "Cantar"], "resposta": 1},
            {"pergunta": "Qual destas palavras é um substantivo abstrato?", "opcoes": ["Amor", "Mesa", "Cadeira", "Livro"], "resposta": 0},
            {"pergunta": "Qual é a forma diminutiva de 'casa'?", "opcoes": ["Casinha", "Casa", "Casão", "Casoca"], "resposta": 0},
            {"pergunta": "Qual destas palavras é um adjetivo?", "opcoes": ["Alto", "Mesa", "Correr", "Livro"], "resposta": 0},
            {"pergunta": "Qual é o coletivo de 'abelha'?", "opcoes": ["Abelharada", "Abelhal", "Enxame", "Colmeia"], "resposta": 2},
        ],
        "Ciências": [
            {"pergunta": "Qual é o maior planeta do sistema solar?", "opcoes": ["Terra", "Marte", "Júpiter", "Saturno"], "resposta": 2},
            {"pergunta": "Qual parte da planta realiza a fotossíntese?", "opcoes": ["Raiz", "Caule", "Folha", "Flor"], "resposta": 2},
            {"pergunta": "Qual destes animais é um anfíbio?", "opcoes": ["Sapo", "Cachorro", "Gato", "Leão"], "resposta": 0},
            {"pergunta": "Qual destes animais é uma ave?", "opcoes": ["Cachorro", "Gato", "Papagaio", "Leão"], "resposta": 2},
            {"pergunta": "O que é um ecossistema?", "opcoes": ["Um grupo de animais", "Uma comunidade de seres vivos interagindo com o meio ambiente", "Uma árvore", "Um rio"], "resposta": 1},
            {"pergunta": "O que é um herbívoro?", "opcoes": ["Um animal que come carne", "Um animal que come plantas", "Um animal que come tudo", "Um animal que não come"], "resposta": 1},
            {"pergunta": "Qual é a função do coração?", "opcoes": ["Respirar", "Bombear sangue", "Digestão", "Mover o corpo"], "resposta": 1},
            {"pergunta": "Qual destes é um exemplo de cadeia alimentar?", "opcoes": ["Planta -> Herbívoro -> Carnívoro", "Planta -> Carnívoro -> Herbívoro", "Herbívoro -> Planta -> Carnívoro", "Carnívoro -> Herbívoro -> Planta"], "resposta": 0},
            {"pergunta": "Qual é o estado físico da água a 100°C?", "opcoes": ["Sólido", "Líquido", "Gasoso", "Plasma"], "resposta": 2},
            {"pergunta": "Qual é a função do pulmão?", "opcoes": ["Digestão", "Respiração", "Circulação", "Locomoção"], "resposta": 1},
        ],
        "História": [
            {"pergunta": "Quem proclamou a independência do Brasil?", "opcoes": ["Dom Pedro I", "Dom Pedro II", "Tiradentes", "Deodoro da Fonseca"], "resposta": 0},
            {"pergunta": "Quem foi Tiradentes?", "opcoes": ["Um pintor", "Um médico", "Um dentista e herói da Inconfidência Mineira", "Um presidente"], "resposta": 2},
            {"pergunta": "O que é uma aldeia indígena?", "opcoes": ["Um grupo de animais", "Um grupo de casas onde vivem indígenas", "Uma cidade grande", "Um tipo de planta"], "resposta": 1},
            {"pergunta": "O que é uma bandeira?", "opcoes": ["Um símbolo de um país", "Uma planta", "Um animal", "Uma montanha"], "resposta": 0},
            {"pergunta": "O que é um museu?", "opcoes": ["Um lugar onde se guardam objetos históricos", "Uma escola", "Um hospital", "Um parque"], "resposta": 0},
            {"pergunta": "Quem foi Zumbi dos Palmares?", "opcoes": ["Um líder indígena", "Um líder dos escravos", "Um presidente", "Um artista"], "resposta": 1},
            {"pergunta": "Quem foi o primeiro presidente do Brasil?", "opcoes": ["Getúlio Vargas", "Juscelino Kubitschek", "Deodoro da Fonseca", "Dom Pedro II"], "resposta": 2},
            {"pergunta": "Em que ano o Brasil foi descoberto?", "opcoes": ["1492", "1500", "1600", "1700"], "resposta": 1},
            {"pergunta": "Quem descobriu o Brasil?", "opcoes": ["Cristóvão Colombo", "Pedro Álvares Cabral", "Vasco da Gama", "Fernão de Magalhães"], "resposta": 1},
            {"pergunta": "O que eram as capitanias hereditárias?", "opcoes": ["Divisões administrativas no Brasil Colônia", "Tipos de plantações", "Grupos de indígenas", "Territórios na África"], "resposta": 0},
        ],
        "Geografia": [
            {"pergunta": "Qual é o maior país da América do Sul?", "opcoes": ["Argentina", "Brasil", "Chile", "Peru"], "resposta": 1},
            {"pergunta": "Qual desses é um rio brasileiro?", "opcoes": ["Nilo", "Amazonas", "Mississipi", "Danúbio"], "resposta": 1},
            {"pergunta": "Qual é a capital do Brasil?", "opcoes": ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador"], "resposta": 2},
            {"pergunta": "Qual é o maior país do mundo?", "opcoes": ["Estados Unidos", "China", "Rússia", "Canadá"], "resposta": 2},
            {"pergunta": "Qual continente está localizado o Brasil?", "opcoes": ["América do Sul", "América do Norte", "Europa", "África"], "resposta": 0},
            {"pergunta": "Qual é o nome do maior deserto do mundo?", "opcoes": ["Sahara", "Atacama", "Gobi", "Kalahari"], "resposta": 0},
            {"pergunta": "Qual é o menor continente?", "opcoes": ["África", "Oceania", "Antártica", "Europa"], "resposta": 1},
            {"pergunta": "Qual é o maior continente?", "opcoes": ["África", "América", "Ásia", "Europa"], "resposta": 2},
            {"pergunta": "Qual é o maior oceano?", "opcoes": ["Atlântico", "Pacífico", "Índico", "Ártico"], "resposta": 1},
            {"pergunta": "Qual país tem a maior população?", "opcoes": ["Estados Unidos", "Índia", "Brasil", "China"], "resposta": 3},
        ],
        "Computação": [
            {"pergunta": "O que é um software?", "opcoes": ["Um programa de computador", "Um hardware", "Um periférico", "Um sistema operacional"], "resposta": 0},
            {"pergunta": "Qual desses dispositivos é de entrada?", "opcoes": ["Monitor", "Impressora", "Teclado", "CPU"], "resposta": 2},
            {"pergunta": "Para que serve o mouse?", "opcoes": ["Digitar", "Selecionar itens na tela", "Armazenar dados", "Exibir imagens"], "resposta": 1},
            {"pergunta": "O que é um vírus de computador?", "opcoes": ["Um hardware", "Um software malicioso", "Um sistema operacional", "Um navegador"], "resposta": 1},
            {"pergunta": "Qual dispositivo usamos para digitar?", "opcoes": ["Mouse", "Teclado", "Monitor", "Impressora"], "resposta": 1},
            {"pergunta": "Qual parte do computador mostra as imagens?", "opcoes": ["Mouse", "Teclado", "Monitor", "CPU"], "resposta": 2},
            {"pergunta": "Qual parte do computador armazena informações?", "opcoes": ["Monitor", "Teclado", "Mouse", "HD"], "resposta": 3},
            {"pergunta": "Qual desses é um navegador de internet?", "opcoes": ["Windows", "Word", "Chrome", "Excel"], "resposta": 2},
            {"pergunta": "O que significa a sigla 'CPU'?", "opcoes": ["Central Processing Unit", "Computer Personal Unit", "Central Personal Unit", "Computer Processing Unit"], "resposta": 0},
            {"pergunta": "Qual desses é um sistema operacional?", "opcoes": ["Microsoft Word", "Google Chrome", "Windows", "Excel"], "resposta": 2},
        ],
        "Arte": [
            {"pergunta": "Qual destas é uma cor primária?", "opcoes": ["Verde", "Amarelo", "Roxo", "Laranja"], "resposta": 1},
            {"pergunta": "Qual destes é um material usado para desenhar?", "opcoes": ["Papel", "Lápis", "Tesoura", "Cola"], "resposta": 1},
            {"pergunta": "Qual destes é um artista famoso?", "opcoes": ["Leonardo da Vinci", "Isaac Newton", "Albert Einstein", "Galileu Galilei"], "resposta": 0},
            {"pergunta": "Qual destes é um estilo de dança?", "opcoes": ["Ballet", "Cálculo", "Geometria", "Física"], "resposta": 0},
            {"pergunta": "Qual destes é um instrumento musical?", "opcoes": ["Violino", "Bola", "Livro", "Computador"], "resposta": 0},
            {"pergunta": "O que usamos para pintar?", "opcoes": ["Pincel", "Cola", "Tesoura", "Borracha"], "resposta": 0},
            {"pergunta": "Qual destes é um gênero musical?", "opcoes": ["Rock", "Física", "Matemática", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destas é uma técnica de pintura?", "opcoes": ["Aquarela", "Biologia", "História", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destes é um famoso pintor?", "opcoes": ["Van Gogh", "Einstein", "Newton", "Edison"], "resposta": 0},
            {"pergunta": "Qual destas é uma forma de arte?", "opcoes": ["Escultura", "Cálculo", "Análise", "Pesquisa"], "resposta": 0},
        ]
    },
    "6° Ano": {
        "Matemática": [
            {"pergunta": "Quanto é 45 + 32?", "opcoes": ["76", "77", "78", "79"], "resposta": 2},
            {"pergunta": "Quanto é 56 - 18?", "opcoes": ["38", "39", "40", "41"], "resposta": 0},
            {"pergunta": "Quanto é 9 x 7?", "opcoes": ["62", "63", "64", "65"], "resposta": 1},
            {"pergunta": "Quanto é 81 ÷ 9?", "opcoes": ["8", "9", "10", "11"], "resposta": 1},
            {"pergunta": "Quanto é 14 x 5?", "opcoes": ["65", "66", "67", "70"], "resposta": 3},
            {"pergunta": "Quanto é 100 - 44?", "opcoes": ["55", "56", "57", "58"], "resposta": 1},
            {"pergunta": "Quanto é 36 + 28?", "opcoes": ["63", "64", "65", "66"], "resposta": 1},
            {"pergunta": "Quanto é 81 ÷ 3?", "opcoes": ["26", "27", "28", "29"], "resposta": 1},
            {"pergunta": "Quanto é 11 x 8?", "opcoes": ["87", "88", "89", "90"], "resposta": 1},
            {"pergunta": "Quanto é 64 ÷ 8?", "opcoes": ["7", "8", "9", "10"], "resposta": 1},
        ],
        "Língua Portuguesa": [
            {"pergunta": "Qual é o sinônimo de 'alegria'?", "opcoes": ["Tristeza", "Felicidade", "Raiva", "Medo"], "resposta": 1},
            {"pergunta": "Qual é o antônimo de 'rápido'?", "opcoes": ["Veloz", "Ágil", "Devagar", "Furioso"], "resposta": 2},
            {"pergunta": "Qual é o coletivo de 'peixe'?", "opcoes": ["Cardume", "Rebanho", "Bando", "Alcateia"], "resposta": 0},
            {"pergunta": "Qual é o diminutivo de 'casa'?", "opcoes": ["Casinha", "Casa", "Casão", "Casinhas"], "resposta": 0},
            {"pergunta": "Qual é o feminino de 'leão'?", "opcoes": ["Leoa", "Leona", "Leonina", "Leonita"], "resposta": 0},
            {"pergunta": "Qual é a forma correta do verbo 'cantar' no futuro do presente?", "opcoes": ["Cantarei", "Cantava", "Cantou", "Cantado"], "resposta": 0},
            {"pergunta": "Qual é o tempo verbal da frase 'Ele está cantando'?", "opcoes": ["Presente", "Pretérito", "Futuro", "Gerúndio"], "resposta": 3},
            {"pergunta": "Qual é a forma correta de conjugação do verbo 'ver' na primeira pessoa do singular no presente?", "opcoes": ["Vê", "Vejo", "Vemos", "Vês"], "resposta": 1},
            {"pergunta": "Qual é a forma correta do plural de 'cão'?", "opcoes": ["Cãos", "Cãezes", "Cães", "Cãozes"], "resposta": 2},
            {"pergunta": "Qual é o verbo da frase 'Nós estudamos matemática'?", "opcoes": ["Nós", "Estudamos", "Matemática", "Nenhuma das opções"], "resposta": 1},
        ],
        "Ciências": [
            {"pergunta": "Qual é a principal fonte de energia para a Terra?", "opcoes": ["Vento", "Água", "Sol", "Petróleo"], "resposta": 2},
            {"pergunta": "Qual é o gás essencial para a respiração humana?", "opcoes": ["Hidrogênio", "Oxigênio", "Nitrogênio", "Dióxido de carbono"], "resposta": 1},
            {"pergunta": "Qual é o maior órgão do corpo humano?", "opcoes": ["Coração", "Fígado", "Pele", "Pulmão"], "resposta": 2},
            {"pergunta": "Qual é a unidade básica da vida?", "opcoes": ["Célula", "Átomo", "Molécula", "Órgão"], "resposta": 0},
            {"pergunta": "Qual é o processo pelo qual as plantas produzem alimento?", "opcoes": ["Fotossíntese", "Respiração", "Digestão", "Transpiração"], "resposta": 0},
            {"pergunta": "Qual destes é um metal?", "opcoes": ["Ouro", "Plástico", "Vidro", "Papel"], "resposta": 0},
            {"pergunta": "Qual é o estado físico da água a 0°C?", "opcoes": ["Líquido", "Sólido", "Gasoso", "Plasma"], "resposta": 1},
            {"pergunta": "Qual é o maior planeta do sistema solar?", "opcoes": ["Terra", "Marte", "Júpiter", "Saturno"], "resposta": 2},
            {"pergunta": "Qual é a função dos pulmões?", "opcoes": ["Bombear sangue", "Filtrar sangue", "Respirar", "Digestionar"], "resposta": 2},
            {"pergunta": "Qual é a parte do corpo humano responsável pelo pensamento?", "opcoes": ["Coração", "Cérebro", "Fígado", "Estômago"], "resposta": 1},
        ],
        "História": [
            {"pergunta": "Quem foi o primeiro presidente do Brasil?", "opcoes": ["Getúlio Vargas", "Juscelino Kubitschek", "Deodoro da Fonseca", "Dom Pedro II"], "resposta": 2},
            {"pergunta": "Quem proclamou a independência do Brasil?", "opcoes": ["Dom Pedro I", "Dom Pedro II", "Tiradentes", "Deodoro da Fonseca"], "resposta": 0},
            {"pergunta": "Quem descobriu o Brasil?", "opcoes": ["Cristóvão Colombo", "Pedro Álvares Cabral", "Vasco da Gama", "Fernão de Magalhães"], "resposta": 1},
            {"pergunta": "O que foram as capitanias hereditárias?", "opcoes": ["Divisões administrativas no Brasil Colônia", "Tipos de plantações", "Grupos de indígenas", "Territórios na África"], "resposta": 0},
            {"pergunta": "Quem foi Tiradentes?", "opcoes": ["Um pintor", "Um médico", "Um dentista e herói da Inconfidência Mineira", "Um presidente"], "resposta": 2},
            {"pergunta": "Quem foi Zumbi dos Palmares?", "opcoes": ["Um líder indígena", "Um líder dos escravos", "Um presidente", "Um artista"], "resposta": 1},
            {"pergunta": "O que é uma aldeia indígena?", "opcoes": ["Um grupo de animais", "Um grupo de casas onde vivem indígenas", "Uma cidade grande", "Um tipo de planta"], "resposta": 1},
            {"pergunta": "O que é um museu?", "opcoes": ["Um lugar onde se guardam objetos históricos", "Uma escola", "Um hospital", "Um parque"], "resposta": 0},
            {"pergunta": "Quem foi o líder da Revolução Francesa?", "opcoes": ["Napoleão Bonaparte", "Louis XVI", "Robespierre", "Voltaire"], "resposta": 2},
            {"pergunta": "Quem foi o imperador romano conhecido por sua crueldade?", "opcoes": ["César", "Augusto", "Nero", "Trajano"], "resposta": 2},
        ],
        "Geografia": [
            {"pergunta": "Qual é o maior país da América do Sul?", "opcoes": ["Argentina", "Brasil", "Chile", "Peru"], "resposta": 1},
            {"pergunta": "Qual é o rio mais longo do mundo?", "opcoes": ["Nilo", "Amazonas", "Mississipi", "Yangtze"], "resposta": 0},
            {"pergunta": "Qual é a capital do Brasil?", "opcoes": ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador"], "resposta": 2},
            {"pergunta": "Qual é o maior continente?", "opcoes": ["África", "América", "Ásia", "Europa"], "resposta": 2},
            {"pergunta": "Qual é o menor continente?", "opcoes": ["África", "Oceania", "Antártica", "Europa"], "resposta": 1},
            {"pergunta": "Qual é o maior oceano?", "opcoes": ["Atlântico", "Pacífico", "Índico", "Ártico"], "resposta": 1},
            {"pergunta": "Qual é a maior floresta tropical do mundo?", "opcoes": ["Floresta Amazônica", "Floresta Negra", "Floresta de Sherwood", "Floresta de Borneo"], "resposta": 0},
            {"pergunta": "Qual país tem a maior população do mundo?", "opcoes": ["Índia", "Estados Unidos", "China", "Brasil"], "resposta": 2},
            {"pergunta": "Qual é a maior montanha do mundo?", "opcoes": ["Monte Everest", "K2", "Kangchenjunga", "Lhotse"], "resposta": 0},
            {"pergunta": "Qual é a capital da França?", "opcoes": ["Londres", "Paris", "Berlim", "Roma"], "resposta": 1},
        ],
        "Computação": [
            {"pergunta": "O que é um software?", "opcoes": ["Um programa de computador", "Um hardware", "Um periférico", "Um sistema operacional"], "resposta": 0},
            {"pergunta": "Qual desses dispositivos é de entrada?", "opcoes": ["Monitor", "Impressora", "Teclado", "CPU"], "resposta": 2},
            {"pergunta": "Para que serve o mouse?", "opcoes": ["Digitar", "Selecionar itens na tela", "Armazenar dados", "Exibir imagens"], "resposta": 1},
            {"pergunta": "O que é um vírus de computador?", "opcoes": ["Um hardware", "Um software malicioso", "Um sistema operacional", "Um navegador"], "resposta": 1},
            {"pergunta": "Qual dispositivo usamos para digitar?", "opcoes": ["Mouse", "Teclado", "Monitor", "Impressora"], "resposta": 1},
            {"pergunta": "Qual parte do computador mostra as imagens?", "opcoes": ["Mouse", "Teclado", "Monitor", "CPU"], "resposta": 2},
            {"pergunta": "Qual parte do computador armazena informações?", "opcoes": ["Monitor", "Teclado", "Mouse", "HD"], "resposta": 3},
            {"pergunta": "Qual desses é um navegador de internet?", "opcoes": ["Windows", "Word", "Chrome", "Excel"], "resposta": 2},
            {"pergunta": "O que significa a sigla 'CPU'?", "opcoes": ["Central Processing Unit", "Computer Personal Unit", "Central Personal Unit", "Computer Processing Unit"], "resposta": 0},
            {"pergunta": "Qual desses é um sistema operacional?", "opcoes": ["Microsoft Word", "Google Chrome", "Windows", "Excel"], "resposta": 2},
        ],
        "Arte": [
            {"pergunta": "Qual destas é uma cor primária?", "opcoes": ["Verde", "Amarelo", "Roxo", "Laranja"], "resposta": 1},
            {"pergunta": "Qual destes é um material usado para desenhar?", "opcoes": ["Papel", "Lápis", "Tesoura", "Cola"], "resposta": 1},
            {"pergunta": "Qual destes é um artista famoso?", "opcoes": ["Leonardo da Vinci", "Isaac Newton", "Albert Einstein", "Galileu Galilei"], "resposta": 0},
            {"pergunta": "Qual destes é um estilo de dança?", "opcoes": ["Ballet", "Cálculo", "Geometria", "Física"], "resposta": 0},
            {"pergunta": "Qual destes é um instrumento musical?", "opcoes": ["Violino", "Bola", "Livro", "Computador"], "resposta": 0},
            {"pergunta": "O que usamos para pintar?", "opcoes": ["Pincel", "Cola", "Tesoura", "Borracha"], "resposta": 0},
            {"pergunta": "Qual destes é um gênero musical?", "opcoes": ["Rock", "Física", "Matemática", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destas é uma técnica de pintura?", "opcoes": ["Aquarela", "Biologia", "História", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destes é um famoso pintor?", "opcoes": ["Van Gogh", "Einstein", "Newton", "Edison"], "resposta": 0},
            {"pergunta": "Qual destas é uma forma de arte?", "opcoes": ["Escultura", "Cálculo", "Análise", "Pesquisa"], "resposta": 0},
        ]
    },
    "7° Ano": {
        "Matemática": [
            {"pergunta": "Quanto é 123 + 456?", "opcoes": ["579", "589", "599", "609"], "resposta": 0},
            {"pergunta": "Quanto é 789 - 321?", "opcoes": ["468", "478", "488", "498"], "resposta": 1},
            {"pergunta": "Quanto é 12 x 12?", "opcoes": ["144", "154", "164", "174"], "resposta": 0},
            {"pergunta": "Quanto é 144 ÷ 12?", "opcoes": ["10", "11", "12", "13"], "resposta": 2},
            {"pergunta": "Qual é a raiz quadrada de 81?", "opcoes": ["7", "8", "9", "10"], "resposta": 2},
            {"pergunta": "Quanto é 11²?", "opcoes": ["120", "121", "122", "123"], "resposta": 1},
            {"pergunta": "Qual é a área de um quadrado de lado 5?", "opcoes": ["20", "25", "30", "35"], "resposta": 1},
            {"pergunta": "Quanto é 15 x 3?", "opcoes": ["45", "50", "55", "60"], "resposta": 0},
            {"pergunta": "Quanto é 60 ÷ 5?", "opcoes": ["10", "11", "12", "13"], "resposta": 2},
            {"pergunta": "Qual é o perímetro de um triângulo de lados 3, 4 e 5?", "opcoes": ["10", "11", "12", "13"], "resposta": 2},
        ],
        "Língua Portuguesa": [
            {"pergunta": "Qual é o sinônimo de 'inteligente'?", "opcoes": ["Burro", "Esperto", "Rápido", "Lento"], "resposta": 1},
            {"pergunta": "Qual é o antônimo de 'alegria'?", "opcoes": ["Felicidade", "Tristeza", "Raiva", "Amor"], "resposta": 1},
            {"pergunta": "Qual é o coletivo de 'livro'?", "opcoes": ["Biblioteca", "Livraria", "Estante", "Livros"], "resposta": 0},
            {"pergunta": "Qual é o diminutivo de 'flor'?", "opcoes": ["Florinha", "Florzinhas", "Florzinha", "Florões"], "resposta": 2},
            {"pergunta": "Qual é o feminino de 'ator'?", "opcoes": ["Atora", "Atriz", "Atoresa", "Atoriza"], "resposta": 1},
            {"pergunta": "Qual é a forma correta do verbo 'correr' no pretérito perfeito?", "opcoes": ["Correu", "Corri", "Corria", "Corrido"], "resposta": 0},
            {"pergunta": "Qual é o tempo verbal da frase 'Nós estudamos ontem'?", "opcoes": ["Presente", "Pretérito", "Futuro", "Gerúndio"], "resposta": 1},
            {"pergunta": "Qual é a forma correta de conjugação do verbo 'estar' na primeira pessoa do singular no presente?", "opcoes": ["Está", "Estás", "Estou", "Estava"], "resposta": 2},
            {"pergunta": "Qual é a forma correta do plural de 'pão'?", "opcoes": ["Pães", "Pãos", "Pãozes", "Pãozões"], "resposta": 0},
            {"pergunta": "Qual é o verbo da frase 'Eles correram para o parque'?", "opcoes": ["Eles", "Correram", "Para", "Parque"], "resposta": 1},
        ],
        "Ciências": [
            {"pergunta": "Qual é o principal componente da água?", "opcoes": ["Hidrogênio", "Oxigênio", "Nitrogênio", "Carbono"], "resposta": 0},
            {"pergunta": "Qual é a função do coração?", "opcoes": ["Respirar", "Bombear sangue", "Digestão", "Mastigação"], "resposta": 1},
            {"pergunta": "Qual é o processo de conversão de água em vapor?", "opcoes": ["Condensação", "Evaporação", "Sublimação", "Solidificação"], "resposta": 1},
            {"pergunta": "Qual destes é um exemplo de fonte de energia renovável?", "opcoes": ["Carvão", "Petróleo", "Vento", "Gás natural"], "resposta": 2},
            {"pergunta": "Qual é o planeta mais próximo do Sol?", "opcoes": ["Marte", "Terra", "Vênus", "Mercúrio"], "resposta": 3},
            {"pergunta": "Qual é o maior animal terrestre?", "opcoes": ["Elefante", "Girafa", "Rinoceronte", "Hipopótamo"], "resposta": 0},
            {"pergunta": "Qual é o processo pelo qual as plantas produzem oxigênio?", "opcoes": ["Fotossíntese", "Respiração", "Transpiração", "Digestão"], "resposta": 0},
            {"pergunta": "Qual é o estado físico da água a 0°C?", "opcoes": ["Líquido", "Sólido", "Gasoso", "Plasma"], "resposta": 1},
            {"pergunta": "Qual é a principal função dos rins?", "opcoes": ["Bombear sangue", "Filtrar sangue", "Respiração", "Digestão"], "resposta": 1},
            {"pergunta": "Qual é a unidade básica da vida?", "opcoes": ["Célula", "Átomo", "Molécula", "Organismo"], "resposta": 0},
        ],
        "História": [
            {"pergunta": "Quem foi o primeiro presidente do Brasil?", "opcoes": ["Getúlio Vargas", "Juscelino Kubitschek", "Deodoro da Fonseca", "Dom Pedro II"], "resposta": 2},
            {"pergunta": "Quem proclamou a independência do Brasil?", "opcoes": ["Dom Pedro I", "Dom Pedro II", "Tiradentes", "Deodoro da Fonseca"], "resposta": 0},
            {"pergunta": "Quem descobriu o Brasil?", "opcoes": ["Cristóvão Colombo", "Pedro Álvares Cabral", "Vasco da Gama", "Fernão de Magalhães"], "resposta": 1},
            {"pergunta": "O que foram as capitanias hereditárias?", "opcoes": ["Divisões administrativas no Brasil Colônia", "Tipos de plantações", "Grupos de indígenas", "Territórios na África"], "resposta": 0},
            {"pergunta": "Quem foi Tiradentes?", "opcoes": ["Um pintor", "Um médico", "Um dentista e herói da Inconfidência Mineira", "Um presidente"], "resposta": 2},
            {"pergunta": "Quem foi Zumbi dos Palmares?", "opcoes": ["Um líder indígena", "Um líder dos escravos", "Um presidente", "Um artista"], "resposta": 1},
            {"pergunta": "O que é uma aldeia indígena?", "opcoes": ["Um grupo de animais", "Um grupo de casas onde vivem indígenas", "Uma cidade grande", "Um tipo de planta"], "resposta": 1},
            {"pergunta": "O que é um museu?", "opcoes": ["Um lugar onde se guardam objetos históricos", "Uma escola", "Um hospital", "Um parque"], "resposta": 0},
            {"pergunta": "Quem foi o líder da Revolução Francesa?", "opcoes": ["Napoleão Bonaparte", "Louis XVI", "Robespierre", "Voltaire"], "resposta": 2},
            {"pergunta": "Quem foi o imperador romano conhecido por sua crueldade?", "opcoes": ["César", "Augusto", "Nero", "Trajano"], "resposta": 2},
        ],
        "Geografia": [
            {"pergunta": "Qual é o maior país da América do Sul?", "opcoes": ["Argentina", "Brasil", "Chile", "Peru"], "resposta": 1},
            {"pergunta": "Qual é o rio mais longo do mundo?", "opcoes": ["Nilo", "Amazonas", "Mississipi", "Yangtze"], "resposta": 0},
            {"pergunta": "Qual é a capital do Brasil?", "opcoes": ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador"], "resposta": 2},
            {"pergunta": "Qual é o maior continente?", "opcoes": ["África", "América", "Ásia", "Europa"], "resposta": 2},
            {"pergunta": "Qual é o menor continente?", "opcoes": ["África", "Oceania", "Antártica", "Europa"], "resposta": 1},
            {"pergunta": "Qual é o maior oceano?", "opcoes": ["Atlântico", "Pacífico", "Índico", "Ártico"], "resposta": 1},
            {"pergunta": "Qual é a maior floresta tropical do mundo?", "opcoes": ["Floresta Amazônica", "Floresta Negra", "Floresta de Sherwood", "Floresta de Borneo"], "resposta": 0},
            {"pergunta": "Qual país tem a maior população do mundo?", "opcoes": ["Índia", "Estados Unidos", "China", "Brasil"], "resposta": 2},
            {"pergunta": "Qual é a maior montanha do mundo?", "opcoes": ["Monte Everest", "K2", "Kangchenjunga", "Lhotse"], "resposta": 0},
            {"pergunta": "Qual é a capital da França?", "opcoes": ["Londres", "Paris", "Berlim", "Roma"], "resposta": 1},
        ],
        "Computação": [
            {"pergunta": "O que é um software?", "opcoes": ["Um programa de computador", "Um hardware", "Um periférico", "Um sistema operacional"], "resposta": 0},
            {"pergunta": "Qual desses dispositivos é de entrada?", "opcoes": ["Monitor", "Impressora", "Teclado", "CPU"], "resposta": 2},
            {"pergunta": "Para que serve o mouse?", "opcoes": ["Digitar", "Selecionar itens na tela", "Armazenar dados", "Exibir imagens"], "resposta": 1},
            {"pergunta": "O que é um vírus de computador?", "opcoes": ["Um hardware", "Um software malicioso", "Um sistema operacional", "Um navegador"], "resposta": 1},
            {"pergunta": "Qual dispositivo usamos para digitar?", "opcoes": ["Mouse", "Teclado", "Monitor", "Impressora"], "resposta": 1},
            {"pergunta": "Qual parte do computador mostra as imagens?", "opcoes": ["Mouse", "Teclado", "Monitor", "CPU"], "resposta": 2},
            {"pergunta": "Qual parte do computador armazena informações?", "opcoes": ["Monitor", "Teclado", "Mouse", "HD"], "resposta": 3},
            {"pergunta": "Qual desses é um navegador de internet?", "opcoes": ["Windows", "Word", "Chrome", "Excel"], "resposta": 2},
            {"pergunta": "O que significa a sigla 'CPU'?", "opcoes": ["Central Processing Unit", "Computer Personal Unit", "Central Personal Unit", "Computer Processing Unit"], "resposta": 0},
            {"pergunta": "Qual desses é um sistema operacional?", "opcoes": ["Microsoft Word", "Google Chrome", "Windows", "Excel"], "resposta": 2},
        ],
        "Arte": [
            {"pergunta": "Qual destas é uma cor primária?", "opcoes": ["Verde", "Amarelo", "Roxo", "Laranja"], "resposta": 1},
            {"pergunta": "Qual destes é um material usado para desenhar?", "opcoes": ["Papel", "Lápis", "Tesoura", "Cola"], "resposta": 1},
            {"pergunta": "Qual destes é um artista famoso?", "opcoes": ["Leonardo da Vinci", "Isaac Newton", "Albert Einstein", "Galileu Galilei"], "resposta": 0},
            {"pergunta": "Qual destes é um estilo de dança?", "opcoes": ["Ballet", "Cálculo", "Geometria", "Física"], "resposta": 0},
            {"pergunta": "Qual destes é um instrumento musical?", "opcoes": ["Violino", "Bola", "Livro", "Computador"], "resposta": 0},
            {"pergunta": "O que usamos para pintar?", "opcoes": ["Pincel", "Cola", "Tesoura", "Borracha"], "resposta": 0},
            {"pergunta": "Qual destes é um gênero musical?", "opcoes": ["Rock", "Física", "Matemática", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destas é uma técnica de pintura?", "opcoes": ["Aquarela", "Biologia", "História", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destes é um famoso pintor?", "opcoes": ["Van Gogh", "Einstein", "Newton", "Edison"], "resposta": 0},
            {"pergunta": "Qual destas é uma forma de arte?", "opcoes": ["Escultura", "Cálculo", "Análise", "Pesquisa"], "resposta": 0},
        ]
    },
    "8° Ano": {
        "Matemática": [
            {"pergunta": "Quanto é 245 + 367?", "opcoes": ["602", "612", "622", "632"], "resposta": 2},
            {"pergunta": "Quanto é 543 - 278?", "opcoes": ["264", "265", "266", "267"], "resposta": 3},
            {"pergunta": "Quanto é 23 x 12?", "opcoes": ["276", "277", "278", "279"], "resposta": 0},
            {"pergunta": "Quanto é 256 ÷ 8?", "opcoes": ["31", "32", "33", "34"], "resposta": 1},
            {"pergunta": "Qual é a raiz quadrada de 121?", "opcoes": ["10", "11", "12", "13"], "resposta": 1},
            {"pergunta": "Quanto é 13²?", "opcoes": ["168", "169", "170", "171"], "resposta": 1},
            {"pergunta": "Qual é a área de um triângulo de base 6 e altura 8?", "opcoes": ["24", "25", "26", "27"], "resposta": 0},
            {"pergunta": "Quanto é 48 x 3?", "opcoes": ["140", "141", "142", "144"], "resposta": 3},
            {"pergunta": "Quanto é 144 ÷ 6?", "opcoes": ["22", "23", "24", "25"], "resposta": 2},
            {"pergunta": "Qual é o perímetro de um quadrado de lado 7?", "opcoes": ["27", "28", "29", "30"], "resposta": 1},
        ],
        "Língua Portuguesa": [
            {"pergunta": "Qual é o sinônimo de 'coragem'?", "opcoes": ["Medo", "Valentia", "Covardia", "Preguiça"], "resposta": 1},
            {"pergunta": "Qual é o antônimo de 'verdade'?", "opcoes": ["Mentira", "Fato", "Realidade", "Sinceridade"], "resposta": 0},
            {"pergunta": "Qual é o coletivo de 'lobo'?", "opcoes": ["Manada", "Bando", "Alcateia", "Grupo"], "resposta": 2},
            {"pergunta": "Qual é o diminutivo de 'passarinho'?", "opcoes": ["Passarote", "Passarote", "Passarote", "Passarote"], "resposta": 2},
            {"pergunta": "Qual é o feminino de 'elefante'?", "opcoes": ["Elefoa", "Elefanta", "Elefantona", "Elefoa"], "resposta": 1},
            {"pergunta": "Qual é a forma correta do verbo 'comer' no futuro do pretérito?", "opcoes": ["Comerá", "Comeria", "Comerei", "Comer"], "resposta": 1},
            {"pergunta": "Qual é o tempo verbal da frase 'Eles haviam terminado a tarefa'?", "opcoes": ["Presente", "Pretérito Mais-que-Perfeito", "Pretérito Perfeito", "Futuro"], "resposta": 1},
            {"pergunta": "Qual é a forma correta de conjugação do verbo 'ir' na primeira pessoa do singular no futuro?", "opcoes": ["Irei", "Vou", "Ia", "Irei"], "resposta": 0},
            {"pergunta": "Qual é a forma correta do plural de 'mão'?", "opcoes": ["Mãos", "Mãos", "Mãos", "Mãos"], "resposta": 0},
            {"pergunta": "Qual é o verbo da frase 'Nós cantaremos na festa'?", "opcoes": ["Nós", "Cantaremos", "Na", "Festa"], "resposta": 1},
        ],
        "Ciências": [
            {"pergunta": "Qual é o principal componente do ar?", "opcoes": ["Oxigênio", "Nitrogênio", "Dióxido de carbono", "Hidrogênio"], "resposta": 1},
            {"pergunta": "Qual é a função dos músculos?", "opcoes": ["Respiração", "Movimento", "Digestão", "Circulação"], "resposta": 1},
            {"pergunta": "Qual é o processo de transformação de gás em líquido?", "opcoes": ["Evaporação", "Sublimação", "Condensação", "Solidificação"], "resposta": 2},
            {"pergunta": "Qual destes é um exemplo de fonte de energia não renovável?", "opcoes": ["Solar", "Eólica", "Hidrelétrica", "Petróleo"], "resposta": 3},
            {"pergunta": "Qual é o planeta mais distante do Sol?", "opcoes": ["Netuno", "Urano", "Saturno", "Júpiter"], "resposta": 0},
            {"pergunta": "Qual é o maior animal aquático?", "opcoes": ["Baleia Azul", "Tubarão Branco", "Golfinho", "Polvo"], "resposta": 0},
            {"pergunta": "Qual é o processo pelo qual os seres vivos se multiplicam?", "opcoes": ["Respiração", "Reprodução", "Digestão", "Locomoção"], "resposta": 1},
            {"pergunta": "Qual é o estado físico da água a 100°C?", "opcoes": ["Líquido", "Sólido", "Gasoso", "Plasma"], "resposta": 2},
            {"pergunta": "Qual é a principal função do fígado?", "opcoes": ["Produzir bile", "Respiração", "Bombear sangue", "Filtrar sangue"], "resposta": 0},
            {"pergunta": "Qual é a unidade básica dos seres vivos?", "opcoes": ["Átomo", "Molécula", "Célula", "Órgão"], "resposta": 2},
        ],
        "História": [
            {"pergunta": "Quem foi o primeiro presidente do Brasil?", "opcoes": ["Getúlio Vargas", "Juscelino Kubitschek", "Deodoro da Fonseca", "Dom Pedro II"], "resposta": 2},
            {"pergunta": "Quem proclamou a independência do Brasil?", "opcoes": ["Dom Pedro I", "Dom Pedro II", "Tiradentes", "Deodoro da Fonseca"], "resposta": 0},
            {"pergunta": "Quem descobriu o Brasil?", "opcoes": ["Cristóvão Colombo", "Pedro Álvares Cabral", "Vasco da Gama", "Fernão de Magalhães"], "resposta": 1},
            {"pergunta": "O que foram as capitanias hereditárias?", "opcoes": ["Divisões administrativas no Brasil Colônia", "Tipos de plantações", "Grupos de indígenas", "Territórios na África"], "resposta": 0},
            {"pergunta": "Quem foi Tiradentes?", "opcoes": ["Um pintor", "Um médico", "Um dentista e herói da Inconfidência Mineira", "Um presidente"], "resposta": 2},
            {"pergunta": "Quem foi Zumbi dos Palmares?", "opcoes": ["Um líder indígena", "Um líder dos escravos", "Um presidente", "Um artista"], "resposta": 1},
            {"pergunta": "O que é uma aldeia indígena?", "opcoes": ["Um grupo de animais", "Um grupo de casas onde vivem indígenas", "Uma cidade grande", "Um tipo de planta"], "resposta": 1},
            {"pergunta": "O que é um museu?", "opcoes": ["Um lugar onde se guardam objetos históricos", "Uma escola", "Um hospital", "Um parque"], "resposta": 0},
            {"pergunta": "Quem foi o líder da Revolução Francesa?", "opcoes": ["Napoleão Bonaparte", "Louis XVI", "Robespierre", "Voltaire"], "resposta": 2},
            {"pergunta": "Quem foi o imperador romano conhecido por sua crueldade?", "opcoes": ["César", "Augusto", "Nero", "Trajano"], "resposta": 2},
        ],
        "Geografia": [
            {"pergunta": "Qual é o maior país da América do Sul?", "opcoes": ["Argentina", "Brasil", "Chile", "Peru"], "resposta": 1},
            {"pergunta": "Qual é o rio mais longo do mundo?", "opcoes": ["Nilo", "Amazonas", "Mississipi", "Yangtze"], "resposta": 0},
            {"pergunta": "Qual é a capital do Brasil?", "opcoes": ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador"], "resposta": 2},
            {"pergunta": "Qual é o maior continente?", "opcoes": ["África", "América", "Ásia", "Europa"], "resposta": 2},
            {"pergunta": "Qual é o menor continente?", "opcoes": ["África", "Oceania", "Antártica", "Europa"], "resposta": 1},
            {"pergunta": "Qual é o maior oceano?", "opcoes": ["Atlântico", "Pacífico", "Índico", "Ártico"], "resposta": 1},
            {"pergunta": "Qual é a maior floresta tropical do mundo?", "opcoes": ["Floresta Amazônica", "Floresta Negra", "Floresta de Sherwood", "Floresta de Borneo"], "resposta": 0},
            {"pergunta": "Qual país tem a maior população do mundo?", "opcoes": ["Índia", "Estados Unidos", "China", "Brasil"], "resposta": 2},
            {"pergunta": "Qual é a maior montanha do mundo?", "opcoes": ["Monte Everest", "K2", "Kangchenjunga", "Lhotse"], "resposta": 0},
            {"pergunta": "Qual é a capital da França?", "opcoes": ["Londres", "Paris", "Berlim", "Roma"], "resposta": 1},
        ],
        "Computação": [
            {"pergunta": "O que é um software?", "opcoes": ["Um programa de computador", "Um hardware", "Um periférico", "Um sistema operacional"], "resposta": 0},
            {"pergunta": "Qual desses dispositivos é de entrada?", "opcoes": ["Monitor", "Impressora", "Teclado", "CPU"], "resposta": 2},
            {"pergunta": "Para que serve o mouse?", "opcoes": ["Digitar", "Selecionar itens na tela", "Armazenar dados", "Exibir imagens"], "resposta": 1},
            {"pergunta": "O que é um vírus de computador?", "opcoes": ["Um hardware", "Um software malicioso", "Um sistema operacional", "Um navegador"], "resposta": 1},
            {"pergunta": "Qual dispositivo usamos para digitar?", "opcoes": ["Mouse", "Teclado", "Monitor", "Impressora"], "resposta": 1},
            {"pergunta": "Qual parte do computador mostra as imagens?", "opcoes": ["Mouse", "Teclado", "Monitor", "CPU"], "resposta": 2},
            {"pergunta": "Qual parte do computador armazena informações?", "opcoes": ["Monitor", "Teclado", "Mouse", "HD"], "resposta": 3},
            {"pergunta": "Qual desses é um navegador de internet?", "opcoes": ["Windows", "Word", "Chrome", "Excel"], "resposta": 2},
            {"pergunta": "O que significa a sigla 'CPU'?", "opcoes": ["Central Processing Unit", "Computer Personal Unit", "Central Personal Unit", "Computer Processing Unit"], "resposta": 0},
            {"pergunta": "Qual desses é um sistema operacional?", "opcoes": ["Microsoft Word", "Google Chrome", "Windows", "Excel"], "resposta": 2},
        ],
        "Arte": [
            {"pergunta": "Qual destas é uma cor primária?", "opcoes": ["Verde", "Amarelo", "Roxo", "Laranja"], "resposta": 1},
            {"pergunta": "Qual destes é um material usado para desenhar?", "opcoes": ["Papel", "Lápis", "Tesoura", "Cola"], "resposta": 1},
            {"pergunta": "Qual destes é um artista famoso?", "opcoes": ["Leonardo da Vinci", "Isaac Newton", "Albert Einstein", "Galileu Galilei"], "resposta": 0},
            {"pergunta": "Qual destes é um estilo de dança?", "opcoes": ["Ballet", "Cálculo", "Geometria", "Física"], "resposta": 0},
            {"pergunta": "Qual destes é um instrumento musical?", "opcoes": ["Violino", "Bola", "Livro", "Computador"], "resposta": 0},
            {"pergunta": "O que usamos para pintar?", "opcoes": ["Pincel", "Cola", "Tesoura", "Borracha"], "resposta": 0},
            {"pergunta": "Qual destes é um gênero musical?", "opcoes": ["Rock", "Física", "Matemática", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destas é uma técnica de pintura?", "opcoes": ["Aquarela", "Biologia", "História", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destes é um famoso pintor?", "opcoes": ["Van Gogh", "Einstein", "Newton", "Edison"], "resposta": 0},
            {"pergunta": "Qual destas é uma forma de arte?", "opcoes": ["Escultura", "Cálculo", "Análise", "Pesquisa"], "resposta": 0},
        ]
    },
    "9° Ano": {
        "Matemática": [
            {"pergunta": "Quanto é 348 + 567?", "opcoes": ["914", "915", "916", "917"], "resposta": 2},
            {"pergunta": "Quanto é 725 - 418?", "opcoes": ["306", "307", "308", "309"], "resposta": 3},
            {"pergunta": "Quanto é 34 x 15?", "opcoes": ["509", "510", "511", "512"], "resposta": 1},
            {"pergunta": "Quanto é 512 ÷ 8?", "opcoes": ["62", "63", "64", "65"], "resposta": 2},
            {"pergunta": "Qual é a raiz quadrada de 144?", "opcoes": ["10", "11", "12", "13"], "resposta": 2},
            {"pergunta": "Quanto é 14²?", "opcoes": ["194", "195", "196", "197"], "resposta": 2},
            {"pergunta": "Qual é a área de um retângulo de lados 8 e 12?", "opcoes": ["94", "95", "96", "97"], "resposta": 2},
            {"pergunta": "Quanto é 64 x 4?", "opcoes": ["254", "255", "256", "257"], "resposta": 2},
            {"pergunta": "Quanto é 192 ÷ 6?", "opcoes": ["30", "31", "32", "33"], "resposta": 2},
            {"pergunta": "Qual é o perímetro de um triângulo de lados 5, 12 e 13?", "opcoes": ["28", "29", "30", "31"], "resposta": 2},
        ],
        "Língua Portuguesa": [
            {"pergunta": "Qual é o sinônimo de 'audaz'?", "opcoes": ["Covarde", "Valente", "Medroso", "Preguiçoso"], "resposta": 1},
            {"pergunta": "Qual é o antônimo de 'paz'?", "opcoes": ["Tranquilidade", "Guerra", "Calma", "Harmonia"], "resposta": 1},
            {"pergunta": "Qual é o coletivo de 'cão'?", "opcoes": ["Matilha", "Rebanho", "Bando", "Alcateia"], "resposta": 0},
            {"pergunta": "Qual é o diminutivo de 'livro'?", "opcoes": ["Livrote", "Livrinho", "Livrões", "Livretos"], "resposta": 1},
            {"pergunta": "Qual é o feminino de 'rei'?", "opcoes": ["Rei", "Rainha", "Reis", "Reia"], "resposta": 1},
            {"pergunta": "Qual é a forma correta do verbo 'fazer' no futuro do presente?", "opcoes": ["Faria", "Faço", "Farei", "Fazer"], "resposta": 2},
            {"pergunta": "Qual é o tempo verbal da frase 'Nós estudaremos amanhã'?", "opcoes": ["Presente", "Pretérito", "Futuro", "Gerúndio"], "resposta": 2},
            {"pergunta": "Qual é a forma correta de conjugação do verbo 'vir' na primeira pessoa do singular no presente?", "opcoes": ["Vem", "Vens", "Venho", "Vim"], "resposta": 2},
            {"pergunta": "Qual é a forma correta do plural de 'pão'?", "opcoes": ["Pães", "Pãos", "Pãozes", "Pãozões"], "resposta": 0},
            {"pergunta": "Qual é o verbo da frase 'Eles escreverão o relatório'?", "opcoes": ["Eles", "Escreverão", "O", "Relatório"], "resposta": 1},
        ],
        "Ciências": [
            {"pergunta": "Qual é o principal componente da água?", "opcoes": ["Hidrogênio", "Oxigênio", "Nitrogênio", "Carbono"], "resposta": 0},
            {"pergunta": "Qual é a função do coração?", "opcoes": ["Respirar", "Bombear sangue", "Digestão", "Mastigação"], "resposta": 1},
            {"pergunta": "Qual é o processo de conversão de água em vapor?", "opcoes": ["Condensação", "Evaporação", "Sublimação", "Solidificação"], "resposta": 1},
            {"pergunta": "Qual destes é um exemplo de fonte de energia renovável?", "opcoes": ["Carvão", "Petróleo", "Vento", "Gás natural"], "resposta": 2},
            {"pergunta": "Qual é o planeta mais próximo do Sol?", "opcoes": ["Marte", "Terra", "Vênus", "Mercúrio"], "resposta": 3},
            {"pergunta": "Qual é o maior animal terrestre?", "opcoes": ["Elefante", "Girafa", "Rinoceronte", "Hipopótamo"], "resposta": 0},
            {"pergunta": "Qual é o processo pelo qual as plantas produzem oxigênio?", "opcoes": ["Fotossíntese", "Respiração", "Transpiração", "Digestão"], "resposta": 0},
            {"pergunta": "Qual é o estado físico da água a 0°C?", "opcoes": ["Líquido", "Sólido", "Gasoso", "Plasma"], "resposta": 1},
            {"pergunta": "Qual é a principal função dos rins?", "opcoes": ["Bombear sangue", "Filtrar sangue", "Respiração", "Digestão"], "resposta": 1},
            {"pergunta": "Qual é a unidade básica da vida?", "opcoes": ["Célula", "Átomo", "Molécula", "Organismo"], "resposta": 0},
        ],
        "História": [
            {"pergunta": "Quem foi o primeiro presidente do Brasil?", "opcoes": ["Getúlio Vargas", "Juscelino Kubitschek", "Deodoro da Fonseca", "Dom Pedro II"], "resposta": 2},
            {"pergunta": "Quem proclamou a independência do Brasil?", "opcoes": ["Dom Pedro I", "Dom Pedro II", "Tiradentes", "Deodoro da Fonseca"], "resposta": 0},
            {"pergunta": "Quem descobriu o Brasil?", "opcoes": ["Cristóvão Colombo", "Pedro Álvares Cabral", "Vasco da Gama", "Fernão de Magalhães"], "resposta": 1},
            {"pergunta": "O que foram as capitanias hereditárias?", "opcoes": ["Divisões administrativas no Brasil Colônia", "Tipos de plantações", "Grupos de indígenas", "Territórios na África"], "resposta": 0},
            {"pergunta": "Quem foi Tiradentes?", "opcoes": ["Um pintor", "Um médico", "Um dentista e herói da Inconfidência Mineira", "Um presidente"], "resposta": 2},
            {"pergunta": "Quem foi Zumbi dos Palmares?", "opcoes": ["Um líder indígena", "Um líder dos escravos", "Um presidente", "Um artista"], "resposta": 1},
            {"pergunta": "O que é uma aldeia indígena?", "opcoes": ["Um grupo de animais", "Um grupo de casas onde vivem indígenas", "Uma cidade grande", "Um tipo de planta"], "resposta": 1},
            {"pergunta": "O que é um museu?", "opcoes": ["Um lugar onde se guardam objetos históricos", "Uma escola", "Um hospital", "Um parque"], "resposta": 0},
            {"pergunta": "Quem foi o líder da Revolução Francesa?", "opcoes": ["Napoleão Bonaparte", "Louis XVI", "Robespierre", "Voltaire"], "resposta": 2},
            {"pergunta": "Quem foi o imperador romano conhecido por sua crueldade?", "opcoes": ["César", "Augusto", "Nero", "Trajano"], "resposta": 2},
        ],
        "Geografia": [
            {"pergunta": "Qual é o maior país da América do Sul?", "opcoes": ["Argentina", "Brasil", "Chile", "Peru"], "resposta": 1},
            {"pergunta": "Qual é o rio mais longo do mundo?", "opcoes": ["Nilo", "Amazonas", "Mississipi", "Yangtze"], "resposta": 0},
            {"pergunta": "Qual é a capital do Brasil?", "opcoes": ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador"], "resposta": 2},
            {"pergunta": "Qual é o maior continente?", "opcoes": ["África", "América", "Ásia", "Europa"], "resposta": 2},
            {"pergunta": "Qual é o menor continente?", "opcoes": ["África", "Oceania", "Antártica", "Europa"], "resposta": 1},
            {"pergunta": "Qual é o maior oceano?", "opcoes": ["Atlântico", "Pacífico", "Índico", "Ártico"], "resposta": 1},
            {"pergunta": "Qual é a maior floresta tropical do mundo?", "opcoes": ["Floresta Amazônica", "Floresta Negra", "Floresta de Sherwood", "Floresta de Borneo"], "resposta": 0},
            {"pergunta": "Qual país tem a maior população do mundo?", "opcoes": ["Índia", "Estados Unidos", "China", "Brasil"], "resposta": 2},
            {"pergunta": "Qual é a maior montanha do mundo?", "opcoes": ["Monte Everest", "K2", "Kangchenjunga", "Lhotse"], "resposta": 0},
            {"pergunta": "Qual é a capital da França?", "opcoes": ["Londres", "Paris", "Berlim", "Roma"], "resposta": 1},
        ],
        "Computação": [
            {"pergunta": "O que é um software?", "opcoes": ["Um programa de computador", "Um hardware", "Um periférico", "Um sistema operacional"], "resposta": 0},
            {"pergunta": "Qual desses dispositivos é de entrada?", "opcoes": ["Monitor", "Impressora", "Teclado", "CPU"], "resposta": 2},
            {"pergunta": "Para que serve o mouse?", "opcoes": ["Digitar", "Selecionar itens na tela", "Armazenar dados", "Exibir imagens"], "resposta": 1},
            {"pergunta": "O que é um vírus de computador?", "opcoes": ["Um hardware", "Um software malicioso", "Um sistema operacional", "Um navegador"], "resposta": 1},
            {"pergunta": "Qual dispositivo usamos para digitar?", "opcoes": ["Mouse", "Teclado", "Monitor", "Impressora"], "resposta": 1},
            {"pergunta": "Qual parte do computador mostra as imagens?", "opcoes": ["Mouse", "Teclado", "Monitor", "CPU"], "resposta": 2},
            {"pergunta": "Qual parte do computador armazena informações?", "opcoes": ["Monitor", "Teclado", "Mouse", "HD"], "resposta": 3},
            {"pergunta": "Qual desses é um navegador de internet?", "opcoes": ["Windows", "Word", "Chrome", "Excel"], "resposta": 2},
            {"pergunta": "O que significa a sigla 'CPU'?", "opcoes": ["Central Processing Unit", "Computer Personal Unit", "Central Personal Unit", "Computer Processing Unit"], "resposta": 0},
            {"pergunta": "Qual desses é um sistema operacional?", "opcoes": ["Microsoft Word", "Google Chrome", "Windows", "Excel"], "resposta": 2},
        ],
        "Arte": [
            {"pergunta": "Qual destas é uma cor primária?", "opcoes": ["Verde", "Amarelo", "Roxo", "Laranja"], "resposta": 1},
            {"pergunta": "Qual destes é um material usado para desenhar?", "opcoes": ["Papel", "Lápis", "Tesoura", "Cola"], "resposta": 1},
            {"pergunta": "Qual destes é um artista famoso?", "opcoes": ["Leonardo da Vinci", "Isaac Newton", "Albert Einstein", "Galileu Galilei"], "resposta": 0},
            {"pergunta": "Qual destes é um estilo de dança?", "opcoes": ["Ballet", "Cálculo", "Geometria", "Física"], "resposta": 0},
            {"pergunta": "Qual destes é um instrumento musical?", "opcoes": ["Violino", "Bola", "Livro", "Computador"], "resposta": 0},
            {"pergunta": "O que usamos para pintar?", "opcoes": ["Pincel", "Cola", "Tesoura", "Borracha"], "resposta": 0},
            {"pergunta": "Qual destes é um gênero musical?", "opcoes": ["Rock", "Física", "Matemática", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destas é uma técnica de pintura?", "opcoes": ["Aquarela", "Biologia", "História", "Geografia"], "resposta": 0},
            {"pergunta": "Qual destes é um famoso pintor?", "opcoes": ["Van Gogh", "Einstein", "Newton", "Edison"], "resposta": 0},
            {"pergunta": "Qual destas é uma forma de arte?", "opcoes": ["Escultura", "Cálculo", "Análise", "Pesquisa"], "resposta": 0},
        ]
    }
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
