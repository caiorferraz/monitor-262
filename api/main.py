import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Função que executa UM ping de forma assíncrona
async def pingar(nome, ip):
    # -c 4 = Enviar 4 pacotes (padrão que você quer)
    # -i 0.2 = Intervalo de 0.2s entre pings (para ser mais rápido que o padrão de 1s)
    comando = ["ping", "-c", "5", "-i", "0.2", ip]
    
    # Executa o processo sem travar o Python
    processo = await asyncio.create_subprocess_exec(
        *comando,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )
    
    return nome, "ONLINE" if await processo.wait() == 0 else "OFFLINE"

@app.get("/status")
async def check_network():
    ativos = {
            "PE00QLAK": "192.168.1.10",
            "PE00QLAK_eth": "192.168.1.11",
            "ZENFONE": "192.168.1.12",
            "NOTE-MAE": "192.168.1.13",
    	    "NOTE-PAULA": "192.168.1.14",
            "NOTE-PAULA_eth": "192.168.1.15",
            "TV-MAE": "192.168.1.16",
            "TV-SALA": "192.168.1.17"
        }
    
    # A MÁGICA: Dispara todos os pings ao mesmo tempo
    tarefas = [pingar(nome, ip) for nome, ip in ativos.items()]
    resultados = await asyncio.gather(*tarefas)
    
    # Transforma a lista de volta em um dicionário para o JSON
    return {nome: status for nome, status in resultados}
