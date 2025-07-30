import datetime

CAMPOS_ANIMAL_NOVO = 6
CAMPOS_ANIMAL_ANTIGO = 5


def carregar_dados_do_csv(nome_arquivo_csv):
    matriz_carregada = []
    try:
        with open(nome_arquivo_csv, 'r', encoding='utf-8') as arquivo_entrada:
            for linha in arquivo_entrada:
                linha_limpa = linha.strip()
                if linha_limpa:
                    try:
                        partes = linha_limpa.split(',')
                        dados_animal = []
                        if len(partes) == CAMPOS_ANIMAL_NOVO:
                            dados_animal = [
                                int(partes[0]),
                                float(partes[1]),
                                int(partes[2]),
                                int(partes[3]),
                                float(partes[4]),
                                partes[5]
                            ]
                            matriz_carregada.append(dados_animal)
                        elif len(partes) == CAMPOS_ANIMAL_ANTIGO:
                            dados_animal = [
                                int(partes[0]),
                                float(partes[1]),
                                int(partes[2]),
                                int(partes[3]),
                                float(partes[4]),
                                ""
                            ]
                            matriz_carregada.append(dados_animal)
                        else:
                            print(
                                f"Aviso: Linha malformada no CSV ignorada (esperava {CAMPOS_ANIMAL_ANTIGO} ou {CAMPOS_ANIMAL_NOVO} colunas): '{linha_limpa}'")
                    except ValueError:
                        print(
                            f"Aviso: Linha com dados não numéricos/formato incorreto no CSV ignorada: '{linha_limpa}'")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao carregar '{nome_arquivo_csv}': {e}")
    return matriz_carregada


def calcular_peso_total_rebanho(matriz_dados):
    peso_total = 0.0
    if matriz_dados:
        for animal_info in matriz_dados:
            if len(animal_info) > 1:
                try:
                    peso_total += float(animal_info[1])
                except ValueError:
                    print(f"Aviso: Peso inválido encontrado para um animal: {animal_info[1]}")
    return peso_total


def calcular_valor_animal(animal_info):
    if len(animal_info) >= CAMPOS_ANIMAL_ANTIGO:
        try:
            peso_kg = float(animal_info[1])
            valor_arroba_compra = float(animal_info[4])
            if valor_arroba_compra > 0:
                return (peso_kg / 30.0) * valor_arroba_compra
            return 0.0
        except (ValueError, TypeError):
            print(f"Aviso: Dados inválidos para cálculo de valor do animal: {animal_info}")
            return 0.0
    return 0.0


def calcular_valor_total_rebanho(matriz_dados):
    valor_total = 0.0
    if matriz_dados:
        for animal_info in matriz_dados:
            valor_total += calcular_valor_animal(animal_info)
    return valor_total


