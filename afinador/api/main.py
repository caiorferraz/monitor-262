import numpy as np
from scipy.fftpack import fft, fftfreq
from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()

# Configurações de áudio
SAMPLE_RATE = 44100
BUFFER_SIZE = 4096

def get_nota_e_freq(audio_data):
    """Transforma os bytes do microfone em Nota e Frequência"""
    if len(audio_data) == 0:
        return "--", 0.0

    # --- ADIÇÃO: VERIFICAÇÃO RMS (ENERGIA REAL) ---
    # Calcula a média quadrática para ignorar ruídos de fundo
    rms = np.sqrt(np.mean(audio_data**2))
    if rms < 0.01:  # Limiar de silêncio (ajuste conforme o microfone do Zenfone)
        return "--", 0.0
    # ----------------------------------------------
    
    # Cálculo de FFT (Física do Som)
    yf = fft(audio_data)
    xf = fftfreq(len(audio_data), 1 / SAMPLE_RATE)
    
    # Filtro para frequências de violão (70Hz a 1300Hz)
    idx = np.where((xf > 70) & (xf < 1300))
    xf = xf[idx]
    yf = np.abs(yf[idx])
    
    # Critério de pico na magnitude da FFT
    if len(yf) == 0 or np.max(yf) < 0.05: 
        return "--", 0.0

    freq_fundamental = xf[np.argmax(yf)]
    
    # ... (mantenha o código anterior até a linha da freq_fundamental)

    freq_fundamental = xf[np.argmax(yf)]
    
    # --- ALTERAÇÃO: TRAVA DE SEGURANÇA PARA FREQUÊNCIA ---
    # Se a frequência for menor que a nota mais grave do violão (E2 ~82Hz), ignoramos.
    if freq_fundamental < 75: 
        return "--", 0.0
    # ----------------------------------------------------

    # Mapeamento de nota (Base 448Hz para sua micro-afinação)
    notas = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    h = 12 * np.log2(freq_fundamental / 448.0)
    n = int(round(h) + 69)
    nome_nota = notas[n % 12]
    
    return nome_nota, float(freq_fundamental)

@app.websocket("/audio")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("✅ Conexão Ativa: Zenfone/PC pronto para processar áudio.")
    try:
        while True:
            # Recebe o áudio bruto
            data = await websocket.receive_bytes()
            
            # Se o JS enviar um buffer vazio antes de fechar, tratamos aqui
            if not data:
                break
                
            audio_data = np.frombuffer(data, dtype=np.float32)
            
            # Processa a física do som (sua lógica RMS e FFT)
            nota, freq = get_nota_e_freq(audio_data)
            
            # Envia resposta
            await websocket.send_json({
                "nota": nota,
                "frequencia": freq
            })
            
    except Exception as e:
        # Quando você sai da aba do Chrome, o JS fecha o socket e cai aqui
        print(f"ℹ️ Microfone liberado no Cliente (Aba oculta ou fechada). Detalhe: {e}")
    finally:
        # Garante que o recurso no servidor seja resetado
        print("🔌 Aguardando nova ativação do microfone...")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)