MONITOR-262 - GUIA DE INSTALAÇÃO (V2)
Este sistema pode ser instalado de duas formas. Tente sempre a Opção A primeiro por ser mais rápida e leve.

ESTRUTURA:
api/ : Lógica em Python (Editável)

interface/ : Painel visual (Editável)

nginx/ : Configuração de rede

compose/ : Comando de inicialização (docker-compose.yaml)

🟢 OPÇÃO A: INSTALAÇÃO PADRÃO (Via Internet)
Use esta opção se você baixou apenas o código-fonte e tem conexão com a rede.

No terminal, dentro da pasta do projeto, execute:
docker compose up -d --build

🟡 OPÇÃO B: CONTINGÊNCIA (Offline / Sem Internet)
Use esta opção se a Opção A falhar ou se o servidor não tiver acesso à internet.

Certifique-se de que o arquivo monitor-offline-v2.tar está na raiz.

Carregue o motor do sistema:
docker load -i monitor-offline-v2.tar

Inicie o sistema:
docker compose up -d

🛠️ MANUTENÇÃO E AJUSTES (MODO VOLUMES):
O sistema utiliza Volumes, o que permite alterar o comportamento sem precisar reiniciar tudo:

Visual: Altere 'index.html' em interface/ e dê F5 no navegador.

Lógica: Altere e salve 'main.py' em api/. O sistema recarrega sozinho.

Rede: Se alterar o nginx.conf, rode:
docker compose restart nginx-service