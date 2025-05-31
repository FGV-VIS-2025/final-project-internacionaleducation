<script>
  import { onMount } from 'svelte';
  import { fade, fly, scale, slide } from 'svelte/transition';
  import BarChart from '../lib/BarChart.svelte';
  import Boxplot from  '../lib/Boxplot.svelte';
  import ScatterPlot from  '../lib/ScatterPlot.svelte';
  import ScatterFun from  '../lib/ScatterFun.svelte';
  import WorldMap from  '../lib/WorldMap.svelte';
  import WorldFun from  '../lib/WorldFun.svelte';
  import MapForScatter from '../lib/MapForScatter.svelte';

  let activeStep = 0;
  let educationData = [];
  let dataWithCost = [];

  let latitude = '';
  let longitude = '';

  async function fetchEducationData(url) {
    const res = await fetch(url);
    const data = await res.json();
    return data;
  }

  function calculateCosts(data) {
    return data
      .map(d => {
        const tuition = Number(d.Tuition_USD);
        const visaFee = Number(d.Visa_Fee_USD);
        const rent = Number(d.Rent_USD);
        const durationYears = Number(d.Duration_Years);

        const total_cost = tuition + visaFee + rent * 12 * durationYears;

        return {
          Country: d.Country,
          City: d.City,
          University: d.University,
          Program: d.Program,
          lat: d.lat,
          lng: d.lng,
          total_cost
        };
      });
  }

  $: showLine = activeStep !== 1;

  // Mudar distância para ScatterPlot
  let selectedPoint = [0, 0];
  let userCoords = null; // Para armazenar os valores digitados

  function getDistance(datum, point) {
    const [latPoint, lngPoint] = point;
    const lat = Number(datum.lat);
    const lng = Number(datum.lng);
    return Math.sqrt((latPoint - lat) ** 2 + (lngPoint - lng) ** 2);
  }

  $: if (educationData.length && selectedPoint) {
    dataWithCost = calculateCosts(educationData).map(d => ({
      ...d,
      distance: getDistance(d, selectedPoint)
    }));
  }

  function salvarCoords() {
    const latNum = parseFloat(latitude);
    const lonNum = parseFloat(longitude);

    if (isNaN(latNum) || isNaN(lonNum)) {
      alert('Digite números válidos para Latitude e Longitude!');
      return;
    }

    userCoords = { lat: latNum, lon: lonNum };
    selectedPoint = [latNum, lonNum]; // atualiza o ponto usado pra distância
  }

  $: dataWithCost = dataWithCost.map(d => ({
    ...d,
    distance: getDistance(d, selectedPoint)
  }));

  // Funcionamento dos Slides
  let currentSlide = 0;

  function next() {
    if (currentSlide < 4) currentSlide += 1;
  }
  function prev() {
    if (currentSlide > 0) currentSlide -= 1;
  }
  function goToSlide(i) {
    currentSlide = i;
  }

  // ONMOUNT
  onMount(() => {
    async function loadData() {
      const data = await fetchEducationData('/education.json');
      educationData = data;
      dataWithCost = calculateCosts(data);
    }

    loadData();

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
      in:fly={{ x: 800, duration: 600 }}
      out:fly={{ x: -800, duration: 600 }}
      style="width: 100%;"
    >
      {#if currentSlide === 0}
        <h2
          in:fly={{ y: -40, duration: 600 }}
          class="title"
        >
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

        <button
          class="button"
          size="long"
          on:click={next}
          aria-label="Avançar para o próximo slide"
          in:scale={{ duration: 400, delay: 600 }}
          on:mouseenter={() => {}}
        >
          <div id="background"></div>
          <div id="text">Próximo →</div>
          <div id="hitbox"></div>
        </button>

      {:else if currentSlide === 1}
        <div class="left-right-container">
          <div class="left">
            <h2
              in:fly={{ y: -40, duration: 600 }}
              class="title"
            >
              Insira sua <strong>localização</strong>
            </h2>
            <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
              Para analisar os custos com base em distância, informe sua <strong>latitude</strong> e <strong>longitude</strong> abaixo.
            </p>

            <form on:submit|preventDefault={salvarCoords} class="coord-form" in:scale={{ duration: 400, delay: 300 }}>
              <label>
                Latitude:
                <input
                  type="text"
                  bind:value={latitude}
                  placeholder="ex: -23.5505"
                  aria-label="Campo para inserir latitude"
                  autocomplete="off"
                />
              </label>
              <label>
                Longitude:
                <input
                  type="text"
                  bind:value={longitude}
                  placeholder="ex: -46.6333"
                  aria-label="Campo para inserir longitude"
                  autocomplete="off"
                />
              </label>
              <button type="submit" class="button-small" aria-label="Salvar coordenadas">
                Salvar
              </button>
            </form>
          </div>

          <div class="right">
            <ScatterPlot data={dataWithCost} />

            <button class="button" size="long" on:click={next} aria-label="Avançar para o próximo slide" in:scale={{ duration: 400, delay: 600 }}>
              <div id="background"></div>
              <div id="text">Próximo →</div>
              <div id="hitbox"></div>
            </button>
          </div>
        </div>

      {:else if currentSlide === 2}
        <div class="left-right-container">
          <div class="left">
            <h2
              in:fly={{ y: -40, duration: 600 }}
              class="title"
            >
              Visualização <strong>BarChart</strong>
            </h2>
            <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
              Gráfico de barras mostrando custos por país e programa para facilitar a comparação.
            </p>
          </div>

          <div class="right">
            {#if educationData.length}
              <BarChart data={educationData} />
            {:else}
              <p>Carregando dados...</p>
            {/if}

            <button class="button" size="long" on:click={next} aria-label="Avançar para o próximo slide" in:scale={{ duration: 400, delay: 600 }}>
              <div id="background"></div>
              <div id="text">Próximo →</div>
              <div id="hitbox"></div>
            </button>
          </div>
        </div>

      {:else if currentSlide === 3}
        <div class="left-right-container">
          <div class="left">
            <h2
              in:fly={{ y: -40, duration: 600 }}
              class="title"
            >
              Visualização <strong>Mapa Mundial</strong>
            </h2>
            <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
              Veja a distribuição geográfica dos custos educacionais em um mapa interativo.
            </p>
          </div>

          <div class="right">
            {#if educationData.length}
              <WorldFun data={educationData} />
            {:else}
              <p>Carregando dados...</p>
            {/if}

            <button class="button" size="long" on:click={next} aria-label="Avançar para o próximo slide" in:scale={{ duration: 400, delay: 600 }}>
              <div id="background"></div>
              <div id="text">Próximo →</div>
              <div id="hitbox"></div>
            </button>
          </div>
        </div>

      {:else if currentSlide === 4}
        <div class="left-right-container">
          <div class="left">
            <h2
              in:fly={{ y: -40, duration: 600 }}
              class="title"
            >
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
                in:fly={{ x: -100, duration: 800, delay: 500 }}
              />
          </div>
        </div>
      {/if}
    </div>
  {/key}
</div>


<footer style="display: flex; justify-content: center; gap: 12px; padding: 1em; background: #f5f5f7;">
  <div id="select" role="tablist" aria-label="Navegação entre slides">
    {#each [
      'Introdução',
      'Custo e Distância',
      'Análise Total',
      'Faculdades pelo Mundo',
      'Conclusão'
    ] as label, i}
      <button
        role="tab"
        aria-selected={currentSlide === i}
        aria-controls={`slide-${i}`}
        id={`tab-${i}`}
        class:selected={currentSlide === i}
        class="dot"
        on:click={() => goToSlide(i)}
        on:keydown={(e) => {
          if (e.key === 'ArrowRight') goToSlide((i + 1) % 5);
          if (e.key === 'ArrowLeft') goToSlide((i + 4) % 5);
        }}
        tabindex={currentSlide === i ? '0' : '-1'}
        title={label}
      >
        <span class="sr-only">Slide {i + 1}</span>
      </button>
    {/each}
  </div>
</footer>

<style>
  .slide {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 80vh;
    text-align: center;
    padding: 20px;
    max-width: 120ch;
    margin-inline: auto;
    user-select: none;
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

  /* Seu CSS para os botões longos na main */
  button.button[size=long] {
    position: relative;
    width: 400px;
    height: 50px;
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
    width: 400px;
    height: 50px;
    opacity: 1;
    pointer-events: none;
    border-radius: 10px;
  }

  button.button[size=long] #text {
    font-family: 'Comic Sans MS', cursive, sans-serif;
    position: relative;
    width: 330px;
    top: 0px;
    margin: 0 auto;
    color: #222;
    font-weight: 700;
    font-size: 1.3rem;
    user-select: none;
    text-shadow: 1px 1px 1px #eee;
  }

  button.button[size=long] #hitbox {
    position: absolute;
    width: 345px;
    height: 50px;
    top: 0;
    left: 27px; 
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
  #select .dot[selected] {
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
  }

  #select .dot:hover:not(.selected) {
    border-color: #2980b9;
    box-shadow: 0 0 6px #2980b9aa;
    transform: scale(1.15);
  }

  /* Tooltip aprimorado para os dots */
  #select .dot[title]:hover::after {
    content: attr(title);
    position: absolute;
    background: #34495e;
    color: #fff;
    padding: 6px 10px;
    font-size: 14px;
    border-radius: 6px;
    top: -38px;
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
    top: -18px;
    left: 50%;
    transform: translateX(-50%);
    pointer-events: none;
    opacity: 1;
    transition: opacity 0.3s ease;
    z-index: 20;
  }

  /* Screen reader only */
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
    height: 100%;
    align-items: start;
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

@media (max-width: 800px) {
  .left-right-container {
    flex-direction: column;
  }
  .left, .right {
    max-width: 100%;
    flex: 1 1 100%;
    text-align: center;
  }
  .left {
    margin-bottom: 1.5rem;
  }
}

.slide-0 {
  background: url('images/background.png') no-repeat center center fixed;
  background-size: cover;
}

</style>
