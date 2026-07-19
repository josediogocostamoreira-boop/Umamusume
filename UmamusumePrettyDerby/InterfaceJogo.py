"""
Camada de interface textual (CLI).

Este modulo so trata de:
- Mostrar ecras e menus.
- Pedir input do utilizador.
- Renderizar resultados.

Nao deve conter regras de negocio pesadas.

EXTENSAO:
- Para novos ecras, adiciona funcoes aqui e chama-as a partir de Jogo.py.
- Como fazer: cria `mostrar_xxx()`/`pedir_xxx()`, retorna dados simples e trata
    a logica no Jogo.py para manter esta camada apenas de interface.
"""

try:
    from UmamusumePrettyDerby.Recursos import Recursos, Cores
except ModuleNotFoundError:
    from Recursos import Recursos, Cores


def mostrar_corredoras(opcoes):
    # Lista corredoras disponiveis para selecao no arranque.
    Recursos.limparConsola()
    Recursos.imprimirSecao("Escolher Corredora")

    for indice in range(len(opcoes)):
        corredora = opcoes[indice]
        num = Recursos.imprimirValor(str(indice + 1))
        nome = Recursos.imprimirNome(corredora.getNome())
        print(f"{num} - {nome}")
        print(f"    {Cores.AZUL_BRILHO}Estilo:{Cores.RESET} {corredora.getEstilo()}")
        speed = Recursos.imprimirValor(corredora.getSpeed())
        stamina = Recursos.imprimirValor(corredora.getStamina())
        power = Recursos.imprimirValor(corredora.getPower())
        guts = Recursos.imprimirValor(corredora.getGuts())
        wit = Recursos.imprimirValor(corredora.getWit())
        print(
            f"    {Cores.AZUL_BRILHO}Speed:{Cores.RESET} {speed} | {Cores.AZUL_BRILHO}Stamina:{Cores.RESET} {stamina} | "
            f"{Cores.AZUL_BRILHO}Power:{Cores.RESET} {power} | {Cores.AZUL_BRILHO}Guts:{Cores.RESET} {guts} | "
            f"{Cores.AZUL_BRILHO}Wit:{Cores.RESET} {wit}"
        )
        mood = corredora.getMood()
        energia = Recursos.imprimirValor(str(corredora.getEnergia()) + "/100")
        print(
            f"    {Cores.AZUL_BRILHO}Mood:{Cores.RESET} {mood} | {Cores.AZUL_BRILHO}Energia:{Cores.RESET} {energia}"
        )

    num_nova = Recursos.imprimirValor(str(len(opcoes) + 1))
    print(f"{num_nova} - Criar a tua propria corredora")
    print(f"    {Cores.AMARELO_BRILHO}Orcamento de 800 pontos, com maximo de 200 por stat.{Cores.RESET}")


