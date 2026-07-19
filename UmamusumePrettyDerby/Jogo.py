"""
Orquestrador principal do jogo.

Este modulo liga:
- Interface (menus e ecras)
- Regras de dominio (Corredora/Corrida)
- Progressao temporal (semanas)
- Encerramento e score final

EXTENSAO:
- Novos menus de acao semanal devem ser adicionados em `processarOpcao`.
- Novas condicoes de fim de jogo podem ser adicionadas em `verificarFimDoJogo`.
- Como fazer: cria um metodo novo (ex.: `loja()`), adiciona opcao no menu da
    InterfaceJogo e liga um novo `elif` em `processarOpcao`.
- Para fim de jogo extra, valida a condicao em `verificarFimDoJogo` e chama
    `encerrarCarreira("motivo")` quando for verdadeira.
"""

try:
    from UmamusumePrettyDerby.DadosCarreira import criar_corredoras_iniciais, obter_carreira_por_opcao
    from UmamusumePrettyDerby.InterfaceJogo import (
        mostrar_calendario,
        mostrar_corredoras,
        mostrar_fim_carreira,
        mostrar_menu_principal,
        mostrar_resultado_corrida,
        pedir_corredora_personalizada,
        pedir_opcao_plano_carreira,
        pedir_tipo_treino
    )
    from UmamusumePrettyDerby.Introducao import mostrar_introducao
    from UmamusumePrettyDerby.Pontuacao import calcular_rank_final, calcular_score_final
    from UmamusumePrettyDerby.Recursos import Recursos, Cores, GerenciadorMusica
except ModuleNotFoundError:
    from DadosCarreira import criar_corredoras_iniciais, obter_carreira_por_opcao
    from InterfaceJogo import (
        mostrar_calendario,
        mostrar_corredoras,
        mostrar_fim_carreira,
        mostrar_menu_principal,
        mostrar_resultado_corrida,
        pedir_corredora_personalizada,
        pedir_opcao_plano_carreira,
        pedir_tipo_treino
    )
    from Introducao import mostrar_introducao
    from Pontuacao import calcular_rank_final, calcular_score_final
    from Recursos import Recursos, Cores, GerenciadorMusica


