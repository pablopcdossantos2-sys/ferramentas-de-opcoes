# EWZ — mapa de opções em aberto

Indicador em **Pine Script v6**, arquivo `EWZ_Mapa_Opcoes.pine`.

O indicador desenha faixas de strikes à direita da última vela do EWZ e exibe um quadro com contratos em aberto (OI), valores em USD e razão put/call. **Os dados de opções são inseridos e atualizados manualmente.** O código não contém cotações reais nem conecta uma API de opções.

## Instalação

1. Abra um gráfico de **EWZ cotado em USD** no TradingView.
2. Abra o **Pine Editor**, crie um indicador e substitua seu conteúdo pelo arquivo `.pine` inteiro, desde `//@version=6`.
3. Salve e selecione **Adicionar ao gráfico**.
4. Nas configurações do indicador, ative **Demonstração — dados FICTÍCIOS** para visualizar o funcionamento. As faixas fictícias ficam entre USD 33 e USD 38; ajuste a escala se estiverem fora da área visível.
5. Para usar dados reais, desative a demonstração, cole as séries no campo **Cole as séries de opções**, informe a **data de referência do OI** e identifique a fonte e o horário dos prêmios.
6. Ajuste a largura das faixas, os vencimentos e a posição do quadro. Deixe espaço à direita da última vela para visualizar as faixas. Sua extensão padrão é de 70 barras.

A opção de demonstração substitui inteiramente os dados colados enquanto estiver ativa. Ela aparece identificada no quadro. Na instalação inicial, a demonstração está desativada e o indicador começa sem dados.

## Formato dos dados

Uma série de opção por linha, sem cabeçalho:

```text
vencimento;tipo;strike;oi;premio;multiplicador
```

| Campo | Conteúdo |
|---|---|
| vencimento | Data válida em `AAAA-MM-DD` |
| tipo | `C` para call; `P` para put |
| strike | Preço de exercício em USD, com ponto decimal |
| oi | Contratos em aberto; inteiro não negativo |
| premio | Prêmio em USD por cota; `NA` se indisponível |
| multiplicador | Multiplicador financeiro do contrato; normalmente `100` para séries padrão |

Exemplo **inteiramente fictício**, com data de referência do OI `2099-12-01`:

```text
2099-12-18;C;35;1000;1.20;100
2099-12-18;P;35;800;0.95;100
2100-01-15;C;35;500;1.60;100
2099-12-18;C;36;1200;NA;100
```

Nesse exemplo, para largura de USD 1, a faixa `[35, 36)` contém OI call de 1.500 e OI put de 800. Seu valor pelo prêmio é USD 200.000 em calls e USD 76.000 em puts: **USD 276.000 no total**. A call de strike 36 vai para `[36, 37)` e conserva seu OI, mas seu valor pelo prêmio aparece como `N/D`.

Use os dados de uma cadeia de opções de EWZ obtida na corretora ou em um fornecedor ao qual você tenha acesso. Converta a exportação para esse formato. Não cole símbolos de outro ativo, contratos ajustados ou séries com entregáveis diferentes. O script verifica o gráfico, mas não consegue confirmar a origem dos dados digitados.

Use ponto decimal, sem símbolos de moeda ou separadores de milhar: `12000` e `1.25`. Campos desconhecidos de OI não devem ser preenchidos com zero. OI é a quantidade de contratos em aberto; não some separadamente o lado comprado e o vendido do mesmo contrato.

Se usar o ponto médio entre bid e ask como prêmio, identifique esse critério na fonte. Uma cotação ausente deve ser `NA`; um zero significa preço zero informado pela fonte. Considere também a data das cotações, pois o cálculo mistura o OI informado com os prêmios que você fornecer.

## O que o valor financeiro representa

O seletor oferece duas medidas, calculadas primeiro por contrato e depois somadas por faixa e tipo:

| Medida | Fórmula | Interpretação |
|---|---|---|
| Valor pelo prêmio — padrão | `Σ(OI × prêmio × multiplicador)` | Estimativa do valor das opções abertas aos prêmios fornecidos |
| Nocional pelo strike | `Σ(OI × strike × multiplicador)` | Referência bruta do valor de exercício dos contratos |