def pedir_corredora_personalizada():
    # Wizard de criacao de personagem personalizada.
    # EXTENSAO: adiciona novos campos (ex.: habilidade especial) neste fluxo.
    # Como fazer: pede o novo input com validacao, guarda numa variavel e inclui
    # esse valor no retorno desta funcao.
    Recursos.limparConsola()
    Recursos.imprimirSecao("Criar A Tua Corredora")
    Recursos.imprimirAviso("Tens 300 pontos extras para distribuir.")
    Recursos.imprimirInfo("Cada stat inicial comeca em 100 e pode subir ate 200.")
    Recursos.imprimirInfo("O total final sera 800 pontos.\n")

    nome = input(f"{Cores.CIANO_BRILHO}Nome da corredora: {Cores.RESET}").strip()
    while nome == "":
        Recursos.imprimirErro("O nome nao pode ficar vazio.")
        nome = input(f"{Cores.CIANO_BRILHO}Nome da corredora: {Cores.RESET}").strip()

    estilos = [
        ("Velocista", "Foca-se em arrancadas rapidas e corridas curtas.", "Vantagem: excelente em provas curtas e com grande speed."),
        ("Resistente", "Prioriza stamina e resistencia para provas longas.", "Vantagem: muito forte em corridas longas e com ritmo constante."),
        ("Equilibrada", "Procura um bom equilibrio entre velocidade e resistencia.", "Vantagem: adapta-se bem a varios tipos de corrida."),
        ("Tactica", "Valoriza inteligencia de corrida e controlo de ritmo.", "Vantagem: destaca-se em provas onde a estrategia faz a diferenca."),
        ("Poderosa", "Foca-se em forca bruta e agressividade na corrida.", "Vantagem: excelente para ultrapassar adversarios no final."),
        ("Versatil", "Tem um conjunto equilibrado de todas as capacidades.", "Vantagem: oferece bom desempenho em muitas situacoes.")
    ]

    print(f"\n{Cores.MAGENTA_BRILHO}Estilos disponiveis:{Cores.RESET}")
    for indice, (nome_estilo, descricao, vantagem) in enumerate(estilos, start=1):
        num = Recursos.imprimirValor(str(indice))
        nome_est = Recursos.imprimirDestaque(nome_estilo)
        print(f"{num} - {nome_est}")
        print(f"    {Cores.CIANO}- {descricao}{Cores.RESET}")
        print(f"    {Cores.VERDE_BRILHO}-> {vantagem}{Cores.RESET}")

    escolha_estilo = input(f"\n{Cores.AMARELO_BRILHO}Escolhe um estilo: {Cores.RESET}").strip()
    if escolha_estilo.isdigit():
        indice_estilo = int(escolha_estilo) - 1
        if 0 <= indice_estilo < len(estilos):
            estilo = estilos[indice_estilo][0]
        else:
            estilo = estilos[2][0]  # Equilibrada como fallback
    else:
        estilo = estilos[2][0]

    stats = {
        "speed": 100,
        "stamina": 100,
        "power": 100,
        "guts": 100,
        "wit": 100
    }
    pontos_restantes = 300
    ordem_stats = [
        ("Speed", "speed"),
        ("Stamina", "stamina"),
        ("Power", "power"),
        ("Guts", "guts"),
        ("Wit", "wit")
    ]

    while pontos_restantes > 0:
        print(f"\n{Cores.AMARELO_BRILHO}Pontos restantes: {pontos_restantes}{Cores.RESET}")
        print(f"{Cores.MAGENTA_BRILHO}Stats atuais:{Cores.RESET}")
        for nome_stat, chave in ordem_stats:
            val = Recursos.imprimirValor(stats[chave])
            print(f"    {Cores.AZUL_BRILHO}{nome_stat}:{Cores.RESET} {val}")

        escolha = input(f"\n{Cores.CIANO_BRILHO}Escolhe uma stat para aumentar (1-5) ou 0 para cancelar: {Cores.RESET}").strip()

        if escolha == "0":
            return None

        if escolha not in {"1", "2", "3", "4", "5"}:
            Recursos.imprimirErro("Opcao invalida.")
            continue

        nome_stat, chave = ordem_stats[int(escolha) - 1]
        max_extra = min(100, pontos_restantes)
        max_val = Recursos.imprimirValor(max_extra)
        print(f"{Cores.CIANO_BRILHO}Maximo de pontos extras para {nome_stat}: {max_val}{Cores.RESET}")

        valor = input(f"{Cores.CIANO_BRILHO}Quantos pontos extras queres dar a {nome_stat}? {Cores.RESET}").strip()

        if not valor.isdigit():
            Recursos.imprimirErro("Valor invalido.")
            continue

        extra = int(valor)

        if extra < 0 or extra > max_extra:
            Recursos.imprimirErro("Valor invalido.")
            continue

        nova_valor = stats[chave] + extra

        if nova_valor > 200:
            Recursos.imprimirAviso("Essa stat nao pode passar os 200 pontos.")
            continue

        stats[chave] = nova_valor
        pontos_restantes -= extra

    Recursos.imprimirSucesso("\nCorredora criada com sucesso!")
    return nome, estilo, stats["speed"], stats["stamina"], stats["power"], stats["guts"], stats["wit"]


