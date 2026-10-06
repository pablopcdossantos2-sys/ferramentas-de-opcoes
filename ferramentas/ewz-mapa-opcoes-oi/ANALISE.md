# Análise — EWZ | Mapa de opções: OI e financeiro

## Resumo

Esta ferramenta é um indicador Pine Script v6 específico para o **EWZ em USD**. Em vez de receber apenas níveis finais, ela recebe uma mini-base de séries de opções no formato:

`vencimento;tipo;strike;oi;premio;multiplicador`

e agrega esses contratos em **faixas de strike** configuráveis.

## O que ela calcula

- Open Interest de calls e puts por faixa.
- Razão Put/Call de OI.
- Valor pelo prêmio: `Σ(OI × prêmio × multiplicador)`.
- Nocional pelo strike: `Σ(OI × strike × multiplicador)`.
- Totais globais após os filtros de vencimento.

## Visualização

O indicador desenha caixas horizontais à direita da última vela:

- laranja quando predomina OI de calls;
- azul quando predomina OI de puts;
- mistura proporcional quando ambos coexistem;
- intensidade vinculada ao OI total da faixa.

Também exibe um quadro paginado com OI, valores em USD e P/C OI.

## Pontos fortes

1. **Transparência do dado bruto.** O usuário enxerga concentração real de OI por faixa, em vez de somente níveis derivados.
2. **Validação rigorosa.** O script rejeita datas inválidas, duplicatas, OI fracionário/negativo e formatos incorretos.
3. **Tratamento correto de ausência.** Prêmio ausente pode ser `NA`; o indicador preserva o OI e evita apresentar soma financeira incompleta como se fosse válida.
4. **Metadados de proveniência.** Exige data de referência do OI e permite registrar fonte/horário dos prêmios.
5. **Boa disciplina conceitual.** O próprio guia deixa explícito que OI e os valores financeiros calculados não equivalem a fluxo negociado, margem, exposição líquida de dealers ou direção garantida.

## Limitações

- Não consulta API ou cadeia de opções automaticamente.
- Não produz histórico nem funciona como backtest/Replay.
- Não calcula GEX, DEX, Vanna ou Gamma Flip.
- Não gera Call Wall/Put Wall como níveis derivados.
- Não projeta EWZ para WIN.
- Não possui a camada de alertas operacionais encontrada em algumas das outras ferramentas.
- O guia informa que a compilação/renderização final no TradingView ainda precisava de validação naquele ambiente.

## Comparação com as demais

### versus Mapa de Opções

É a ferramenta mais próxima conceitualmente do **Mapa de Opções**. Ambas trabalham com OI e valor nocional, mas em camadas diferentes:

- **Mapa de Opções:** aquisição, histórico, persistência e análise em WebApp.
- **EWZ Mapa de Opções em Aberto:** visualização de snapshot dentro do TradingView.

A combinação natural é o WebApp/collector exportar diretamente o texto aceito pelo Pine.

### versus EWZ GEX → WIN

São complementares:

- **EWZ Mapa OI:** mostra onde está o estoque de contratos por strike/faixa.
- **EWZ GEX → WIN:** tenta transformar a cadeia em métricas de gamma e projetar níveis para o WIN.

Um mesmo coletor pode alimentar os dois formatos.

### versus quantedOptions Levels [qO]

O qO é mais sofisticado em GEX/DEX, ladder e conversão entre proxies. A ferramenta EWZ OI é mais simples em derivadas, mas é mais explícita sobre o dado bruto, multiplicador, prêmio, OI ausente e proveniência.

### versus Options Levels

Options Levels recebe 13 preços finais (Walls, Flip, Whales e sigmas). O EWZ Mapa OI recebe séries de opções e constrói agregações. Portanto, ele transporta mais informação primária, porém não produz os níveis sofisticados daquele indicador.

### versus Support and Resistance from Options Data

Support & Resistance oferece mais métricas e alertas (IV, Vanna, Implied Move, walls de curto prazo, bounce/rejection). O EWZ Mapa OI é mais conservador: mostra estrutura de OI e valores financeiros sem transformar isso automaticamente em sinal operacional.

## Melhor uso no ecossistema

Arquitetura recomendada:

```text
Coletor de cadeia EWZ
        │
        ├── exportação RAW → EWZ Mapa de Opções em Aberto
        │                    (OI, P/C, valores por faixa)
        │
        └── motor derivado → EWZ GEX → WIN
                             (GEX, Walls, Flip, projeção)
```

Assim, uma única aplicação portátil de coleta pode produzir **dois blocos copiáveis**: um para análise estrutural de OI e outro para níveis derivados de gamma.
