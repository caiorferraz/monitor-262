============================================================
MONITOR-262 - GUIA DE INSTALAÇÃO OFFLINE
============================================================

Este pacote contém tudo o necessário para rodar o sistema
sem dependência de internet.

ESTRUTURA:
- monitor-offline-v1.tar  : Motor do sistema (Imagens Docker)
- compose/                : Comandos de inicialização
- interface/              : Arquivos do painel (HTML)
- nginx/                  : Configurações de rede

------------------------------------------------------------
PASSO A PASSO PARA RODAR (MODO PRODUÇÃO):
------------------------------------------------------------

1. Carregar o "Motor" no Docker:
   docker load -i monitor-offline-v1.tar

2. Iniciar o sistema:
   docker compose -f compose/docker-compose-offline-prod.yaml up -d

3. Acessar no navegador:
   http://localhost

------------------------------------------------------------
MANUTENÇÃO:
- Para atualizar o HTML: basta editar a pasta 'interface'.
- Para ver se está rodando: docker ps
- Para parar tudo: docker compose -f compose/docker-compose-offline-prod.yaml down
============================================================

------------------------------------------------------------
MODO MANUTENÇÃO / DESENVOLVIMENTO (MODO 4):
------------------------------------------------------------

Use este modo apenas se precisar alterar o código Python (API) 
ou as configurações em tempo real.

1. Pare a execução atual (se houver):
   docker compose -f compose/docker-compose-offline-prod.yaml down

2. Inicie em modo desenvolvimento:
   docker compose -f compose/docker-compose-offline-dev.yaml up -d

3. Como funciona:
   - A pasta 'api/' local será espelhada dentro do container.
   - Qualquer alteração no arquivo 'main.py' será refletida 
     automaticamente (hot-reload).
   - Se precisar forçar uma reconstrução da imagem localmente:
     docker compose -f compose/docker-compose-offline-dev.yaml up -d --build

------------------------------------------------------------
DICA DE OURO (VERSIONAMENTO):
------------------------------------------------------------
Se você fizer uma alteração crítica no código dentro da pasta 'api' 
durante a manutenção no cliente, LEMBRE-SE de copiar esses arquivos 
de volta para o seu repositório Git oficial ao retornar à base.
============================================================
