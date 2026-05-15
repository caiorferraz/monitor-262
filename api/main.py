import asyncio
import re
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from contextlib import asynccontextmanager

# Mantive a variável global, mas agora a rota lerá o arquivo para garantir o tempo real
ATIVOS = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # O startup agora serve apenas para log ou inicializações fixas
    print("API Iniciada")
    yield
    ATIVOS.clear()

app = FastAPI(lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# --- CONFIGURAÇÕES FIXAS --- 
# Cancela se não responder em 900ms (tempo alto o suficiente 
# para evitar falsos negativos, mas baixo o bastante
# para dar folga ao ciclo de 1 segundo)
TIMEOUT = "0.9" 
COUNT = "1"

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

    # LEITURA EM TEMPO REAL: Movida para dentro da rota
    # para garantir que cada chamada leia o estado atual do arquivo
    ativos_locais = {}
    try:
        with open("ips.txt", "r") as f:
            for linha in f:     
                linha = linha.strip()
                # Ignora linhas vazias ou comentadas com #
                if not linha or linha.startswith("#"):
                    continue           
                if ":" in linha:
                    nome, ip = linha.strip().split(":", 1)
                    ativos_locais[nome.strip().upper()] = ip.strip()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo ips.txt não encontrado.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao ler ips.txt: {e}")

    # Dispara todos os pings em paralelo
    tarefas = [pingar(nome, ip) for nome, ip in ativos_locais.items()]
    resultados = await asyncio.gather(*tarefas)
    
    dados_finais = {nome: info for nome, info in resultados}

    # Calcula quanto tempo o processamento levou (ex: 0.1s ou 0.8s)
    tempo_gasto = time.time() - inicio_ciclo
    
    # O SEGREDO: Calcula quanto falta para completar 1 segundo
    tempo_de_espera = max(0, 1.0 - tempo_gasto)

    # Segura a resposta até completar o 1 segundo cravado
    await asyncio.sleep(tempo_de_espera)

    return dados_finais