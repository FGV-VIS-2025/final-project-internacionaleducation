<script>
  import { onMount } from 'svelte';
  import { fade, fly, scale, slide } from 'svelte/transition';
  import BarChart from '../lib/BarChart.svelte';
  import Boxplot from '../lib/Boxplot.svelte';
  import ScatterPlot from '../lib/ScatterPlot.svelte';
  import ScatterFun from '../lib/ScatterFun.svelte';
  import WorldMap from '../lib/WorldMap.svelte';
  import WorldFun from '../lib/WorldFun.svelte';
  import WorldFun2 from '../lib/WorldFun2.svelte';
  import MapForScatter from '../lib/MapForScatter.svelte';
  import Tooltip from '../lib/Tooltip.svelte';
  import ContinentBarChart from '../lib/ContinentBarChart.svelte';
  import CountryCostBoxplot from '../lib/CountryCostBoxplot.svelte';

  // Variáveis de estado
  let activeStep = 0;
  let educationData = [];
  let dataWithCost = [];
  let currentSlide = 0;
  let transitionDirection = 1; // 1 para próximo, -1 para anterior

  // Variáveis para filtros e interações
  let latitude = '';
  let longitude = '';
  let selectedPoint = [0, 0];
  let selectedContinent = null;
  let continentColorMap = {};

  // Constantes
  const numPaises = 71;
  const numCidades = 556;
  const numFaculdades = 622;

  // Funções de manipulação de dados
  async function fetchEducationData(url) {
    const res = await fetch(url);
    return await res.json();
  }

  function calculateCosts(data) {
    return data.map(d => {
      const tuition = Number(d.Tuition_USD);
      const visaFee = Number(d.Visa_Fee_USD);
      const rent = Number(d.Rent_USD);
      const durationYears = Number(d.Duration_Years);
      const total_cost = tuition + visaFee + rent * 12 * durationYears;
      return {
        Country: d.Country,
        City: d.City,
        Continent: d.Continent,
        University: d.University,
        Program: d.Program,
        Level: d.Level,
        lat: d.lat,
        lng: d.lng,
        total_cost
      };
    });
  }

  function getDistance(datum, point) {
    const [latPoint, lngPoint] = point;
    const lat = Number(datum.lat);
    const lng = Number(datum.lng);
    return Math.sqrt((latPoint - lat) ** 2 + (lngPoint - lng) ** 2);
  }

  // Declarações Reativas (lógica principal)
  $: if (educationData.length) {
    const baseCostData = calculateCosts(educationData);
    if (selectedPoint) {
      dataWithCost = baseCostData.map(d => ({
        ...d,
        distance: getDistance(d, selectedPoint)
      }));
    } else {
      dataWithCost = baseCostData;
    }
  }

  // Variáveis para armazenar os valores selecionados
  let selectedLevel = "";
  let selectedCountry = "";
  let selectedProgram = "";

  // Filtra os países com base no nível, programa e país selecionados
  $: countries = Array.from(new Set(
    educationData.filter(d =>
      (!selectedProgram || d.Program === selectedProgram) &&
      (!selectedLevel || d.Level === selectedLevel)  
    ).map(d => d.Country)
  )).sort();

  // Filtra os programas com base no país, nível e programa selecionados
  $: programs = Array.from(new Set(
    educationData.filter(d =>
      (!selectedCountry || d.Country === selectedCountry) &&
      (!selectedLevel || d.Level === selectedLevel)  
    ).map(d => d.Program)
  )).sort();

  // Filtra os dados com base no país, programa e nível selecionados
  $: filteredEducation = educationData.filter(d =>
    (!selectedCountry || d.Country === selectedCountry) &&
    (!selectedProgram || d.Program === selectedProgram) &&
    (!selectedLevel || d.Level === selectedLevel) 
  );
    
  $: filteredDataForBoxplot = selectedContinent
    ? dataWithCost.filter(d => d.Continent === selectedContinent)
    : dataWithCost;
  
  // Funções de Evento
  function handleColorsGenerated(event) {
    continentColorMap = event.detail;
  }

  function handleContinentSelect(event) {
    const continent = event.detail;
    selectedContinent = (selectedContinent === continent) ? null : continent;
  }
  
  // Funções de Navegação
  function next() {
    if (currentSlide < 7) {
      transitionDirection = 1;
      currentSlide += 1;
    }
  }
  function prev() {
    if (currentSlide > 0) {
      transitionDirection = -1;
      currentSlide -= 1;
    }
  }
  function goToSlide(i) {
    transitionDirection = i > currentSlide ? 1 : -1;
    currentSlide = i;
  }

  // Lifecycle
  onMount(() => {
    async function loadData() {
      educationData = await fetchEducationData('./education.json');
    }
    loadData();

    // IntersectionObserver para scrollytelling (se aplicável)
    const steps = document.querySelectorAll('.scroll-step');
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const index = +entry.target.dataset.index;
          if (index > activeStep) activeStep = index;
        }
      });
    }, { threshold: 0.5 });
    steps.forEach(step => observer.observe(step));
    return () => observer.disconnect();
  });
