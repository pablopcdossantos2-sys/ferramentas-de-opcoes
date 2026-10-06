# Banco de dados de ferramentas de opções

Este diretório preserva as ferramentas analisadas na conversa, junto com uma ficha técnica resumida de cada uma.

## Regra do repositório

Sempre que uma nova ferramenta relacionada a opções for anexada ou analisada, ela deve ganhar:

1. uma pasta própria em `ferramentas/`;
2. o código-fonte recebido, quando disponível;
3. documentação/origem, quando fornecida;
4. uma ficha de análise;
5. uma entrada em `catalogo.json`;
6. inclusão no web-portfólio comparativo da raiz.

## Ferramentas catalogadas

| ID | Ferramenta | Tipo | Foco |
|---|---|---|---|
| `ewz-gex-win` | EWZ GEX → WIN | Aplicação + Pine | GEX do EWZ e projeção para WIN |
| `mapa-de-opcoes` | Mapa de Opções | WebApp | Cadeia, OI e Notional OI |
| `ewz-mapa-opcoes-oi` | EWZ — Mapa de Opções em Aberto | Pine v6 | OI por faixas de strike e valores financeiros |
| `quantedoptions-qo` | quantedOptions Levels [qO] | Pine v6 | Walls, Gamma/DEX e ladder por strike |
| `options-levels` | Options Levels | Pine v5 | 13 níveis pré-calculados |
| `support-resistance-options-data` | Support and Resistance levels from Options Data | Pine v6 | 17 métricas, Vanna, IV e alertas |

## Observação sobre origem

Alguns códigos foram fornecidos pelo usuário como anexos para análise. Eles são preservados aqui como material de referência, sem afirmar autoria, licença ou validação independente além do que estiver explicitamente documentado em cada pasta.
