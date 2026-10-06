# Ferramentas de Opções — Web Portfólio

Web portfólio comparativo das ferramentas relacionadas a opções analisadas ao longo do projeto.

## Objetivo

Reunir, em uma única interface, uma visão técnica e comparativa das seguintes soluções:

- **EWZ GEX → WIN** — aplicação portátil com GUI + indicador Pine para coletar/formatar dados de GEX do EWZ e projetá-los no WIN.
- **Mapa de Opções** — aplicação voltada a Open Interest, Notional OI, histórico e matriz strike × vencimento.
- **EWZ — Mapa de Opções em Aberto** — indicador Pine que recebe séries de opções, agrega OI por faixas de strike e calcula valor por prêmio, nocional pelo strike e P/C OI.
- **quantedOptions Levels [qO]** — indicador Pine voltado à visualização de Call/Put Wall, Gamma Flip, Gamma/DEX e perfil de strikes.
- **Options Levels** — indicador Pine simples para 13 níveis pré-calculados, incluindo Walls, Gamma Flip, Whales e sigmas.
- **Support and Resistance levels from Options Data** — indicador Pine com 17 métricas por ticker, incluindo IV, Vanna, Implied Move, Walls e alertas avançados.

## Estrutura

```text
.
├── index.html
├── styles.css
├── app.js
├── ferramentas/
│   ├── README.md
│   ├── catalogo.json
│   └── <uma pasta por ferramenta>/
├── paginas/
│   └── <uma página HTML por ferramenta>/
└── .github/
    └── workflows/
        └── pages.yml
```

## Banco de dados de ferramentas

A pasta `ferramentas/` funciona como acervo do projeto. Códigos recebidos na conversa são preservados em subpastas próprias, junto com fichas de análise. Cada ferramenta agora possui também uma página HTML individual navegável com seções padronizadas de Objetivo, Input, Cálculos, Visualização, Automação, Limitações, Código-fonte e Comparação. O arquivo `ferramentas/catalogo.json` mantém um índice legível por máquina.

A regra adotada daqui em diante é: **toda nova ferramenta de opções analisada deve ser catalogada no repositório e incluída no web-portfólio.**

## Páginas individuais

Cada ferramenta possui uma ficha HTML navegável em `paginas/`, com estrutura fixa:

- Objetivo
- Input
- Cálculos
- Visualização
- Automação
- Limitações
- Código-fonte
- Comparação

Os cards da página inicial apontam diretamente para essas fichas, e cada ficha permite navegar para a anterior, para a próxima e para a matriz comparativa geral.

## Executar localmente

Não há etapa de build. Basta abrir `index.html` no navegador.

Para servir via HTTP localmente, opcionalmente:

```powershell
python -m http.server 8000
```

Depois acesse `http://localhost:8000`.

## GitHub Pages

O workflow em `.github/workflows/pages.yml` publica o site por GitHub Actions.

Se o repositório ainda não estiver configurado para Pages:

1. Abra **Settings → Pages**.
2. Em **Build and deployment**, selecione **GitHub Actions**.
3. Execute novamente o workflow **Deploy GitHub Pages**, se necessário.

## Nota de fonte

No momento em que este portfólio foi criado, o próprio repositório `ferramentas-de-opcoes` estava vazio. Portanto, ele foi utilizado como **destino do portfólio**, não como fonte de uma ferramenta adicional. A ferramenta adicional relacionada a opções incluída na comparação é o projeto **Mapa de Opções**, trabalhado separadamente.

## Critério da comparação

As marcações representam funcionalidades observadas no código ou na documentação analisada. Quando algo depende de um serviço externo não fornecido, isso é indicado explicitamente.

