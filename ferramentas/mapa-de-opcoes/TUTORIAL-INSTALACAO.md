# Tutorial de instalação — Mapa de Opções

Este documento diferencia o **projeto conceitual/documentado** de uma distribuição executável pronta.

> **Estado atual no catálogo:** a documentação descreve o WebApp e sua arquitetura, mas o código executável do projeto não está preservado dentro deste repositório de ferramentas. Na inspeção que originou o catálogo, o repositório relacionado não fornecia uma instalação reproduzível. Por isso, não é correto inventar comandos de instalação.

## O que existe hoje

A ficha do projeto documenta uma aplicação voltada a:

- cadeia de opções;
- Open Interest;
- Notional Open Interest;
- filtros NTM;
- snapshots históricos;
- importação de dados e coletores.

O repositório relacionado é:

`https://github.com/pablopcdossantos2-sys/mapa-de-opcoes`

## Como verificar se já existe uma versão instalável

1. Abra o repositório relacionado.
2. Procure por um `README.md` com seção de instalação.
3. Procure por arquivos típicos do projeto, como `package.json`, `requirements.txt`, `pyproject.toml` ou scripts de inicialização.
4. Verifique se há uma seção **Releases** com pacote pronto.
5. Não execute comandos copiados de documentação antiga se eles não corresponderem aos arquivos atuais do repositório.

## Se o código ainda estiver ausente

Nesse caso, **não há instalação a realizar**. O item permanece no catálogo como projeto complementar e referência arquitetural.

Quando o código executável estiver disponível, este tutorial deverá ser atualizado usando apenas os comandos e dependências reais da versão publicada.

## Critério de instalação concluída

Só considere a ferramenta instalada quando houver uma versão do código que:

- inicialize sem erro;
- abra o dashboard;
- permita selecionar um ativo;
- carregue ou importe uma cadeia de opções;
- identifique claramente dados demonstrativos versus dados reais.

## Por que este tutorial não fornece comandos genéricos

Uma versão antiga da ideia mencionava Streamlit/Python, enquanto a revisão posterior descreve uma arquitetura com frontend e persistência diferentes. Usar comandos de um protótipo antigo como se fossem a instalação atual seria enganoso.
