# SuperTetê v1.3.1
Essa versão é a mesma da 1.3, mas com mudanças
nos arquivos que agora estão no formato ASCII 
e também nos códigos

SuperTetê é um jogo de plataforma 2D em pixel art criado com Python e Pygame.

## 🎮 Sobre o Jogo

- Personagens: Tetê e Lilice
- Animações de idle, corrida e pulo
- Sistema de vidas e corações
- Mísseis voadores como obstáculo
- Menus de seleção de personagem e pausa
- Música e efeitos sonoros

## 🚀 Requisitos

- Python 3.13
- Pygame 2.5.2

## 📦 Instalação

1. Clone ou copie o projeto.
2. Instale o pygame-ce:

```bash
pip install pygame-ce
Execute o jogo:

bash
Copiar
Editar
python main.py
Estrutura do Projeto
arduino
Copiar
Editar
SuperTete/
│
├── assets/         # Assets (imagens e sons)
│   ├── images/     
│   └── sounds/
│
├── core/           # Código-fonte do jogo
│   ├── config.py
│   ├── assets.py
│   ├── menu.py
│   ├── hud.py
│   └── gameover.py
│
├── main.py         # Entrada principal do jogo
└── README.md

Como adicionar assets
Coloque as imagens na pasta assets/images/

Coloque os sons na pasta assets/sounds/

Os arquivos de exemplo já estão configurados com nomes esperados.

css
Copiar
Editar

---

### 📄 main.py

```python
import pygame
import sys
from core import config, menu

def main():
    pygame.init()
    pygame.mixer.init()
    tela = pygame.display.set_mode((config.TELA_LARGURA, config.TELA_ALTURA))
    pygame.display.set_caption("SuperTetê")

    # Inicia o menu inicial
    personagem_escolhido = menu.menu_principal(tela)
    print(f"Personagem escolhido: {personagem_escolhido}")

    # Aqui depois você vai chamar a lógica do jogo principal.
    # Exemplo:
    # jogo.iniciar_jogo(tela, personagem_escolhido)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tela.fill((0, 0, 0))
        pygame.display.flip()

if __name__ == "__main__":
    main()


    Agora que temos o início montado, vamos para:

config.py

assets.py

menu.py

hud.py

gameover.py

e por fim, os placeholders de imagens e sons.

📄 core/config.py
Este arquivo guarda as configurações globais do jogo:

python
Copiar
Editar
import os
import sys

# Tamanho da tela
TELA_LARGURA = 1280
TELA_ALTURA = 720

# Cores dos botões
COR_BOTAO = (50, 150, 250)
COR_BOTAO_HOVER = (70, 170, 250)

# Configurações de vidas
VIDAS_MAXIMAS = 5
LIFE_MAXIMO = 5

# Tamanhos dos ícones
TAMANHO_ICONE = (65, 65)
TAMANHO_CORACAO = (35, 35)