class Jogo:
    def __init__(self):
        # Estado global da sessao.
        self.__corredora = None
        self.__corridas = []
        self.__semanaAtual = 1
        self.__semanaFinal = 12
        self.__planoCarreira = ""
        self.__terminado = False
        self.__scoreFinal = 0
        self.__rankFinal = "G"

    # =====================
    # Getters / Setters
    # =====================
    # Mantidos para facilitar testes e evolucao sem expor atributos internos.
    def getCorredora(self):
        return self.__corredora

    def getCorridas(self):
        return self.__corridas

    def getSemanaAtual(self):
        return self.__semanaAtual

    def getSemanaFinal(self):
        return self.__semanaFinal

    def getPlanoCarreira(self):
        return self.__planoCarreira

    def getTerminado(self):
        return self.__terminado

    def setCorredora(self, corredora):
        self.__corredora = corredora

    def setCorridas(self, corridas):
        self.__corridas = corridas

    def setSemanaAtual(self, semanaAtual):
        self.__semanaAtual = semanaAtual

    def setSemanaFinal(self, semanaFinal):
        self.__semanaFinal = semanaFinal

    def setPlanoCarreira(self, planoCarreira):
        self.__planoCarreira = planoCarreira

    def setTerminado(self, terminado):
        self.__terminado = terminado

    def iniciarJogo(self):
        # Arranque da sessao: introducao, escolha de personagem/plano e loop principal.
        mostrar_introducao()
        self.escolherCorredora()
        self.escolherPlanoCarreira()
        
        # Parar a musica do prologo e iniciar musica de fundo
        GerenciadorMusica.pararMusica()
        Recursos.pausa(1)
        GerenciadorMusica.tocarMusica("sounds/jogo_fundo.mp3", loop=True)

        while self.__terminado is False:
            self.verificarFimDoJogo()

            if self.__terminado is False:
                self.mostrarMenuPrincipal()
                opcao = input("Escolha: ")
                Recursos.limparConsola()
                self.processarOpcao(opcao)

    def escolherCorredora(self):
            # Ecran de selecao de corredora pre-definida ou personalizada.
        opcoes = criar_corredoras_iniciais()

        while self.__corredora is None:
            mostrar_corredoras(opcoes)
            escolha = input("\nEscolha: ")

            if escolha.isdigit():
                posicao = int(escolha) - 1

                if 0 <= posicao < len(opcoes):
                    self.__corredora = opcoes[posicao]
                    nome = Recursos.imprimirNome(self.__corredora.getNome())
                    print(f"\n{Cores.VERDE_BRILHO}Escolheste:{Cores.RESET} {nome}")
                    Recursos.esperarEnter()
                elif int(escolha) == len(opcoes) + 1:
                    dados = pedir_corredora_personalizada()

                    if dados is None:
                        Recursos.imprimirAviso("\nCriacao cancelada.")
                        Recursos.esperarEnter()
                    else:
                        nome, estilo, speed, stamina, power, guts, wit = dados
                        self.__corredora = Corredora(nome, estilo, speed, stamina, power, guts, wit)
                        nome_cor = Recursos.imprimirNome(self.__corredora.getNome())
                        print(f"\n{Cores.VERDE_BRILHO}Escolheste:{Cores.RESET} {nome_cor}")
                        Recursos.esperarEnter()
                else:
                    Recursos.imprimirErro("\nOpcao invalida.")
                    Recursos.esperarEnter()
            else:
                Recursos.imprimirErro("\nOpcao invalida.")
                Recursos.esperarEnter()

    def escolherPlanoCarreira(self):
        # Seleciona conjunto de corridas (calendario da temporada).
        while self.__planoCarreira == "":
            escolha = pedir_opcao_plano_carreira()
            plano, corridas = obter_carreira_por_opcao(escolha)

            if plano != "":
                self.__planoCarreira = plano
                self.__corridas = corridas
            else:
                Recursos.imprimirErro("\nOpcao invalida.")
                Recursos.esperarEnter()

        self.__semanaFinal = self.__corridas[-1].getSemana()
        plano_val = Recursos.imprimirDestaque(self.__planoCarreira)
        print(f"\n{Cores.VERDE_BRILHO}Plano escolhido:{Cores.RESET} {plano_val}")
        Recursos.esperarEnter()

    def mostrarMenuPrincipal(self):
        # Renderiza o dashboard da semana atual.
        mostrar_menu_principal(
            self.__planoCarreira,
            self.__semanaAtual,
            self.__semanaFinal,
            self.__corredora,
            self.obterTextoProximaCorrida(),
            self.obterTurnosAteProximaCorrida(),
            self.obterCorridaDaSemana()
        )

    def processarOpcao(self, opcao):
        # Router das escolhas do jogador no menu principal.
        # EXTENSAO: adiciona novos `elif` para funcionalidades extra.
        # Como fazer: cria um numero novo no menu e aponta para um metodo da classe.
        if opcao == "1":
            self.__corredora.mostrarEstado()
            Recursos.esperarEnter()

        elif opcao == "2":
            self.menuTreino()

        elif opcao == "3":
            self.mostrarCalendario()
            Recursos.esperarEnter()

        elif opcao == "4":
            self.participarCorridaDaSemana()

        elif opcao == "5":
            self.recriacao()

        elif opcao == "6":
            self.descansar()

        elif opcao == "7":
            self.avancarSemanaSemTreino()

        elif opcao == "8":
            Recursos.imprimirAviso("\nSaindo do jogo.")
            self.__terminado = True

        else:
            Recursos.imprimirErro("\nOpcao invalida.")
            Recursos.esperarEnter()

    def menuTreino(self):
        # Fluxo de treino semanal com validacao de opcao.
        tipoTreino = pedir_tipo_treino(self.__corredora)

        if tipoTreino is None:
            return

        if tipoTreino == "":
            Recursos.imprimirErro("\nOpcao invalida.")
            Recursos.esperarEnter()
            return

        treinou, mensagens = self.__corredora.treinar(tipoTreino)

        print()
        for mensagem in mensagens:
            print(f"{Cores.CIANO_BRILHO}{mensagem}{Cores.RESET}")

        if treinou:
            self.resolverFimDaSemana()
        else:
            Recursos.esperarEnter()

    def mostrarCalendario(self):
        # Encaminha para a interface de calendario.
        mostrar_calendario(self.__corridas)

    def participarCorridaDaSemana(self):
        # Permite disparar manualmente a corrida da semana atual.
        corrida = self.obterCorridaDaSemana()

        if corrida is None:
            Recursos.imprimirAviso("\nNao existe corrida marcada para esta semana.")
            Recursos.esperarEnter()
            return

        if corrida.getFechada():
            Recursos.imprimirAviso("\nEsta corrida ja ficou fechada.")
            Recursos.esperarEnter()
            return

        self.disputarCorrida(corrida)
        if self.__terminado is False:
            self.avancarSemanaDepoisDeAcao()

    def disputarCorrida(self, corrida):
        # Executa corrida, mostra resultado e verifica condicoes de fim.
        Recursos.imprimirSecao("Corrida")
        corrida.mostrarDetalhes()
        print()

        resultado = corrida.disputar(self.__corredora)
        mostrar_resultado_corrida(resultado)

        if resultado["posicao"] != 1:
            self.encerrarCarreira("Perdeste a corrida principal: " + corrida.getNome())
            return

        Recursos.imprimirSucesso("Objetivo cumprido: vitoria na corrida principal.")

        if corrida.getSemana() == self.__semanaFinal:
            Recursos.esperarEnter("Pressiona ENTER para ver o resumo da carreira...")
            self.encerrarCarreira("Venceste a corrida final e completaste a carreira.")

    def descansar(self):
        # Acao semanal de recuperacao total de energia.
        recuperado = self.__corredora.descansar()
        rec_val = Recursos.imprimirValor(recuperado)
        ene_val = Recursos.imprimirValor(str(self.__corredora.getEnergia()) + "/100")
        print(f"\n{Cores.CIANO_BRILHO}A corredora descansou e recuperou {rec_val} pontos de energia.{Cores.RESET}")
        print(f"{Cores.AZUL_BRILHO}Energia atual: {ene_val}{Cores.RESET}")
        self.resolverFimDaSemana()

    def recriacao(self):
        # Acao semanal focada em mood + ganhos menores.
        Recursos.imprimirSecao("Recriacao")
        Recursos.imprimirInfo("A corredora teve um momento leve fora dos treinos.")
        Recursos.imprimirInfo("Isto melhora o mood e da ganhos pequenos de stats.")
        print()

        mensagens = self.__corredora.recriar()

        for mensagem in mensagens:
            print(f"{Cores.MAGENTA_BRILHO}{mensagem}{Cores.RESET}")

        self.resolverFimDaSemana()

    def avancarSemanaSemTreino(self):
        # Acao neutra para passar turno sem efeitos de treino.
        self.__corredora.passarTurnoSemTreino()
        Recursos.imprimirInfo("\nA semana passou sem treino especial.")
        self.resolverFimDaSemana()

    def resolverFimDaSemana(self):
        # Ao finalizar uma acao, resolve corrida obrigatoria se existir,
        # e depois avanca para a semana seguinte.
        corrida = self.obterCorridaDaSemana()

        if corrida is not None and corrida.getFechada() is False:
            Recursos.imprimirAviso("\nChegou a corrida principal: " + Recursos.imprimirDestaque(corrida.getNome()))
            Recursos.imprimirInfo("A carreira continua apenas com uma vitoria.")
            print()
            self.disputarCorrida(corrida)

        if self.__terminado is False:
            self.avancarSemanaDepoisDeAcao()

    def avancarSemanaDepoisDeAcao(self):
        # Incrementa o calendario global quando a carreira ainda esta ativa.
        if self.__terminado:
            return

        self.__semanaAtual += 1
        semana_val = Recursos.imprimirValor(self.__semanaAtual)
        print(f"\n{Cores.VERDE_BRILHO}Avancaste para a semana {semana_val}{Cores.RESET}")
        Recursos.esperarEnter()

    def obterCorridaDaSemana(self):
        # Procura corrida exatamente marcada para a semana atual.
        for corrida in self.__corridas:
            if corrida.getSemana() == self.__semanaAtual:
                return corrida

        return None

    def obterTextoProximaCorrida(self):
        # Texto de apoio para o menu principal.
        for corrida in self.__corridas:
            if corrida.getFechada() is False and corrida.getSemana() >= self.__semanaAtual:
                return corrida.getNome() + " (semana " + str(corrida.getSemana()) + ")"

        return "nenhuma"

    def obterTurnosAteProximaCorrida(self):
        # Numero de turnos restantes ate a proxima corrida nao fechada.
        for corrida in self.__corridas:
            if corrida.getFechada() is False and corrida.getSemana() >= self.__semanaAtual:
                return corrida.getSemana() - self.__semanaAtual + 1

        return 0

    def encerrarCarreira(self, motivo):
        # Fecha sessao, calcula score/rank e apresenta resumo final.
        if self.__terminado:
            return

        self.__scoreFinal = calcular_score_final(self.__corredora)
        self.__rankFinal = calcular_rank_final(self.__scoreFinal)
        self.__terminado = True

        # Parar musica de fundo e tocar som de fim
        GerenciadorMusica.pararMusica()
        GerenciadorMusica.tocarSom("sounds/fim_carreira.mp3", loop=False)
        Recursos.pausa(2)

        mostrar_fim_carreira(
            self.__corredora,
            self.__planoCarreira,
            self.__scoreFinal,
            self.__rankFinal,
            motivo
        )

    def verificarFimDoJogo(self):
        # Condicao de fim por calendario completo.
        # EXTENSAO: adicionar aqui condicoes extra (ex.: objetivo de fans).
        # Como fazer: depois da verificacao atual, adiciona outro `if` e encerra
        # com `self.encerrarCarreira(...)` para mostrar o resumo final.
        if self.__semanaAtual <= self.__semanaFinal:
            return False

        self.encerrarCarreira("Completaste todas as corridas principais da carreira.")
        return True

