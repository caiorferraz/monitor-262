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
