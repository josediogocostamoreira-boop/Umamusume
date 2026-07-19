import os

try:
    from UmamusumePrettyDerby.Recursos import Recursos, Cores, GerenciadorMusica
except ModuleNotFoundError:
    from Recursos import Recursos, Cores, GerenciadorMusica


def mostrar_introducao():
    """
    Sequencia narrativa inicial do jogo.

    EXTENSAO:
    - Para adicionar novos capitulos de historia/tutorial, segue o padrao:
            limpar consola -> imprimir secao -> mensagens -> esperarEnter.
        - Como fazer: duplica um bloco existente, troca o titulo/textos e adiciona
            `Recursos.esperarEnter()` no fim para manter o ritmo da narrativa.
        """

    # Tocar musica do prologo
    GerenciadorMusica.tocarMusica("sounds/prologo.mp3", loop=False)
    
    Recursos.limparConsola()
    Recursos.imprimirSecao("Prologo")
    Recursos.imprimirInfo("Neste mundo, existem raparigas especiais conhecidas como Umamusumes.")
    Recursos.imprimirInfo("Elas carregam o espirito, a velocidade e a vontade de antigas lendas das pistas.")
    Recursos.imprimirInfo("Cada uma corre por um motivo: gloria, amizade, orgulho, ou o sonho de ouvir")
    Recursos.imprimirInfo("o estadio inteiro gritar o seu nome no fim da reta final.")
    Recursos.esperarEnter()

    Recursos.limparConsola()
    Recursos.imprimirSecao("A Academia")
    Recursos.imprimirInfo("Na academia, as Umamusumes treinam todos os dias para transformar talento em vitoria.")
    Recursos.imprimirInfo("Mas uma carreira nao e feita so de velocidade.")
    Recursos.imprimirInfo("Energia, mood, descanso, estrategia e coragem tambem decidem quem cruza a meta em primeiro.")
    Recursos.imprimirInfo("Uma corredora forte mas esgotada pode falhar. Uma corredora motivada pode superar limites.")
    Recursos.esperarEnter()

    Recursos.limparConsola()
    Recursos.imprimirSecao("A Tua Funcao")
    Recursos.imprimirInfo("Tu seras o treinador.")
    Recursos.imprimirInfo("Vais escolher uma Umamusume, definir um plano de carreira e preparar cada etapa.")
    Recursos.imprimirInfo("Entre corridas principais, teras turnos para treinar, descansar ou fazer recreacao.")
    Recursos.imprimirAviso("Treinar aumenta bastante os stats, mas gasta energia.")
    Recursos.imprimirInfo("Descansar recupera a energia para o maximo.")
    Recursos.imprimirInfo("Recriacao melhora o mood e da pequenos ganhos, mas nao substitui treino serio.")
    Recursos.esperarEnter()

    Recursos.limparConsola()
    Recursos.imprimirSecao("Como o Jogo Funciona")
    Recursos.imprimirInfo("Todas as corredoras comecam com Mood Normal e Energia 100/100.")
    Recursos.imprimirInfo("O Mood vai de Awful ate Great e afeta treino e corrida.")
    Recursos.imprimirAviso("Cada stat pode chegar no maximo a 1200 pontos.")
    Recursos.imprimirInfo("Cada treino gasta energia entre 8 e 20 pontos.")
    Recursos.imprimirInfo("Treinar muitas vezes a mesma coisa ou correr muitas vezes seguidas pode baixar o mood.")
    Recursos.imprimirAviso("Quando chega uma corrida principal, tens de vencer.")
    Recursos.imprimirErro("Se perderes uma corrida principal, a carreira acaba e recebes um score com rank de G a S.")
    Recursos.esperarEnter()

    Recursos.limparConsola()
    caminhoLogo = os.path.join(os.path.dirname(__file__), "assets", "ascii", "logo.txt")
    Recursos.imprimirAscii(
        caminhoLogo,
        f"""
{Cores.MAGENTA_BRILHO}{Cores.NEGRITO}======================================
        UMAMUSUME PRETTY DERBY
======================================{Cores.RESET}
        """
    )
    Recursos.imprimirSucesso("Bem-vindo ao Umamusume Pretty Derby.")
    Recursos.imprimirAviso("A pista esta pronta. A carreira vai comecar.")
    Recursos.esperarEnter("Pressiona ENTER para comecar...")

