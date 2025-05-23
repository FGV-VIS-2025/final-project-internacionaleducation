<script>
  import { onMount } from 'svelte';
  import BarChart from '../lib/BarChart.svelte';
  import Boxplot from  '../lib/Boxplot.svelte';
  import ScatterPlot from  '../lib/ScatterPlot.svelte';
  import WorldMap from  '../lib/WorldMap.svelte';

  let activeStep = 0;

  let educationData = [];

  onMount(() => {
    // carregar dados async
    (async () => {
      const res = await fetch('/education.json');
      educationData = await res.json();
    })();

    // configurar observer
    const steps = document.querySelectorAll('.scroll-step');
    const observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const index = +entry.target.dataset.index;
            if (index > activeStep) {
              activeStep = index;
            }
          }
        });
      },
      { threshold: 0.5 }
    );

    steps.forEach(step => observer.observe(step));

    return () => observer.disconnect();
  });
</script>

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
<div class="container">
  <div
    class="left scroll-step {activeStep >= 1 ? 'visible' : 'hidden'}"
    data-index="1"
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
    class="right scroll-step {activeStep >= 1 ? 'visible' : 'hidden'}"
    data-index="1"
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

<!------------------------------------------------ Step 2 -------------------------------------------------------->
<div class="container">
  <div
    class="left scroll-step {activeStep >= 2 ? 'visible' : 'hidden'}"
    data-index="2"
  >
    <h1 class="title">
      <span class="line1">Gráfico 2:</span>
      <span class="line2">Bertinho</span>
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
    <p>GRÁFICO!</p>

    <Boxplot data={educationData}/>

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
      <span class="line1">Gráfico 4:</span>
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
    class="right scroll-step {activeStep >= 4 ? 'visible' : 'hidden'}"
    data-index="4"
  >
    <h2>Resultados</h2>
    <p>GRÁFICO!</p>

    <p class="emphasized">LOL</p>

    <WorldMap data={educationData}/>

  </div>
</div>

<style>
  .scroll-step {
    min-height: 100vh; /* espaço para scroll */
    padding: 2rem;
    box-sizing: border-box;
  }

  .hidden {
    opacity: 0.2;
    transition: opacity 0.5s ease;
  }

  .visible {
    opacity: 1;
    transition: opacity 0.5s ease;
  }
</style>