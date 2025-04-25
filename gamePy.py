import pygame
import sys
import random
import math

# Inicialização
pygame.init()

# Tela
LARGURA, ALTURA = 800, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("RPG - Fuja dos Inimigos!")

# Cores
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)

# Fonte
fonte = pygame.font.SysFont("arial", 40)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Estados do jogo
ESTADO_MENU = "menu"
ESTADO_CONTAGEM = "contagem"
ESTADO_JOGO = "jogo"
ESTADO_GAMEOVER = "gameover"
estado = ESTADO_MENU

# Função para criar jogador e inimigos
def criar_jogo():
    jogador = pygame.Rect(400, 300, 40, 40)
    inimigos = []
    for _ in range(5):
        x = random.randint(0, LARGURA - 40)
        y = random.randint(0, ALTURA - 40)
        inimigos.append(pygame.Rect(x, y, 40, 40))
    return jogador, inimigos

# Função para mover inimigos
def mover_inimigo(inimigo, alvo, vel=2):
    dx = alvo.x - inimigo.x
    dy = alvo.y - inimigo.y
    dist = math.hypot(dx, dy)
    if dist != 0:
        dx /= dist
        dy /= dist
    inimigo.x += dx * vel
    inimigo.y += dy * vel
    inimigo.x = max(0, min(LARGURA - inimigo.width, inimigo.x))
    inimigo.y = max(0, min(ALTURA - inimigo.height, inimigo.y))

# Inicializa personagens
jogador, inimigos = criar_jogo()

# Loop principal
while True:
    for evento in pygame.event.get():
        # Percorre todos os eventos que estão na fila de eventos do pygame
        if evento.type == pygame.QUIT:
            # Se o jogador fechar a janela do jogo, finaliza o pygame e o programa
            pygame.quit()
            sys.exit()
        # Se alguma tecla for pressionada...
        elif evento.type == pygame.KEYDOWN:
            # Se estamos no MENU e a tecla pressionada for ENTER:
            # Muda para o estado de CONTAGEM REGRESSIVA antes do jogo começar
            if estado == ESTADO_MENU and evento.key == pygame.K_RETURN:
                estado = ESTADO_CONTAGEM
                tempo_contagem = pygame.time.get_ticks()
            # Se estamos na tela de GAME OVER e a tecla pressionada for ENTER:
            # Retorna para o MENU inicial
            elif estado == ESTADO_GAMEOVER and evento.key == pygame.K_RETURN:
                estado = ESTADO_MENU

    TELA.fill(PRETO)

    # Se o jogo estiver no estado de MENU:
    # Mostra a mensagem "Pressione ENTER para jogar" no centro da tela.
    if estado == ESTADO_MENU:
        texto = fonte.render("Pressione ENTER para jogar", True, BRANCO)
        TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2 - texto.get_height() // 2))

    # Se o jogo estiver na fase de contagem regressiva:
    # Calcula quanto tempo já passou desde que apertou ENTER.
    elif estado == ESTADO_CONTAGEM:
        agora = pygame.time.get_ticks()
        tempo_passado = (agora - tempo_contagem) // 1000  # em segundos

        numero = 3 - tempo_passado
        if numero > 0:
            texto = fonte.render(str(numero), True, BRANCO)
            TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2 - texto.get_height() // 2))
        else:
            jogador, inimigos = criar_jogo()
            estado = ESTADO_JOGO

    # Se o jogo estiver ativo:
    # Lida com movimento do jogador, inimigos, colisões e desenha os elementos na tela.
    elif estado == ESTADO_JOGO:
        # Movimento do jogador
        teclas = pygame.key.get_pressed()
        vel_jogador = 4
        if teclas[pygame.K_w] and jogador.top > 0:
            jogador.y -= vel_jogador
        if teclas[pygame.K_s] and jogador.bottom < ALTURA:
            jogador.y += vel_jogador
        if teclas[pygame.K_a] and jogador.left > 0:
            jogador.x -= vel_jogador
        if teclas[pygame.K_d] and jogador.right < LARGURA:
            jogador.x += vel_jogador

        # Movimento inimigos
        for inimigo in inimigos:
            mover_inimigo(inimigo, jogador)

        # Colisão
        for inimigo in inimigos:
            if jogador.colliderect(inimigo):
                estado = ESTADO_GAMEOVER

        # Desenhar
        pygame.draw.rect(TELA, VERDE, jogador)
        for inimigo in inimigos:
            pygame.draw.rect(TELA, VERMELHO, inimigo)

    # Se o jogador perder (colidir com um inimigo):
    # Mostra a mensagem de Game Over e instruções para retornar ao menu.
    elif estado == ESTADO_GAMEOVER:
        texto = fonte.render("Você foi pego!", True, VERMELHO)
        TELA.blit(texto, (LARGURA // 2 - texto.get_width() // 2, ALTURA // 2 - 60))
        texto2 = fonte.render("Pressione ENTER para voltar ao menu", True, BRANCO)
        TELA.blit(texto2, (LARGURA // 2 - texto2.get_width() // 2, ALTURA // 2 + 10))

    pygame.display.flip()
    clock.tick(FPS)