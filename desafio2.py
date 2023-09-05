import csv
import matplotlib.pyplot as plt

# Criando função para armazenar o arquivo em uma lista
dados_lista = []

with open("Anexo_Arquivo_Dados_Projeto_Logica_e_programacao_de_computadores.csv", 'r') as csv_file:
    csv_cabecalho = csv_file.readline()  # Lê a primeira linha (cabeçalho)
    for row in csv_file:  # Itera e inclui as linhas dentro da lista criada
        dados_lista.append(row)

# Função para validar dados de entrada e criar input do usuário
def val_dados(dados, min_value=None, max_value=None):
    while True:
        try:
            entrada = int(input(dados))
            if (min_value is None or entrada >= min_value) and (max_value is None or entrada <= max_value):
                return entrada
            else:
                print(f"Digite um valor entre {min_value} e {max_value}.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")

# Seleção da categoria
while True:
    print("*** Selecione as Categorias ***")
    print("1) Todos os dados")
    print("2) Precipitação")
    print("3) Temperatura")
    print("4) Umidade e Vento")
    categoria = val_dados("Opção: ", 1, 4)
    if categoria in [1, 2, 3, 4]:
        break
    else:
        print("Opção inválida. Escolha novamente.")

# Período de pesquisa
print("*** Escolha o Período da Pesquisa *** ")

mes_inicial = val_dados("Informe o mês inicial: ", 1, 12)
ano_inicial = val_dados("Informe o ano inicial: ", 1961, 2016)
mes_final = val_dados("Informe o mês final: ", 1, 12)
ano_final = val_dados("Informe o ano final: ", 1961, 2016)

# Função para retornar dados da categoria selecionada no período especificado
def input_categoria(mes_inicial, ano_inicial, mes_final, ano_final, categoria):
    lista_categoria = []

    for row in dados_lista:
        valores = row.split(',')
        parte_dados = valores[0].split('/')
        mes = int(parte_dados[1])
        ano = int(parte_dados[2])

        if ano_inicial <= ano <= ano_final and mes_inicial <= mes <= mes_final:
            if categoria == 1:
                lista_categoria.append(row)
            elif categoria == 2 and valores[1]:
                lista_categoria.append(row)
            elif categoria == 3 and (valores[2] or valores[3]):
                lista_categoria.append(row)
            elif categoria == 4 and (valores[6] or valores[7]):
                lista_categoria.append(row)
    return lista_categoria

# Retorna os dados da categoria selecionada no período
dados_filtrados = input_categoria(mes_inicial, ano_inicial, mes_final, ano_final, categoria)

# Exibe os dados da categoria selecionada
for linha in dados_filtrados:
    valores = linha.split(',')
    print("Data:", valores[0], 'Precipitação:', valores[1], 'Temp Max:', valores[2], 'Temp Min:', valores[3],
          'Horas Insolaradas:', valores[4], 'Tem Med:', valores[5], 'Umidade:', valores[6], 'Velocidade Vento:',
          valores[7])

# Função para calcular o mês menos chuvoso e a menor precipitação
def get_mes_menos_chuvoso():
    dados_chuva = {}

    for row in dados_lista:
        valores = row.split(',')
        parte_dados = valores[0].split('/')
        mes = int(parte_dados[1])
        ano = int(parte_dados[2])
        chuva = float(valores[1]) if valores[1] else 0

        if (mes, ano) not in dados_chuva:
            dados_chuva[(mes, ano)] = chuva
        else:
            dados_chuva[(mes, ano)] += chuva

    mes_menos_chuvoso = min(dados_chuva, key=dados_chuva.get)
    return mes_menos_chuvoso, dados_chuva[mes_menos_chuvoso]

# Calcula o mês menos chuvoso
mes_menos_chuvoso, chuva_menos_chuvoso = get_mes_menos_chuvoso()
print(f"Mês menos chuvoso: {mes_menos_chuvoso[0]}/{mes_menos_chuvoso[1]} - Menor Precipitação: {chuva_menos_chuvoso} mm")

# Função para calcular a média da temperatura mínima para todo o período de 2006 a 2016
def calcular_media_temp_min_periodo():
    soma_temp = 0
    contador = 0

    for row in dados_lista:
        valores = row.split(',')
        parte_dados = valores[0].split('/')
        ano = int(parte_dados[2])

        if 2006 <= ano <= 2016:
            if valores[3]:
                soma_temp += float(valores[3])
                contador += 1

    if contador > 0:
        media_temp = soma_temp / contador
        return media_temp
    else:
        return None

# Calcula a média geral da temperatura mínima para o período especificado
media_temp_geral = calcular_media_temp_min_periodo()

if media_temp_geral is not None:
    print(f"Média geral da temperatura mínima para todo o período de 2006 a 2016: {media_temp_geral:.2f} °C")
else:
    print("Não há dados disponíveis para calcular a média geral da temperatura mínima.")

# Função para calcular a média da temperatura mínima para um mês e ano específico / usado no gráfico
def calcular_media_temp_min_mes_ano(mes, ano):
    soma_temp = 0
    contador = 0

    for row in dados_lista:
        valores = row.split(',')
        parte_dados = valores[0].split('/')
        mes_dados = int(parte_dados[1])
        ano_dados = int(parte_dados[2])

        if mes_dados == mes and ano_dados == ano:
            if valores[3]:
                soma_temp += float(valores[3])
                contador += 1

    if contador > 0:
        media_temp = soma_temp / contador
        return media_temp
    else:
        return None

# Função para calcular a média da temperatura mínima para um mês específico(input) em todos os anos de 2006 a 2016
def calcular_media_temp_min_mes(mes):
    soma_temp = 0
    contador = 0

    for ano in range(2006, 2017):
        media_temp_mes_ano = calcular_media_temp_min_mes_ano(mes, ano)
        if media_temp_mes_ano is not None:
            soma_temp += media_temp_mes_ano
            contador += 1

    if contador > 0:
        media_temp_mes = soma_temp / contador
        return media_temp_mes
    else:
        return None

# Solicita o mês ao usuário
mes_selecionado = val_dados("Digite o mês (1 a 12) para calcular a média da temperatura mínima:", 1, 12)

# Chama a função para calcular a média da temperatura mínima para o mês escolhido
media_temp_mes = calcular_media_temp_min_mes(mes_selecionado)

# Validação dos dados da temperatura
if media_temp_mes is not None:
    print(f"Média da temperatura mínima para o mês {mes_selecionado} (2006 a 2016): {media_temp_mes:.2f} °C")
else:
    print(f"Não há dados disponíveis para calcular a média da temperatura mínima para o mês {mes_selecionado} (2006 a 2016).")

# Função para gerar gráfico de barras
def gerar_grafico_barras(rotulos, valores, rotulo_x, rotulo_y, titulo):
    plt.bar(rotulos, valores)
    plt.xlabel(rotulo_x)
    plt.ylabel(rotulo_y)
    plt.title(titulo)
    plt.xticks(rotation=45)
    plt.ylim(0, 30)  # Define os limites do eixo y de 0 a 30°C
    plt.tight_layout()
    plt.show()

# Anos de 2006 a 2016
anos = [ano for ano in range(2006, 2017)]  # Usamos 2017 para incluir o ano final

# Calcular as médias das temperaturas mínimas para cada ano
medias_temperatura = [calcular_media_temp_min_mes_ano(mes_selecionado, ano) for ano in anos]

# Gerar o gráfico
gerar_grafico_barras(anos, medias_temperatura, "Ano", "Temperatura Média", "Médias de Temperatura Mínima")
