# Tutorial de instalação — EWZ — Mapa de Opções em Aberto

Este indicador funciona dentro do TradingView e não exige instalação de Python ou outro programa.

## O que você precisa

- Uma conta no TradingView.
- Um gráfico do **EWZ cotado em USD**.
- O arquivo `source/EWZ_Mapa_Opcoes.pine`.
- Para uso real, uma cadeia de opções do EWZ convertida para o formato aceito pelo indicador.

## Passo 1 — abrir o gráfico correto

1. Entre no TradingView.
2. Pesquise por **EWZ**.
3. Abra um gráfico do ETF EWZ cotado em dólares.
4. Deixe algum espaço livre à direita das velas para visualizar as faixas desenhadas pelo indicador.

## Passo 2 — instalar o código Pine

1. Abra **Pine Editor**.
2. Abra o arquivo `source/EWZ_Mapa_Opcoes.pine` no repositório.
3. Copie todo o conteúdo, desde `//@version=6`.
4. Cole no Pine Editor.
5. Clique em **Salvar**.
6. Dê um nome, por exemplo `EWZ — Mapa de Opções em Aberto`.
7. Clique em **Adicionar ao gráfico**.

## Passo 3 — testar com demonstração

1. Abra as configurações do indicador.
2. Ative **Demonstração — dados FICTÍCIOS**.
3. Ajuste a escala do gráfico se necessário.
4. Confirme que aparecem faixas entre aproximadamente USD 33 e USD 38 e um quadro com os dados.

A demonstração usa números fictícios e serve somente para confirmar que o indicador está funcionando.

## Passo 4 — usar dados reais

Desative a demonstração e cole as séries no campo de entrada. Cada linha deve seguir:

```text
vencimento;tipo;strike;oi;premio;multiplicador
```

Exemplo de estrutura:

```text
2099-12-18;C;35;1000;1.20;100
2099-12-18;P;35;800;0.95;100
```

Use:

- `C` para call;
- `P` para put;
- ponto como separador decimal;
- `NA` quando o prêmio estiver ausente;
- a data real de referência do OI.

## Passo 5 — preencher metadados

Informe a data de referência do Open Interest e identifique a fonte/horário dos prêmios. Isso é importante porque OI e prêmio podem ter referências temporais diferentes.

## Como saber se deu certo

A instalação está correta quando:

- o código compila;
- o indicador reconhece o gráfico do EWZ;
- as faixas aparecem à direita das velas;
- o quadro exibe OI e valores;
- entradas inválidas geram mensagem em vez de resultados silenciosamente incorretos.

## Limites

O indicador não busca a cadeia automaticamente. Os dados precisam ser atualizados manualmente sempre que você quiser um novo snapshot.
