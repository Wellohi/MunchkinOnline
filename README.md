# MunchkinOnline

🃏 Virtual Tabletop - Jogo de Cartas Multiplayer
Um simulador de mesa virtual leve e em tempo real, desenvolvido com Python (Flask + WebSockets) e JavaScript (Konva.js). Criado especificamente para hospedar partidas de cartas customizadas (como Munchkin) para até 4 jogadores, com sincronização instantânea de movimento, rotação, embaralhamento e sistema de "mão privada".

📁 Estrutura de Pastas Necessária
Antes de iniciar, certifique-se de que suas imagens (.png ou .jpg) estão organizadas exatamente nesta estrutura dentro da pasta do projeto:
```
MunchkinOnline/
│
├── static/
│   ├── cartas_porta/
│   ├── cartas_tesouro/
│   └── verso_cartas/
│
├── templates/
│   └── index.html
│
└── app.py
```

⚙️ 1. Configuração do Ambiente Local
Para rodar o servidor na sua máquina, você precisará do Python instalado.

Abra o terminal na pasta raiz do projeto.

Instale as bibliotecas necessárias executando o comando:

(Nota: O pacote eventlet é crucial para garantir a baixa latência dos WebSockets).

Inicie o servidor do jogo:

O jogo estará rodando localmente. Você pode testar abrindo http://localhost:5000 no seu navegador.

🌐 2. Configurando o Ngrok (Multiplayer)
Para jogar com seus amigos sem precisar hospedar o jogo em um servidor web pago, utilizamos o Ngrok para criar um túnel seguro até a sua máquina.

Crie uma conta gratuita em  e baixe o executável.

Autentique o Ngrok no seu computador (você só faz isso uma vez) usando o token fornecido no painel do site:

Com o app.py rodando em um terminal, abra um segundo terminal na pasta onde o Ngrok foi baixado e inicie o túnel.

⚠️ IMPORTANTE (Redução de Lag): Utilize a flag --region sa para forçar o uso dos servidores na América do Sul. Isso reduz drasticamente a latência da partida.

    ngrok http 5000 --region sa

Copie o link gerado (ex: https://abcd-123.sa.ngrok.io) e envie para os outros jogadores.

🎮 3. Controles e Atalhos da Mesa
A mesa foi projetada para ser ágil e fluida. Coloque o cursor do mouse sobre uma carta ou pilha e utilize os comandos abaixo:

Movimentação
Arrastar (Clique Esquerdo): Move apenas a carta do topo.

Arrastar Pilha (Shift + Clique Esquerdo): Agarra e move todas as cartas que estiverem empilhadas naquela posição.

Ações na Carta (Atalhos de Teclado)
Visualizar / Zoom (Segurar Z): Exibe a carta em tamanho gigante no centro da tela para facilitar a leitura. (Se a carta estiver virada para baixo, o zoom mostrará apenas o verso).

Virar Carta / Flip (F): Vira a carta revelando sua frente ou escondendo-a (verso).

Embaralhar / Shuffle (S): Mistura aleatoriamente todas as cartas da pilha sob o cursor.

Rotacionar (Clique Direito): Tomba a carta em -90 graus horizontalmente (útil para indicar itens usados ou virados).

Zona Privada (A "Mão" do Jogador)
A parte inferior escura da tela é a sua Mão.

Ao arrastar uma carta para esta área, ela desaparece instantaneamente da tela dos outros jogadores.

Dentro da sua mão, o movimento é livre (o snap-to-grid é desativado) para que você organize suas cartas como preferir.

Ao arrastar a carta de volta para a parte superior (a Mesa), ela reaparece publicamente para todos e volta a se alinhar à grade magnética.

Dica para o Host: O estado do jogo é mantido na memória do servidor Flask. Evitem atualizar a página (F5) no meio da partida, pois isso fará com que o navegador recarregue a mesa no estado inicial.


Link das cartas: https://drive.google.com/file/d/1x1u1SOy-G_7S68Wt1_S72870tAQ-KFXv/view?usp=sharing



### Métodos alternativos de conexão:

Túnel SSH Nativo

Você vai utilizar o serviço gratuito localhost.run, que foi construído especificamente para receber túneis SSH sem exigir cadastros.

Mantenha o Jogo Rodando: Deixe o seu primeiro terminal rodando o servidor Python (python app.py) na porta 5000.

Abra um Novo Terminal: Abra uma nova janela do PowerShell (exatamente como você fez para tentar o comando anterior).

Execute o Comando de Encaminhamento: Cole o comando abaixo e aperte Enter:

    ```
    ssh -R 80:localhost:5000 nokey@localhost.run
    ```

Se o terminal perguntar algo como "Are you sure you want to continue connecting (yes/no/[fingerprint])?", basta digitar yes e dar Enter.

Ele vai processar por alguns segundos e devolver uma URL limpa e segura (geralmente terminada em .lhr.life).

Copie esse link e abra no navegador. O túnel SSH costuma ter uma rota muito mais limpa e direta que o Ngrok, ajudando a derrubar a latência. 

### O "Port Forwarding" Nativo do VS Code (Recomendado)

Se você está escrevendo seus scripts Python usando o Visual Studio Code, a Microsoft embutiu recentemente uma rede global de tunelamento diretamente no editor (os Dev Tunnels). É absurdamente rápido, usa a rede global da Azure (que tem datacenters no Brasil, reduzindo sua latência a quase zero), e não exige nenhum privilégio de administrador, pois roda dentro do próprio VS Code.

Como utilizar:

Com o seu projeto aberto no VS Code, deixe o seu servidor Python rodando no terminal (python app.py).

Olhe para a parte inferior do VS Code (onde fica o Terminal, Console de Depuração, etc.). Você verá uma aba chamada "Portas" (Ports). Clique nela.

Clique no botão "Encaminhar uma Porta" (Forward a Port) e digite 5000. Dê Enter.

O VS Code pedirá para você fazer login com sua conta GitHub ou Microsoft (é rápido e gratuito).

Assim que logar, ele vai gerar um link. A mágica aqui: clique com o botão direito na coluna "Visibilidade" (Visibility), que estará como Private, e mude para Public.

### Túnel SSH sobre HTTPS (Pinggy.io)

A porta 443 é a porta universal do tráfego HTTPS (navegação web segura). Nenhum firewall ou sistema operacional bloqueia a porta 443, caso contrário, você não conseguiria abrir nenhum site na internet. O serviço Pinggy.io permite receber túneis por essa porta, furando qualquer bloqueio de rede sem precisar de instalação.

Como utilizar:

Mantenha o seu servidor python app.py rodando no primeiro terminal.

Abra o segundo terminal (PowerShell ou CMD).

Cole este comando exato e dê Enter:

Bash
ssh -p 443 -R0:localhost:5000 a.pinggy.io
Ele vai se conectar e exibir um painel visual muito bacana direto no seu terminal de texto.

Procure pela URL pública (algo como https://rnxyz-123-45.a.free.pinggy.link). Copie e compartilhe.

(Nota: Quando seus amigos acessarem o link do Pinggy pela primeira vez, pode aparecer uma tela de aviso deles dizendo que é um túnel gratuito, basta clicar no botão para prosseguir para o site).