def pedir_opcao_plano_carreira():
    # Mostra os planos existentes e devolve a opcao escolhida.
    Recursos.limparConsola()
    Recursos.imprimirSecao("Plano De Carreira")
    Recursos.imprimirInfo("Cada etapa tem 3 turnos de preparacao antes da corrida principal.")
    Recursos.imprimirAviso("Para continuar a carreira, tens de vencer cada corrida principal.\n")
    
    op1 = Recursos.imprimirDestaque("Sprint Stars")
    print(f"1 - {op1}")
    print(f"    {Cores.CIANO}Corridas curtas. Speed e Power sao muito importantes.{Cores.RESET}")
    
    op2 = Recursos.imprimirDestaque("Derby Classico")
    print(f"2 - {op2}")
    print(f"    {Cores.CIANO}Corridas medias e longas. Stamina e equilibrio sao essenciais.{Cores.RESET}")
    
    op3 = Recursos.imprimirDestaque("Tactica Mile")
    print(f"3 - {op3}")
    print(f"    {Cores.CIANO}Corridas de milha. Wit ajuda muito nas decisoes.{Cores.RESET}")
    
    return input(f"\n{Cores.AMARELO_BRILHO}Escolha: {Cores.RESET}")


def mostrar_menu_principal(
        plano,
        semanaAtual,
        semanaFinal,
        corredora,
        textoProximaCorrida,
        turnosAteProximaCorrida,
        corridaDaSemana):
    # Dashboard principal da semana atual.
    import os
    Recursos.limparConsola()
    
    # Mostrar ASCII art do menu principal
    caminhoAscii = os.path.join(os.path.dirname(__file__), "assets", "ascii", "menu_principal.txt")
    Recursos.imprimirAscii(caminhoAscii)
    
    Recursos.imprimirSecao("Menu Principal")
    plano_val = Recursos.imprimirDestaque(plano)
    print(f"Plano: {plano_val}")
    semana_val = Recursos.imprimirValor(f"{semanaAtual}/{semanaFinal}")
    print(f"Semana: {semana_val}")
    nome = Recursos.imprimirNome(corredora.getNome())
    print(f"Corredora: {nome}")
    energia = Recursos.imprimirValor(f"{corredora.getEnergia()}/100")
    print(f"Energia: {energia}")
    mood = corredora.getMood()
    print(f"Mood: {Cores.VERDE_BRILHO}{mood}{Cores.RESET}")
    prox = Recursos.imprimirDestaque(textoProximaCorrida)
    print(f"Proxima corrida: {prox}")
    turnos = Recursos.imprimirValor(turnosAteProximaCorrida)
    print(f"Turnos de preparacao restantes: {turnos}")

    if corridaDaSemana is not None and corridaDaSemana.getFechada() is False:
        print(f"\n{Cores.VERMELHO_BRILHO}{Cores.NEGRITO}! Corrida principal esta semana: {corridaDaSemana.getNome()}{Cores.RESET}")
        print(f"{Cores.AMARELO}Depois da tua acao, a corrida acontece automaticamente.{Cores.RESET}")

    print(f"\n{Cores.MAGENTA_BRILHO}Opcoes:{Cores.RESET}")
    print("1 - Ver estado da corredora")
    print("2 - Treinar")
    print("3 - Ver calendario de corridas")
    print("4 - Competir agora na corrida principal")
    print("5 - Recriacao")
    print("6 - Descansar")
    print("7 - Avancar semana sem treinar")
    print("8 - Sair")


def pedir_tipo_treino(corredora):
    # Menu de treino com mapeamento da opcao textual para codigo interno.
    Recursos.imprimirSecao("Treino")
    max_stats = Recursos.imprimirValor("1200")
    print(f"Stats maximos: {max_stats} pontos cada.")
    energia = Recursos.imprimirValor(corredora.getEnergia())
    print(f"Energia atual: {energia}")
    mood = corredora.getMood()
    print(f"Mood atual: {mood}")
    print(f"\n{Cores.VERDE_BRILHO}Opcoes de treino:{Cores.RESET}")
    print("1 - Speed  (+70 Speed, +10 Wit,  -8 a -20 energia)")
    print("2 - Stamina (+70 Stamina, +10 Guts, -8 a -20 energia)")
    print("3 - Power  (+65 Power, +15 Guts, -8 a -20 energia)")
    print("4 - Guts   (+60 Guts,  +20 Power, -8 a -20 energia)")
    print("5 - Wit    (+60 Wit,   +10 Speed, -8 a -20 energia)")
    print("6 - Voltar")

    escolha = input(f"\n{Cores.AMARELO_BRILHO}Escolha o treino: {Cores.RESET}")

    if escolha == "1":
        return "speed"
    elif escolha == "2":
        return "stamina"
    elif escolha == "3":
        return "power"
    elif escolha == "4":
        return "guts"
    elif escolha == "5":
        return "wit"
    elif escolha == "6":
        return None

    return ""


