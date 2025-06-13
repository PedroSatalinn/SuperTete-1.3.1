# core/menu.py

import pygame
import sys
from core.config import TELA_LARGURA, TELA_ALTURA, COR_BOTAO, COR_BOTAO_HOVER

def desenhar_menu(tela, menu_imagem, texto_menu, texto_jogar, texto_sair):
    tela.blit(menu_imagem, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    tela.blit(texto_menu, (TELA_LARGURA / 2 - texto_menu.get_width() / 2, 100))
    jogar_btn = pygame.Rect(TELA_LARGURA / 2 - 100, TELA_ALTURA / 2, 200, 50)
    sair_btn = pygame.Rect(TELA_LARGURA / 2 - 100, TELA_ALTURA / 2 + 100, 200, 50)
    pygame.draw.rect(tela, COR_BOTAO_HOVER if jogar_btn.collidepoint(mouse_pos) else COR_BOTAO, jogar_btn)
    pygame.draw.rect(tela, COR_BOTAO_HOVER if sair_btn.collidepoint(mouse_pos) else COR_BOTAO, sair_btn)
    tela.blit(texto_jogar, (jogar_btn.centerx - texto_jogar.get_width() / 2, jogar_btn.centery - texto_jogar.get_height() / 2))
    tela.blit(texto_sair, (sair_btn.centerx - texto_sair.get_width() / 2, sair_btn.centery - texto_sair.get_height() / 2))
    return jogar_btn, sair_btn

def selecionar_personagem(tela, selecao_imagem):
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                return 'tete' if evento.pos[0] < TELA_LARGURA / 2 else 'lilice'
        tela.blit(selecao_imagem, (0, 0))
        pygame.display.flip()
