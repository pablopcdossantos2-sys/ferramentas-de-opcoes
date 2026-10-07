# Tutorial de instalação — EWZ GEX → WIN

Este tutorial foi escrito para usuários com pouca familiaridade com programação ou terminal.

> **Estado atual do projeto:** o repositório preserva o indicador Pine do TradingView. A aplicação desktop/GUI ainda é um protótipo em desenvolvimento e não está arquivada aqui como instalador pronto. Portanto, a parte reproduzível hoje é a instalação do indicador Pine.

## O que você precisa

- Uma conta no TradingView.
- Um navegador atualizado.
- Acesso a um gráfico do WIN ou do contrato/ativo que você pretende usar.
- O arquivo `source/EWZ_GEX_WIN_Pro.pine` deste repositório.

Não é necessário instalar Python, Node.js ou outro ambiente para usar somente o indicador Pine.

## Parte 1 — instalar o indicador no TradingView

1. Abra o TradingView no navegador.
2. Abra um gráfico do WIN ou do ativo em que deseja visualizar as projeções.
3. Na parte inferior do TradingView, abra **Pine Editor**.
4. Abra no GitHub o arquivo `source/EWZ_GEX_WIN_Pro.pine`.
5. Copie todo o conteúdo do arquivo, começando em `//@version=6`.
6. Apague o conteúdo existente no Pine Editor.
7. Cole o código.
8. Clique em **Salvar** e dê um nome ao indicador, por exemplo `EWZ GEX → WIN`.
9. Clique em **Adicionar ao gráfico**.

Se o TradingView mostrar um erro de compilação, não continue operando como se o indicador estivesse validado. Registre a mensagem de erro para correção.

## Parte 2 — configurar a referência

O indicador possui dois modos de referência:

- **Automática — fechamento NY**: tenta sincronizar EWZ e o ativo do gráfico no fechamento regular de Nova York.
- **Manual sincronizada**: você informa o preço do EWZ e do WIN observados no mesmo instante.

Para os primeiros testes, use o modo automático em gráfico intradiário e confira se os preços de referência exibidos fazem sentido.

## Parte 3 — informar os níveis

A versão preservada no repositório recebe os níveis GEX por campos de configuração. Abra **Configurações → Inputs** do indicador e informe os níveis disponíveis para:

- Call/Put teto;
- Call Wall 1 e 2;
- Gamma resistência;
- Gamma Flip;
- Gamma suporte;
- Put Wall 2;
- Put Wall chão.

Se um nível não estiver disponível, deixe-o zerado/desativado conforme a configuração do indicador.

## Parte 4 — aplicação GUI

A arquitetura do projeto prevê uma aplicação portátil com botão de atualização e exportação de dados para o TradingView. Essa parte ainda deve ser consolidada no repositório antes de existir um tutorial de instalação reproduzível do executável.

Quando o instalador/arquivo portátil estiver versionado, este tutorial deverá ser ampliado com:

1. download do executável;
2. primeira abertura;
3. atualização dos dados;
4. verificação da data da cadeia;
5. cópia do bloco TradingView;
6. colagem no indicador compatível.

## Como saber se a instalação deu certo

A instalação do Pine está correta quando:

- o indicador aparece na lista de indicadores do gráfico;
- as configurações abrem sem erro;
- os níveis informados são desenhados;
- o painel mostra a referência EWZ/WIN;
- o TradingView não exibe erro de compilação.

## Limitação importante

Instalar o indicador não torna a coleta de dados automática. A automação da cadeia de opções pertence à aplicação externa em desenvolvimento.
