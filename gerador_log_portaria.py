import random
import datetime

# Tipos de eventos e dados simulados
moradores = [
    {"id": 1023, "nome": "João Pereira"},
    {"id": 1045, "nome": "Larissa Tavares"},
    {"id": 1011, "nome": "Fernanda Lopes"},
    {"id": 1050, "nome": "Diego Ramos"},
    {"id": 1087, "nome": "Carla Martins"}
]

visitantes = [
    "Carlos Silva", "Ana Costa", "Marcelo Lima", "Rafael Mota", "Paulo Henrique"
]

prestadores = [
    {"nome": "José Almeida", "empresa": "HidroLimp"},
    {"nome": "Mariana Souza", "empresa": "FixTudo"}
]

entregadores = [
    {"nome": "Lucas G.", "empresa": "iFood"},
    {"nome": "Roberto M.", "empresa": "Correios"}
]

# Funções para gerar entradas de log
def gerar_timestamp():
    return datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def gerar_evento():
    evento = random.choice([
        "ACCESS_GRANTED", "ACCESS_DENIED", "DELIVERY", "SYSTEM", "ALERT"
    ])

    if evento == "ACCESS_GRANTED":
        tipo = random.choice(["morador", "visitante", "prestador"])
        if tipo == "morador":
            m = random.choice(moradores)
            return f"{gerar_timestamp()} ACCESS_GRANTED | Morador ID: {m['id']} | Nome: {m['nome']} | Entrada pelo portão principal"
        elif tipo == "visitante":
            v = random.choice(visitantes)
            apto = random.randint(101, 1205)
            return f"{gerar_timestamp()} ACCESS_GRANTED | Visitante: {v} | Apto: {apto} | Autorizado por morador via app"
        else:
            p = random.choice(prestadores)
            return f"{gerar_timestamp()} ACCESS_GRANTED | Prestador de serviço: {p['nome']} | Empresa: {p['empresa']} | Acesso liberado 10h às 12h"

    elif evento == "ACCESS_DENIED":
        v = random.choice(visitantes)
        motivo = random.choice([
            "Não autorizado pelo morador",
            "Tentativa de acesso com QR Code expirado",
            "Tentativa de acesso fora do horário permitido"
        ])
        return f"{gerar_timestamp()} ACCESS_DENIED  | Visitante: {v} | Motivo: {motivo}"

    elif evento == "DELIVERY":
        e = random.choice(entregadores)
        destino = random.choice(["locker 05", f"apartamento {random.randint(101, 1205)}"])
        return f"{gerar_timestamp()} DELIVERY       | {e['empresa']} - Entregador: {e['nome']} | Encomenda entregue no {destino}"

    elif evento == "SYSTEM":
        acao = random.choice([
            "Portaria reiniciada - Versão 3.4.7",
            "Backup automático concluído com sucesso",
            f"Reconhecimento facial atualizado para Morador ID: {random.choice(moradores)['id']}"
        ])
        return f"{gerar_timestamp()} SYSTEM         | {acao}"

    elif evento == "ALERT":
        alerta = random.choice([
            "Porta da garagem permaneceu aberta por 3 minutos",
            "Tentativa de acesso múltiplo em menos de 30 segundos",
            "Falha na leitura do QR Code no portão social"
        ])
        return f"{gerar_timestamp()} ALERT          | {alerta}"

# Gerar o log com N entradas
def gerar_log(qtd_linhas=50, arquivo="log_portaria_virtual.log"):
    with open(arquivo, "w", encoding="utf-8") as f:
        for _ in range(qtd_linhas):
            f.write(gerar_evento() + "\n")
    print(f"Arquivo de log '{arquivo}' gerado com sucesso!")

# Executar o gerador
if __name__ == "__main__":
    gerar_log()
