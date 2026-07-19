"""
Utilitarios partilhados do projeto.

Inclui:
- Som e musica
- Cores ANSI
- Helpers de UI textual

EXTENSAO:
- Se precisares de novas funcoes de apresentacao, coloca-as em `Recursos`.
- Se adicionares um novo backend de audio, centraliza em `GerenciadorMusica`.
- Como fazer: cria wrappers com `@staticmethod` para manter chamadas simples
    no resto do projeto (ex.: `Recursos.imprimirX(...)`).
"""

import os
import time
import sys

try:
    import winsound
except ImportError:
    winsound = None

try:
    import pygame
    PYGAME_DISPONIVEL = True
except ImportError:
    PYGAME_DISPONIVEL = False

ERRO_AUDIO = ""

# Habilitar suporte a ANSI colors no Windows (Python 3.10+)
if sys.platform == 'win32':
    os.system('color')

# Inicializar pygame mixer se disponível
if PYGAME_DISPONIVEL:
    try:
        pygame.mixer.init()
    except Exception:
        PYGAME_DISPONIVEL = False
        ERRO_AUDIO = "Nao foi possivel iniciar o mixer do pygame."

# ============================================================
# CLASSE GERENCIADOR DE MÚSICA
# ============================================================

class GerenciadorMusica:
    """Gerencia música de fundo e efeitos sonoros do jogo"""
    
    _musica_atual = None
    _volume = 0.7
    _aviso_emitido = False

    @staticmethod
    def _garantirMixer():
        global PYGAME_DISPONIVEL, ERRO_AUDIO

        if not PYGAME_DISPONIVEL:
            return False

        if pygame.mixer.get_init() is not None:
            return True

        try:
            pygame.mixer.init()
            return True
        except Exception as ex:
            ERRO_AUDIO = str(ex)
            PYGAME_DISPONIVEL = False
            return False

    @staticmethod
    def _avisarAudioIndisponivel(contexto):
        if GerenciadorMusica._aviso_emitido:
            return

        detalhe = ERRO_AUDIO if ERRO_AUDIO != "" else "pygame nao instalado ou sem suporte de audio."
        print(f"[AUDIO] {contexto}: {detalhe}")
        GerenciadorMusica._aviso_emitido = True
    
    @staticmethod
    def tocarMusica(caminho, loop=True):
        """Toca uma música de fundo com loop opcional"""
        # EXTENSAO: para fade in/out, aplicar transicoes antes de stop/play.
        # Como fazer: usa `pygame.mixer.music.fadeout(ms)` no stop e
        # `pygame.mixer.music.play(loops, fade_ms=...)` no arranque.
        if not GerenciadorMusica._garantirMixer():
            GerenciadorMusica._avisarAudioIndisponivel("Nao foi possivel tocar musica")
            return
        
        try:
            caminho_completo = os.path.join(os.path.dirname(__file__), caminho)
            
            if os.path.exists(caminho_completo):
                if GerenciadorMusica._musica_atual:
                    pygame.mixer.music.stop()
                
                pygame.mixer.music.load(caminho_completo)
                pygame.mixer.music.set_volume(GerenciadorMusica._volume)
                
                loops = -1 if loop else 0
                pygame.mixer.music.play(loops)
                GerenciadorMusica._musica_atual = caminho_completo
        except Exception as ex:
            GerenciadorMusica._avisarAudioIndisponivel("Erro ao carregar musica")
            if ERRO_AUDIO == "":
                # Regista o motivo para diagnostico futuro.
                globals()["ERRO_AUDIO"] = str(ex)
    
    @staticmethod
    def pararMusica():
        """Para a música que está a tocar"""
        if not GerenciadorMusica._garantirMixer():
            return
        
        try:
            pygame.mixer.music.stop()
            GerenciadorMusica._musica_atual = None
        except Exception:
            pass
    
    @staticmethod
    def pausarMusica():
        """Pausa a música"""
        if not GerenciadorMusica._garantirMixer():
            return
        
        try:
            pygame.mixer.music.pause()
        except Exception:
            pass
    
    @staticmethod
    def retomarMusica():
        """Retoma a música pausada"""
        if not GerenciadorMusica._garantirMixer():
            return
        
        try:
            pygame.mixer.music.unpause()
        except Exception:
            pass
    
    @staticmethod
    def definirVolume(volume):
        """Define o volume da música (0.0 a 1.0)"""
        if not GerenciadorMusica._garantirMixer():
            return
        
        try:
            volume = max(0.0, min(1.0, volume))
            GerenciadorMusica._volume = volume
            pygame.mixer.music.set_volume(volume)
        except Exception:
            pass
    
    @staticmethod
    def tocarSom(caminho, loop=False):
        """Toca um som de efeito"""
        if not GerenciadorMusica._garantirMixer():
            GerenciadorMusica._avisarAudioIndisponivel("Nao foi possivel tocar som")
            return
        
        try:
            caminho_completo = os.path.join(os.path.dirname(__file__), caminho)
            
            if os.path.exists(caminho_completo):
                som = pygame.mixer.Sound(caminho_completo)
                som.set_volume(GerenciadorMusica._volume)
                
                loops = -1 if loop else 0
                som.play(loops)
                return som
        except Exception as ex:
            GerenciadorMusica._avisarAudioIndisponivel("Erro ao carregar som")
            if ERRO_AUDIO == "":
                globals()["ERRO_AUDIO"] = str(ex)
        
        return None


