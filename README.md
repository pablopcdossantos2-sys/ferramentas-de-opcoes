# Ferramentas de Opções — Web Portfólio

Repositório de desenvolvimento e pesquisa sobre ferramentas de opções. O objetivo principal é desenvolver o **EWZ GEX → WIN**; o web-portfólio e o banco de dados de outras ferramentas existem como suporte de pesquisa e comparação.

## Prioridades do projeto

1. **Objetivo principal — EWZ GEX → WIN:** desenvolver a ferramenta inspirada na metodologia discutida no início da conversa, em que níveis de Gamma Exposure do EWZ são usados como referência e projetados para o WIN.
2. **Objetivo secundário — biblioteca de referências:** reunir, preservar e analisar outras ferramentas baseadas em opções, OI, GEX, Walls, Vanna, DEX, sigmas e conceitos relacionados, com a finalidade de compreender diferentes abordagens e identificar melhorias futuras para o projeto principal.

As ferramentas do catálogo **não possuem a mesma prioridade de desenvolvimento**. Salvo indicação posterior, alterações de produto devem favorecer primeiro o EWZ GEX → WIN.

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
│       ├── index.html
│       ├── tutorial.html
│       └── source/ ou desktop/
└── .github/
    └── workflows/
        ├── pages.yml
        └── build-ewz-gex-win-desktop.yml
```

## Banco de dados de ferramentas

A pasta `ferramentas/` funciona como acervo do projeto. Códigos recebidos na conversa são preservados em subpastas próprias, junto com fichas de análise. Cada ferramenta agora possui também uma página HTML individual navegável com seções padronizadas de Objetivo, Input, Cálculos, Visualização, Automação, Limitações, Código-fonte e Comparação. O arquivo `ferramentas/catalogo.json` mantém um índice legível por máquina.

A regra adotada daqui em diante é: **toda nova ferramenta de opções analisada deve ser catalogada no repositório e incluída no web-portfólio.**

## Páginas individuais

Cada ferramenta possui uma ficha HTML navegável em `ferramentas/<id>/index.html`, com estrutura fixa:

- Objetivo
- Input
- Cálculos
- Visualização
- Automação
- Limitações
- Código-fonte
- Comparação

Os cards da página inicial apontam para essas fichas. Cada ficha também oferece o tutorial web de instalação da ferramenta e retorno à matriz comparativa geral.

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


## Glossário didático da matriz

A Matriz funcional possui ícones de informação nos principais conceitos de opções. Ao clicar, o site abre uma explicação em linguagem didática com quatro blocos: definição simples, leitura prática, exemplo e cuidado de interpretação. O objetivo é permitir que leitores sem familiaridade prévia com opções compreendam a comparação antes de avaliar cada ferramenta.


## Tutoriais de instalação

Cada ferramenta catalogada possui uma página `tutorial.html` dentro de sua própria pasta. Os tutoriais usam o mesmo visual do web-portfólio e são escritos para usuários com pouca familiaridade com terminal, GitHub ou Pine Script.

Quando a instalação completa não pode ser reproduzida com os arquivos atualmente preservados, o tutorial declara isso explicitamente em vez de inventar dependências ou comandos. Essa regra é especialmente importante para ferramentas que dependem de geradores externos de dados ou de componentes ainda não arquivados.

A partir de agora, toda nova ferramenta adicionada ao banco deve possuir também um tutorial de instalação em HTML integrado ao web-portfólio.


## Referências visuais

Quando uma ferramenta analisada vier acompanhada de uma imagem, captura de tela ou exemplo visual relevante, esse material também deve fazer parte do acervo sempre que puder ser preservado adequadamente.

As imagens ficam em `assets/tool-screenshots/`, devem registrar a origem e são exibidas tanto no portfólio quanto na ficha individual da ferramenta. A imagem serve para explicar a interface e o uso da solução; não deve ser apresentada como prova de desempenho.

Atualmente há referências visuais catalogadas para:

- quantedOptions Levels [qO];
- Options Levels;
- Support and Resistance levels from Options Data.


## Aplicação desktop do projeto principal

A aplicação complementar do **EWZ GEX → WIN** está em desenvolvimento em `ferramentas/ewz-gex-win/desktop/`.

A versão alpha já possui:

- GUI em Tkinter;
- coleta do Barchart por sessão real do Microsoft Edge via Playwright;
- captura de dados de opções/gamma/OI;
- agregação local de GEX por strike;
- tentativa de extração de Call Wall, Put Wall e Gamma Flip publicados;
- identificação explícita de níveis locais de baixa confiança;
- exportação do bloco `EWZGEX1`;
- importação desse bloco pelo Pine;
- testes unitários e workflow de build portátil para Windows.

O workflow `.github/workflows/build-ewz-gex-win-desktop.yml` gera um ZIP portátil como artifact do GitHub Actions. A aplicação permanece **alpha** até a coleta e os níveis serem validados em uso real.


### Estado metodológico do EWZ GEX → WIN

A versão desktop atual é **0.2.0-alpha.1**. Após revisar a transcrição da palestra, o projeto passou a separar explicitamente:

- EWZ atual/pré-mercado para contextualização dos strikes;
- fechamento regular EWZ D-1 como referência percentual;
- WIN no mesmo instante como âncora da projeção 1:1.

A GUI também possui uma janela **Perfil GEX por strike** para auditar Call GEX, Put GEX, Net GEX e OI antes de aceitar os níveis. O próximo gargalo de validação não é mais a fórmula EWZ → WIN, mas a seleção automática dos níveis que devem representar a metodologia original.