def mostrar_calendario(corridas):
    # Vista resumida de todas as corridas da carreira.
    Recursos.imprimirSecao("Calendario De Corridas")

    for corrida in corridas:
        corrida.mostrarResumo()


def mostrar_resultado_corrida(resultado):
    # Ecran de resultado apos disputa de corrida.
    import os
    Recursos.limparConsola()
    
    # Mostrar ASCII de vitoria ou derrota
    if resultado["posicao"] == 1:
        caminhoAscii = os.path.join(os.path.dirname(__file__), "assets", "ascii", "vitoria.txt")
        Recursos.imprimirAscii(
            caminhoAscii,
            f"{Cores.VERDE_BRILHO}{Cores.NEGRITO}VITORIA!{Cores.RESET}"
        )
    else:
        caminhoAscii = os.path.join(os.path.dirname(__file__), "assets", "ascii", "derrota.txt")
        Recursos.imprimirAscii(
            caminhoAscii,
            f"{Cores.AMARELO_BRILHO}Nao desta vez...{Cores.RESET}"
        )
    
    Recursos.pausa(1)
    Recursos.imprimirSecao("Resultado Da Corrida")
    pontuacao = Recursos.imprimirValor(resultado["pontuacao"])
    print(f"Pontuacao final: {pontuacao}")
    posicao = Recursos.imprimirValor(f"{resultado['posicao']}.")
    print(f"Posicao: {posicao} lugar")
    fans = Recursos.imprimirValor(resultado["fans"])
    print(f"Fans ganhos: {fans}")
    energia = Recursos.imprimirValor(resultado["energia"])
    print(f"Energia -{energia}")
    msg = resultado["mensagem"]
    print(f"Resultado: {Cores.VERDE_BRILHO}{msg}{Cores.RESET}")

    for efeito in resultado["efeitos"]:
        print(f"{Cores.AZUL_BRILHO}{efeito}{Cores.RESET}")


def mostrar_fim_carreira(corredora, plano, score, rank, motivo):
    # Resumo final com estatisticas globais da temporada.
    # EXTENSAO: adiciona aqui mais indicadores (ex.: taxa de vitoria, recordes).
    # Como fazer: calcula o valor antes do print e mostra em mais uma linha no
    # mesmo formato das estatisticas existentes.
    Recursos.limparConsola()
    Recursos.imprimirSecao("Fim Da Carreira")
    motivo_val = Recursos.imprimirDestaque(motivo)
    print(f"Motivo: {motivo_val}")
    nome = Recursos.imprimirNome(corredora.getNome())
    print(f"Corredora: {nome}")
    plano_val = Recursos.imprimirDestaque(plano)
    print(f"Plano: {plano_val}")
    score_val = Recursos.imprimirValor(score)
    print(f"Score final: {score_val}")
    rank_val = Recursos.imprimirValor(rank)
    print(f"Rank final: {rank_val}")
    vitorias = Recursos.imprimirValor(corredora.getVitorias())
    print(f"Vitorias: {vitorias}")
    corridas = Recursos.imprimirValor(corredora.getCorridasDisputadas())
    print(f"Corridas disputadas: {corridas}")
    fans = Recursos.imprimirValor(corredora.getFans())
    print(f"Fans: {fans}")
    mood = corredora.getMood()
    print(f"Mood final: {mood}")
    energia = Recursos.imprimirValor(f"{corredora.getEnergia()}/100")
    print(f"Energia final: {energia}")
    media = Recursos.imprimirValor(corredora.getMediaStats())
    print(f"Media de stats: {media}")
    print()

    if corredora.getVitorias() >= 3:
        Recursos.imprimirSucesso("Final: carreira lendaria. A tua corredora dominou a epoca.")
    elif corredora.getVitorias() >= 1:
        Recursos.imprimirInfo("Final: boa carreira. Ha talento para continuar a crescer.")
    else:
        Recursos.imprimirAviso("Final: epoca dificil. Com mais treino, a proxima pode ser melhor.")

    corredora.mostrarEstado()
    Recursos.esperarEnter("Pressiona ENTER para terminar...")