# ============================================================
# CÓDIGOS DE COR ANSI
# ============================================================

class Cores:
    # Paleta ANSI usada em toda a interface de consola.
    # EXTENSAO: adicionar novos tons aqui para temas alternativos.
    # Como fazer: adiciona uma constante ANSI e usa-a nos metodos de `Recursos`.
    # Estilos
    RESET = '\033[0m'
    NEGRITO = '\033[1m'
    ATENUADO = '\033[2m'
    ITALICO = '\033[3m'
    SUBLINHADO = '\033[4m'
    
    # Cores do Texto
    PRETO = '\033[30m'
    VERMELHO = '\033[31m'
    VERDE = '\033[32m'
    AMARELO = '\033[33m'
    AZUL = '\033[34m'
    MAGENTA = '\033[35m'
    CIANO = '\033[36m'
    BRANCO = '\033[37m'
    
    # Cores Brilhantes
    VERMELHO_BRILHO = '\033[91m'
    VERDE_BRILHO = '\033[92m'
    AMARELO_BRILHO = '\033[93m'
    AZUL_BRILHO = '\033[94m'
    MAGENTA_BRILHO = '\033[95m'
    CIANO_BRILHO = '\033[96m'
    BRANCO_BRILHO = '\033[97m'


# ============================================================
# CLASSE RECURSOS
# ============================================================

