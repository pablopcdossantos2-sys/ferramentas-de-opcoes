# Tutorial de instalação — quantedOptions Levels [qO]

O arquivo preservado no catálogo é um indicador Pine Script. A ferramenta depende de um **snapshot externo** produzido fora do TradingView.

## O que você precisa

- Conta no TradingView.
- Arquivo `source/quantedOptions_Levels_qO.pine`.
- Um snapshot compatível com o formato esperado pelo indicador para uso real.

## Passo 1 — instalar o Pine

1. Abra um gráfico no TradingView.
2. Abra **Pine Editor**.
3. Abra no repositório o arquivo `source/quantedOptions_Levels_qO.pine`.
4. Copie todo o código.
5. Apague o conteúdo do Pine Editor e cole o código.
6. Clique em **Salvar**.
7. Dê um nome ao indicador.
8. Clique em **Adicionar ao gráfico**.

## Passo 2 — entender a dependência externa

O indicador não coleta a cadeia de opções e não calcula sozinho Call Wall, Put Wall, Gamma Flip, GEX ou DEX.

Ele espera receber um snapshot textual no formato da ferramenta externa, com prefixo/versionamento como `qo1|` e campos contendo níveis e perfil por strike.

Sem esse snapshot, o indicador pode ser instalado, mas não terá os dados necessários para reproduzir a análise completa.

## Passo 3 — inserir o snapshot

1. Abra **Configurações → Inputs** do indicador.
2. Localize o campo destinado ao snapshot.
3. Cole o texto completo produzido pelo gerador compatível.
4. Confirme a alteração.
5. Verifique se o header mostra ticker, data/hora e os níveis esperados.

## Passo 4 — usar em outro ativo/proxy

O código possui lógica de conversão para determinados pares ETF/índice/futuro. Use apenas combinações reconhecidas pelo script e confira o estado de conversão mostrado pelo indicador.

## Como saber se deu certo

- O Pine compila sem erro.
- O indicador reconhece o snapshot.
- Call Wall, Put Wall e Gamma Flip aparecem.
- Top strikes e ladder são desenhados quando presentes no snapshot.
- O header não indica erro de parsing.

## Limitação importante

O repositório preserva o indicador Pine, não o gerador externo original dos snapshots. Portanto, este tutorial ensina a instalar o componente TradingView; a aquisição dos dados depende do ecossistema externo correspondente.