# Caminho de recursos para compatibilidade com PyInstaller (futuramente se empacotar)
def resource_path(relative_path):
    """Obtém o caminho absoluto do recurso, compatível com PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
📄 core/assets.py
Este arquivo irá carregar imagens e sons:

python
Copiar
Editar
import pygame
from core import config

class Assets:
    def __init__(self):
        self.carregar_imagens()
        self.carregar_sons()

    def carregar_imagens(self):
        self.menu_imagem = pygame.image.load(config.resource_path('assets/images/menu.png')).convert()
        self.selecao_imagem = pygame.image.load(config.resource_path('assets/images/selecao.png')).convert()
        self.bloco_imagem = pygame.image.load(config.resource_path('assets/images/bloco.png')).convert_alpha()
        self.bloco_imagem = pygame.transform.scale(self.bloco_imagem, (20, 20))

        self.cenario = pygame.image.load(config.resource_path('assets/images/cenario.png')).convert()
        self.cenario = pygame.transform.scale(self.cenario, (3000, config.TELA_ALTURA))

        self.missel_imagem = pygame.image.load(config.resource_path('assets/images/missel.png')).convert_alpha()
        self.missel_imagem = pygame.transform.scale(self.missel_imagem, (70, 70))

        self.icones = {
            "tete": pygame.transform.scale(
                pygame.image.load(config.resource_path("assets/images/tete_icone.png")).convert_alpha(),
                config.TAMANHO_ICONE
            ),
            "lilice": pygame.transform.scale(
                pygame.image.load(config.resource_path("assets/images/lilice_icone.png")).convert_alpha(),
                config.TAMANHO_ICONE
            )
        }

        self.coracoes = [
            pygame.transform.scale(
                pygame.image.load(config.resource_path(f"assets/images/coracao{i}.png")).convert_alpha(),
                config.TAMANHO_CORACAO
            )
            for i in range(1, 6)
        ]

    def carregar_sons(self):
        self.som_pulo = pygame.mixer.Sound(config.resource_path("assets/sounds/pulo.wav"))
        self.musicamenu = config.resource_path("assets/sounds/musicamenu.mp3")
        self.musicafase = config.resource_path("assets/sounds/musicafase1.mp3")
🔧 Observação importante:

Claro que por enquanto esses arquivos de imagem e som ainda não existem — iremos criá-los como placeholders de teste nos próximos passos.

O Assets facilita tudo: basta importar e chamar assets = Assets() para ter tudo carregado.

📄 core/menu.py
Este arquivo cuida do menu principal e da seleção de personagem:

python
Copiar
Editar
import pygame
import sys
from core import config

class Menu:
    def __init__(self, tela, assets):
        self.tela = tela
        self.assets = assets
        self.fonte = pygame.font.Font(None, 48)

    def desenhar_menu(self):
        self.tela.blit(self.assets.menu_imagem, (0, 0))

        texto_titulo = self.fonte.render("Super Tetê", True, (255, 255, 255))
        texto_jogar = self.fonte.render("Jogar", True, (255, 255, 255))
        texto_sair = self.fonte.render("Sair", True, (255, 255, 255))

        self.tela.blit(texto_titulo, (config.TELA_LARGURA // 2 - texto_titulo.get_width() // 2, 100))

        # Botões
        self.jogar_btn = pygame.Rect(config.TELA_LARGURA // 2 - 100, config.TELA_ALTURA // 2, 200, 50)
        self.sair_btn = pygame.Rect(config.TELA_LARGURA // 2 - 100, config.TELA_ALTURA // 2 + 100, 200, 50)

        mouse_pos = pygame.mouse.get_pos()

        pygame.draw.rect(self.tela, config.COR_BOTAO_HOVER if self.jogar_btn.collidepoint(mouse_pos) else config.COR_BOTAO, self.jogar_btn)
        pygame.draw.rect(self.tela, config.COR_BOTAO_HOVER if self.sair_btn.collidepoint(mouse_pos) else config.COR_BOTAO, self.sair_btn)

        self.tela.blit(texto_jogar, (self.jogar_btn.centerx - texto_jogar.get_width() // 2, self.jogar_btn.centery - texto_jogar.get_height() // 2))
        self.tela.blit(texto_sair, (self.sair_btn.centerx - texto_sair.get_width() // 2, self.sair_btn.centery - texto_sair.get_height() // 2))

    def executar_menu(self):
        clock = pygame.time.Clock()

        pygame.mixer.music.load(self.assets.musicamenu)
        pygame.mixer.music.play(-1)

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.jogar_btn.collidepoint(evento.pos):
                        pygame.mixer.music.stop()
                        return self.selecionar_personagem()
                    elif self.sair_btn.collidepoint(evento.pos):
                        pygame.quit()
                        sys.exit()

            self.desenhar_menu()
            pygame.display.flip()
            clock.tick(60)

    def selecionar_personagem(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.pos[0] < config.TELA_LARGURA / 2:
                        return "tete"
                    else:
                        return "lilice"

            self.tela.blit(self.assets.selecao_imagem, (0, 0))
            pygame.display.flip()


📄 core/hud.py
python
Copiar
Editar
import pygame
from core import config

class HUD:
    def __init__(self, tela, assets):
        self.tela = tela
        self.assets = assets
        self.fonte_hud = pygame.font.Font(None, 36)

    def desenhar(self, vidas, life, personagem):
        icone = self.assets.icones[personagem]
        self.tela.blit(icone, (20, 20))
        self.tela.blit(self.fonte_hud.render(f"x {vidas}", True, (255, 255, 255)), (95, 40))

        for i in range(life):
            frame = int(pygame.time.get_ticks() / 150) % len(self.assets.imagens_coracao)
            self.tela.blit(self.assets.imagens_coracao[frame], (20 + i * (config.tamanho_coracao[0] + 5), 95))

📄 entities/player.py
python
Copiar
Editar
import pygame
from core import config

class Player(pygame.Rect):
    def __init__(self, x, y, plataformas, imagens_andar, imagem_pulo, imagem_parado, som_pulo):
        super().__init__(x, y, 40, 60)
        self.plataformas = plataformas
        self.imagens_andar = imagens_andar
        self.imagem_pulo = imagem_pulo
        self.imagem_parado = imagem_parado
        self.som_pulo = som_pulo

        self.velocidade_x = 10
        self.velocidade_y = 0
        self.gravidade = 2 * (config.TELA_ALTURA / 600)

        self.no_chao = False
        self.movimento = False
        self.direcao = "direita"

    def mover(self, teclas):
        self.movimento = False
        if teclas[pygame.K_a]:
            self.x -= self.velocidade_x
            self.direcao = "esquerda"
            self.movimento = True
        if teclas[pygame.K_d]:
            self.x += self.velocidade_x
            self.direcao = "direita"
            self.movimento = True

        self.x = max(0, self.x)

    def aplicar_gravidade(self):
        self.velocidade_y += self.gravidade
        self.y += self.velocidade_y
        self.no_chao = False
        for plataforma in self.plataformas:
            rect = pygame.Rect(plataforma["x"], plataforma["y"], plataforma["width"], plataforma["height"])
            if self.colliderect(rect) and self.velocidade_y > 0:
                self.bottom = rect.top + 20
                self.velocidade_y = 0
                self.no_chao = True

    def pular(self):
        if self.no_chao:
            self.velocidade_y = -20 * (config.TELA_ALTURA / 600)
            self.som_pulo.play()

    def obter_imagem(self):
        if self.velocidade_y != 0:
            img = self.imagem_pulo
        elif self.movimento:
            frame = int(pygame.time.get_ticks() / 100) % len(self.imagens_andar)
            img = self.imagens_andar[frame]
        else:
            img = self.imagem_parado

        if self.direcao == "esquerda":
            img = pygame.transform.flip(img, True, False)
        return img

Aqui criamos a classe Player que:

Estende pygame.Rect para representar o retângulo do personagem

Controla movimentação, pulo, gravidade e colisões

Possui método para retornar a imagem correta para desenhar

import pygame
import sys
import random
from core import config
from entities.player import Player
from core.assets import carregar_imagens_personagem, carregar_sons, carregar_imagens_icone, carregar_imagens_coracao

class Game:
    def __init__(self, tela):
        self.tela = tela
        self.clock = pygame.time.Clock()
        self.plataformas = self.criar_plataformas()
        self.camera_x = 0
        self.vidas = config.VIDAS_MAXIMAS
        self.life = config.LIFE_MAXIMO
        self.morreu = False
        self.pause = False

        # Carregar assets
        self.cenario = pygame.transform.scale(pygame.image.load(config.resource_path('cenariofase1.png')), (3000, config.TELA_ALTURA))
        self.bloco_imagem = pygame.transform.scale(pygame.image.load(config.resource_path('bloco.png')), (20, 20))
        self.missel_imagem = pygame.transform.scale(pygame.image.load(config.resource_path('missil.png')), (70, 70))
        self.som_pulo = carregar_sons('sompulo.mp3')

        # Escolha de personagem
        self.personagem_escolhido = self.selecionar_personagem()
        imagens_andar, imagem_pulo, imagem_parado = carregar_imagens_personagem(self.personagem_escolhido)
        self.player = Player(self.plataformas[0]['x'] + 10, self.plataformas[0]['y'] - 80, self.plataformas, imagens_andar, imagem_pulo, imagem_parado, self.som_pulo)

        self.checkpoint = self.plataformas[0]
        self.misseis = [pygame.Rect(random.randint(0, 10000), random.randint(0, config.TELA_ALTURA), 20, 20) for _ in range(10)]

        self.icones = carregar_imagens_icone()
        self.imagens_coracao = carregar_imagens_coracao()
        self.fonte = pygame.font.Font(None, 36)

    def criar_plataformas(self):
        return [{"x": i * 200, "y": 550 - (i % 5) * 50, "width": 100, "height": 50} for i in range(30)]

    def selecionar_personagem(self):
        # Aqui você pode colocar sua lógica de seleção (ou importar do menu)
        # Por enquanto retorna 'tete' fixo
        return 'tete'

    def atualizar(self):
        if not self.pause and not self.morreu:
            teclas = pygame.key.get_pressed()
            self.player.mover(teclas)
            self.player.aplicar_gravidade()

            # Pulo via evento capturado em main.py (pode ser passado para cá)

            self.camera_x = max(self.player.x - config.TELA_LARGURA // 2, 0)

            # Verificar quedas e colisão com misseis, atualizar vida e vidas

            if self.player.y > config.TELA_ALTURA:
                self.life -= 1
                if self.life <= 0:
                    self.vidas -= 1
                    self.life = config.LIFE_MAXIMO
                    self.player.x = self.checkpoint['x'] + 10
                    self.player.y = self.checkpoint['y'] - 80
                    self.player.velocidade_y = 0
                    self.camera_x = 0
                    if self.vidas <= 0:
                        self.morreu = True

            for missel in self.misseis:
                if self.player.colliderect(missel):
                    self.life -= 1
                    missel.x = random.randint(self.player.x + 800, self.player.x + 1600)
                    missel.y = random.randint(0, config.TELA_ALTURA)
                    if self.life <= 0:
                        self.vidas -= 1
                        self.life = config.LIFE_MAXIMO
                        self.player.x = self.checkpoint['x'] + 10
                        self.player.y = self.checkpoint['y'] - 80
                        self.player.velocidade_y = 0
                        self.camera_x = 0
                        if self.vidas <= 0:
                            self.morreu = True
                missel.x -= 5
                if missel.x < 0:
                    missel.x = random.randint(0, 10000)
                    missel.y = random.randint(0, config.TELA_ALTURA)

    def desenhar(self):
        self.tela.fill((0, 0, 0))
        largura_cenario = self.cenario.get_width()
        for i in range((config.TELA_LARGURA // largura_cenario) + 2):
            self.tela.blit(self.cenario, (i * largura_cenario - self.camera_x % largura_cenario, 0))

        for plataforma in self.plataformas:
            rect = pygame.Rect(plataforma["x"] - self.camera_x, plataforma["y"], plataforma["width"], plataforma["height"])
            x = rect.x
            while x < rect.x + rect.width:
                self.tela.blit(self.bloco_imagem, (x, rect.y + rect.height - self.bloco_imagem.get_height()))
                x += self.bloco_imagem.get_width()

        img = self.player.obter_imagem()
        self.tela.blit(img, (self.player.x - self.camera_x, self.player.y))

        for missel in self.misseis:
            self.tela.blit(self.missel_imagem, (missel.x - self.camera_x, missel.y))

        if self.morreu and self.vidas <= 0:
            gameover = pygame.image.load(config.resource_path(f"{self.personagem_escolhido}gameover.png"))
            gameover = pygame.transform.scale(gameover, (config.TELA_LARGURA, config.TELA_ALTURA))
            self.tela.blit(gameover, (0, 0))
        else:
            self.desenhar_HUD()

        if self.pause:
            texto = self.fonte.render("Pausado - ESC para continuar", True, (255, 255, 255))
            self.tela.blit(texto, (config.TELA_LARGURA // 2 - texto.get_width() // 2, config.TELA_ALTURA // 2))

    def desenhar_HUD(self):
        icone = self.icones[self.personagem_escolhido]
        self.tela.blit(icone, (20, 20))
        self.tela.blit(self.fonte.render(f"x {self.vidas}", True, (255, 255, 255)), (95, 40))
        for i in range(self.life):
            frame = int(pygame.time.get_ticks() / 150) % len(self.imagens_coracao)
            self.tela.blit(self.imagens_coracao[frame], (20 + i * (config.TAMANHO_CORACAO[0] + 5), 95))

