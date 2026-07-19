import random

try:
    from UmamusumePrettyDerby.Recursos import Cores, Recursos
except ModuleNotFoundError:
    from Recursos import Cores, Recursos


class Corrida:
    """
    Modelo de uma corrida principal no calendario.

    Responsabilidades:
    - Definir parametros da prova (dificuldade/pesos/premios).
    - Simular resultado com base na Corredora.
    - Guardar estado da corrida (fechada, participada, resultado).

    EXTENSAO:
        - Para mecanicas especiais por corrida (chuva, pista pesada, bonus de estilo),
            acrescenta fatores em `calcularPontuacao`.
        - Como fazer: calcula um `modificador` (ex.: 0.9 em chuva) e multiplica a
            variavel `base` antes do bonus de energia.
        """

    def __init__(
            self,
            nome,
            semana,
            distancia,
            dificuldade,
            premioFans,
            pesoSpeed,
            pesoStamina,
            pesoPower,
            pesoGuts,
            pesoWit):
        # Metadados da corrida e pesos de desempenho.
        self.__nome = nome
        self.__semana = semana
        self.__distancia = distancia
        self.__dificuldade = dificuldade
        self.__premioFans = premioFans
        self.__pesoSpeed = pesoSpeed
        self.__pesoStamina = pesoStamina
        self.__pesoPower = pesoPower
        self.__pesoGuts = pesoGuts
        self.__pesoWit = pesoWit
        self.__fechada = False
        self.__participada = False
        self.__resultado = "Pendente"

    # =====================
    # Getters / Setters
    # =====================
    # Mantidos simples para preservar encapsulamento do estado da corrida.
    def getNome(self):
        return self.__nome

    def getSemana(self):
        return self.__semana

    def getDistancia(self):
        return self.__distancia

    def getDificuldade(self):
        return self.__dificuldade

    def getPremioFans(self):
        return self.__premioFans

    def getFechada(self):
        return self.__fechada

    def getParticipada(self):
        return self.__participada

    def getResultado(self):
        return self.__resultado

    def setNome(self, nome):
        self.__nome = nome

    def setSemana(self, semana):
        self.__semana = semana

    def setDistancia(self, distancia):
        self.__distancia = distancia

    def setDificuldade(self, dificuldade):
        self.__dificuldade = dificuldade

    def setPremioFans(self, premioFans):
        self.__premioFans = premioFans

    def setFechada(self, fechada):
        self.__fechada = fechada

    def setParticipada(self, participada):
        self.__participada = participada

    def setResultado(self, resultado):
        self.__resultado = resultado

    def disputar(self, corredora):
        # Fluxo completo da corrida: calcular performance, gerar posicao,
        # aplicar efeitos na corredora e devolver payload para a interface.
        pontuacao = self.calcularPontuacao(corredora)
        posicao = self.calcularPosicao(pontuacao)
        venceu = posicao == 1
        fans = self.calcularFans(posicao)

        corredora.adicionarFans(fans)
        efeitos = corredora.registarCorrida(venceu)
        corredora.gastarEnergia(10)

        self.__fechada = True
        self.__participada = True
        self.__resultado = str(posicao) + ". lugar"

        return {
            "pontuacao": pontuacao,
            "posicao": posicao,
            "fans": fans,
            "energia": 10,
            "mensagem": self.criarMensagemResultado(posicao),
            "efeitos": efeitos
        }

    def faltar(self):
        # Fecha corrida sem participacao (helper para regras futuras).
        self.__fechada = True
        self.__participada = False
        self.__resultado = "Nao participou"

    def calcularPontuacao(self, corredora):
        # Pontuacao base = soma ponderada das stats.
        # Depois aplica mood, bonus de energia e variacao aleatoria.
        base = (
            corredora.getSpeed() * self.__pesoSpeed
            + corredora.getStamina() * self.__pesoStamina
            + corredora.getPower() * self.__pesoPower
            + corredora.getGuts() * self.__pesoGuts
            + corredora.getWit() * self.__pesoWit
        )
        base *= corredora.getMultiplicadorMoodCorrida()
        bonusEnergia = corredora.getEnergia() * 0.45
        variacao = random.randint(-25, 75)
        pontuacao = round(base + bonusEnergia + variacao)

        if pontuacao < 0:
            return 0

        return pontuacao

    def calcularPosicao(self, pontuacao):
        # Converte diferenca para uma faixa de posicoes.
        # EXTENSAO: se quiseres mais granularidade, adiciona mais faixas.
        # Como fazer: insere novos `elif` com intervalos menores e devolve
        # `random.randint(...)` para cada faixa.
        diferenca = pontuacao - self.__dificuldade

        if diferenca >= 0:
            return 1
        elif diferenca >= -90:
            return random.randint(2, 3)
        elif diferenca >= -170:
            return random.randint(4, 6)

        return random.randint(7, 10)

    def calcularFans(self, posicao):
        # Recompensa proporcional ao resultado da corrida.
        if posicao == 1:
            return self.__premioFans
        elif posicao <= 3:
            return round(self.__premioFans * 0.60)
        elif posicao <= 6:
            return round(self.__premioFans * 0.30)

        return round(self.__premioFans * 0.15)

    def criarMensagemResultado(self, posicao):
        # Mensagem curta para feedback narrativo.
        if posicao == 1:
            return "Vitoria! O treino deu resultado."
        elif posicao <= 3:
            return "Podio! Ainda nao foi vitoria, mas foi uma grande corrida."
        elif posicao <= 6:
            return "Resultado aceitavel. Precisa de mais preparacao."

        return "Resultado fraco. A proxima epoca pede outro plano de treino."

    def mostrarResumo(self):
        # Vista compacta usada no calendario.
        semana = Recursos.imprimirValor(str(self.__semana).rjust(2))
        nome = Recursos.imprimirDestaque(self.__nome)
        distancia = Recursos.imprimirValor(self.__distancia)
        dificuldade = Recursos.imprimirValor(self.__dificuldade)
        estado_cor = Cores.VERDE_BRILHO if self.__resultado == "Vitoria!" else Cores.AZUL_BRILHO if self.__participada else Cores.AMARELO_BRILHO
        estado = f"{estado_cor}{self.__resultado}{Cores.RESET}"
        print(
            f"Semana {semana} - {nome} | {distancia} | "
            f"{Cores.MAGENTA_BRILHO}Dificuldade:{Cores.RESET} {dificuldade} | "
            f"{Cores.MAGENTA_BRILHO}Estado:{Cores.RESET} {estado}"
        )

    def mostrarDetalhes(self):
        # Vista detalhada antes da corrida comecar.
        nome = Recursos.imprimirDestaque(self.__nome)
        semana = Recursos.imprimirValor(self.__semana)
        distancia = Recursos.imprimirValor(self.__distancia)
        dificuldade = Recursos.imprimirValor(self.__dificuldade)
        premios = Recursos.imprimirValor(self.__premioFans)
        
        print(f"{Cores.MAGENTA_BRILHO}Nome:{Cores.RESET} {nome}")
        print(f"{Cores.MAGENTA_BRILHO}Semana:{Cores.RESET} {semana}")
        print(f"{Cores.MAGENTA_BRILHO}Distancia:{Cores.RESET} {distancia}")
        print(f"{Cores.MAGENTA_BRILHO}Dificuldade:{Cores.RESET} {dificuldade}")
        print(f"{Cores.MAGENTA_BRILHO}Premio de fans:{Cores.RESET} {premios}")
        
        pSpeed = Recursos.imprimirValor(self.__pesoSpeed)
        pStamina = Recursos.imprimirValor(self.__pesoStamina)
        pPower = Recursos.imprimirValor(self.__pesoPower)
        pGuts = Recursos.imprimirValor(self.__pesoGuts)
        pWit = Recursos.imprimirValor(self.__pesoWit)
        
        print(
            f"{Cores.MAGENTA_BRILHO}Pesos:{Cores.RESET} "
            f"{Cores.AZUL_BRILHO}Speed{Cores.RESET} {pSpeed} | "
            f"{Cores.AZUL_BRILHO}Stamina{Cores.RESET} {pStamina} | "
            f"{Cores.AZUL_BRILHO}Power{Cores.RESET} {pPower} | "
            f"{Cores.AZUL_BRILHO}Guts{Cores.RESET} {pGuts} | "
            f"{Cores.AZUL_BRILHO}Wit{Cores.RESET} {pWit}"
        )

