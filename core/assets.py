# core/assets.py

import pygame
import os
import sys
from core.config import TELA_LARGURA, TELA_ALTURA, tamanho_icone, tamanho_coracao

def carregar_imagens_personagem(nome):
    imagens = []
    for i in range(4):
        imagem = pygame.image.load(f'assets/images/{nome}_frame{i}.png').convert_alpha()
        imagem = pygame.transform.scale(imagem, (100, 100))
        imagens.append(imagem)
    imagem_parado = pygame.image.load(f'assets/images/{nome}_frame_parado.png').convert_alpha()
    imagem_parado = pygame.transform.scale(imagem_parado, (100, 100))
    return imagens[:3], imagens[3], imagem_parado

def inicializar_jogo():
    pygame.init()
    pygame.mixer.init()
    menu_imagem = pygame.image.load('assets/images/imagemmenu.png')
    menu_imagem = pygame.transform.scale(menu_imagem, (TELA_LARGURA, TELA_ALTURA))
    selecao_imagem = pygame.image.load('assets/images/selecao_personagem.png')
    selecao_imagem = pygame.transform.scale(selecao_imagem, (TELA_LARGURA, TELA_ALTURA))
    bloco_imagem = pygame.image.load('assets/images/bloco.png')
    bloco_imagem = pygame.transform.scale(bloco_imagem, (20, 20))
    cenario = pygame.transform.scale(pygame.image.load('assets/images/cenariofase1.png'), (3000, TELA_ALTURA))
    som_pulo = pygame.mixer.Sound('assets/sounds/sompulo.mp3')
    missel_imagem = pygame.image.load('assets/images/missil.png')
    missel_imagem = pygame.transform.scale(missel_imagem, (70, 70))
    return menu_imagem, selecao_imagem, bloco_imagem, cenario, som_pulo, missel_imagem

def criar_plataformas():
    return [{"x": i * 200, "y": 550 - (i % 5) * 50, "width": 100, "height": 50} for i in range(30)]