O prêmio de opções é cotado por unidade do ativo e contratos padrão geralmente representam 100 unidades. Ajustes podem alterar os termos do contrato. [OIC — Options Basics](https://www.optionseducation.org/optionsoverview/options-basics).

**Essas medidas não são volume financeiro efetivamente negociado**, margem depositada nem exposição líquida dos participantes. Para volume financeiro negociado seria necessário agregar negócios com seus respectivos preços e quantidades. OI é apurado a partir das posições que permanecem abertas após a compensação, e sozinho não indica direção de mercado. [OIC — General Information](https://www.optionseducation.org/referencelibrary/faq/general-information).

## Como ler o gráfico e o quadro

- As faixas usam o limite inferior inclusivo e o superior exclusivo: `[35, 36)` inclui strike 35 e exclui strike 36. Largura de USD 0,50 separa `[35, 35.5)` de `[35.5, 36)`.
- A cor se aproxima do laranja quando predomina OI call e do azul quando predomina OI put. Havendo ambos, a cor é uma mistura proporcional. Quanto maior o OI total, mais forte o preenchimento. As cores podem ser alteradas nas configurações.
- Os textos das faixas mostram `C` e `P` em contratos. O quadro mostra os respectivos valores em USD.
- A marca `>` destaca a faixa que contém o último preço do gráfico.
- **P/C OI** é `OI put ÷ OI call`. Quando OI call é zero, aparece `N/D`.
- **TOTAL — todas as páginas** soma todas as faixas após os filtros. A paginação muda o quadro; todas as faixas continuam desenhadas.
- `K`, `M` e `B` significam mil, milhão e bilhão. Desative a abreviação para ver valores em USD com duas casas decimais.
- Se alguma série com OI positivo não tiver prêmio, o valor daquele tipo na faixa, o total da faixa e os totais correspondentes aparecem como `N/D`. Isso impede que uma soma incompleta seja apresentada como total. O modo nocional continua disponível.

O indicador bloqueia séries duplicadas por vencimento/tipo/strike, datas inválidas, OI fracionário ou negativo e formatos incorretos. Séries com OI zero não criam faixas. O limite é de 1.000 linhas e 120 faixas; filtre a exportação antes de colar caso ela exceda esses limites.

Os filtros de vencimento são inclusivos. Preencher início e fim com a mesma data seleciona um único vencimento. Por padrão, vencimentos anteriores à **data de referência do OI** são excluídos. Esse critério preserva o retrato daquela data; ele não transforma um arquivo antigo em dados atuais.

## Atualização e limites

Atualize o texto e a data do OI sempre que receber um novo conjunto de dados. O movimento do EWZ não atualiza OI nem prêmios. O código não possui atualização automática e não reconstrói o histórico de opções para backtest ou Replay. As caixas à direita são uma representação do conjunto fornecido, não uma previsão de preço.

A documentação pública de acesso a dados do Pine não oferece uma função para enumerar a cadeia inteira e recuperar seu OI. `request.security()` consulta séries de símbolos disponíveis; isso não fornece automaticamente a cadeia de EWZ. Por essa razão, esta versão usa entrada de texto. [TradingView — Other timeframes and data](https://www.tradingview.com/pine-script-docs/concepts/other-timeframes-and-data/).

## Verificação realizada

Foram conferidas a aritmética da demonstração, a agregação de diferentes vencimentos no mesmo strike e a classificação de strikes nas fronteiras das faixas.

Com a demonstração ativada, largura USD 1 e filtros de vencimento vazios, os resultados esperados são:

| Medida | Calls | Puts | Total |
|---|---:|---:|---:|
| OI | 12.300 | 10.500 | 22.800 |
| Valor pelo prêmio | USD 1.035.500 | USD 1.009.000 | USD 2.044.500 |
| Nocional pelo strike | USD 44.110.000 | USD 36.020.000 | USD 80.130.000 |

São 12 séries distribuídas em 5 faixas. **A compilação e a renderização no editor do TradingView não foram executadas neste ambiente.** As verificações numéricas não substituem essa validação final.