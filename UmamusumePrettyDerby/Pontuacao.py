"""
Regras de pontuacao final da carreira.

EXTENSAO:
- Se quiseres mudar o meta do jogo, ajusta os pesos de score.
- Se adicionares novas metricas (ex.: trofeus, missões), soma-as em
    `calcular_score_final` e adapta os thresholds de rank.
- Como fazer: adiciona o novo termo no `return int(...)`, testa 2-3 carreiras e
    depois reajusta os limites em `calcular_rank_final` para manter progressao.
"""

def calcular_score_final(corredora):
        # Score composto por performance tecnica, resultados e estado final.
    return int(
        corredora.getMediaStats() * 6
        + corredora.getFans()
        + corredora.getVitorias() * 500
        + corredora.getCorridasDisputadas() * 150
        + corredora.getEnergia() * 5
        + corredora.getMoodIndice() * 250
    )


def calcular_rank_final(score):
    # Conversao de score numerico para rank textual.
    # EXTENSAO: para ranks adicionais (ex.: SS), adiciona mais faixas no topo.
    # Como fazer: coloca primeiro os thresholds mais altos para evitar colisao
    # logica nos `elif` seguintes.
    if score >= 15000:
        return "S"
    elif score >= 12000:
        return "A"
    elif score >= 9000:
        return "B"
    elif score >= 6500:
        return "C"
    elif score >= 4500:
        return "D"
    elif score >= 3000:
        return "E"
    elif score >= 1800:
        return "F"

    return "G"
