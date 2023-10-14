import pygame
from sys import exit
from random import randint, choice

def animacao_personagem():
    global jogador_index, jogador_retangulo, movimento_x_personagem, direcao_personagem, movimento_y_personagem

    # Atualize a posição vertical do jogador com base nas teclas pressionadas
    jogador_retangulo.x += movimento_x_personagem
    jogador_retangulo.y += movimento_y_personagem

    if jogador_retangulo.right >= 960:
        jogador_retangulo.right = 960
    elif jogador_retangulo.left <= 0:
        jogador_retangulo.left = 0

    # Verifique se o jogador não ultrapassa os limites superior e inferior da tela
    if jogador_retangulo.top < 0:
        jogador_retangulo.top = 0
    elif jogador_retangulo.bottom > 540:  # Ajuste este valor de acordo com a altura da tela
        jogador_retangulo.bottom = 540

    if movimento_x_personagem == 0:  # Jogador está parado
        jogador_superficies = jogador_parado_superficie
    else:  # Jogador está se movimentando
        jogador_superficies = jogador_andando_superficie

    jogador_index += 0.11
    if jogador_index > len(jogador_superficies) - 1:
        jogador_index = 0

    if direcao_personagem == 1:
        jogador = pygame.transform.flip(jogador_superficies[int(jogador_index)], True, False)
    else:
        jogador = jogador_superficies[int(jogador_index)]

    tela.blit(jogador, jogador_retangulo)

def adicionar_objeto():
    global lista_monstro_objetos

    objeto_lista_aleatoria = ['lobo'] * 30 + ['lobo_branco'] * 30 + ['wolf'] * 30 + ['coracao'] * 10
    tipo_objeto = choice(objeto_lista_aleatoria)

    # Define as posições para que os objetos apareçam fora da tela pela direita
    posicao = (randint(960, 990), randint(125, 490))  # Ajusta a posição para sair pela direita
    velocidade = randint(5, 10)

    
    if tipo_objeto == 'lobo':
        lobo_img = pygame.transform.flip(lobo_superficies[0], True, False)  # Inverte o lobo para a esquerda
        objeto_rect = lobo_img.get_rect(center=posicao)
        # objeto_rect.right = 0  # Define a posição inicial dos lobos à direita da tela
    elif tipo_objeto == 'lobo_branco':
        lobo_branco_img = pygame.transform.flip(lobo_branco_supercicies[0], True, False)  # Inverte o lobo branco
        objeto_rect = lobo_branco_img.get_rect(center=posicao)
        # objeto_rect.right = 0  # Define a posição inicial dos lobos brancos à direita da tela
    elif tipo_objeto == 'wolf':
        wolf_img = pygame.transform.flip(wolf_superficies[0], True, False)  # Inverte o lobo para a esquerda
        objeto_rect = wolf_img.get_rect(center=posicao)
        # objeto_rect.right = 0  # Define a posição inicial dos lobos à direita da tela
    elif tipo_objeto == 'coracao':
        objeto_rect = coracao_superficies[0].get_rect(center=posicao)
        # objeto_rect.right = 0 

    lista_monstro_objetos.append({
        'tipo': tipo_objeto,
        'rect': objeto_rect,
        'velocidade': velocidade
    })

def movimento_objetos_direita():
    global lista_monstro_objetos, lobo_index, lobo_branco_index

    # Crie uma cópia da lista de objetos para evitar problemas de iteração
    objetos_a_remover = []

    for objeto in lista_monstro_objetos:
        objeto['rect'].x -= objeto['velocidade']

        if objeto['tipo'] == 'lobo':
            tela.blit(pygame.transform.flip(lobo_superficies[lobo_index], True, False), objeto['rect'])
        elif objeto['tipo'] == 'lobo_branco':
            tela.blit(pygame.transform.flip(lobo_branco_supercicies[lobo_branco_index], True, False), objeto['rect'])
        elif objeto['tipo'] == 'wolf':
            tela.blit(pygame.transform.flip(wolf_superficies[wolf_index], True, False), objeto['rect'])
        elif objeto['tipo'] == 'coracao':
            tela.blit(pygame.transform.flip(coracao_superficies[coracao_index], True, False), objeto['rect'])

        # Verifique se o objeto saiu pela direita da tela
        if objeto['rect'].right < 0:
            objetos_a_remover.append(objeto)

    # Remova os objetos que saíram pela direita da tela
    for objeto in objetos_a_remover:
        lista_monstro_objetos.remove(objeto)

