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
})();
