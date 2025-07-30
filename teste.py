import random
import datetime

# --- Configurações ---
NOME_ARQUIVO_CSV = "dados_animais.txt"
NUM_ANIMAIS = 300
BRINCO_INICIAL = 1
ANO_CORRENTE = 2025 # Usando o ano de referência das últimas interações
DATA_CORRENTE_PARA_VACINA = datetime.date(ANO_CORRENTE, 6, 2) # Data de referência

POSSIVEIS_VACINAS = ["Febre Aftosa", "Brucelose", "Raiva", "Clostridiose", "Botulismo", "Leptospirose", "IBR/BVD"]

def gerar_data_aleatoria_para_vacina(ano_compra, mes_compra):
    """Gera uma data plausível para vacina após ou próxima à data de compra."""
    try:
        data_inicio_vacina = datetime.date(ano_compra, mes_compra, 1)

        data_fim_vacina = DATA_CORRENTE_PARA_VACINA

        if data_inicio_vacina > data_fim_vacina: # Compra no futuro em relação à DATA_CORRENTE_PARA_VACINA
            if ano_compra >= DATA_CORRENTE_PARA_VACINA.year:
                 ano_vac = ano_compra
                 # Se o ano de compra é o ano corrente da vacina, o mês da vacina não pode ser anterior ao mês de compra
                 mes_vac = random.randint(mes_compra if ano_compra == DATA_CORRENTE_PARA_VACINA.year and mes_compra <= DATA_CORRENTE_PARA_VACINA.month else 1, 12)
                 dia_vac = random.randint(1, 28) # Simples para evitar erros de dia/mês
                 return f"{dia_vac:02d}/{mes_vac:02d}/{ano_vac}"
            else: # Fallback improvável com a lógica atual
                 return f"{random.randint(1,28):02d}/{random.randint(1,12):02d}/{ano_compra}"

        delta_dias = (data_fim_vacina - data_inicio_vacina).days
        if delta_dias < 0: # Caso a data de compra seja futura
             dias_aleatorios = 0 # Vacina no mesmo dia/mês da compra (simplificado)
             data_aleatoria = data_inicio_vacina + datetime.timedelta(days=random.randint(0, 60)) # até 2 meses depois
             if data_aleatoria.year > ano_compra + 1: # Limita ao ano seguinte da compra
                 data_aleatoria = datetime.date(ano_compra +1, random.randint(1,12), random.randint(1,28))

        else:
            dias_aleatorios = random.randrange(delta_dias + 1)
            data_aleatoria = data_inicio_vacina + datetime.timedelta(days=dias_aleatorios)

        return data_aleatoria.strftime("%d/%m/%Y")
    except ValueError: # Lida com datas inválidas, ex: ano_compra > ANO_CORRENTE
        # Se compra é no futuro, agenda vacina nesse ano futuro
        ano_vac = ano_compra
        mes_vac = random.randint(1,12)
        dia_vac = random.randint(1,28)
        return f"{dia_vac:02d}/{mes_vac:02d}/{ano_vac}"

# --- Geração dos Dados dos Animais ---
linhas_csv_animais = []

for i in range(NUM_ANIMAIS):
    brinco = BRINCO_INICIAL + i
    peso_kg = random.randint(150, 750) # Peso como inteiro
    mes_compra = random.randint(1, 12)

    # Ano da compra (favorecendo anos recentes)
    if random.random() < 0.7:
        ano_compra = random.randint(ANO_CORRENTE - 3, ANO_CORRENTE + 1) # Permite até o próximo ano
    else:
        ano_compra = random.randint(2015, ANO_CORRENTE - 4)
    ano_compra = max(1900, min(ano_compra, ANO_CORRENTE + 1)) # Garante limites do script original

    valor_arroba = random.randint(36, 64) * 5 # Valor inteiro, múltiplo de 5 (entre 180 e 320)

    # Vacinas
    vacinas_str = ""
    num_vacinas_registro = 0
    if random.random() < 0.65: # 65% de chance de ter ao menos uma vacina
        num_vacinas_registro = random.randint(1, 3) # 1 a 3 registros de vacina

    entradas_vacina = []
    if num_vacinas_registro > 0:
        # Garante vacinas únicas para o mesmo animal nesta geração
        vacinas_escolhidas_animal = random.sample(POSSIVEIS_VACINAS, min(num_vacinas_registro, len(POSSIVEIS_VACINAS)))
        for nome_vacina in vacinas_escolhidas_animal:
            data_vacina = gerar_data_aleatoria_para_vacina(ano_compra, mes_compra)
            entradas_vacina.append(f"{nome_vacina} {data_vacina}")
        vacinas_str = "; ".join(entradas_vacina)

    # Formato da linha CSV: Brinco,Peso(kg),Mês,Ano,ValorArroba,Vacinas
    linha_animal = f"{brinco},{peso_kg},{mes_compra},{ano_compra},{valor_arroba},{vacinas_str}"
    linhas_csv_animais.append(linha_animal)

# --- Escrever no arquivo CSV ---
try:
    with open(NOME_ARQUIVO_CSV, 'w', encoding='utf-8') as f:
        for linha in linhas_csv_animais:
            f.write(linha + "\n")
    print(f"Arquivo '{NOME_ARQUIVO_CSV}' gerado com sucesso com {NUM_ANIMAIS} animais.")
    print("Agora você pode executar o seu script FSJmain.py.")
except IOError:
    print(f"Erro: Não foi possível escrever no arquivo '{NOME_ARQUIVO_CSV}'. Verifique as permissões.")
except Exception as e:
    print(f"Um erro inesperado ocorreu: {e}")