def colisoes_jogador():
    global lobo_colisao, lobo_branco_colisao, wolf_colisao, fogo_colisao, coracao_colisao, vida_jogador

    for objeto in lista_monstro_objetos:
        if jogador_retangulo.colliderect(objeto['rect']):
            if objeto['tipo'] == 'lobo':
                lobo_colisao += 1
                if vida_jogador > 0:
                    vida_jogador -= 1  # Reduza uma vida do jogador se ele tiver mais de 0 vidas
                if vida_jogador <= 0:
                    # O jogador não tem mais vidas, você pode adicionar a lógica de game over aqui
                    print("Game Over")
            elif objeto['tipo'] == 'lobo_branco':
                lobo_branco_colisao += 1
                if vida_jogador > 0:
                    vida_jogador -= 1  # Reduza uma vida do jogador se ele tiver mais de 0 vidas
                if vida_jogador <= 0:
                    print("Game Over")
            elif objeto['tipo'] == 'wolf':
                wolf_colisao += 1
            elif objeto['tipo'] == 'fogo':
                fogo_colisao += 1
            elif objeto['tipo'] == 'coracao':
                coracao_colisao += 1
                vida_jogador += 1

            lista_monstro_objetos.remove(objeto)

def movimento_fogo():
    global lista_fogo_objetos, fogo_rect

    # Adicione o código para lidar com colisões do fogo com outros objetos
    objetos_a_remover = []

    for fogo in lista_fogo_objetos:
        if fogo['tipo'] == 'fogo':
            fogo['rect'].x += fogo['velocidade']

            for monstro in lista_monstro_objetos:
                if fogo['rect'].colliderect(monstro['rect']):
                    print("MaTEI")

            tela.blit(fogo_superficies[fogo_index], fogo['rect'])


def mostra_texto():
    texto_coracoes = fonte_pixel.render(f"vida: {vida_jogador}", True, '#FFFFFF')
    logo_coracoes = pygame.transform.scale(coracao_superficies[0],(40,40))

    tela.blit(texto_coracoes,(885,10))
    tela.blit(logo_coracoes,(885,50))

def disparar_fogo(): 

    global lista_fogo_objetos, jogador_retangulo

    fogo_rect = fogo_superficies[0].get_rect(center=jogador_retangulo.midright)
    velocidade_fogo = 10

    lista_fogo_objetos.append({
        'tipo': 'fogo',
        'rect': fogo_rect,
        'velocidade': velocidade_fogo,
        'dano': 10,  # Exemplo de dano causado
        'cor': (0, 255, 0),  # Exemplo de cor do fogo (verde)
        'tempo_de_vida': 60
    })
    

##
# INICIO
##

pygame.init()

# Define tamanhos e configurações da tela

tamanho = (960, 540)
tela = pygame.display.set_mode(tamanho)

pygame.display.set_caption("Fantasia")

# Fazendo as importações das imagens
fonte_pixel = pygame.font.Font('objeto/Enchanted Land.otf', 36)  # Você precisa especificar uma fonte aqui

atras = pygame.image.load('fundo/image_fundo1.png').convert_alpha()
chao = pygame.image.load('fundo/image_fundo2.png').convert_alpha()
mato = pygame.image.load('fundo/image_fundo3.png').convert_alpha()
pedras = pygame.image.load('fundo/image_fundo3.png').convert_alpha()
arvores = pygame.image.load('fundo/image_fundo5.png').convert_alpha()

