import pandas as pd  # Importa a biblioteca pandas para manipulação de dados em formato de DataFrame.
from sklearn.ensemble import IsolationForest  # Importa o modelo Isolation Forest para detecção de anomalias.
import matplotlib.pyplot as plt  # Importa a biblioteca matplotlib para criação de gráficos.
import seaborn as sns  # Importa a biblioteca seaborn para visualizações de dados mais avançadas.
import sqlite3  # Importa a biblioteca sqlite3 para interação com bancos de dados SQLite.
import re  # Importa a biblioteca re para trabalhar com expressões regulares.
from logs.logger import log_evento # importa o arquivo de log a ser analisado

# Constantes para configurações
# log_evento = 'log_portaria_virtual.log'  # Define o nome do arquivo de log a ser analisado.
BANCO_DE_DADOS = 'acessos.db'  # Define o nome do arquivo do banco de dados SQLite.
CONTAMINACAO_ISOLATION_FOREST = 0.05  # Define a taxa de contaminação para o modelo Isolation Forest (proporção de anomalias esperadas).

def carregar_dados(log_evento):
    """Carrega dados de um arquivo CSV e retorna um DataFrame do pandas."""
    try:
        df = pd.read_csv(log_evento)  # Tenta ler o arquivo CSV para um DataFrame.
        return df  # Retorna o DataFrame se a leitura for bem-sucedida.
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{log_evento}' não encontrado.")  # Lança uma exceção se o arquivo não for encontrado.
    except pd.errors.EmptyDataError:
        raise ValueError(f"Arquivo '{log_evento}' está vazio.")  # Lança uma exceção se o arquivo estiver vazio.
    except pd.errors.ParserError:
        raise ValueError(f"Erro ao analisar o arquivo '{log_evento}'. Verifique o formato.")  # Lança uma exceção se houver um erro ao analisar o arquivo.

def limpar_e_preparar_dados(df):
    """Limpa e prepara os dados para análise."""
    df.columns = df.columns.str.strip()  # Remove espaços extras dos nomes das colunas.
    df['Data e Hora'] = pd.to_datetime(df['Data e Hora'])  # Converte a coluna 'Data e Hora' para o tipo datetime.
    df['Hora'] = df['Data e Hora'].dt.hour  # Extrai a hora da coluna 'Data e Hora' e cria uma nova coluna 'Hora'.
    df['Minuto'] = df['Data e Hora'].dt.minute  # Extrai o minuto da coluna 'Data e Hora' e cria uma nova coluna 'Minuto'.
    df['Tipo de Usuário'] = df['Observações'].apply(extrair_tipo_usuario)  # Aplica a função para extrair o tipo de usuário das observações.
    df = df[pd.to_numeric(df['Tempo de Resposta (segundos)'], errors='coerce').notna()]  # Garante que a coluna 'Tempo de Resposta (segundos)' contenha apenas valores numéricos válidos.
    df['Tempo de Resposta (segundos)'] = df['Tempo de Resposta (segundos)'].astype(int)  # Converte a coluna 'Tempo de Resposta (segundos)' para inteiro.
    return df  # Retorna o DataFrame limpo e preparado.

def extrair_tipo_usuario(observacao):
    """Extrai o tipo de usuário usando regex."""
    if isinstance(observacao, str):  # Verifica se a observação é uma string.
        match = re.match(r'(\w+)', observacao)  # Procura a primeira palavra na observação usando regex.
        if match:
            return match.group(1)  # Retorna a primeira palavra encontrada.
    return 'Desconhecido'  # Retorna 'Desconhecido' se não for possível extrair o tipo de usuário.

def detectar_anomalias(df, contaminacao=CONTAMINACAO_ISOLATION_FOREST):
    """Detecta anomalias no tempo de resposta usando Isolation Forest."""
    modelo_if = IsolationForest(contamination=contaminacao)  # Cria um modelo Isolation Forest com a taxa de contaminação especificada.
    df['Anomalia'] = modelo_if.fit_predict(df[['Tempo de Resposta (segundos)']])  # Treina o modelo e detecta anomalias na coluna 'Tempo de Resposta (segundos)'.
    return df  # Retorna o DataFrame com a coluna 'Anomalia' adicionada.

def classificar_acessos(df):
    """Classifica os acessos com base em anomalias e outros critérios."""
    def classificar_acesso(row):  # Define uma função interna para classificar cada acesso.
        if row['Anomalia'] == -1:  # Se o acesso for uma anomalia (anomalia = -1).
            return 'Suspeito'  # Classifica como 'Suspeito'.
        elif row['Status'] == 'Negado' or 'Alarme' in row['Tipo de Evento']:  # Se o acesso for negado ou envolver um alarme.
            return 'Crítico'  # Classifica como 'Crítico'.
        else:
            return 'Normal'  # Classifica como 'Normal' para todos os outros casos.
    df['Classificação'] = df.apply(classificar_acesso, axis=1)  # Aplica a função de classificação a cada linha do DataFrame.
    return df  # Retorna o DataFrame com a coluna 'Classificação' adicionada.