def salvar_dados_completos(matriz_dados, nome_arquivo_csv, nome_arquivo_formatado):
    sucesso_formatado = False
    sucesso_csv = False

    try:
        with open(nome_arquivo_formatado, 'w', encoding='utf-8') as arquivo_saida:
            if not matriz_dados:
                arquivo_saida.write("Nenhum animal foi registrado.\n")
            else:
                cabecalho = f"{'Índice':<7} | {'Brinco':<10} | {'Peso (kg)':<10} | {'Peso (@)':<10} | {'Mês':<5} | {'Ano':<7} | {'Vlr Arroba R$':<15} | {'Vacinas':<30}\n"
                arquivo_saida.write(cabecalho)
                separador_largura = 115
                separador = "-" * separador_largura + "\n"
                arquivo_saida.write(separador)

                for indice, animal_info in enumerate(matriz_dados):
                    peso_kg = animal_info[1]
                    peso_arroba = peso_kg / 30.0
                    vacinas = animal_info[5] if len(animal_info) == CAMPOS_ANIMAL_NOVO else ""
                    linha_dados_animal = f"{indice:<7} | {str(animal_info[0]):<10} | {peso_kg:<10.2f} | {peso_arroba:<10.2f} | {str(animal_info[2]):<5} | {str(animal_info[3]):<7} | {animal_info[4]:<15.2f} | {vacinas:<30}\n"
                    arquivo_saida.write(linha_dados_animal)

                arquivo_saida.write(separador)
                peso_total_do_rebanho = calcular_peso_total_rebanho(matriz_dados)
                linha_peso_total = f"O peso total de todos os animais registrados é: {peso_total_do_rebanho:.2f} kg\n"
                arquivo_saida.write(linha_peso_total)

                valor_total_estimado = calcular_valor_total_rebanho(matriz_dados)
                linha_valor_total = f"O valor total estimado do rebanho é: R$ {valor_total_estimado:.2f}\n"
                arquivo_saida.write(linha_valor_total)
            sucesso_formatado = True
    except IOError:
        print(f"Erro IO: Não foi possível escrever no arquivo '{nome_arquivo_formatado}'.")
    except Exception as e:
        print(f"Erro inesperado ao salvar '{nome_arquivo_formatado}': {e}")

    try:
        with open(nome_arquivo_csv, 'w', encoding='utf-8') as arquivo_saida_csv:
            if matriz_dados:
                for animal_info in matriz_dados:
                    if len(animal_info) == CAMPOS_ANIMAL_ANTIGO:
                        animal_info_completo = list(animal_info) + [""]
                    else:
                        animal_info_completo = list(animal_info)

                    linha_para_salvar_lista_str = [str(item) for item in animal_info_completo]
                    linha_para_salvar_str = ",".join(linha_para_salvar_lista_str)
                    arquivo_saida_csv.write(linha_para_salvar_str + "\n")
            else:
                arquivo_saida_csv.write("")
            sucesso_csv = True
    except IOError:
        print(f"Erro IO: Não foi possível escrever no arquivo '{nome_arquivo_csv}'.")
    except Exception as e:
        print(f"Erro inesperado ao salvar '{nome_arquivo_csv}': {e}")

    return sucesso_formatado and sucesso_csv