</script>

<div class="slide" aria-live="polite" role="region" aria-label="Apresentação de slides">
  {#key currentSlide}
    <div
      in:fly={{ x: 800 * transitionDirection, duration: 600, delay: 100 }}
      out:fly={{ x: -800 * transitionDirection, duration: 600 }}
      style="width: 100%; position: absolute; top: 10;"
    >
      {#if currentSlide === 0}
        <h2 in:fly={{ y: -40, duration: 600 }} class="title">
          Como os custos afetam a <strong>educação global</strong>?
        </h2>
        <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
          Este projeto visa <strong>analisar</strong> como as variações nos custos educacionais impactam estudantes no mundo todo.
          Usamos <em>visualizações interativas</em> baseadas em dados reais para trazer insights sobre <strong>desigualdades</strong> e oportunidades.
        </p>
        <p class="emphasized" in:scale={{ duration: 500, delay: 400 }}>
          Explore os dados e gráficos abaixo, ou navegue direto para as visualizações se já conhece o projeto!
        </p>
        <div style="display: flex; justify-content: center;">
          <img
            src="images/educacao.png"
            alt="Ilustração sobre educação"
            class="illustration-below"
            in:fly={{ x: -100, duration: 800, delay: 500 }}
          />
        </div>

      {:else if currentSlide === 1}
        <h2 in:fly={{ y: -40, duration: 600 }} class="title">
          Fontes de dados de instituições de alto nível
        </h2>
        <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
          Aqui trabalhamos apenas com dados de faculdades de alto nível ao redor do mundo.
          Abaixo, você vê o número de países, cidades e instituições diferentes contempladas:
        </p>
        <div class="stats-grid" in:scale={{ duration: 500, delay: 400 }}>
          <div class="stat-box">
            <div class="stat-number">{numPaises}</div>
            <div class="stat-label">Países</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">{numCidades}</div>
            <div class="stat-label">Cidades</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">{numFaculdades}</div>
            <div class="stat-label">Faculdades</div>
          </div>
        </div>
        <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
          Na base de dados você encontra não só informações sobre a faculdade, mas também sobre
          o custo de vida do país, o câmbio (em relação ao dólar), custo médio de aluguel, etc..
        </p>

      {:else if currentSlide === 2}
        <div class="left-right-container">
          <div class="left">
            <h2 in:fly={{ y: -40, duration: 600 }} class="title">
              Encontre as mais próximas de <strong>você!</strong>
            </h2>
            <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
              Para analisar as faculdades mais próximas de você, <strong>clique no mapa</strong> abaixo
              e analise a disponibilidade!
            </p>
            <WorldMap on:select={(e) => {
              latitude = e.detail.lat.toFixed(6);
              longitude = e.detail.lng.toFixed(6);
              selectedPoint = [e.detail.lat, e.detail.lng];
            }} />
          </div>
          <div class="right">
            <ScatterPlot data={dataWithCost} />
          </div>
        </div>

      {:else if currentSlide === 3}
        <h2 in:fly={{ y: -40, duration: 600 }} class="title">
          Como calculamos o <strong>preço por faculdade</strong>?
        </h2>
        <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
          A partir dos dados, para encontrar o custo total de cada curso usou-se uma fórmula
          simples, que considera o custo de todas mensalidades, do aluguel durante o período 
          (pode variar entre 3 a 6 anos!) e o VISA:
        </p>
        <div class="formula-container">
          <pre class="formula"><code><Tooltip text="Custo total do curso, incluindo mensalidade, aluguel e taxa de visto">total_cost</Tooltip> = <Tooltip text="Valor das mensalidades do curso, em dólares">tuition</Tooltip> + <Tooltip text="Taxa para emissão de visto de estudante">visaFee</Tooltip> + <Tooltip text="Aluguel mensal, em dólares">rent</Tooltip> * 12 * <Tooltip text="Duração do curso em anos">durationYears</Tooltip></code></pre>
          <p class="slide-text">
            O custo anual de vida estimado é em dólar, e é dado por:
          </p>
          <pre class="formula"><code><Tooltip text="Custo anual de vida, incluindo aluguel e seguro">      anual_cost</Tooltip> = (<Tooltip text="Valor do aluguel mensal, em dólares">rent</Tooltip> + <Tooltip text="Seguro saúde ou de vida, obrigatório em alguns países">insurance</Tooltip>) * 12</code></pre>
        </div>

      {:else if currentSlide === 4}
        <div class="left-right-container">
          <div class="left">
            <h2 in:fly={{ y: -40, duration: 600 }} class="title">
              Comparação de <strong>Custos Educacionais</strong>
            </h2>
            <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
              Gráfico de barras mostrando custos por país e programa para facilitar a comparação.
            </p>
            <label for="level-select" class="slide-text">Filtrar por nível de curso:</label>
            <select id="level-select" bind:value={selectedLevel} in:scale={{ duration: 400, delay: 300 }}>
              <option value="">Todos</option>
              <option value="Bachelor">Bacharel</option>
              <option value="Master">Mestrado</option>
              <option value="PhD">PhD</option>
            </select>

            <label for="country-select" class="slide-text">Filtrar por país:</label>
            <select id="country-select" bind:value={selectedCountry} in:scale={{ duration: 400, delay: 300 }}>
              <option value="">Todos</option>
              {#each countries as country}
                <option value={country}>{country}</option>
              {/each}
            </select>

            <label for="program-select" class="slide-text">Filtrar por curso:</label>
            <select id="program-select" bind:value={selectedProgram} in:scale={{ duration: 400, delay: 300 }}>
              <option value="">Todos</option>
              {#each programs as program}
                <option value={program}>{program}</option>
              {/each}
            </select>
          </div>
          
          <div class="right">
            {#if filteredEducation.length}
              <BarChart data={filteredEducation} />
            {:else}
              <p>Sem dados para esse país.</p>
            {/if}
          </div>
        </div>

      {:else if currentSlide === 5}
        <div class="left-right-container">
          <div class="left">
            <h2 in:fly={{ y: -40, duration: 600 }} class="title">
              Visualização <strong>Mapa Mundial</strong>
            </h2>
            <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
              Veja a distribuição geográfica dos custos educacionais em um mapa interativo.
            </p>
          </div>
          <div class="right">
            {#if educationData.length}
              <WorldFun2 data={educationData} />
            {:else}
              <p>Carregando dados...</p>
            {/if}
          </div>
        </div>

      {:else if currentSlide === 6}
        <div class="left-right-container">
          <div class="left">
            <h2 in:fly={{ y: -40, duration: 600 }} class="title">
              Análise Interativa: <strong>Continente & Custo</strong>
            </h2>
            <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
              Clique em um continente no gráfico de barras para filtrar a distribuição de custos por país no gráfico à direita. Clique novamente para limpar a seleção.
            </p>
            <div in:scale={{ duration: 500, delay: 400 }}>
              {#if dataWithCost.length}
                <ContinentBarChart
                  data={dataWithCost}
                  on:continentSelect={handleContinentSelect}
                  on:colorsGenerated={handleColorsGenerated}
                  selected={selectedContinent}
                />
              {:else}
                <p>Carregando dados do gráfico...</p>
              {/if}
            </div>
          </div>
          <div class="right">
            {#if filteredDataForBoxplot.length}
              <CountryCostBoxplot 
                data={filteredDataForBoxplot} 
                colors={continentColorMap} 
              />
            {:else}
              <p>Nenhum dado para exibir. Selecione um continente.</p>
            {/if}
          </div>
        </div>

      {:else if currentSlide === 7}
        <div class="left-right-container">
          <div class="left">
            <h2 in:fly={{ y: -40, duration: 600 }} class="title">
              Conclusão & Próximos Passos
            </h2>
            <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
              Analisamos os impactos dos custos na educação global. <strong>Continue explorando os dados</strong> e <em>contribua com feedback</em> para futuras versões.
            </p>
            <p class="slide-text" in:fly={{ y: 20, delay: 350, duration: 600 }}>
              Obrigado por acompanhar! 🌍🎓
            </p>
          </div>
          <div class="right">
            <img
              src="images/books_end.jpg"
              alt="Livros Desenhos"
              class="illustration-below"
              in:fly={{ x: 100, duration: 800, delay: 500 }}
            />
          </div>
        </div>
      {/if}
    </div>
  {/key}
</div>

<div class="bottom-navigation">
    <div class="nav-button-wrapper">
        {#if currentSlide > 0}
            <button class="button" size="long" on:click={prev} aria-label="Voltar para o slide anterior" transition:fade>
                <div id="background"></div>
                <div id="text">← Anterior</div>
                <div id="hitbox"></div>
            </button>
        {/if}
    </div>

    <footer style="background: transparent;">
        <div id="select" role="tablist" aria-label="Navegação entre slides">
            {#each Array(8) as _, i}
                <button
                    role="tab"
                    aria-selected={currentSlide === i}
                    aria-controls={`slide-${i}`}
                    id={`tab-${i}`}
                    class:selected={currentSlide === i}
                    class="dot"
                    on:click={() => goToSlide(i)}
                    on:keydown={(e) => {
                        const totalSlides = 8;
                        if (e.key === 'ArrowRight') goToSlide((i + 1) % totalSlides);
                        if (e.key === 'ArrowLeft') goToSlide((i - 1 + totalSlides) % totalSlides);
                    }}
                    tabindex={currentSlide === i ? '0' : '-1'}
                    title={`Slide ${i}: ${[
                        'Introdução', 'Base de Dados', 'Custo e Distância', '"How to?"',
                        'Comparação Geral', 'Faculdades pelo Mundo', 'Análise Interativa', 'Conclusão'
                    ][i]}`}
                >
                    <span class="sr-only">Slide {i + 1}</span>
                </button>
            {/each}
        </div>
    </footer>

    <div class="nav-button-wrapper">
        {#if currentSlide < 7}
            <button class="button" size="long" on:click={next} aria-label="Avançar para o próximo slide" transition:fade>
                <div id="background"></div>
                <div id="text">Próximo →</div>
                <div id="hitbox"></div>
            </button>
        {/if}
    </div>
</div>


<style>
  /* ESTILOS ANTERIORES PERMANECEM OS MESMOS */
  .slide {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 85vh; /* Aumentado para dar espaço para a navegação inferior */
    text-align: center;
    padding: 20px;
    max-width: 120ch;
    margin-inline: auto;
    user-select: none;
    position: relative;
  }

  .title {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 2.4rem;
    color: #2c3e50;
    margin-bottom: 0.3em;
    letter-spacing: 0.03em;
  }

  .slide-text {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 1.25rem;
    line-height: 1.6;
    color: #444;
    max-width: 60ch;
    margin: 0.5em auto 1.5em;
  }

  .slide-text strong {
    color: #e74c3c;
    cursor: help;
    border-bottom: 1.5px dotted #e74c3c;
    transition: color 0.3s;
  }
  .slide-text strong:hover {
    color: #c0392b;
  }

  .slide-text em {
    font-style: italic;
    color: #2980b9;
  }

  .emphasized {
    font-weight: 700;
    font-size: 1.2rem;
    color: #34495e;
    margin-top: 0;
    margin-bottom: 2rem;
    user-select: text;
  }

  .illustration-below {
    max-width: 300px;
    margin-top: 1rem;
    margin-bottom: 2rem;
    filter: drop-shadow(1px 2px 4px rgba(0,0,0,0.1));
    border-radius: 12px;
  }

  form.coord-form {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
  }
  form.coord-form label {
    font-weight: 600;
    font-size: 1rem;
    color: #333;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
  form.coord-form input {
    margin-top: 4px;
    padding: 0.5rem 0.7rem;
    font-size: 1rem;
    border-radius: 5px;
    border: 1.5px solid #bbb;
    width: 140px;
    transition: border-color 0.3s ease;
  }
  form.coord-form input:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 5px #3498dbaa;
  }
  button.button-small {
    align-self: flex-end;
    padding: 0.5rem 1rem;
    font-weight: 600;
    font-size: 1rem;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  button.button-small:hover {
    background: #2980b9;
  }

  button.button[size=long] {
    position: relative;
    width: 300px; /* Largura aumentada */
    height: 55px; /* Altura aumentada */
    border: none;
    background: none;
    cursor: pointer;
    padding: 0;
    overflow: hidden;
    border-radius: 10px;
    box-shadow: 0 6px 12px rgb(0 0 0 / 0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  button.button[size=long]:hover {
    z-index: 100;
    transform: scale(1.05);
    box-shadow: 0 10px 18px rgb(0 0 0 / 0.2);
  }

  button.button[size=long] #background {
    background: url(/images/button_long.png) no-repeat center;
    background-size: cover;
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    width: 100%;
    height: 100%;
    opacity: 1;
    pointer-events: none;
    border-radius: 10px;
  }

  button.button[size=long] #text {
    font-family: 'Comic Sans MS', cursive, sans-serif;
    position: relative;
    width: 90%;
    top: 0px;
    margin: 0 auto;
    color: #222;
    font-weight: 700;
    font-size: 1.3rem; /* Fonte aumentada */
    user-select: none;
    text-shadow: 1px 1px 1px #eee;
    line-height: 55px; /* Centraliza verticalmente com a nova altura */
  }

  button.button[size=long] #hitbox {
    position: absolute;
    width: 95%;
    height: 100%;
    top: 0;
    left: 2.5%; /* Centralizado */
    pointer-events: auto;
    border-radius: 10px;
  }

  #select {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 14px;
  }

  #select .dot.selected,
  #select .dot[aria-selected="true"] {
    background: #34495e;
    box-shadow: 0 0 8px #34495eaa;
    border: none;
    transform: scale(1.3);
    transition: all 0.25s ease;
  }

  #select .dot {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    border: 2px solid #34495e;
    display: inline-block;
    cursor: pointer;
    background: transparent;
    transition: all 0.3s ease;
    position: relative; /* Para o tooltip */
  }

  #select .dot:hover:not(.selected) {
    border-color: #2980b9;
    box-shadow: 0 0 6px #2980b9aa;
    transform: scale(1.15);
  }

  #select .dot[title]:hover::after {
    content: attr(title);
    position: absolute;
    background: #34495e;
    color: #fff;
    padding: 6px 10px;
    font-size: 14px;
    border-radius: 6px;
    bottom: 125%; /* Posição acima do dot */
    left: 50%;
    transform: translateX(-50%);
    white-space: nowrap;
    pointer-events: none;
    opacity: 1;
    transition: opacity 0.3s ease;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    z-index: 20;
  }

  #select .dot[title]:hover::before {
    content: '';
    position: absolute;
    border: 6px solid transparent;
    border-top-color: #34495e;
    bottom: 125%;
    margin-bottom: -12px;
    left: 50%;
    transform: translateX(-50%);
    pointer-events: none;
    opacity: 1;
    transition: opacity 0.3s ease;
    z-index: 20;
  }

  .sr-only {
    position: absolute !important;
    width: 1px !important;
    height: 1px !important;
    padding: 0 !important;
    margin: -1px !important;
    overflow: hidden !important;
    clip: rect(0,0,0,0) !important;
    border: 0 !important;
  }

  .left-right-container {
    display: flex;
    flex-direction: row;
    gap: 2rem;
    width: 100%;
    align-items: center;
    justify-content: center;
    padding: 1rem 0;
    box-sizing: border-box;
  }

.left {
  flex: 0 0 40%;
  max-width: 40%;
  text-align: left;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.right {
  flex: 0 0 60%;
  max-width: 60%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}

@media (max-width: 1024px) {
  .left-right-container {
    flex-direction: column;
    align-items: center;
  }
  .left, .right {
    max-width: 90%;
    flex: 1 1 100%;
    text-align: center;
    align-items: center;
  }
  .left {
    margin-bottom: 1.5rem;
  }
}

  .stats-grid {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin: 2rem 0;
    flex-wrap: wrap; /* Para telas menores */
  }
  .stat-box {
    background: #f5f5f5;
    border-radius: 8px;
    padding: 1rem 1.5rem;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }
  .stat-number {
    font-size: 2rem;
    font-weight: bold;
    color: #333;
  }
  .stat-label {
    font-size: 1rem;
    color: #666;
  }

  .formula-container {
    margin: 2rem auto;
    max-width: 800px;
    padding: 0 1rem;
}

.formula {
    background: #272c34;
    color: #f8f8f2;
    padding: 1rem 2rem; /* Padding ajustado */
    border-radius: 8px;
    font-family: 'Fira Code', monospace;
    margin: 1rem 0;
    white-space: pre-wrap;
    text-align: left;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.formula:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
}

/* NOVOS ESTILOS PARA NAVEGAÇÃO INFERIOR */
.bottom-navigation {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1em 2em;
    background: #f5f5f7;
    box-sizing: border-box;
    z-index: 1000;
    box-shadow: 0 -2px 5px rgba(0,0,0,0.08);
}

.nav-button-wrapper {
    flex: 1;
    display: flex;
}

.nav-button-wrapper:first-child {
    justify-content: flex-start;
}

.nav-button-wrapper:last-child {
    justify-content: flex-end;
}

footer {
    flex-shrink: 0;
}

@media (max-width: 768px) {
    .bottom-navigation {
        padding: 0.5em;
    }
    .nav-button-wrapper .button {
        display: none; /* Esconde botões grandes em telas pequenas */
    }
    footer {
        width: 100%;
        justify-content: center;
    }
}

#country-select, #program-select, #level-select {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  font-size: 16px;
  color: #333;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

/* Efeito quando o select está em foco */
#country-select:focus, #program-select:focus, #level-select:focus {
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.4);
  outline: none;
}

#country-select, #program-select, #level-select option {
  font-size: 16px;
  color: #333;
}

#country-select:hover, #program-select:hover, #level-select:hover{
  border-color: #0056b3;
}

#country-select, #program-select, #level-select{
  transition: all 0.3s ease;
}
</style>