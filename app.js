(() => {
  const root = document.documentElement;
  const saved = localStorage.getItem("options-portfolio-theme");
  if (saved) root.dataset.theme = saved;

  const toggle = document.getElementById("themeToggle");
  toggle?.addEventListener("click", () => {
    const next = root.dataset.theme === "light" ? "dark" : "light";
    root.dataset.theme = next;
    localStorage.setItem("options-portfolio-theme", next);
  });

  const search = document.getElementById("featureSearch");
  const rows = [...document.querySelectorAll("#comparisonTable tbody tr")];
  search?.addEventListener("input", (event) => {
    const term = event.target.value.trim().toLocaleLowerCase("pt-BR");
    rows.forEach((row) => {
      const haystack = row.textContent.toLocaleLowerCase("pt-BR");
      row.classList.toggle("hidden", term && !haystack.includes(term));
    });
  });

  const concepts = {
    "open-interest": {
      title: "Open Interest (OI)",
      simple: "É a quantidade de contratos de opções que continuam abertos no mercado ao fim da referência usada pela fonte. Um contrato aberto existe porque há duas pontas — alguém comprado e alguém vendido — portanto OI não indica, sozinho, quem está 'apostando na alta' ou na baixa.",
      reading: "OI alto em determinado strike mostra que existe muita posição em aberto naquele preço de exercício. Isso ajuda a localizar regiões relevantes da cadeia, mas não revela a estratégia completa dos participantes.",
      example: "Se o strike 35 do EWZ tem OI de 20.000 calls, isso significa 20.000 contratos de call ainda abertos — não 20.000 compradores líquidos.",
      caution: "Não confunda OI com volume. Volume mede contratos negociados durante um período; OI mede contratos que permanecem abertos."
    },
    "notional-oi": {
      title: "Notional Open Interest",
      simple: "É uma forma de traduzir a quantidade de contratos em uma referência monetária bruta. No nosso Mapa de Opções, a convenção principal é OI × multiplicador do contrato × preço do ativo.",
      reading: "Serve para comparar o tamanho econômico aproximado do estoque de posições ao longo do tempo ou entre grupos de opções, desde que a mesma metodologia seja usada.",
      example: "Com 10.000 contratos, multiplicador 100 e EWZ a US$ 40, o nocional de referência é US$ 40 milhões.",
      caution: "Não é dinheiro efetivamente investido, prêmio pago, risco máximo, margem ou exposição líquida ajustada por delta."
    },
    "premium-oi-value": {
      title: "Valor por prêmio × OI",
      simple: "É uma estimativa do valor das opções abertas aos prêmios fornecidos: OI × prêmio da opção × multiplicador do contrato.",
      reading: "É útil para ter uma ordem de grandeza do valor das opções abertas quando existe um prêmio de referência válido para cada contrato.",
      example: "1.000 contratos com prêmio de US$ 1,20 e multiplicador 100 resultam em US$ 120.000 nessa medida.",
      caution: "Não representa necessariamente quanto foi pago originalmente pelas posições. O prêmio atual pode ser muito diferente do preço pelo qual cada posição foi aberta."
    },
    "walls": {
      title: "Call Wall e Put Wall",
      simple: "São nomes usados por algumas metodologias de análise de opções para destacar strikes onde existe concentração relevante de exposição — normalmente associada a gamma, OI ou uma combinação definida pelo fornecedor.",
      reading: "A Call Wall costuma ser tratada como uma região superior relevante e a Put Wall como uma região inferior relevante. A interpretação exata depende da fórmula usada pela ferramenta.",
      example: "Se uma metodologia identifica grande concentração de exposição em calls no strike 38 e em puts no strike 34, esses strikes podem ser apresentados como Call Wall e Put Wall.",
      caution: "Wall não é uma barreira física nem uma garantia de suporte ou resistência. Diferentes fornecedores podem calcular Walls de formas diferentes."
    },
    "gamma-flip": {
      title: "Gamma Flip",
      simple: "É o nível de preço em que, segundo uma determinada metodologia de exposição agregada, o sinal do gamma líquido estimado muda de positivo para negativo ou vice-versa.",
      reading: "Ele é usado como referência de possível mudança no comportamento de hedge dos dealers. Acima e abaixo do Flip, algumas abordagens esperam dinâmicas diferentes de estabilização ou amplificação do movimento.",
      example: "Se o gamma agregado estimado cruza zero quando o EWZ está em US$ 36,10, esse preço pode ser marcado como Gamma Flip.",
      caution: "O cálculo depende de hipóteses sobre posições e convenções de sinal. Não existe um único Gamma Flip universal válido para todos os fornecedores."
    },
    "gex": {
      title: "GEX — Gamma Exposure",
      simple: "Gamma mede quanto o delta de uma opção tende a mudar quando o preço do ativo muda. GEX tenta transformar esse gamma em uma medida de exposição agregada, normalmente combinando gamma, Open Interest, multiplicador e preço do ativo.",
      reading: "Ao agregar GEX por strike, podemos observar onde a cadeia concentra maior sensibilidade de gamma. É desse tipo de perfil que muitas metodologias derivam Walls e Flip.",
      example: "Dois strikes com o mesmo OI podem ter GEX muito diferente porque o gamma das opções e a proximidade do vencimento também importam.",
      caution: "A fórmula e o sinal atribuídos a calls e puts variam entre metodologias. GEX não revela diretamente a posição líquida real de todos os dealers."
    },
    "dex": {
      title: "DEX — Delta Exposure",
      simple: "É uma medida agregada baseada no delta das opções. Delta estima quanto o preço de uma opção tende a variar para uma pequena mudança no preço do ativo subjacente.",
      reading: "DEX tenta resumir a sensibilidade direcional da cadeia, geralmente combinando delta, OI e multiplicador. Pode complementar o GEX porque delta e gamma descrevem aspectos diferentes da exposição.",
      example: "Uma call com delta 0,60 reage, de forma aproximada e local, como 0,60 unidade do ativo para uma variação de US$ 1 no subjacente, antes de considerar outras mudanças.",
      caution: "Assim como GEX, a exposição agregada depende de convenções e não identifica automaticamente quem está comprado ou vendido em cada contrato."
    },
    "vanna": {
      title: "Vanna",
      simple: "Vanna é uma grega de segunda ordem. Ela descreve como o delta de uma opção muda quando a volatilidade implícita muda — ou, de forma equivalente, como a vega muda quando o preço do ativo se move.",
      reading: "Algumas ferramentas tentam localizar níveis onde a exposição de Vanna é relevante para estimar como mudanças simultâneas de preço e volatilidade podem afetar hedges.",
      example: "Se a volatilidade implícita cai enquanto o ativo sobe, a Vanna ajuda a descrever parte da mudança adicional no delta das opções.",
      caution: "É um conceito mais avançado e muito dependente do modelo. Um 'nível de Vanna' não deve ser tratado como suporte ou resistência garantidos."
    },
    "implied-move": {
      title: "Implied Move",
      simple: "É uma estimativa do movimento de preço que o mercado de opções está precificando para um horizonte específico, geralmente derivada dos prêmios ou da volatilidade implícita.",
      reading: "Pode ser exibido como uma faixa em torno do preço atual, por exemplo preço ± movimento implícito.",
      example: "Com ativo a US$ 40 e implied move de US$ 2, a faixa simples seria aproximadamente US$ 38 a US$ 42 para o horizonte considerado.",
      caution: "Não significa que o preço ficará dentro da faixa, nem que há uma probabilidade fixa universal sem conhecer exatamente a metodologia usada."
    },
    "iv": {
      title: "IV — Volatilidade Implícita",
      simple: "É a volatilidade que, inserida em um modelo de precificação, torna o preço teórico da opção compatível com o preço observado no mercado.",
      reading: "IV costuma aumentar quando opções ficam relativamente mais caras e diminuir quando ficam relativamente mais baratas, mantendo os demais fatores comparáveis. Ela expressa expectativa/precificação de incerteza, não direção.",
      example: "IV alta pode coexistir tanto com expectativa de forte alta quanto de forte queda; ela fala principalmente sobre magnitude e preço da incerteza.",
      caution: "IV não é a mesma coisa que volatilidade futura realizada e não indica, sozinha, se o ativo vai subir ou cair."
    },
    "put-call-ratio": {
      title: "Put/Call Ratio",
      simple: "É uma razão entre puts e calls. A ferramenta precisa dizer qual grandeza está sendo comparada — por exemplo OI de puts ÷ OI de calls ou volume de puts ÷ volume de calls.",
      reading: "Valores acima de 1 indicam que a medida de puts usada no numerador é maior que a de calls. É uma descrição da estrutura observada, não uma classificação automática de mercado bearish/bullish.",
      example: "OI de puts = 30.000 e OI de calls = 20.000 resulta em P/C OI = 1,5.",
      caution: "Uma put pode ser hedge, parte de um spread ou posição vendida. Portanto a razão não revela sozinha a intenção dos participantes."
    },
    "whale-top-strikes": {
      title: "Whale Levels / Top Strikes",
      simple: "É um rótulo informal para strikes que a ferramenta considera especialmente relevantes por concentração de OI, GEX, volume ou outra métrica.",
      reading: "Top strikes é um nome mais neutro: simplesmente ranqueia strikes pela métrica escolhida. 'Whale' sugere grande participante, mas normalmente o dado público não identifica quem abriu as posições.",
      example: "Os cinco strikes com maior GEX podem ser apresentados como Top 5. Outra ferramenta pode chamá-los de Whale 1–5.",
      caution: "Não assuma que um Whale Level prova a atuação de uma 'baleia' específica. É uma convenção visual/heurística."
    },
    "sigma-levels": {
      title: "Níveis σ (sigma)",
      simple: "Sigma (σ) representa desvio-padrão. Em ferramentas de mercado, níveis σ costumam marcar distâncias estatísticas acima e abaixo de uma referência, como preço médio, movimento esperado ou distribuição modelada.",
      reading: "σ1 e σ2 normalmente significam um e dois desvios-padrão segundo a metodologia adotada. A fórmula exata precisa ser conhecida para interpretar os níveis corretamente.",
      example: "Se uma ferramenta usa preço de referência 100 e desvio estimado 2, um esquema simples poderia marcar +1σ em 102 e −1σ em 98.",
      caution: "Os níveis não têm significado universal sem saber qual distribuição, horizonte e volatilidade foram usados no cálculo."
    }
  };

  const dialog = document.getElementById("conceptDialog");
  const dialogTitle = document.getElementById("conceptTitle");
  const dialogBody = document.getElementById("conceptBody");
  const closeButtons = [
    document.getElementById("conceptClose"),
    document.getElementById("conceptCloseBottom")
  ].filter(Boolean);

  const renderConcept = (concept) => {
    dialogTitle.textContent = concept.title;
    dialogBody.innerHTML = `
      <h3>Em termos simples</h3>
      <p class="concept-simple">${concept.simple}</p>
      <h3>Como ler na prática</h3>
      <p>${concept.reading}</p>
      <div class="concept-example"><strong>Exemplo didático</strong><p>${concept.example}</p></div>
      <div class="concept-caution"><strong>Cuidado com a interpretação</strong><p>${concept.caution}</p></div>
    `;
  };

  document.querySelectorAll(".concept-info").forEach((button) => {
    button.addEventListener("click", () => {
      const concept = concepts[button.dataset.concept];
      if (!concept || !dialog) return;
      renderConcept(concept);
      dialog.showModal();
    });
  });

  closeButtons.forEach((button) => button.addEventListener("click", () => dialog?.close()));

  dialog?.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });
})();