def visualizar_arquivo_txt(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo_entrada:
            print(f"\n--- Conteúdo do Arquivo: {nome_arquivo} ---")
            for linha in arquivo_entrada:
                print(linha, end='')
            print("\n--- Fim do Conteúdo do Arquivo ---")
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
    except UnicodeDecodeError:
        print(f"Erro de decodificação ao ler '{nome_arquivo}'.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao ler o arquivo '{nome_arquivo}': {e}")


def registro():
    nome_arquivo_csv_principal = "dados_animais.txt"
    nome_arquivo_formatado_principal = "dados_animais_formatado.txt"
    ano_atual = datetime.datetime.now().year

    matriz_dados = carregar_dados_do_csv(nome_arquivo_csv_principal)
    numero_animais_existentes = len(matriz_dados)
    print(f"Atualmente existem {numero_animais_existentes} animais registrados.")

    try:
        quantidade_novos_str = input("Quantos NOVOS Animais você deseja registrar? (ou '0' para nenhum): ").strip()
        quantidade_novos = 0 if not quantidade_novos_str else int(quantidade_novos_str)

        if quantidade_novos < 0:
            print("A quantidade não pode ser negativa.")
            return
        if quantidade_novos == 0 and numero_animais_existentes == 0:
            print("Nenhum novo animal para registrar e nenhum animal existente.")
            salvar_dados_completos(matriz_dados, nome_arquivo_csv_principal, nome_arquivo_formatado_principal)
            return
        elif quantidade_novos == 0 and numero_animais_existentes > 0:
            print("Nenhum novo animal para registrar. Os dados existentes serão re-salvos.")
    except ValueError:
        print("Quantidade inválida. Por favor, digite um número.")
        return

    print("\n--- Registrando Novos Animais ---")
    novos_animais_adicionados_nesta_sessao = 0
    for i in range(quantidade_novos):
        print(f"\nRegistrando Animal Nº {numero_animais_existentes + novos_animais_adicionados_nesta_sessao + 1}:")
        try:
            brinco_str = input("Numeração do brinco: ")
            if not brinco_str: raise ValueError("Brinco não pode ser vazio.")
            brinco = int(brinco_str)

            brinco_existe = any(len(animal) > 0 and animal[0] == brinco for animal in matriz_dados)
            if brinco_existe:
                print(f"Erro: Animal com brinco {brinco} já existe. Tente um número diferente.")
                continue

            peso_str = input("Peso (kg): ")
            if not peso_str: raise ValueError("Peso não pode ser vazio.")
            peso = float(peso_str)
            if peso <= 0: raise ValueError("Peso deve ser um valor positivo.")

            mes_compra_str = input("Mês da compra (MM): ")
            if not mes_compra_str: raise ValueError("Mês da compra não pode ser vazio.")
            mes_compra = int(mes_compra_str)
            if not (1 <= mes_compra <= 12): raise ValueError("Mês da compra inválido (1-12).")

            ano_compra_str = input(f"Ano da compra (AAAA, ex: {ano_atual}): ")
            if not ano_compra_str: raise ValueError("Ano da compra não pode ser vazio.")
            ano_compra = int(ano_compra_str)
            if not (1900 <= ano_compra <= ano_atual + 1):
                raise ValueError(f"Ano da compra inválido (deve ser entre 1900 e {ano_atual + 1}).")

            valor_arroba_str = input("Valor da Arroba na compra (R$): ")
            if not valor_arroba_str: raise ValueError("Valor da arroba não pode ser vazio.")
            valor_arroba = float(valor_arroba_str)
            if valor_arroba <= 0: raise ValueError("Valor da arroba deve ser positivo.")

            vacinas_inicial = ""

        except ValueError as ve:
            print(f"Entrada inválida: {ve}. Por favor, use números e formatos corretos.")
            continue

        dados_animal_atual = [brinco, peso, mes_compra, ano_compra, valor_arroba, vacinas_inicial]
        matriz_dados.append(dados_animal_atual)
        novos_animais_adicionados_nesta_sessao += 1

    if quantidade_novos > 0 and novos_animais_adicionados_nesta_sessao == 0:
        print("Nenhum novo animal foi efetivamente adicionado nesta sessão devido a erros ou duplicidade.")
    elif novos_animais_adicionados_nesta_sessao > 0:
        print(f"{novos_animais_adicionados_nesta_sessao} novo(s) animal(is) pronto(s) para serem salvos.")

    print("\n--- Matriz Completa de Dados dos Animais (Antigos + Novos em memória) ---")
    if not matriz_dados:
        print("Nenhum animal registrado na memória.")
    else:
        cabecalho_registro = f"{'Índice':<7} | {'Brinco':<10} | {'Peso (kg)':<10} | {'Peso (@)':<10} | {'Mês':<5} | {'Ano':<7} | {'Vlr Arroba R$':<15} | {'Vacinas':<30}"
        print(cabecalho_registro)
        separador_registro_largura = 115
        separador_registro = "-" * separador_registro_largura
        print(separador_registro)
        for indice, animal_info in enumerate(matriz_dados):
            peso_kg_reg = animal_info[1]
            peso_arroba_reg = peso_kg_reg / 30.0
            vacinas_reg = animal_info[5] if len(animal_info) == CAMPOS_ANIMAL_NOVO else ""
            print(
                f"{indice:<7} | {animal_info[0]:<10} | {peso_kg_reg:<10.2f} | {peso_arroba_reg:<10.2f} | {animal_info[2]:<5} | {animal_info[3]:<7} | {animal_info[4]:<15.2f} | {vacinas_reg:<30}")
        print(separador_registro)

        peso_total_do_rebanho_atual = calcular_peso_total_rebanho(matriz_dados)
        print(f"O peso total de todos os animais registrados é: {peso_total_do_rebanho_atual:.2f} kg")
        valor_total_estimado_atual = calcular_valor_total_rebanho(matriz_dados)
        print(f"O valor total estimado do rebanho é: R$ {valor_total_estimado_atual:.2f}")

    print("\nSalvando todos os dados...")
    if salvar_dados_completos(matriz_dados, nome_arquivo_csv_principal, nome_arquivo_formatado_principal):
        if novos_animais_adicionados_nesta_sessao > 0:
            print("Novos animais registrados e todos os dados salvos com sucesso!")
        elif (quantidade_novos == 0 and numero_animais_existentes > 0) or \
                (
                        quantidade_novos > 0 and novos_animais_adicionados_nesta_sessao == 0 and numero_animais_existentes > 0):
            print("Dados existentes re-salvos com sucesso (nenhum novo animal efetivamente adicionado ou solicitado).")
        elif not matriz_dados:
            print("O rebanho está vazio. Arquivos atualizados (vazios ou com apenas cabeçalho).")
    else:
        print("ERRO: Houve um problema ao salvar os dados.")


def deletar_animal():
    nome_arquivo_csv_principal = "dados_animais.txt"
    nome_arquivo_formatado_principal = "dados_animais_formatado.txt"

    matriz_dados = carregar_dados_do_csv(nome_arquivo_csv_principal)

    if not matriz_dados:
        print("Não há animais registrados para deletar.")
        return

    print("\n--- Deletar Animal do Rebanho ---")
    print("Animais registrados atualmente:")
    cabecalho_delecao = f"{'Índice':<7} | {'Brinco':<10} | {'Peso (kg)':<10} | {'Peso (@)':<10} | {'Mês':<5} | {'Ano':<7} | {'Vlr Arroba R$':<15} | {'Vacinas':<30}"
    print(cabecalho_delecao)
    separador_delecao_largura = 115
    separador_delecao = "-" * separador_delecao_largura
    print(separador_delecao)
    for i, animal in enumerate(matriz_dados):
        peso_kg_del = animal[1]
        peso_arroba_del = peso_kg_del / 30.0
        vacinas_del = animal[5] if len(animal) == CAMPOS_ANIMAL_NOVO else ""
        print(
            f"{i:<7} | {animal[0]:<10} | {peso_kg_del:<10.2f} | {peso_arroba_del:<10.2f} | {animal[2]:<5} | {animal[3]:<7} | {animal[4]:<15.2f} | {vacinas_del:<30}")
    print(separador_delecao)

    try:
        brinco_para_deletar_str = input(
            "Digite o número do brinco do animal a ser deletado (ou 'c' para cancelar): ").strip()
        if brinco_para_deletar_str.lower() == 'c':
            print("Deleção cancelada.")
            return
        brinco_para_deletar = int(brinco_para_deletar_str)
    except ValueError:
        print("Número do brinco inválido. Deve ser um número.")
        return

    animal_encontrado_dados = None
    indice_do_animal_na_lista = -1

    for indice, animal_info_loop in enumerate(matriz_dados):
        if len(animal_info_loop) > 0 and animal_info_loop[0] == brinco_para_deletar:
            animal_encontrado_dados = animal_info_loop
            indice_do_animal_na_lista = indice
            break

    if animal_encontrado_dados:
        print("\n--- Animal Encontrado ---")
        peso_kg_found = animal_encontrado_dados[1]
        peso_arroba_found = peso_kg_found / 30.0
        vacinas_found = animal_encontrado_dados[5] if len(animal_encontrado_dados) == CAMPOS_ANIMAL_NOVO else ""
        print(f"  Brinco: {animal_encontrado_dados[0]}")
        print(f"  Peso (kg): {peso_kg_found:.2f}")
        print(f"  Peso (@): {peso_arroba_found:.2f}")
        print(f"  Data Compra: {animal_encontrado_dados[2]:02d}/{animal_encontrado_dados[3]}")
        print(f"  Valor Arroba: R$ {animal_encontrado_dados[4]:.2f}")
        print(f"  Vacinas: {vacinas_found}")
        valor_individual_estimado = calcular_valor_animal(animal_encontrado_dados)
        print(f"  Valor Estimado do Animal: R$ {valor_individual_estimado:.2f}")

        confirmacao = input("Tem certeza que deseja deletar este animal? (s/n): ").strip().lower()

        if confirmacao == 's':
            matriz_dados.pop(indice_do_animal_na_lista)
            print("Animal deletado da lista em memória.")
            print("Salvando alterações nos arquivos...")
            if salvar_dados_completos(matriz_dados, nome_arquivo_csv_principal, nome_arquivo_formatado_principal):
                print("Alterações salvas com sucesso!")
                if not matriz_dados:
                    print("Todos os animais foram deletados. O rebanho está vazio.")
            else:
                print("ERRO: Houve um problema ao salvar as alterações nos arquivos.")
        else:
            print("Deleção cancelada pelo usuário.")
    else:
        print(f"Nenhum animal encontrado com o brinco número {brinco_para_deletar}.")


def alterar_informacoes_animal():
    nome_arquivo_csv_principal = "dados_animais.txt"
    nome_arquivo_formatado_principal = "dados_animais_formatado.txt"
    ano_atual = datetime.datetime.now().year

    matriz_dados = carregar_dados_do_csv(nome_arquivo_csv_principal)

    if not matriz_dados:
        print("Não há animais registrados para alterar.")
        return

    try:
        brinco_alvo_str = input(
            "Digite o número do brinco do animal que deseja alterar (ou 'c' para cancelar): ").strip()
        if brinco_alvo_str.lower() == 'c':
            print("Alteração cancelada.")
            return
        brinco_alvo = int(brinco_alvo_str)
    except ValueError:
        print("Número do brinco inválido. Deve ser um número.")
        return

    animal_original_dados = None
    animal_encontrado_copia = None
    indice_animal_alvo = -1
    for indice, animal_info_loop in enumerate(matriz_dados):
        if len(animal_info_loop) > 0 and animal_info_loop[0] == brinco_alvo:
            animal_original_dados = animal_info_loop
            animal_encontrado_copia = list(animal_info_loop)
            if len(animal_encontrado_copia) == CAMPOS_ANIMAL_ANTIGO:
                animal_encontrado_copia.append("")
            indice_animal_alvo = indice
            break

    if not animal_encontrado_copia:
        print(f"Nenhum animal encontrado com o brinco número {brinco_alvo}.")
        return

    def exibir_dados_animal_para_alteracao(animal_dados_copia):
        print("\n--- Dados Atuais do Animal (para alteração) ---")
        peso_kg_alt = animal_dados_copia[1]
        peso_arroba_alt = peso_kg_alt / 30.0
        vacinas_alt = animal_dados_copia[5]
        print(f"  1. Brinco: {animal_dados_copia[0]}")
        print(f"  2. Peso (kg): {peso_kg_alt:.2f}")
        print(f"     Peso (@): {peso_arroba_alt:.2f}")
        print(f"  3. Mês Compra: {animal_dados_copia[2]}")
        print(f"  4. Ano Compra: {animal_dados_copia[3]}")
        print(f"  5. Valor Arroba Compra: R$ {animal_dados_copia[4]:.2f}")
        print(f"  6. Vacinas: {vacinas_alt}")
        valor_estimado_ind = calcular_valor_animal(animal_dados_copia)
        print(f"  Valor Estimado Atual do Animal: R$ {valor_estimado_ind:.2f}")
        print("---------------------------------------")

    exibir_dados_animal_para_alteracao(animal_encontrado_copia)
    houve_alteracao_em_memoria = False

    while True:
        try:
            campo_para_alterar = input(
                "Qual informação deseja alterar (1-6)? Digite 's' para salvar e sair, 'c' para cancelar e sair: ").strip().lower()

            if campo_para_alterar == 'c':
                print("Alterações descartadas para este animal.")
                return
            if campo_para_alterar == 's':
                if houve_alteracao_em_memoria:
                    print("Salvando alterações...")
                    matriz_dados[indice_animal_alvo] = animal_encontrado_copia
                    if salvar_dados_completos(matriz_dados, nome_arquivo_csv_principal,
                                              nome_arquivo_formatado_principal):
                        print("Alterações salvas com sucesso nos arquivos!")
                    else:
                        print("ERRO: Houve um problema ao salvar as alterações nos arquivos.")
                else:
                    print("Nenhuma alteração foi feita neste animal.")
                return

            if not campo_para_alterar.isdigit() or not (
                    1 <= int(campo_para_alterar) <= CAMPOS_ANIMAL_NOVO):
                print(f"Opção inválida. Por favor, escolha um número de 1 a {CAMPOS_ANIMAL_NOVO}, 's' ou 'c'.")
                continue

            campo_idx_map = int(campo_para_alterar)

            if campo_idx_map == 1:
                novo_brinco_str = input(f"Novo número do Brinco (atual: {animal_encontrado_copia[0]}): ").strip()
                if not novo_brinco_str: raise ValueError("Brinco não pode ser vazio.")
                novo_brinco = int(novo_brinco_str)
                if novo_brinco != animal_encontrado_copia[0]:
                    brinco_duplicado = any(
                        idx != indice_animal_alvo and len(outro_animal) > 0 and outro_animal[0] == novo_brinco
                        for idx, outro_animal in enumerate(matriz_dados)
                    )
                    if brinco_duplicado:
                        raise ValueError(f"O brinco {novo_brinco} já está registrado em outro animal.")
                animal_encontrado_copia[0] = novo_brinco
                print(f"Brinco atualizado para {novo_brinco} (em memória).")
                houve_alteracao_em_memoria = True

            elif campo_idx_map == 2:
                novo_peso_str = input(f"Novo Peso (kg) (atual: {animal_encontrado_copia[1]:.2f}): ").strip()
                if not novo_peso_str: raise ValueError("Peso não pode ser vazio.")
                novo_peso = float(novo_peso_str)
                if novo_peso <= 0: raise ValueError("Peso deve ser positivo.")
                animal_encontrado_copia[1] = novo_peso
                print(f"Peso atualizado para {novo_peso:.2f} kg (em memória).")
                houve_alteracao_em_memoria = True

            elif campo_idx_map == 3:
                novo_mes_str = input(f"Novo Mês da Compra (MM) (atual: {animal_encontrado_copia[2]}): ").strip()
                if not novo_mes_str: raise ValueError("Mês não pode ser vazio.")
                novo_mes = int(novo_mes_str)
                if not (1 <= novo_mes <= 12): raise ValueError("Mês inválido (1-12).")
                animal_encontrado_copia[2] = novo_mes
                print(f"Mês da compra atualizado para {novo_mes:02d} (em memória).")
                houve_alteracao_em_memoria = True

            elif campo_idx_map == 4:
                novo_ano_str = input(f"Novo Ano da Compra (AAAA) (atual: {animal_encontrado_copia[3]}): ").strip()
                if not novo_ano_str: raise ValueError("Ano não pode ser vazio.")
                novo_ano = int(novo_ano_str)
                if not (1900 <= novo_ano <= ano_atual + 1):
                    raise ValueError(f"Ano inválido (deve ser entre 1900 e {ano_atual + 1}).")
                animal_encontrado_copia[3] = novo_ano
                print(f"Ano da compra atualizado para {novo_ano} (em memória).")
                houve_alteracao_em_memoria = True

            elif campo_idx_map == 5:
                novo_valor_arroba_str = input(
                    f"Novo Valor da Arroba (R$) (atual: {animal_encontrado_copia[4]:.2f}): ").strip()
                if not novo_valor_arroba_str: raise ValueError("Valor da arroba não pode ser vazio.")
                novo_valor_arroba = float(novo_valor_arroba_str)
                if novo_valor_arroba <= 0: raise ValueError("Valor da arroba deve ser positivo.")
                animal_encontrado_copia[4] = novo_valor_arroba
                print(f"Valor da arroba atualizado para R$ {novo_valor_arroba:.2f} (em memória).")
                houve_alteracao_em_memoria = True

            elif campo_idx_map == 6:
                print(f"Vacinas atuais: {animal_encontrado_copia[5]}")
                novas_vacinas_str = input(f"Digite o texto completo para o campo Vacinas: ").strip()
                animal_encontrado_copia[5] = novas_vacinas_str
                print(f"Vacinas atualizadas para '{novas_vacinas_str}' (em memória).")
                houve_alteracao_em_memoria = True

            exibir_dados_animal_para_alteracao(animal_encontrado_copia)

        except ValueError as ve:
            print(f"Erro na entrada: {ve}. Tente novamente.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")


def achar_animal():
    nome_arquivo_csv_principal = "dados_animais.txt"
    matriz_dados = carregar_dados_do_csv(nome_arquivo_csv_principal)

    if not matriz_dados:
        print("Não há animais registrados para buscar.")
        return

    print("\n--- Achar Animal no Rebanho ---")
    try:
        brinco_para_achar_str = input(
            "Digite o número do brinco do animal a ser buscado (ou 'c' para cancelar): ").strip()
        if brinco_para_achar_str.lower() == 'c':
            print("Busca cancelada.")
            return
        brinco_para_achar = int(brinco_para_achar_str)
    except ValueError:
        print("Número do brinco inválido. Deve ser um número.")
        return

    animal_encontrado_dados = None
    for animal_info_loop in matriz_dados:
        if len(animal_info_loop) >= 1 and animal_info_loop[0] == brinco_para_achar:
            animal_encontrado_dados = animal_info_loop
            break

    if animal_encontrado_dados:
        print("\n--- Animal Encontrado ---")
        peso_kg_achado = animal_encontrado_dados[1]
        peso_arroba_achado = peso_kg_achado / 30.0
        vacinas_achado = animal_encontrado_dados[5] if len(animal_encontrado_dados) == CAMPOS_ANIMAL_NOVO else ""
        print(f"  Brinco: {animal_encontrado_dados[0]}")
        print(f"  Peso (kg): {peso_kg_achado:.2f}")
        print(f"  Peso (@): {peso_arroba_achado:.2f}")
        print(f"  Data Compra: {animal_encontrado_dados[2]:02d}/{animal_encontrado_dados[3]}")
        print(f"  Valor Arroba na Compra: R$ {animal_encontrado_dados[4]:.2f}")
        print(f"  Vacinas: {vacinas_achado}")
        valor_individual_estimado = calcular_valor_animal(animal_encontrado_dados)
        print(f"  Valor Estimado do Animal: R$ {valor_individual_estimado:.2f}")
    else:
        print(f"Nenhum animal encontrado com o brinco número {brinco_para_achar}.")


def adicionar_dados_vacinacao():
    nome_arquivo_csv_principal = "dados_animais.txt"
    nome_arquivo_formatado_principal = "dados_animais_formatado.txt"
    matriz_dados = carregar_dados_do_csv(nome_arquivo_csv_principal)

    if not matriz_dados:
        print("Não há animais registrados para adicionar dados de vacinação.")
        return

    print("\n--- Adicionar Dados de Vacinação ---")
    brincos_str = input(
        "Digite os números dos brincos dos animais a vacinar, separados por vírgula (ex: 101,102,105): ").strip()
    if not brincos_str:
        print("Nenhum brinco fornecido.")
        return

    try:
        brincos_para_vacinar = [int(b.strip()) for b in brincos_str.split(',')]
    except ValueError:
        print("Formato de brincos inválido. Use números separados por vírgula.")
        return

    nome_vacina = input("Nome da vacina aplicada: ").strip()
    if not nome_vacina:
        print("Nome da vacina não pode ser vazio.")
        return

    data_vacina_str = input("Data da vacinação (DD/MM/AAAA): ").strip()
    try:
        datetime.datetime.strptime(data_vacina_str, "%d/%m/%Y")
    except ValueError:
        print("Formato de data inválido. Use DD/MM/AAAA.")
        return

    nova_entrada_vacina = f"{nome_vacina} {data_vacina_str}"
    animais_atualizados_count = 0
    animais_nao_encontrados = []

    for brinco_alvo in brincos_para_vacinar:
        animal_encontrado = False
        for i, animal_info in enumerate(matriz_dados):

            if len(animal_info) == CAMPOS_ANIMAL_ANTIGO:
                matriz_dados[i].append("")

            if animal_info[0] == brinco_alvo:
                vacinas_atuais = matriz_dados[i][5]
                if vacinas_atuais:
                    matriz_dados[i][5] = f"{vacinas_atuais}; {nova_entrada_vacina}"
                else:
                    matriz_dados[i][5] = nova_entrada_vacina
                animais_atualizados_count += 1
                animal_encontrado = True
                print(f"Vacina '{nova_entrada_vacina}' adicionada ao animal com brinco {brinco_alvo}.")
                break
        if not animal_encontrado:
            animais_nao_encontrados.append(brinco_alvo)

    if animais_nao_encontrados:
        print(f"Aviso: Os seguintes brincos não foram encontrados: {', '.join(map(str, animais_nao_encontrados))}")

    if animais_atualizados_count > 0:
        print(f"\n{animais_atualizados_count} animal(is) tiveram dados de vacinação atualizados em memória.")
        confirm_salvar = input("Deseja salvar estas alterações nos arquivos? (s/n): ").strip().lower()
        if confirm_salvar == 's':
            if salvar_dados_completos(matriz_dados, nome_arquivo_csv_principal, nome_arquivo_formatado_principal):
                print("Dados de vacinação salvos com sucesso!")
            else:
                print("ERRO: Houve um problema ao salvar os dados de vacinação.")
        else:
            print("Alterações nos dados de vacinação não foram salvas.")
    elif not animais_nao_encontrados:
        print("Nenhum animal foi atualizado (verifique os brincos digitados).")


def menu():
    while True:
        print("\n##########################################")
        print("###     Sistema de Gerenciamento     ###")
        print("###       da Fazenda São José        ###")
        print("##########################################")
        print("\nEscolha uma opção:")
        print("1- Registrar Gado")
        print("2- Deletar Animal do Rebanho")
        print("3- Conferir Informações do Rebanho (arquivo formatado)")
        print("4- Alterar Informações de um Animal")
        print("5- Encontrar um Animal")
        print("6- Adicionar Dados de Vacinação")
        print("7- Sair")

        try:
            opcao_str = input("Opção: ").strip()
            if not opcao_str:
                print("Nenhuma opção digitada. Tente novamente.")
                continue
            opcao = int(opcao_str)
        except ValueError:
            print("Opção inválida. Por favor, digite um número.")
            continue

        if opcao == 1:
            registro()
        elif opcao == 2:
            deletar_animal()
        elif opcao == 3:
            visualizar_arquivo_txt("dados_animais_formatado.txt")
        elif opcao == 4:
            alterar_informacoes_animal()
        elif opcao == 5:
            achar_animal()
        elif opcao == 6:
            adicionar_dados_vacinacao()
        elif opcao == 7:
            print("Saindo do sistema...")
            break
        else:
            print("Opção não encontrada. Tente novamente.")

        print("Você deseja voltar ao menu? (s/n)")
        voltar = input("")
        if voltar.lower() != 's':
            print("Saindo do sistema...")
            break


def main():
    menu()


if __name__ == "__main__":
    main()