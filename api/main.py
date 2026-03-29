import asyncio
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- CONFIGURAÇÕES DE REDE (O "Cérebro" do Monitoramento) ---
COUNT = "3"          # Quantidade de pacotes por tentativa
TIMEOUT = "0.9"      # Tempo máximo de espera por cada resposta (em segundos)
INTERVAL = "1"     # Pausa entre cada um dos 3 pacotes (em segundos)

# --- CATÁLOGO DE PERFIS (POLÍTICAS DE REDE) ---
PERFIS = {
    "ultra_rapido": {"c": "2", "w": "0.4", "i": "0.1"}, # Foca em velocidade (Total < 1s)
    "padrao_wifi":  {"c": "3", "w": "0.9", "i": "0.3"}, # O seu equilíbrio atual
    "missao_critica": {"c": "5", "w": "1", "i": "0.1"} # 5 pings para garantir que não caia
}
# -----------------------------------------------------------

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

async def pingar(nome, ip):
    # Usamos as variáveis globais para montar o comando
    comando = ["ping", "-c", COUNT, "-i", TIMEOUT, "-W", INTERVAL, ip]
    
    processo = await asyncio.create_subprocess_exec(
        *comando,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL
    )
    
    stdout, _ = await processo.communicate()
    saida = stdout.decode()

    # O Linux retorna 0 se pelo menos 1 pacote voltou (Lógica de Resiliência)
    status = "ONLINE" if processo.returncode == 0 else "OFFLINE"

    tempos = re.findall(r'time=(\d+\.?\d*)', saida)
    tempos = [float(t) for t in tempos]

    if tempos:
        media_raw = sum(tempos) / len(tempos)
        media = round(media_raw, 2) if media_raw < 1 else int(media_raw)
    else:
        media = None

    return nome, {
        "ip": ip,
        "status": status,
        "latencia": media
    }

@app.get("/status")
async def check_network():
    # Sua lista de ativos (crescendo para 16 dispositivos!)
    ativos = {
        "DNS CLOUDFLARE": "1.1.1.1",
        "DNS GOOGLE": "8.8.8.8",
        "MODEM": "187.3.32.117",
        "ROTEADOR": "192.168.1.1",
        "ACCESS POINT": "192.168.1.3",
        "PE00QLAK": "192.168.1.10",        
        "ZENFONE": "192.168.1.12",
        "PE00QLAK_eth": "192.168.1.11",
        "CEL-MAE": "192.168.1.18",
        "TV-MAE": "192.168.1.16",
        "NOTE-MAE": "192.168.1.13",
        "TV-SALA": "192.168.1.17",
        "NOTE-PAULA": "192.168.1.14",
        "CEL-PAULA": "192.168.1.20",
        "NOTE-PAULA_eth": "192.168.1.15",
        "PLAYSTATION": "192.168.1.19"
    }

    # Dispara os pings em paralelo (Escalabilidade)
    tarefas = [pingar(nome, ip) for nome, ip in ativos.items()]
    resultados = await asyncio.gather(*tarefas)
    
    return {nome: info for nome, info in resultados}