class Recursos:
    """Helpers de renderizacao e interacao para a interface CLI."""

    @staticmethod
    def limparConsola():
        # No PyCharm, os comandos cls/clear nem sempre limpam bem a consola.
        # Esta solução é mais simples e funciona em praticamente todos os ambientes.
        print("\n" * 100)

    @staticmethod
    def pausa(segundos):
        # Faz uma pausa na execução do programa.
        # Serve para dar mais ritmo à narrativa do jogo.
        time.sleep(segundos)

    @staticmethod
    def imprimirAscii(caminhoFicheiro, textoAlternativo=""):
        # Tenta imprimir o conteúdo de um ficheiro ASCII.
        # Se o ficheiro não existir, mostra um texto alternativo.

        if os.path.exists(caminhoFicheiro):
            try:
                with open(caminhoFicheiro, "r", encoding="utf-8") as ficheiro:
                    conteudo = ficheiro.read()
                    print(conteudo)
            except Exception:
                print(textoAlternativo)
        else:
            print(textoAlternativo)

    @staticmethod
    def tocarAudio(caminhoFicheiro):
        # Tenta tocar um ficheiro de áudio .wav.
        # O winsound funciona apenas em Windows.
        # Se não for possível tocar áudio, o programa continua normalmente.

        if winsound is None:
            return

        # EXTENSAO: se quiseres suportar mp3/ogg aqui, substituir winsound por pygame.
        # Como fazer: carregar `pygame.mixer.Sound(caminho)` e chamar `.play()`.
        if os.path.exists(caminhoFicheiro):
            try:
                winsound.PlaySound(
                    caminhoFicheiro,
                    winsound.SND_FILENAME | winsound.SND_ASYNC
                )
            except Exception:
                pass

    @staticmethod
    def tocarAudioBloqueante(caminhoFicheiro):
        # Toca um áudio e espera que ele termine antes de continuar.
        # Pode ser útil para sons curtos, como vitória ou derrota.

        if winsound is None:
            return

        if os.path.exists(caminhoFicheiro):
            try:
                winsound.PlaySound(
                    caminhoFicheiro,
                    winsound.SND_FILENAME
                )
            except Exception:
                pass

    @staticmethod
    def pararAudio():
        # Para qualquer áudio que esteja a tocar.
        # Só funciona se winsound estiver disponível.

        if winsound is not None:
            try:
                winsound.PlaySound(None, 0)
            except Exception:
                pass

    @staticmethod
    def esperarEnter(mensagem="Pressiona ENTER para continuar..."):
        # Pausa o jogo até o utilizador carregar em ENTER.
        input(f"\n{Cores.AMARELO}{mensagem}{Cores.RESET}")

    @staticmethod
    def imprimirLinha(tamanho=40, simbolo="=", cor=None):
        # Imprime uma linha decorativa.
        if cor is None:
            cor = Cores.CIANO_BRILHO
        print(f"{cor}{simbolo * tamanho}{Cores.RESET}")

    @staticmethod
    def imprimirTitulo(titulo):
        # Imprime um título formatado para a consola com cores.
        Recursos.imprimirLinha(cor=Cores.VERDE_BRILHO)
        print(f"{Cores.VERDE_BRILHO}{Cores.NEGRITO}{titulo.center(40)}{Cores.RESET}")
        Recursos.imprimirLinha(cor=Cores.VERDE_BRILHO)

    @staticmethod
    def imprimirTituloSecundario(titulo):
        # Imprime um título secundário com cores.
        print(f"{Cores.AZUL_BRILHO}{Cores.NEGRITO}{titulo}{Cores.RESET}")

    @staticmethod
    def imprimirSecao(titulo):
        # Imprime uma secção do jogo com cores.
        print(f"{Cores.MAGENTA_BRILHO}{Cores.NEGRITO}===== {titulo.upper()} ====={Cores.RESET}")

    @staticmethod
    def imprimirTextoColorido(texto, cor=Cores.BRANCO):
        # Imprime um texto com uma cor específica.
        print(f"{cor}{texto}{Cores.RESET}")

    @staticmethod
    def imprimirSucesso(texto):
        # Imprime uma mensagem de sucesso em verde.
        print(f"{Cores.VERDE_BRILHO}{Cores.NEGRITO}{texto}{Cores.RESET}")

    @staticmethod
    def imprimirAviso(texto):
        # Imprime uma mensagem de aviso em amarelo.
        print(f"{Cores.AMARELO_BRILHO}{Cores.NEGRITO}{texto}{Cores.RESET}")

    @staticmethod
    def imprimirErro(texto):
        # Imprime uma mensagem de erro em vermelho.
        print(f"{Cores.VERMELHO_BRILHO}{Cores.NEGRITO}{texto}{Cores.RESET}")

    @staticmethod
    def imprimirInfo(texto):
        # Imprime uma mensagem informativa em ciano.
        print(f"{Cores.CIANO_BRILHO}{texto}{Cores.RESET}")

    @staticmethod
    def imprimirNome(nome):
        # Imprime um nome (corredora, etc) em magenta.
        return f"{Cores.MAGENTA_BRILHO}{nome}{Cores.RESET}"

    @staticmethod
    def imprimirValor(valor):
        # Imprime um valor (números, stats) em amarelo.
        return f"{Cores.AMARELO_BRILHO}{valor}{Cores.RESET}"

    @staticmethod
    def imprimirDestaque(texto):
        # Imprime um texto destacado em ciano brilho e negrito.
        return f"{Cores.CIANO_BRILHO}{Cores.NEGRITO}{texto}{Cores.RESET}"