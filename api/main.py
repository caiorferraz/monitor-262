import asyncio
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

async def pingar(nome, ip):
    # -c 2 = Envia 2 pacotes
    # -W 0.9 = Timeout  
    # -i 1 = Intervalo entre pings
    comando = ["ping", "-c", "2", "-i", "1", "-W", "0.9", ip]   
    processo = await asyncio.create_subprocess_exec(
        *comando,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL
    )
   
    stdout, _ = await processo.communicate()
    saida = stdout.decode()

    status = "ONLINE" if processo.returncode == 0 else "OFFLINE"

    # Extrai tempos: time=XX ms
    tempos = re.findall(r'time=(\d+\.?\d*)', saida)
    tempos = [float(t) for t in tempos]

    if tempos:
        media_raw = sum(tempos) / len(tempos)
        media = round(media_raw, 2) if media_raw < 1 else int(media_raw)
    else:
        media = None

    return nome, {
        "status": status,
        "latencia": media
    }

@app.get("/status")
async def check_network():
    ativos = {
        "ROUTER": "192.168.1.1",
        "ACCESS POINT": "192.168.1.3",
        "PE00QLAK": "192.168.1.10",
        "PE00QLAK_eth": "192.168.1.11",
        "ZENFONE": "192.168.1.12",
        "NOTE-MAE": "192.168.1.13",
        "NOTE-PAULA": "192.168.1.14",
        "NOTE-PAULA_eth": "192.168.1.15",
        "TV-MAE": "192.168.1.16",
        "TV-SALA": "192.168.1.17",
        "CEL-MAE": "192.168.1.18",
        "PLAYSTATION": "192.168.1.19"
    }

    # Dispara os 8 pings em paralelo
    tarefas = [pingar(nome, ip) for nome, ip in ativos.items()]
    resultados = await asyncio.gather(*tarefas)
   
    return {nome: info for nome, info in resultados}