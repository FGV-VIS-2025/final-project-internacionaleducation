<script>
  import { onMount } from 'svelte';
  import BarChart from '../lib/BarChart.svelte';
  import Boxplot from  '../lib/Boxplot.svelte';
  import ScatterPlot from  '../lib/ScatterPlot.svelte';
  import ScatterFun from  '../lib/ScatterFun.svelte';
  import WorldMap from  '../lib/WorldMap.svelte';
  import WorldFun from  '../lib/WorldFun.svelte';

  let activeStep = 0;
  let educationData = [];
  let bachelorDataWithCost = [];

  // Função para buscar dados do JSON
  async function fetchEducationData(url) {
    const res = await fetch(url);
    const data = await res.json();
    return data;
  }

  // Função para calcular custo total filtrando bacharelados
  function calculateBachelorCosts(data) {
    return data
      .filter(d => d.Level === "Bacharel")
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
          total_cost
        };
      });
  }

  $: showLine = activeStep !== 1;

  onMount(() => {
    async function loadData() {
      const data = await fetchEducationData('/education.json');
      educationData = data;
      bachelorDataWithCost = calculateBachelorCosts(data);
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

{#if showLine}
  <div class="vertical-line"></div>
{/if}

<!------------------------------------------------ Step 0 -------------------------------------------------------->
<div class="container">
  <div
    class="left scroll-step {activeStep >= 0 ? 'visible' : 'hidden'}"
    data-index="0"
  >
    <h1 class="title">
      <span class="line1">Explorando</span>
      <span class="line2">os Custos</span>
      <span class="line3">da Educação</span>
    </h1>
  </div>

  <div
    class="right scroll-step {activeStep >= 0 ? 'visible' : 'hidden'}"
    data-index="0"
  >
    <h2>Como os custos afetam a educação global?</h2>
    <p>
      O objetivo deste projeto é explorar como as variações nos custos de educação impactam estudantes ao redor do mundo.
      Utilizamos visualizações interativas baseadas em dados reais para oferecer insights sobre tendências econômicas,
      desigualdades e oportunidades.
    </p>

    <p class="emphasized">
      Continue explorando para visualizar os dados e gráficos; se já estiver familiarizado com o projeto, acesse diretamente a visualização!
    </p>

    <img src="images/educacao.png" alt="Educação" class="illustration-below" />
  </div>
</div>


<!------------------------------------------------ Step 1 -------------------------------------------------------->
<div class="container full-width scroll-step {activeStep >= 1 ? 'visible' : 'hidden'}" data-index="1">
  <div class="full-map-section">
    <h2>Mapa Global: Custo da Educação</h2>
    <p class="map-description">
      Explore visualmente como os custos de educação variam entre os países.
    </p>
    
    <WorldMap data={educationData} />
  </div>
</div>
<!------------------------------------------------ Step 2 -------------------------------------------------------->
<div class="container">
  <div
    class="left scroll-step {activeStep >= 2 ? 'visible' : 'hidden'}"
    data-index="2"
  >
    <h1 class="title">
      <span class="line1">Gráfico em Mapa:</span>
      <span class="line2">Comparando os Países</span>
      <p>
        Lorem ipsum dolor sit amet. Aut nihil inventore rem magni voluptatem ut iste nesciunt cum dolorem praesentium qui porro
        dolor ea magni illum. Sit eveniet voluptas ut eligendi tempora aut nesciunt harum.
        Sed blanditiis voluptates et blanditiis culpa ad eveniet excepturi ea Quis voluptatem ex consequatur quia. Eum officia
        mollitia et quam explicabo in quia unde sed ipsam harum et earum explicabo. Ut dolor commodi in cumque impedit ab libero
        porro et perspiciatis molestiae.
        Sit unde tempore ex dicta magnam in temporibus dignissimos. Sit iure optio aut repellat pariatur et fuga itaque eum ullam
        earum hic nemo iste. Et quia dolore sit quasi eligendi nam deserunt illum eum iure tenetur. Ut totam ratione est quae
        voluptates et quae animi.
      </p>
    </h1>
  </div>

  <div
    class="right scroll-step {activeStep >= 2 ? 'visible' : 'hidden'}"
    data-index="2"
  >
    <h2>Resultados</h2>

    {#if educationData.length}
      <!-- Passa os dados transformados para WorldFun -->
      <WorldFun data={educationData} />
    {:else}
      <p>Carregando dados...</p>
    {/if}

    <p class="emphasized">LOL</p>
  </div>
</div>

<!------------------------------------------------ Step 3 -------------------------------------------------------->
<div class="container">
  <div
    class="left scroll-step {activeStep >= 3 ? 'visible' : 'hidden'}"
    data-index="3"
  >
    <h1 class="title">
      <span class="line1">Gráfico 3:</span>
      <span class="line2">Comparando</span>
      <p>
        Lorem ipsum dolor sit amet. Aut nihil inventore rem magni voluptatem ut iste nesciunt cum dolorem praesentium qui porro
        dolor ea magni illum. Sit eveniet voluptas ut eligendi tempora aut nesciunt harum.
        Sed blanditiis voluptates et blanditiis culpa ad eveniet excepturi ea Quis voluptatem ex consequatur quia. Eum officia
        mollitia et quam explicabo in quia unde sed ipsam harum et earum explicabo. Ut dolor commodi in cumque impedit ab libero
        porro et perspiciatis molestiae.
        Sit unde tempore ex dicta magnam in temporibus dignissimos. Sit iure optio aut repellat pariatur et fuga itaque eum ullam
        earum hic nemo iste. Et quia dolore sit quasi eligendi nam deserunt illum eum iure tenetur. Ut totam ratione est quae
        voluptates et quae animi.
      </p>
    </h1>
  </div>

  <div
    class="right scroll-step {activeStep >= 3 ? 'visible' : 'hidden'}"
    data-index="3"
  >
    <h2>Resultados</h2>
    <p>GRÁFICO!</p>

    <p class="emphasized">LOL</p>

    <ScatterPlot data={educationData}/>

  </div>
</div>

<!------------------------------------------------ Step 4 -------------------------------------------------------->
<div class="container">
  <div
    class="left scroll-step {activeStep >= 4 ? 'visible' : 'hidden'}"
    data-index="4"
  >
    <h1 class="title">
      <span class="line1">Gráfico em Mapa:</span>
      <span class="line2">Comparando os Países</span>
      <p>
        Lorem ipsum dolor sit amet. Aut nihil inventore rem magni voluptatem ut iste nesciunt cum dolorem praesentium qui porro
        dolor ea magni illum. Sit eveniet voluptas ut eligendi tempora aut nesciunt harum.
        Sed blanditiis voluptates et blanditiis culpa ad eveniet excepturi ea Quis voluptatem ex consequatur quia. Eum officia
        mollitia et quam explicabo in quia unde sed ipsam harum et earum explicabo. Ut dolor commodi in cumque impedit ab libero
        porro et perspiciatis molestiae.
        Sit unde tempore ex dicta magnam in temporibus dignissimos. Sit iure optio aut repellat pariatur et fuga itaque eum ullam
        earum hic nemo iste. Et quia dolore sit quasi eligendi nam deserunt illum eum iure tenetur. Ut totam ratione est quae
        voluptates et quae animi.
      </p>
    </h1>
  </div>

  <div
    class="right scroll-step {activeStep >= 4 ? 'visible' : 'hidden'}"
    data-index="4"
  >
    <h2>Resultados</h2>
    <p>GRÁFICO!</p>

    {#if educationData.length}
      <BarChart data={educationData} />
    {:else}
      <p>Carregando dados...</p>
    {/if}

    <p class="emphasized">LOL</p>

  </div>
</div>

<style>
  body {
    font-family: 'Segoe UI', sans-serif;
    background-color: #f9f9fb;
    color: #333;
    margin: 0;
    padding: 0;
  }

  .container {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    min-height: 100vh;
    padding: 4rem 6%;
    gap: 2rem;
    border-bottom: 1px solid #ddd;
  }

  .left, .right {
    flex: 1;
    max-width: 40%;
  }

  .title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 1rem;
    line-height: 1.3;
    animation: fadeInUp 0.8s ease-out both;
  }

  .title .line1, .title .line2, .title .line3 {
    display: block;
  }

  h2 {
    font-size: 1.6rem;
    margin-bottom: 1rem;
    animation: fadeIn 0.6s ease-out both;
  }

  p {
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 1rem;
  }

  .emphasized {
    font-weight: bold;
    font-style: italic;
    color: #555;
    margin-top: 1.5rem;
  }

  .illustration-below {
    width: 100%;
    max-width: 100%;
  }

  .scroll-step {
    opacity: 0.2;
    transition: opacity 0.8s ease, transform 0.8s ease;
    transform: translateY(20px);
  }

  .scroll-step.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .vertical-line {
    position: fixed;
    top: 0;
    left: 45%;
    width: 4px;
    height: 100vh;
    background: linear-gradient(to bottom, #ccc, transparent);
    z-index: -1;
  }

  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  .full-width {
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem 0;
  }

  .full-map-section {
    width: 100%;
    max-width: 100%;
    padding: 0 2rem;
    text-align: center;
  }

  .full-map-section h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  .map-description {
    font-size: 1rem;
    color: #555;
    margin-bottom: 2rem;
  }

  .full-map-section :global(svg),
  .full-map-section :global(canvas),
  .full-map-section :global(div) {
    width: 100% !important;
    max-width: 100% !important;
    height: 80vh;
  }
</style>
