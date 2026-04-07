import asyncio
import re
import time
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# --- CONFIGURAÇÕES FIXAS --- 
COUNT = "1"
TIMEOUT = "0.9" # Se não responder em 900ms, cancela para dar tempo do ciclo
INTERVAL = "0.1"

async def pingar(nome, ip):
    comando = ["ping", "-c", COUNT, "-W", TIMEOUT, ip]
    processo = await asyncio.create_subprocess_exec(
        *comando,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL
    )
    stdout, _ = await processo.communicate()
    saida = stdout.decode()
    
    status = "ONLINE" if processo.returncode == 0 else "OFFLINE"
    tempos = re.findall(r'time=(\d+\.?\d*)', saida)
    
    # Arredondamento
    if tempos:
        val = float(tempos[0])
        latencia = round(val, 2) if val < 1 else int(round(val))
    else:
        latencia = None

    return nome, {"ip": ip, "status": status, "latencia": latencia}

@app.get("/status")
async def check_network():

    inicio_ciclo = time.time()

    ativos = {}
    with open("ips.txt", "r") as f:
        for linha in f:
            if ":" in linha:
                nome, ip = linha.strip().split(":", 1)
                ativos[nome.strip().upper()] = ip.strip()

    # Dispara todos os pings em paralelo
    tarefas = [pingar(nome, ip) for nome, ip in ativos.items()]
    resultados = await asyncio.gather(*tarefas)
    
    dados_finais = {nome: info for nome, info in resultados}

    # Calcula quanto tempo o processamento levou (ex: 0.1s ou 0.8s)
    tempo_gasto = time.time() - inicio_ciclo
    
    # O SEGREDO: Calcula quanto falta para completar 1.0 segundo
    tempo_de_espera = max(0, 1.0 - tempo_gasto)

    # Segura a resposta até completar o 1 segundo cravado
    await asyncio.sleep(tempo_de_espera)

    return dados_finais
