from flask import Flask, jsonify, request, render_template
import requests
from datetime import datetime, timedelta
import sqlite3
from scipy.stats import ttest_ind
import holidays

app = Flask(__name__)

def get_cotacao_api(data):
    formatted_date = data.strftime('%m-%d-%Y')
    link = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{formatted_date}'&$top=100&$format=json"
    requisicao = requests.get(link)
    info = requisicao.json()

    if not info['value']:
        return None

    cotacao = (info['value'][0]['cotacaoCompra'] + info['value'][0]['cotacaoVenda']) / 2
    return cotacao

def get_cotacao_bd(data, cursor):
    query = f"SELECT Cotacao, Variacao FROM 'cotacoes' WHERE Data = '{data}'"
    cursor.execute(query)
    resultado = cursor.fetchone()
    if resultado:
        cotacao, variacao = resultado
        return cotacao, variacao
    else:
        return None, None

def insert_into_db(data, cotacao, variacao, conn):
    with conn:
        conn.execute(f"INSERT INTO 'cotacoes' (Data, Cotacao, Variacao) VALUES (?, ?, ?)", (data, cotacao, variacao))

# Carrega os feriados brasileiros
br_holidays = holidays.Brazil()

def verificar_dia_util(data_str):
    formato_interno = "%Y-%m-%d"
    try:
        # Converte a string para um objeto datetime
        data = datetime.strptime(data_str, formato_interno)
    except ValueError:
        # Retorna False ou levanta um erro se a data for inválida
        return False

    # Verifica se é um dia da semana e se não é feriado
    return data.weekday() < 5 and data not in br_holidays


def find_last_business_day(data):
    if data.weekday() == 0:  # Se for segunda-feira, comece com a sexta-feira anterior
        data -= timedelta(days=3)
    else:  # Caso contrário, apenas volte um dia
        data -= timedelta(days=1)

    # Volte até encontrar um dia útil
    while data.weekday() >= 5 or data in br_holidays:
        data -= timedelta(days=1)
    return data

def get_all_variations(cursor):
    query = "SELECT Variacao FROM 'cotacoes' WHERE Variacao IS NOT NULL"
    cursor.execute(query)
    result = cursor.fetchall()
    return [float(var[0].replace(',', '.')) if isinstance(var[0], str) else float(var[0]) for var in result if var[0]]


def calculate_p_value(variacao_atual, variations):
    # Calcula e retorna o p-valor da variação atual em relação às variações anteriores.
    if len(variations) < 500:
        return None  # Retorna None quando não há dados suficientes

    # Teste t para duas amostras independentes
    _, p_value = ttest_ind(variations, [variacao_atual])
    return p_value


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cotacao', methods=['GET'])
def get_cotacao():
    data_input = request.args.get('data', default=None, type=str)
    if not data_input:
        return jsonify({'error': 'Data não fornecida'}), 400
    
    try:
        formato_usuario = "%d/%m/%Y"
        formato_interno = "%Y-%m-%d"
        # Converte a data de entrada para o formato interno
        data_formatada = datetime.strptime(data_input, formato_usuario).strftime(formato_interno)
    except ValueError:
        return jsonify({'error': 'Formato de data inválido. Use DD/MM/AAAA.'}), 400

    if not verificar_dia_util(data_formatada):
        return jsonify({'error': 'Não há cotação disponível para finais de semana ou feriados.'}), 400

    with sqlite3.connect('cotacoes_dolar.db') as conn:
        cursor = conn.cursor()
        # Busca pela cotação usando o formato interno
        cotacao_atual, variacao_atual = get_cotacao_bd(data_formatada, cursor)
        cotacao_anterior = None

        if not cotacao_atual:
            cotacao_atual = get_cotacao_api(datetime.strptime(data_formatada, formato_interno))
            if cotacao_atual is None:
                return jsonify({'error': 'Não foi possível obter a cotação para a data fornecida.'}), 404
            # Inserção usa o formato interno
            insert_into_db(data_formatada, cotacao_atual, None, conn)

        # A busca pela última data útil deve usar o formato interno
        last_business_day = find_last_business_day(datetime.strptime(data_formatada, formato_interno))
        last_business_day_str = last_business_day.strftime(formato_interno)
        cotacao_anterior, _ = get_cotacao_bd(last_business_day_str, cursor)

        if not cotacao_anterior:
            # A API deve receber a data no formato que ela espera
            cotacao_anterior = get_cotacao_api(last_business_day)
            if cotacao_anterior:
                # Inserção usa o formato interno
                insert_into_db(last_business_day_str, cotacao_anterior, None, conn)

        # A resposta deve usar o formato que o usuário espera
        response = {
            'data': data_input,
            'cotacao': cotacao_atual
        }

    if cotacao_atual:
        if variacao_atual is None and cotacao_anterior:
            variacao_atual = ((cotacao_atual - cotacao_anterior) / cotacao_anterior) * 100
            cursor.execute(f"UPDATE 'cotacoes' SET Variacao = ? WHERE Data = ?", (variacao_atual, data_formatada))
            conn.commit()
        
        response['variacao'] = variacao_atual

        variations = get_all_variations(cursor)
        p_value = calculate_p_value(variacao_atual, variations)

        response['p_valor'] = p_value if p_value is not None else 'Dados insuficientes para análise estatística.'

        return render_template('cotacao.html', response = response)
    
    else:
        return render_template('erro.html', message='Não foi possível obter as cotações para as datas informadas.')

if __name__ == '__main__':
    app.run(debug=True)