# Transforma as imagens para a escala do jogo
atras = pygame.transform.scale(atras, tamanho)
arvores = pygame.transform.scale(arvores, tamanho)
chao = pygame.transform.scale(chao, tamanho)
mato = pygame.transform.scale(mato, tamanho)
pedras = pygame.transform.scale(pedras, tamanho)

jogador_index = 0

jogador_pulando_superficies = []

jogador_parado_superficie = []
for imagem in range(1, 8):
    img = pygame.image.load(f'jogador/parado/parado{imagem}.png').convert_alpha()
    jogador_parado_superficie.append(img)

jogador_andando_superficie = []
for imagem in range(1, 13):
    img = pygame.image.load(f'jogador/andando/andando{imagem}.png').convert_alpha()
    jogador_andando_superficie.append(img)

# carrega os lobos para tela
wolf_superficies = []
wolf_index = 0
for image in range(1, 9):
    img = pygame.image.load(f'objeto/wolf/wolf{image}.png').convert_alpha()
    img = pygame.transform.scale(img, (90, 90))
    wolf_superficies.append(img)

lobo_branco_supercicies = []
lobo_branco_index = 0
for image in range(1, 6):
    img = pygame.image.load(f'objeto/lobo_branco/lobo_branco{image}.png').convert_alpha()
    img = pygame.transform.scale(img, (80, 80))
    lobo_branco_supercicies.append(img)

lobo_superficies = []
lobo_index = 0
for image in range(1, 5):
    img = pygame.image.load(f'objeto/lobo/lobo{image}.png').convert_alpha()
    img = pygame.transform.scale(img, (80, 80))
    lobo_superficies.append(img)

# carrega o cora para tela
coracao_superficies = []
coracao_index = 0
for imagem in range(1, 4):
    img =  pygame.image.load(f'objeto/coracao/Heart{imagem}.png').convert_alpha() 
    img = pygame.transform.scale(img, (40, 40))
    coracao_superficies.append(img)

fogo_superficies = []
fogo_index = 0
for image in range(1, 5):
    img = pygame.image.load(f'objeto/fogo/fogo_verde{image}.png').convert_alpha()
    img = pygame.transform.scale(img, (80, 80))
    fogo_superficies.append(img)

jogador_retangulo = jogador_parado_superficie[jogador_index].get_rect(center=(100, 430))

lista_monstro_objetos = []
lista_fogo_objetos = []

relogio = pygame.time.Clock()

movimento_x_personagem = 0
movimento_y_personagem = 0
direcao_personagem = 0
vida_jogador = 3

novo_objeto_time = pygame.USEREVENT + 1
pygame.time.set_timer(novo_objeto_time, 500)

jogo_ativo = True

coracao_colisao = 1
lobo_colisao = 3
lobo_branco_colisao = 0
wolf_colisao = 0
fogo_colisao = 0
dispara_fogo = 0

while jogo_ativo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RIGHT:
                movimento_x_personagem = 5
                direcao_personagem = 0
            if evento.key == pygame.K_LEFT:
                movimento_x_personagem = -5
                direcao_personagem = 1
            if evento.key == pygame.K_UP:
                movimento_y_personagem = -5
            if evento.key == pygame.K_DOWN:
                movimento_y_personagem = 5

            # Dispara o fogo ao pressionar a tecla Enter
            if evento.key == pygame.K_SPACE:
                # movimento_fogo()
                disparar_fogo()

        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_RIGHT:
                movimento_x_personagem = 0
            if evento.key == pygame.K_LEFT:
                movimento_x_personagem = 0
            if evento.key == pygame.K_UP:
                movimento_y_personagem = 0
            if evento.key == pygame.K_DOWN:
                movimento_y_personagem = 0

        if evento.type == novo_objeto_time:
            adicionar_objeto()

    tela.blit(chao, (0, 0))
    tela.blit(atras, (0, 0))
    tela.blit(arvores, (0, 0))
    tela.blit(mato, (0, 0))
    tela.blit(pedras, (0, 0))

    animacao_personagem()
    movimento_objetos_direita()
    movimento_fogo()
    colisoes_jogador()
    mostra_texto()


    pygame.display.update()

    relogio.tick(60)

