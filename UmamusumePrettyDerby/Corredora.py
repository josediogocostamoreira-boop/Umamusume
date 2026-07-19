import random

try:
    from UmamusumePrettyDerby.Recursos import Cores, Recursos
except ModuleNotFoundError:
    from Recursos import Cores, Recursos


class Corredora:
    """
    Modelo principal da atleta.

    Responsabilidades:
    - Guardar stats, energia, mood e progresso da carreira.
    - Aplicar regras de treino, descanso, recreacao e corridas.

    EXTENSAO:
    - Novos atributos permanentes (ex.: tecnica, carisma) devem ser adicionados
            aqui com getters/setters e integracao em treino/corrida.
        - Como fazer: cria `self.__novoAtributo` no `__init__`, adiciona `get/set` e
            usa esse atributo em `calcularPontuacao` (Corrida) ou `treinar` (Corredora).
    """

    # Limites globais para manter o balanceamento consistente.
    STAT_MAXIMO = 1200
    ENERGIA_MAXIMA = 100
    MOODS = ["Awful", "Bad", "Normal", "Good", "Great"]
    MOOD_NORMAL = 2

    def __init__(self, nome, estilo, speed, stamina, power, guts, wit):
        # Base da ficha da corredora.
        self.__nome = nome
        self.__estilo = estilo
        self.__speed = self.__limitarStat(speed)
        self.__stamina = self.__limitarStat(stamina)
        self.__power = self.__limitarStat(power)
        self.__guts = self.__limitarStat(guts)
        self.__wit = self.__limitarStat(wit)
        self.__energia = 100
        self.__fans = 0
        self.__vitorias = 0
        self.__corridasDisputadas = 0
        self.__moodIndice = self.MOOD_NORMAL
        self.__ultimoTreino = ""
        self.__treinosMesmoTipo = 0
        self.__corridasSeguidas = 0

    # =====================
    # Getters / Setters
    # =====================
    # Estes metodos encapsulam o estado interno.
    # EXTENSAO: se adicionares novos atributos, cria metodos equivalentes.
    # Como fazer: segue o padrao getX/setX e usa `__limitarStat` se for stat numerica.
    def getNome(self):
        return self.__nome

    def getEstilo(self):
        return self.__estilo

    def getSpeed(self):
        return self.__speed

    def getStamina(self):
        return self.__stamina

    def getPower(self):
        return self.__power

    def getGuts(self):
        return self.__guts

    def getWit(self):
        return self.__wit

    def getEnergia(self):
        return self.__energia

    def getMood(self):
        return self.MOODS[self.__moodIndice]

    def getMoodIndice(self):
        return self.__moodIndice

    def getFans(self):
        return self.__fans

    def getVitorias(self):
        return self.__vitorias

    def getCorridasDisputadas(self):
        return self.__corridasDisputadas

    def setNome(self, nome):
        self.__nome = nome

    def setEstilo(self, estilo):
        self.__estilo = estilo

    def setSpeed(self, speed):
        self.__speed = self.__limitarStat(speed)

    def setStamina(self, stamina):
        self.__stamina = self.__limitarStat(stamina)

    def setPower(self, power):
        self.__power = self.__limitarStat(power)

    def setGuts(self, guts):
        self.__guts = self.__limitarStat(guts)

    def setWit(self, wit):
        self.__wit = self.__limitarStat(wit)

    def setEnergia(self, energia):
        if energia < 0:
            self.__energia = 0
        elif energia > self.ENERGIA_MAXIMA:
            self.__energia = self.ENERGIA_MAXIMA
        else:
            self.__energia = energia

    def setMood(self, mood):
        if isinstance(mood, str):
            mood = mood.strip().lower()

            for indice in range(len(self.MOODS)):
                if self.MOODS[indice].lower() == mood:
                    self.__moodIndice = indice
                    return

        if isinstance(mood, int):
            if mood < 0:
                self.__moodIndice = 0
            elif mood >= len(self.MOODS):
                self.__moodIndice = len(self.MOODS) - 1
            else:
                self.__moodIndice = mood

    def setFans(self, fans):
        if fans < 0:
            self.__fans = 0
        else:
            self.__fans = fans

    def setVitorias(self, vitorias):
        if vitorias < 0:
            self.__vitorias = 0
        else:
            self.__vitorias = vitorias

    def setCorridasDisputadas(self, corridasDisputadas):
        if corridasDisputadas < 0:
            self.__corridasDisputadas = 0
        else:
            self.__corridasDisputadas = corridasDisputadas

    def treinar(self, tipoTreino):
        # Impede treino quando energia esta demasiado baixa.
        if self.__energia < 8:
            return False, [
                "Energia demasiado baixa para treinar.",
                "Usa descansar para evitar uma epoca desastrosa."
            ]

        tipoTreino = tipoTreino.lower()
        mensagens = []

        # Cada treino aumenta stats principais e secundarias.
        # EXTENSAO: para novo treino (ex.: "tatica"), adiciona mais um bloco `elif`.
        # Como fazer: define `ganhos` e `nomeTreino`, e inclui a nova opcao no menu
        # de `pedir_tipo_treino` em InterfaceJogo.py.
        if tipoTreino == "speed":
            ganhos = {"speed": 70, "wit": 10}
            nomeTreino = "Speed"
        elif tipoTreino == "stamina":
            ganhos = {"stamina": 70, "guts": 10}
            nomeTreino = "Stamina"
        elif tipoTreino == "power":
            ganhos = {"power": 65, "guts": 15}
            nomeTreino = "Power"
        elif tipoTreino == "guts":
            ganhos = {"guts": 60, "power": 20}
            nomeTreino = "Guts"
        elif tipoTreino == "wit":
            ganhos = {"wit": 60, "speed": 10}
            nomeTreino = "Wit"
        else:
            return False, ["Treino invalido."]

        custoEnergia = random.randint(8, 20)
        fator = self.__calcularFatorTreino()

        if fator < 1:
            mensagens.append("O treino rendeu menos por causa da energia ou do mood.")
        else:
            mensagens.append("Treino de " + nomeTreino + " concluido com sucesso.")

        for stat in ganhos:
            ganho = int(ganhos[stat] * fator)
            ganhoReal = self.adicionarStat(stat, ganho)
            mensagens.append(stat.capitalize() + " +" + str(ganhoReal))

        self.gastarEnergia(custoEnergia)
        mensagens.append("Energia -" + str(custoEnergia))
        mensagens += self.__registarTreino(tipoTreino)

        return True, mensagens

    def adicionarStat(self, stat, valor):
        # Atualiza uma stat com limites de seguranca e devolve ganho real.
        stat = stat.lower()

        if stat == "speed":
            anterior = self.__speed
            self.setSpeed(self.__speed + valor)
            return self.__speed - anterior
        elif stat == "stamina":
            anterior = self.__stamina
            self.setStamina(self.__stamina + valor)
            return self.__stamina - anterior
        elif stat == "power":
            anterior = self.__power
            self.setPower(self.__power + valor)
            return self.__power - anterior
        elif stat == "guts":
            anterior = self.__guts
            self.setGuts(self.__guts + valor)
            return self.__guts - anterior
        elif stat == "wit":
            anterior = self.__wit
            self.setWit(self.__wit + valor)
            return self.__wit - anterior

        return 0

    def gastarEnergia(self, valor):
        # Wrapper para manter chamadas de negocio legiveis.
        self.setEnergia(self.__energia - valor)

    def recuperarEnergia(self, valor):
        # Recuperacao parcial (nao usada no loop atual, mas pronta para eventos).
        energiaAnterior = self.__energia
        self.setEnergia(self.__energia + valor)
        return self.__energia - energiaAnterior

    def descansar(self):
        # Descanso repoe energia e limpa penalizadores de sequencia.
        energiaAnterior = self.__energia
        self.setEnergia(self.ENERGIA_MAXIMA)
        self.__limparSequencias()
        return self.__energia - energiaAnterior

    def recriar(self):
        # Recreacao melhora mood e aplica ganhos pequenos em todas as stats.
        # EXTENSAO: aqui e um bom ponto para eventos aleatorios positivos.
        # Como fazer: cria uma chance com `random.random()` e adiciona mensagens no
        # array `mensagens` para o jogador ver o efeito.
        mensagens = []
        moodAnterior = self.getMood()
        self.__aumentarMood()
        moodAtual = self.getMood()

        if moodAnterior == moodAtual:
            mensagens.append("Mood ja estava no maximo: " + moodAtual)
        else:
            mensagens.append("Mood aumentou: " + moodAnterior + " -> " + moodAtual)

        ganhos = {
            "speed": random.randint(3, 7),
            "stamina": random.randint(3, 7),
            "power": random.randint(3, 7),
            "guts": random.randint(3, 7),
            "wit": random.randint(3, 7)
        }

        for stat in ganhos:
            ganhoReal = self.adicionarStat(stat, ganhos[stat])
            mensagens.append(stat.capitalize() + " +" + str(ganhoReal))

        self.__limparSequencias()
        return mensagens

    def passarTurnoSemTreino(self):
        # Avanco de semana sem acao: remove stacks de repeticao.
        self.__limparSequencias()

    def adicionarFans(self, valor):
        # Centraliza acumulacao de fans.
        self.setFans(self.__fans + valor)

    def registarCorrida(self, venceu):
        # Regista estatisticas de carreira apos corrida.
        mensagens = []
        self.__corridasDisputadas += 1
        self.__corridasSeguidas += 1

        if venceu:
            self.__vitorias += 1

        if self.__corridasSeguidas >= 2:
            mensagem = self.__diminuirMood()

            if mensagem != "":
                mensagens.append("Muitas corridas seguidas baixaram o mood: " + mensagem)

            self.__corridasSeguidas = 0

        return mensagens

    def getMediaStats(self):
        # Media simples usada no score final.
        total = self.__speed + self.__stamina + self.__power + self.__guts + self.__wit
        return round(total / 5)

    def mostrarEstado(self):
        # Renderiza um resumo detalhado para o menu de estado.
        Recursos.imprimirSecao("Estado Da Corredora")
        nome = Recursos.imprimirNome(self.__nome)
        print(f"{Cores.MAGENTA_BRILHO}Nome:{Cores.RESET} {nome}")
        estilo = Recursos.imprimirValor(self.__estilo)
        print(f"{Cores.MAGENTA_BRILHO}Estilo:{Cores.RESET} {estilo}")
        energia = Recursos.imprimirValor(str(self.__energia) + "/" + str(self.ENERGIA_MAXIMA))
        print(f"{Cores.MAGENTA_BRILHO}Energia:{Cores.RESET} {energia}")
        mood = self.getMood()
        print(f"{Cores.MAGENTA_BRILHO}Mood:{Cores.RESET} {Cores.VERDE_BRILHO}{mood}{Cores.RESET}")
        fans = Recursos.imprimirValor(self.__fans)
        print(f"{Cores.MAGENTA_BRILHO}Fans:{Cores.RESET} {fans}")
        vitorias = Recursos.imprimirValor(self.__vitorias)
        print(f"{Cores.MAGENTA_BRILHO}Vitorias:{Cores.RESET} {vitorias}")
        corridasDisp = Recursos.imprimirValor(self.__corridasDisputadas)
        print(f"{Cores.MAGENTA_BRILHO}Corridas disputadas:{Cores.RESET} {corridasDisp}")
        print()
        speed = Recursos.imprimirValor(self.__formatarStat(self.__speed))
        print(f"{Cores.AZUL_BRILHO}Speed:{Cores.RESET} {speed}")
        stamina = Recursos.imprimirValor(self.__formatarStat(self.__stamina))
        print(f"{Cores.AZUL_BRILHO}Stamina:{Cores.RESET} {stamina}")
        power = Recursos.imprimirValor(self.__formatarStat(self.__power))
        print(f"{Cores.AZUL_BRILHO}Power:{Cores.RESET} {power}")
        guts = Recursos.imprimirValor(self.__formatarStat(self.__guts))
        print(f"{Cores.AZUL_BRILHO}Guts :{Cores.RESET} {guts}")
        wit = Recursos.imprimirValor(self.__formatarStat(self.__wit))
        print(f"{Cores.AZUL_BRILHO}Wit  :{Cores.RESET} {wit}")

    def __calcularFatorTreino(self):
        # Determina se o treino rende totalmente ou com penalizacao.
        # Depende de energia + mood.
        if self.__energia >= 60:
            chanceSucesso = 0.97
        elif self.__energia >= 30:
            chanceSucesso = 0.88
        else:
            chanceSucesso = 0.68

        chanceSucesso += (self.__moodIndice - self.MOOD_NORMAL) * 0.07

        if chanceSucesso < 0.15:
            chanceSucesso = 0.15
        elif chanceSucesso > 0.98:
            chanceSucesso = 0.98

        if random.random() <= chanceSucesso:
            return self.getMultiplicadorMoodTreino()

        return 0.70 * self.getMultiplicadorMoodTreino()

    def getMultiplicadorMoodTreino(self):
        # Multiplicador de desempenho em treino por mood.
        multiplicadores = [0.75, 0.90, 1.00, 1.08, 1.18]
        return multiplicadores[self.__moodIndice]

    def getMultiplicadorMoodCorrida(self):
        # Multiplicador de desempenho em corrida por mood.
        multiplicadores = [0.88, 0.94, 1.00, 1.04, 1.08]
        return multiplicadores[self.__moodIndice]

    def __registarTreino(self, tipoTreino):
        # Controla repeticao de treino para evitar spam da mesma opcao.
        mensagens = []

        if self.__ultimoTreino == tipoTreino:
            self.__treinosMesmoTipo += 1
        else:
            self.__ultimoTreino = tipoTreino
            self.__treinosMesmoTipo = 1

        if self.__treinosMesmoTipo >= 4:
            mensagem = self.__diminuirMood()

            if mensagem != "":
                mensagens.append("Treinar sempre a mesma coisa baixou o mood: " + mensagem)

            self.__treinosMesmoTipo = 0

        return mensagens

    def __aumentarMood(self):
        # Sobe um nivel de mood sem ultrapassar o maximo.
        if self.__moodIndice < len(self.MOODS) - 1:
            self.__moodIndice += 1

    def __diminuirMood(self):
        # Desce um nivel de mood e devolve transicao para feedback visual.
        moodAnterior = self.getMood()

        if self.__moodIndice > 0:
            self.__moodIndice -= 1

        moodAtual = self.getMood()

        if moodAnterior == moodAtual:
            return ""

        return moodAnterior + " -> " + moodAtual

    def __limparSequencias(self):
        # Reinicia contadores de sequencia (treino repetido/corridas seguidas).
        self.__ultimoTreino = ""
        self.__treinosMesmoTipo = 0
        self.__corridasSeguidas = 0

    def __formatarStat(self, valor):
        # Formata stat com padding e barra visual.
        return str(valor).rjust(4) + "/" + str(self.STAT_MAXIMO) + " " + self.__barra(valor)

    def __barra(self, valor):
        # Converte um valor numerico numa barra ASCII para feedback imediato.
        tamanho = 20
        preenchido = round((valor / self.STAT_MAXIMO) * tamanho)
        return "[" + ("#" * preenchido) + ("." * (tamanho - preenchido)) + "]"

    def __limitarStat(self, valor):
        # Garante que nenhuma stat fica abaixo de 0 ou acima do limite global.
        if valor < 0:
            return 0

        if valor > self.STAT_MAXIMO:
            return self.STAT_MAXIMO

        return valor

