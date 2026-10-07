# Tutorial de instalação — Support and Resistance levels from Options Data

Este é um indicador Pine v6 que recebe uma string externa com métricas de opções para um ou mais tickers.

## O que você precisa

- Conta no TradingView.
- Arquivo `source/Support_and_Resistance_levels_from_Options_Data.pine`.
- Uma string compatível com os campos esperados pelo indicador.

## Passo 1 — instalar o código

1. Abra um gráfico no TradingView.
2. Abra **Pine Editor**.
3. Abra no repositório o arquivo `source/Support_and_Resistance_levels_from_Options_Data.pine`.
4. Copie todo o conteúdo.
5. Cole no Pine Editor.
6. Clique em **Salvar**.
7. Dê um nome ao indicador.
8. Clique em **Adicionar ao gráfico**.

## Passo 2 — entender os dados necessários

O indicador espera, por ticker, um conjunto de valores que inclui itens como:

- S1 e R1;
- Implied Move;
- Put Wall e Call Wall;
- Gamma Flip;
- IV;
- Put/Call Ratio;
- tendência e atividade;
- Walls de curto prazo e anteriores;
- Vanna positiva e negativa;
- stop sugerido.

Esses valores são produzidos fora do Pine.

## Passo 3 — inserir a string

1. Abra **Configurações → Inputs**.
2. Localize o campo de dados.
3. Cole a string completa, preservando os separadores e a ordem.
4. Confirme.
5. Confira se os níveis exibidos pertencem ao ticker do gráfico.

## Passo 4 — configurar alertas

Depois que os dados estiverem corretos:

1. clique em **Criar alerta** no TradingView;
2. selecione este indicador;
3. escolha a condição desejada, como proximidade, rompimento ou outra condição exposta pelo código;
4. configure frequência e notificação.

## Como saber se deu certo

- O Pine compila.
- Os níveis principais aparecem.
- O painel mostra métricas coerentes com o ticker.
- As opções de alerta ficam disponíveis.

## Limitação importante

A instalação do Pine não instala nem reproduz o gerador externo dos 17 campos. Sem uma fonte compatível de dados, o indicador não consegue preencher sozinho as métricas.
