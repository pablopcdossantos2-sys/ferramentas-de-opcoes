# Ferramentas de Opções — Web Portfólio

Web portfólio comparativo das ferramentas relacionadas a opções analisadas ao longo do projeto.

## Objetivo

Reunir, em uma única interface, uma visão técnica e comparativa das seguintes soluções:

- **EWZ GEX → WIN** — aplicação portátil com GUI + indicador Pine para coletar/formatar dados de GEX do EWZ e projetá-los no WIN.
- **Mapa de Opções** — aplicação voltada a Open Interest, Notional OI, histórico e matriz strike × vencimento.
- **quantedOptions Levels [qO]** — indicador Pine voltado à visualização de Call/Put Wall, Gamma Flip, Gamma/DEX e perfil de strikes.
- **Options Levels** — indicador Pine simples para 13 níveis pré-calculados, incluindo Walls, Gamma Flip, Whales e sigmas.
- **Support and Resistance levels from Options Data** — indicador Pine com 17 métricas por ticker, incluindo IV, Vanna, Implied Move, Walls e alertas avançados.

## Estrutura

```text
.
├── index.html
├── styles.css
├── app.js
└── .github/
    └── workflows/
        └── pages.yml
```

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

