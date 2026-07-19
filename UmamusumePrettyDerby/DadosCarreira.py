"""
Dados de configuracao da carreira.

Este modulo centraliza:
- Corredoras iniciais pre-definidas.
- Planos de carreira.
- Calendario e parametros de cada corrida.

EXTENSAO:
- Para criar um novo plano, adiciona uma funcao `criar_carreira_<nome>()`
  e regista a opcao em `obter_carreira_por_opcao`.
- Como fazer: copia uma carreira existente, ajusta nome/dificuldade/pesos e
    depois adiciona um novo `elif` no router de opcoes.
"""

try:
    from UmamusumePrettyDerby.Corredora import Corredora
    from UmamusumePrettyDerby.Corrida import Corrida
except ModuleNotFoundError:
    from Corredora import Corredora
    from Corrida import Corrida


def criar_corredoras_iniciais():
    # Pool de personagens disponiveis no inicio.
    # EXTENSAO: adiciona mais Corredora(...) para aumentar variedade.
    # Como fazer: usa o mesmo formato (nome, estilo, 5 stats) e mantem os valores
    # numa faixa parecida para nao quebrar o balanceamento.
    return [
        Corredora("Agnes Tachyon", "Especialista em corridas curtas", 240, 160, 170, 120, 130),
        Corredora("Gold Ship", "Forte em provas longas", 170, 240, 180, 220, 120),
        Corredora("Tamamo Cross", "Equilibrada e tactica", 190, 220, 160, 180, 180),
        Corredora("Oguri Cap", "Crescimento equilibrado", 190, 190, 190, 190, 190)
    ]


def obter_carreira_por_opcao(opcao):
    # Router simples de opcoes de menu para plano de carreira.
    # EXTENSAO: adiciona aqui novas opcoes quando criares mais planos.
    # Como fazer: cria `elif opcao == "N": return "Nome", criar_carreira_nome()`.
    if opcao == "1":
        return "Sprint Stars", criar_carreira_sprint()
    elif opcao == "2":
        return "Derby Classico", criar_carreira_classica()
    elif opcao == "3":
        return "Tactica Mile", criar_carreira_tactica()

    return "", []


def criar_carreira_sprint():
    # Plano focado em corridas curtas (speed/power com maior impacto).
    return [
        Corrida("Estreia das Promessas", 3, "Curta", 250, 800, 0.50, 0.10, 0.25, 0.05, 0.10),
        Corrida("Taca Relampago", 6, "Curta", 335, 1600, 0.50, 0.10, 0.30, 0.00, 0.10),
        Corrida("Festival dos 1200m", 9, "Curta", 435, 2800, 0.55, 0.10, 0.25, 0.00, 0.10),
        Corrida("Grande Premio Sprint", 12, "Curta", 535, 5000, 0.55, 0.10, 0.25, 0.00, 0.10)
    ]


def criar_carreira_classica():
    # Plano equilibrado com foco progressivo em stamina.
    return [
        Corrida("Debut Classico", 3, "Media", 235, 900, 0.30, 0.25, 0.25, 0.10, 0.10),
        Corrida("Copa de Primavera", 6, "Media", 310, 1800, 0.30, 0.25, 0.25, 0.10, 0.10),
        Corrida("Derby da Academia", 9, "Longa", 385, 3200, 0.25, 0.35, 0.20, 0.15, 0.05),
        Corrida("Coroa Classica", 12, "Longa", 460, 5600, 0.25, 0.35, 0.20, 0.15, 0.05)
    ]


def criar_carreira_tactica():
    # Plano em que Wit ganha muito peso no desempenho.
    return [
        Corrida("Teste de Milha", 3, "Milha", 245, 850, 0.30, 0.15, 0.15, 0.05, 0.35),
        Corrida("Mile Cup", 6, "Milha", 320, 1700, 0.30, 0.15, 0.15, 0.05, 0.35),
        Corrida("Noite das Estrategias", 9, "Milha", 405, 3000, 0.25, 0.15, 0.15, 0.05, 0.40),
        Corrida("Final Tactica Mile", 12, "Milha", 490, 5300, 0.25, 0.15, 0.15, 0.05, 0.40)
    ]

