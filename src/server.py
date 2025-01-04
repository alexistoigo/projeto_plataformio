import socket
import json
import asyncio
from telegram import Bot


CHAT_ID = ""

NOME_BOT = ""
API_BOT = ""



placas_usadas = []


def get_empresa(localizacao):
    with open("/Users/alexistoigo/Documents/PlatformIO/Projects/projeto/src/empresas.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        for empresa in dados["empresas_refrigeracao"]:
            if empresa["cidade"].lower() == localizacao.lower():
                return empresa
        return None


def get_motorista_infos(placa):
    with open("/Users/alexistoigo/Documents/PlatformIO/Projects/projeto/src/motoristas.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
        for motorista in dados:
            if motorista["placa"].lower() == placa.lower():
                return motorista
        return None


async def process(data):
    placa, temperatura, umidade, localizacao, sensores_camara_fria = data.split()
    empresa = get_empresa(localizacao)
    motorista = get_motorista_infos(placa)
    if placa in placas_usadas:
        return
    msg = build_message(
        temperatura, umidade, localizacao, sensores_camara_fria, empresa, motorista
    )
    placas_usadas.append(placa)
    await send_message(msg)


def build_message(
    temperatura, umidade, localizacao, sensores_camara_fria, empresa, motorista
):
    mensagem = f"🚨Falha no sistema de refrigeração🚨\n\n"
    mensagem += f"Temperatura: {temperatura}°C - Umidade: {umidade}\n"
    mensagem += "Informações do veículo:\n"
    mensagem += f'\tMotorista: {motorista["nome_motorista"]}\n'
    mensagem += f'\tPlaca: {motorista["placa"]}\n'
    mensagem += f'\tNumero Telefone: {motorista["numero_telefone"]}\n'
    mensagem += f"\tLocalização: {localizacao}\n"

    if sensores_camara_fria.count("1") > 0:
        mensagem += "\tSensores da câmara fria com falha:\n"
        if sensores_camara_fria[0] == "1":
            mensagem += "\t\tSensor 1: Compressor\n"
        if sensores_camara_fria[1] == "1":
            mensagem += "\t\tSensor 2: Condensador\n"
        if sensores_camara_fria[2] == "1":
            mensagem += "\t\tSensor 3: Ventiladores\n"
        if sensores_camara_fria[3] == "1":
            mensagem += "\t\tSensor 4: Termostatos e Controladores\n"

    mensagem += "\nInformações da empresa de refrigeração:\n"
    mensagem += f'\tNome: {empresa["nome_empresa"]}\n'
    mensagem += f'\tCidade: {empresa["cidade"]}\n'
    mensagem += f'\tResponsável: {empresa["responsavel"]}\n'
    mensagem += f'\tTelefone:{empresa["telefone"]}\n\n'
    mensagem += f'Para entrar em contato com a empresa via WhatsApp, clique (https://wa.me/{empresa["telefone"]})\n\n'

    return mensagem


async def send_message(message):
    bot = Bot(token=API_BOT)
    await bot.send_message(chat_id=CHAT_ID, text=message)


async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    print(f"Conectado por {addr}")

    while True:
        data = await reader.read(1024)
        if not data:
            break
        data_decoded = data.decode()
        print(f"Recebido: {data_decoded}")
        await process(data_decoded)

    writer.close()
    await writer.wait_closed()


async def start_server(host="192.168.90.108", port=65432):
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f"Servidor escutando em {addr}")

    async with server:
        await server.serve_forever()


asyncio.run(start_server())