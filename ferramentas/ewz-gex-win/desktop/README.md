# EWZ GEX → WIN Desktop — desenvolvimento

Aplicação desktop/GUI complementar ao indicador Pine do projeto principal.

## Estado

**Alpha de desenvolvimento.** A interface, o núcleo de agregação GEX, a captura via Microsoft Edge e o formato de exportação `EWZGEX1` já estão implementados. A coleta real no Barchart ainda precisa ser validada em máquinas Windows diferentes e acompanhada após mudanças no site.

## Arquitetura

- **Tkinter** para a GUI, evitando frameworks visuais pesados.
- **Playwright + Microsoft Edge instalado no Windows** para carregar a página real do Barchart com JavaScript e reutilizar uma sessão persistente.
- Captura das respostas JSON de opções utilizadas pela própria página.
- Fallback para uma requisição same-origin disparada dentro da sessão do navegador.
- Agregação local de GEX por strike.
- Extração, quando possível, de **Call Wall**, **Put Wall** e **Gamma Flip** publicados na página.
- Níveis adicionais do método original são exibidos como **estimativas locais de baixa confiança** quando não existe valor publicado equivalente.
- Exportação de um único bloco `EWZGEX1|...` para o indicador Pine.

## Decisão metodológica importante

O Barchart descreve publicamente seu Gamma Exposure como baseado em gamma e Open Interest para um movimento de 1% do ativo. O núcleo local utiliza a aproximação:

`gamma × OI × 100 × spot² × 1%`

com puts negativas para construir um perfil líquido por strike.

Essa aproximação **não é tratada como reprodução perfeita do cálculo proprietário do Barchart**. Por isso, a aplicação registra a origem e a confiança de cada nível e evita inventar um Gamma Flip quando ele não puder ser extraído da página.

## Desenvolvimento local

Requer Python 3.11+ e Microsoft Edge.

```powershell
cd ferramentas\ewz-gex-win\desktop
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Não é necessário instalar o Chromium do Playwright: o aplicativo usa o Microsoft Edge já instalado.

## Testes

```powershell
pip install -r requirements-build.txt
pytest -q
```

## Build portátil

O arquivo `EWZ_GEX_WIN_Desktop.spec` gera uma pasta portátil para Windows com PyInstaller. O workflow `build-ewz-gex-win-desktop.yml` executa testes e publica um ZIP como artifact do GitHub Actions.

## Próximas validações

1. validar a coleta contra o Barchart em Windows 10 e 11;
2. conferir os campos retornados em dias com diferentes conjuntos de vencimentos;
3. comparar Call Wall / Put Wall / Gamma Flip extraídos com os valores exibidos visualmente na página;
4. calibrar ou substituir os níveis auxiliares específicos da metodologia do curso;
5. só então marcar a aplicação como versão estável e finalizar o tutorial de instalação para usuários finais.