def alertar_acessos_criticos(df):
    """Alerta para acessos críticos."""
    acessos_criticos = df[df['Classificação'] == 'Crítico']  # Filtra os acessos críticos.
    if not acessos_criticos.empty:  # Verifica se há acessos críticos.
        print("\nALERTA: Acessos Críticos Detectados!")
        for index, row in acessos_criticos.iterrows():  # Itera sobre os acessos críticos e imprime os detalhes.
            print(f"- Data/Hora: {row['Data e Hora']}")
            print(f"- Tipo de Evento: {row['Tipo de Evento']}")
            print(f"- Usuário/Veículo: {row['Usuário/Veículo']}")
            print(f"- Observações: {row['Observações']}\n")

def visualizar_distribuicao_acessos(df):
    """Visualiza a distribuição de acessos por hora e retorna a figura."""
    plt.figure(figsize=(10, 6))  # Cria uma nova figura com tamanho específico.
    ax = sns.countplot(x='Hora', data=df)  # Cria um gráfico de contagem de acessos por hora.
    plt.title('Distribuição de Acessos por Hora do Dia')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Número de Acessos')
    for p in ax.patches:  # Adiciona a contagem de acessos em cada barra.
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=10, color='black', weight='bold')
    return plt.gcf()  # Retorna a figura atual.

def visualizar_anomalias(df):
    """Visualiza anomalias no tempo de resposta e retorna a figura."""
    plt.figure(figsize=(10, 6))  # Cria uma nova figura com tamanho específico.
    sns.scatterplot(x='Data e Hora', y='Tempo de Resposta (segundos)', hue='Anomalia', data=df)  # Cria um gráfico de dispersão para visualizar anomalias.
    plt.title('Anomalias no Tempo de Resposta')
    plt.xlabel('Data e Hora')
    plt.ylabel('Tempo de Resposta (segundos)')
    return plt.gcf()  # Retorna a figura atual.

def visualizar_tipos_eventos(df):
    """Visualiza a contagem de tipos de eventos e retorna a figura."""
    plt.figure(figsize=(12, 6))  # Cria uma nova figura com tamanho específico.
    ax = sns.countplot(x='Tipo de Evento', data=df)  # Cria um gráfico de contagem de tipos de eventos.
    plt.title('Contagem de Tipos de Eventos')
    plt.xlabel('Tipo de Evento')
    plt.ylabel('Contagem')
    plt.xticks(rotation=45, ha='right')  # Rotaciona os rótulos do eixo x para melhor visualização.
    for p in ax.patches:  # Adiciona a contagem de cada tipo de evento em cada barra.
        ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='bottom', fontsize=10, color='black', weight='bold')
    plt.tight_layout()  # Ajusta o layout da figura para evitar sobreposição.
    return plt.gcf()  # Retorna a figura atual.

def armazenar_dados_sqlite(df, database_file=BANCO_DE_DADOS):
    """Armazena os dados em um banco de dados SQLite."""
    try:
        conn = sqlite3.connect(database_file)  # Conecta ao banco de dados SQLite.
        df.to_sql('acessos', conn, if_exists='replace', index=False)  # Salva o DataFrame na tabela 'acessos', substituindo a tabela existente se houver uma.
        conn.close()  # Fecha a conexão com o banco de dados.
        print(f"\nDados armazenados com sucesso em '{database_file}'.")
    except sqlite3.Error as e:
        print(f"Erro ao armazenar dados em SQLite: {e}")  # Imprime uma mensagem de erro se houver um problema ao armazenar os dados.

def analisar_logs_acesso(caminho_arquivo=ARQUIVO_LOG):
    """Função principal para analisar logs de acesso."""
    try:
        df = carregar_dados(log_evento)  # Carrega os dados do arquivo de log.
        df = limpar_e_preparar_dados(df)  # Limpa e prepara os dados.
        df = detectar_anomalias(df)  # Detecta anomalias nos dados.
        df = classificar_acessos(df)  # Classifica os acessos.
        alertar_acessos_criticos(df)  # Alerta sobre acessos críticos.
        figuras = [  # Cria uma lista com as figuras das visualizações.
            visualizar_distribuicao_acessos(df),
            visualizar_anomalias(df),
            visualizar_tipos_eventos(df)
        ]
        plt.show() # Exibe todas as figuras

        armazenar_dados_sqlite(df)  # Armazena os dados no banco de dados SQLite.
    except (FileNotFoundError, ValueError, sqlite3.Error) as e:
        print(f"Ocorreu um erro: {e}")  # Imprime uma mensagem de erro se ocorrer uma exceção.

# Exemplo de uso
analisar_logs_acesso()  # Chama a função principal para analisar os logs de acesso.