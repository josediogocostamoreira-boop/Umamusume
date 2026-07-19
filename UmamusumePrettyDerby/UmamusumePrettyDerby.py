"""
Ponto de entrada do jogo.

Fluxo principal:
1) Mostra menu inicial.
2) Cria a classe Jogo.
3) Inicia o loop da carreira.

EXTENSAO:
- Se quiseres adicionar um menu de opcoes antes de jogar (ex.: dificuldade, idioma),
    este e o melhor sitio para chamar essa configuracao antes de `jogo.iniciarJogo()`.
    Como fazer: cria `mostrar_menu_opcoes()`, guarda a escolha numa variavel e passa
    essa configuracao para a classe Jogo antes de iniciar o loop.
"""

try:
    from UmamusumePrettyDerby.Jogo import Jogo
    from UmamusumePrettyDerby.Recursos import Recursos
except ModuleNotFoundError:
    from Jogo import Jogo
    from Recursos import Recursos


def mostrar_menu_inicial():
    """Mostra o ecran inicial com identidade visual do jogo."""
    Recursos.limparConsola()
    
    # Exibir ASCII Art do menu inicial
    import os
    caminhoAscii = os.path.join(os.path.dirname(__file__), "assets", "ascii", "menu_inicio.txt")
    Recursos.imprimirAscii(
        caminhoAscii,
        """
        +---------------------------------------------+
        |          UMAMUSUME PRETTY DERBY            |
        |           Treina - Corre - Vence           |
        +---------------------------------------------+
        """
    )
    
    print()
    Recursos.imprimirInfo("Pressiona ENTER para comecar a tua jornada como treinador...\n")
    Recursos.esperarEnter()


def main():
    # Sequencia minima para arrancar a aplicacao.
    mostrar_menu_inicial()
    jogo = Jogo()
    jogo.iniciarJogo()


if __name__ == "__main__":
    # Garante que o jogo so arranca quando este ficheiro e executado diretamente.
    main()

