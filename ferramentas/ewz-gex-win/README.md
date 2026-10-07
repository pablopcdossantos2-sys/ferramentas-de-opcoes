# EWZ GEX → WIN

Projeto principal do repositório. A ferramenta é híbrida: uma aplicação desktop/GUI coleta e organiza dados do EWZ, enquanto o indicador Pine projeta os níveis para o WIN.

## Componentes

- `desktop/` — aplicação Windows em fase alpha.
- `source/EWZ_GEX_WIN_Pro.pine` — indicador TradingView.
- `tutorial.html` — tutorial web de instalação e primeiro uso.

## Fluxo atual

1. A aplicação abre a página Gamma Exposure do EWZ no Barchart por meio de uma sessão real do Microsoft Edge.
2. Captura respostas JSON de opções usadas pela página.
3. Organiza gamma e Open Interest por strike.
4. Extrai níveis publicados quando identificáveis e calcula proxies locais para níveis auxiliares.
5. Permite revisão manual dos valores.
6. Gera uma única linha `EWZGEX1|...`.
7. O Pine recebe essa linha no campo **Bloco EWZGEX1** e projeta os níveis EWZ → WIN.

## Estado

A aplicação desktop é **alpha**. O núcleo e a GUI já estão implementados, mas a coleta precisa ser testada em diferentes instalações do Windows e os níveis precisam ser comparados sistematicamente com a página de referência antes de uma versão estável.

O Gamma Flip não é inventado quando não é possível extraí-lo de forma confiável. Níveis específicos da metodologia original, quando não correspondem a um nível publicado pelo Barchart, são identificados como estimativas locais de baixa confiança.
