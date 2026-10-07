# Tutorial de instalação — Options Levels

Este é um indicador Pine Script simples que recebe uma lista de **13 níveis já calculados**.

## O que você precisa

- Conta no TradingView.
- Arquivo `source/Options_Levels.pine`.
- Os 13 valores que deseja desenhar.

## Passo 1 — instalar o indicador

1. Abra o TradingView e o gráfico desejado.
2. Abra **Pine Editor**.
3. Abra `source/Options_Levels.pine` no repositório.
4. Copie o código inteiro.
5. Cole no Pine Editor.
6. Clique em **Salvar**.
7. Dê um nome ao indicador.
8. Clique em **Adicionar ao gráfico**.

## Passo 2 — preparar os dados

A lista deve seguir exatamente a ordem esperada pelo script:

1. Call Wall
2. Put Wall
3. Gamma Flip
4. Dark Gamma
5. Whale 1
6. Whale 2
7. Whale 3
8. Whale 4
9. Whale 5
10. Upper Sigma 1
11. Upper Sigma 2
12. Lower Sigma 1
13. Lower Sigma 2

Não altere a ordem.

## Passo 3 — colar a lista

1. Abra **Configurações → Inputs**.
2. Localize o campo de níveis.
3. Cole os 13 números no formato esperado pelo script.
4. Confirme.
5. Ative ou desative os grupos visuais desejados.

## Como saber se deu certo

O indicador deve mostrar as linhas correspondentes aos níveis críticos, Whales e sigmas, com seus rótulos. Se os níveis aparecerem em posições absurdas, confira primeiro a ordem e o separador da lista.

## Limitação importante

O script não calcula os 13 níveis. Ele apenas recebe valores produzidos externamente e os desenha.
