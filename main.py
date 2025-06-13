import pygame
import sys
import random

from core.config import TELA_LARGURA, TELA_ALTURA, vidas_maximas, life_maximo, tamanho_icone, tamanho_coracao
from core.assets import inicializar_jogo, criar_plataformas, carregar_imagens_personagem
from core.menu import desenhar_menu, selecionar_personagem
from core.hud import desenhar_HUD
from core.gameover import desenhar_gameover

def main():
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption("Super Tetê")
    clock = pygame.time.Clock()

    menu_imagem, selecao_imagem, bloco_imagem, cenario, som_pulo, missel_imagem = inicializar_jogo()
    plataformas = criar_plataformas()
    fonte = pygame.font.Font(None, 36)
    texto_menu = fonte.render("Menu de Início", True, (255, 255, 255))
    texto_jogar = fonte.render("Jogar", True, (255, 255, 255))
    texto_sair = fonte.render("Sair", True, (255, 255, 255))

    pygame.mixer.music.load("assets/sounds/musicamenu.mp3")
    pygame.mixer.music.play(-1)

    menu = True
    personagem_escolhido = None

    while menu:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                jogar_btn, sair_btn = desenhar_menu(tela, menu_imagem, texto_menu, texto_jogar, texto_sair)
                if jogar_btn.collidepoint(evento.pos):
                    personagem_escolhido = selecionar_personagem(tela, selecao_imagem)
                    menu = False
                elif sair_btn.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        desenhar_menu(tela, menu_imagem, texto_menu, texto_jogar, texto_sair)
        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/sounds/musicafase1.mp3")
    pygame.mixer.music.play(-1)

    imagens_andar, imagem_pulo, imagem_parado = carregar_imagens_personagem(personagem_escolhido)
    personagem = pygame.Rect(plataformas[0]["x"] + 10, plataformas[0]["y"] - 80, 40, 60)
    checkpoint = plataformas[0]
    misseis = [pygame.Rect(random.randint(0, 10000), random.randint(0, TELA_ALTURA), 20, 20) for _ in range(10)]

    personagem_velocidade_x, personagem_velocidade_y, gravidade = 10, 0, 2 * (TELA_ALTURA / 600)
    camera_x, vidas, life = 0, vidas_maximas, life_maximo
    no_chao, movimento, morreu, pause = False, False, False, False
    direcao = "direita"

    icones = {
        "tete": pygame.transform.scale(pygame.image.load("assets/images/tete_icone.png").convert_alpha(), tamanho_icone),
        "lilice": pygame.transform.scale(pygame.image.load("assets/images/lilice_icone.png").convert_alpha(), tamanho_icone)
    }
    imagens_coracao = [
        pygame.transform.scale(pygame.image.load(f"assets/images/coracao{i}.png").convert_alpha(), tamanho_coracao)
        for i in range(1, 6)
    ]

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and no_chao and not pause:
                    personagem_velocidade_y = -20 * (TELA_ALTURA / 600)
                    som_pulo.play()
                if evento.key == pygame.K_ESCAPE:
                    pause = not pause
                if evento.key == pygame.K_r and morreu and vidas > 0:
                    personagem.x = checkpoint["x"] + 10
                    personagem.y = checkpoint["y"] - 80
                    personagem_velocidade_y = 0
                    camera_x = 0
                    morreu = False
                    life = life_maximo

        if not pause and not morreu:
            teclas = pygame.key.get_pressed()
            movimento = False
            if teclas[pygame.K_a]:
                personagem.x -= personagem_velocidade_x
                direcao = "esquerda"
                movimento = True
            if teclas[pygame.K_d]:
                personagem.x += personagem_velocidade_x
                direcao = "direita"
                movimento = True

            camera_x = max(personagem.x - TELA_LARGURA // 2, 0)
            personagem.x = max(0, personagem.x)
            personagem_velocidade_y += gravidade
            personagem.y += personagem_velocidade_y
            no_chao = False

            for plataforma in plataformas:
                rect = pygame.Rect(plataforma["x"], plataforma["y"], plataforma["width"], plataforma["height"])
                if personagem.colliderect(rect) and personagem_velocidade_y > 0:
                    personagem.bottom = rect.top + 20
                    personagem_velocidade_y = 0
                    no_chao = True

            if personagem.y > TELA_ALTURA:
                life -= 1
                if life <= 0:
                    vidas -= 1
                    life = life_maximo
                    personagem.x = checkpoint["x"] + 10
                    personagem.y = checkpoint["y"] - 80
                    personagem_velocidade_y = 0
                    camera_x = 0
                    if vidas <= 0:
                        morreu = True

            for missel in misseis:
                if personagem.colliderect(missel):
                    life -= 1
                    missel.x = random.randint(personagem.x + 800, personagem.x + 1600)
                    missel.y = random.randint(0, TELA_ALTURA)
                    if life <= 0:
                        vidas -= 1
                        life = life_maximo
                        personagem.x = checkpoint["x"] + 10
                        personagem.y = checkpoint["y"] - 80
                        personagem_velocidade_y = 0
                        camera_x = 0
                        if vidas <= 0:
                            morreu = True
                missel.x -= 5
                if missel.x < 0:
                    missel.x = random.randint(0, 10000)
                    missel.y = random.randint(0, TELA_ALTURA)

        tela.fill((0, 0, 0))
        largura_cenario = cenario.get_width()
        for i in range((TELA_LARGURA // largura_cenario) + 2):
            tela.blit(cenario, (i * largura_cenario - camera_x % largura_cenario, 0))

        for plataforma in plataformas:
            rect = pygame.Rect(plataforma["x"] - camera_x, plataforma["y"], plataforma["width"], plataforma["height"])
            x = rect.x
            while x < rect.x + rect.width:
                tela.blit(bloco_imagem, (x, rect.y + rect.height - bloco_imagem.get_height()))
                x += bloco_imagem.get_width()

        img = imagem_pulo if personagem_velocidade_y != 0 else (
            imagens_andar[int(pygame.time.get_ticks() / 100) % len(imagens_andar)] if movimento else imagem_parado)
        if direcao == "esquerda":
            img = pygame.transform.flip(img, True, False)
        tela.blit(img, (personagem.x - camera_x, personagem.y))

        for missel in misseis:
            tela.blit(missel_imagem, (missel.x - camera_x, missel.y))

        if morreu and vidas <= 0:
            desenhar_gameover(tela, personagem_escolhido, TELA_LARGURA, TELA_ALTURA)
        else:
            desenhar_HUD(tela, vidas, life, personagem_escolhido, icones, imagens_coracao)

        if pause:
            texto = fonte.render("Pausado - ESC para continuar", True, (255, 255, 255))
            tela.blit(texto, (TELA_LARGURA // 2 - texto.get_width() // 2, TELA_ALTURA // 2))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
