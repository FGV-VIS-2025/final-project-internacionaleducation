<script>
  import { onMount } from 'svelte';
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

  import { fade } from 'svelte/transition';

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
</script>

<div class="slide">
  {#key currentSlide}
    <div
      out:fade={{ duration: 0 }}
      in:fade={{ duration: 500, delay: 500 }}
      style="width: 100%;"
    >
      {#if currentSlide === 0}
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
        




        <button class="button" size="long" on:click={next}>
          <div id="background"></div>
          <div id="text">Próximo →</div>
          <div id="hitbox"></div>
        </button>
      {:else if currentSlide === 1}
        <h2>Slide 2</h2>
        <ScatterPlot data={dataWithCost}/>





        <button class="button" size="long" on:click={next}>
          <div id="background"></div>
          <div id="text">Próximo →</div>
          <div id="hitbox"></div>
        </button>
      {:else if currentSlide === 2}
        <h2>BarChart</h2>
        {#if educationData.length}
          <BarChart data={educationData} />
        {:else}
          <p>Carregando dados...</p>
        {/if}
      


        <button class="button" size="long" on:click={next}>
          <div id="background"></div>
          <div id="text">Próximo →</div>
          <div id="hitbox"></div>
        </button>
      {:else if currentSlide === 3}
        <h2>Mapa</h2>
        {#if educationData.length}
          <!-- Passa os dados transformados para WorldFun -->
          <WorldFun data={educationData} />
        {:else}
          <p>Carregando dados...</p>
        {/if}


        <button class="button" size="long" on:click={next}>
          <div id="background"></div>
          <div id="text">Próximo →</div>
          <div id="hitbox"></div>
        </button>
      {:else if currentSlide === 4}
        <h2>Slide 5</h2>
        <p>Último slide, sem botão pra avançar.</p>
      {/if}
    </div>
  {/key}
</div>

<footer style="display: flex; justify-content: center; gap: 10px; padding: 1em; background: #eee;">
  <div id="select">
    <div class="dot" data-balloon="0. Introdução" data-balloon-pos="up" on:click={() => goToSlide(0)} class:selected={currentSlide === 0}></div>
    <div class="dot" data-balloon="1. Coldplay" data-balloon-pos="up" on:click={() => goToSlide(1)} class:selected={currentSlide === 1}></div>
    <div class="dot" data-balloon="2. Cinivius" data-balloon-pos="up" on:click={() => goToSlide(2)} class:selected={currentSlide === 2}></div>
    <div class="dot" data-balloon="3. ss" data-balloon-pos="up" on:click={() => goToSlide(3)} class:selected={currentSlide === 3}></div>
    <div class="dot" data-balloon="4. lol" data-balloon-pos="up" on:click={() => goToSlide(4)} class:selected={currentSlide === 4}></div>
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
    max-width: 100ch; 
    margin-inline: auto; 
  }

  footer {
    height: 7vh;
    padding: 1em;
    background: #eee;
    display: flex;
    justify-content: center;
    gap: 10px;
    align-items: center;
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
  }

  .button:hover {
    z-index: 100;
    transform: scale(1.02, 1.02);
  }

  button.button[size=long] #text {
    font-family: 'Comic Sans MS';
    position: relative;
    width: 330px;
    top: 0px;
    margin: 0 auto;
    color: #000;
    font-weight: bold;
    font-size: 1.2rem;
    user-select: none;
  }

  button.button[size=long] #hitbox {
    position: absolute;
    width: 345px;
    height: 50px;
    top: 0;
    left: 27px; 
    pointer-events: auto;
  }

  #select {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
  }

  #select .dot[selected],
  #select .dot.selected {
    background: #3d3d50;
  }

  #select .dot {
    width: 30px;
    height: 30px;
    border-radius: 40px;
    border: 1px solid #000000;
    display: inline-block;
    margin: 0 5px;
    cursor: pointer;
    background: transparent;
  }

  [data-balloon] {
    position: relative;
    cursor: pointer;
  }

  [data-balloon]:before,
  [data-balloon]:after {
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translate(-50%, 10px);
    transform-origin: top;
    opacity: 0;
    pointer-events: none;
    transition: all 0.1s ease-out 0.1s;
    z-index: 10;
  }

  [data-balloon]:after {
    content: attr(data-balloon);
    background: rgba(17, 17, 17, 0.9);
    color: #fff;
    padding: 0.5em 1em;
    font-size: 18px;
    white-space: nowrap;
    border-radius: 4px;
    margin-bottom: 26px;
  }

  [data-balloon]:before {
    content: "";
    border: 6px solid transparent;
    border-top-color: rgba(17, 17, 17, 0.9);
    margin-bottom: 20px;
  }

  [data-balloon]:hover:before,
  [data-balloon]:hover:after {
    opacity: 1;
    transform: translate(-50%, 0);
    pointer-events: auto;
  }
</style>
