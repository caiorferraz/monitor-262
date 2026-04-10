===============================================================================
                          MONITOR-262 - Versão 2.0
===============================================================================

1. SOBRE O PROJETO
------------------
O Monitor-262 é uma ferramenta leve desenvolvida para monitorar a latência 
da sua rede local ou de serviços externos em tempo real. Ele foi desenhado
para ser portátil e indestrutível, rodando totalmente via Docker.

2. ESTRUTURA DE PASTAS
----------------------
/
|-- api/           -> Lógica em Python e arquivo de alvos (ips.txt)
|-- interface/     -> Painel visual (HTML/JS)
|-- nginx/         -> Configurações do servidor de rede
|-- docker-compose.yml -> Comando de inicialização do sistema
`-- README.txt     -> Este manual de instruções

3. COMO INSTALAR
----------------
Existem duas formas de colocar o sistema para rodar:

OPÇÃO A: Instalação Padrão (Via Internet)
Use esta opção se você tem conexão com a rede para baixar as imagens base.
No terminal, dentro da pasta do projeto, execute:
   
   docker compose up -d --build

OPÇÃO B: Contingência (Offline / Sem Internet)
Use esta se a Opção A falhar ou se o servidor estiver isolado. 
Certifique-se de que o arquivo 'monitor-offline-v2.tar' está na pasta.
1. Carregue o motor do sistema:
   docker load -i monitor-offline-v2.tar
2. Inicie o sistema:
   docker compose up -d

4. CONFIGURAÇÃO DE ALVOS (IPS.TXT)
----------------------------------
Você define quem o Monitor-262 deve vigiar:
1. Acesse a pasta 'api/' e abra o arquivo 'ips.txt'.
2. Adicione ou altere os IPs conforme sua necessidade.
3. Não precisa reiniciar: O sistema lê o arquivo em tempo real. 
   Assim que você salvar, os novos alvos aparecerão no painel (F5).

5. MANUTENÇÃO E AJUSTES (MODO LIVE)
-----------------------------------
O sistema utiliza Volumes, permitindo alterações sem "parar a máquina":
- Visual: Altere 'index.html' em 'interface/' e dê F5 no navegador.
- Lógica: Altere 'main.py' em 'api/'. O sistema recarrega sozinho.
- Rede: Se alterar o 'nginx.conf', rode: docker compose restart nginx-service

6. ACESSO
----------
Após iniciar, abra o seu navegador e acesse: http://localhost

-------------------------------------------------------------------------------
Desenvolvido por: Caio Ferraz
-------------------------------------------------------------------------------