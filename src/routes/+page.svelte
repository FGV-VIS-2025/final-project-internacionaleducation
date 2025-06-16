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
  import PyramidScatter from '../lib/PyramidScatter.svelte';

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

  let selectedCountries = [];

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
        Category: d.course_category,
        Level: d.Level,
        Rank: d.world_rank,
        lat: d.lat,
        lng: d.lng,
        total_cost
      };
    });
  }

  function getDistance(datum, point) {
    const R = 6371; // raio médio da Terra em km
    const toRad = deg => deg * Math.PI / 180;

    const lat1 = toRad(Number(datum.lat));
    const lon1 = toRad(Number(datum.lng));
    const [lat2, lon2] = point.map(toRad);

    const dLat = lat2 - lat1;
    const dLon = lon2 - lon1;

    const a = Math.sin(dLat / 2) ** 2
            + Math.cos(lat1) * Math.cos(lat2)
            * Math.sin(dLon / 2) ** 2;
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return R * c; // distância em km
  }

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

  $: countries = Array.from(new Set(
    educationData
      .filter(d =>
        (!selectedProgram || d.course_category === selectedProgram) &&
        (!selectedLevel   || d.Level === selectedLevel)
      )
      .map(d => d.Country)
  )).sort();

  $: programs = Array.from(new Set(
    educationData
      .filter(d =>
        (!selectedCountry || d.Country === selectedCountry) &&
        (!selectedLevel   || d.Level === selectedLevel)
      )
      .map(d => d.course_category)
  )).sort();

  $: filteredEducation = educationData.filter(d =>
    (!selectedCountry  || d.Country === selectedCountry) &&
    (!selectedProgram  || d.course_category === selectedProgram) &&
    (!selectedLevel    || d.Level === selectedLevel)
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
    if (currentSlide < 13) {
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

  let userResponse = ''; // Variável para armazenar a resposta do usuário
  
  // Função que altera a resposta do usuário e avança o slide
  function handleUserResponse(response) {
    userResponse = response;
    // Avança para o próximo slide
    next();
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
              Para analisar as faculdades de alto padrão mais próximas de você, <strong>clique no mapa</strong> abaixo
              e analise a sua proximidade!
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
            <label for="level-select" class="slide-text" style="margin-bottom: 10px;">Filtrar por nível de curso:</label>
            <select id="level-select" bind:value={selectedLevel} in:scale={{ duration: 400, delay: 300 }}>
              <option value="">Todos</option>
              <option value="Bachelor">Bacharel</option>
              <option value="Master">Mestrado</option>
              <option value="PhD">PhD</option>
            </select>

            <label for="country-select" class="slide-text" style="margin-bottom: 10px;">Filtrar por país:</label>
            <select id="country-select" bind:value={selectedCountry} in:scale={{ duration: 400, delay: 300 }}>
              <option value="">Todos</option>
              {#each countries as country}
                <option value={country}>{country}</option>
              {/each}
            </select>

            <label for="program-select" class="slide-text" style="margin-bottom: 10px;">Filtrar por curso:</label>
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
        <h2 in:fly={{ y: -40, duration: 600 }} class="title">
          Estudar nos EUA... <strong>Como pagar!?</strong>
        </h2>
        <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
          Observando os gráficos anteriores, podemos ver uma disparidade de custo
          nas universidades estadounidenses até em relação a grandes faculdades 
          europeias e asiáticas. Comparando o custo médio total:
        </p>
        <div class="stats-grid" in:scale={{ duration: 500, delay: 400 }}>
          <div class="stat-box">
            <div class="stat-number">~120k USD</div>
            <div class="stat-label">Estados Unidos</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">~65k USD</div>
            <div class="stat-label">Europa</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">~26k USD</div>
            <div class="stat-label">China/Japão/Coréia</div>
          </div>
        </div>
        <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
          Olhando para os dados, é claro que estudar nos EUA demanda um <strong>poder financeiro</strong>
          muito maior. Porém, será que esse preço todo vale a pena? Será que a educação é
          de <strong>maior qualidade</strong>?
        </p>

      {:else if currentSlide === 6}
        <h2 in:fly={{ y: -40, duration: 600 }} class="title">
              Ranking Mundial de Universidades
            </h2>
            <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
              O ranking mundial de universidades é uma lista que leva em conta <strong>diversos parâmetros</strong> 
              que ajudam a determinar a posição das instituições de ensino no cenário global, como:
            </p>
            
            <div class="stats-carousel" in:scale={{ duration: 500, delay: 400 }}>
              {#each [
                { title: 'Quality of Education', desc: 'Qualidade do Ensino' },
                { title: 'Alumni Employment', desc: 'Empregabilidade' },
                { title: 'Quality of Faculty', desc: 'Qualidade do Corpo Docente' },
                { title: 'Publications', desc: 'Publicações' },
                { title: 'Citations', desc: 'Citações' }
              ] as item}
                <div class="stat-item">
                  <div class="stat-title">{item.title}</div>
                  <div class="stat-desc">{item.desc}</div>
                </div>
              {/each}
            </div>

            <p class="slide-text" in:fly={{ y: 20, delay: 400, duration: 600 }}>
              A partir disso, podemos definir quais universidades mais se destacam globalmente e/ou 
              possuem os <strong>melhores pesquisadores</strong>. Ela é uma análise interessante a se adicionar, principalmente
              para a análise do próximo slide. Será que as universidades norte americanas <strong>"se pagam?"</strong>
            </p>

            <div class="button-container">
              <button class="button" size="long" on:click={() => handleUserResponse('yes')} in:scale={{ duration: 400, delay: 600 }}>
                <div id="background"></div>
                <div id="text">Sim, são as melhores.</div>
                <div id="hitbox"></div>
              </button>

              <button class="button" size="long" on:click={() => handleUserResponse('no')} in:scale={{ duration: 400, delay: 600 }}>
                <div id="background"></div>
                <div id="text">Não, são caras demais!</div>
                <div id="hitbox"></div>
              </button>
            </div>

      {:else if currentSlide === 7}
        <h2 in:fly={{ y: -40, duration: 600 }} class="title">
          Dados não <strong>Mentem</strong>
        </h2>
        {#if userResponse === 'yes'}
          <p class="slide-text" style="margin-bottom: 10px;" in:fly={{ y: 20, delay: 200, duration: 600 }}>
            Sim! As melhores e mais prestigiosas faculdades do mundo, de fato, estão nos Estados Unidos. O preço pode valer a pena pela qualidade!
          </p>
        {:else}
          <p class="slide-text" style="margin-bottom: 10px;" in:fly={{ y: 20, delay: 200, duration: 600 }}>
            Não é bem assim! O custo é mais alto, mas a qualidade de ensino e infraestrutura de algumas universidades podem justificar seu preço.
          </p>
        {/if}
          {#if educationData.length}
            <PyramidScatter data={dataWithCost} />
          {:else}
            <p>Carregando dados...</p>
          {/if}
        {#if userResponse === 'yes'}
          <p class="slide-text" style="margin-bottom: 10px;" in:fly={{ y: 20, delay: 200, duration: 600 }}>
            Como sua intuição falou, podemos ver que, principalmente no top 20, a maioria é americana, mostrando que pode ser
            um bom caminho para pesquisadores com ambição.
          </p>
        {:else}
          <p class="slide-text" style="margin-bottom: 10px;" in:fly={{ y: 20, delay: 200, duration: 600 }}>
            Mesmo que você possa duvidar, a maioria das universidades no top 20 global é americana (ainda que, sim, sejam custosas)
          </p>
        {/if}

      {:else if currentSlide === 8}
        <div class="left-right-container">
          <div class="left">
            <h2 in:fly={{ y: -40, duration: 600 }} class="title">
              Análise Geral <strong>de Todas as Universidades</strong>
            </h2>
            <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
              Agora que você já explorou o custo educacional ao redor do mundo no mapa anterior e pôde observar, 
              de forma geral, as universidades mais prestigiosas globalmente e sua localização, sinta-se mais livre
              com o próximo mapa. Nele, você pode olhar cada instituição em específico, útil para uma análise mais
              individual!
            </p>
          </div>
          <div class="right">
            <p class="slide-text interactive" in:fly={{ y: 20, delay: 600, duration: 600 }}>
              <strong>O mapa interativo a seguir</strong> mostra de forma clara e objetiva a distribuição global dos custos educacionais.
              Clique, explore e descubra: como a sua cidade ou país se compara com o resto do mundo?
            </p>

            <img
              src="images/lupa.png"
              alt="Lupa cartoon"
              class="illustration-below"
              in:fly={{ x: 100, duration: 800, delay: 500 }}
            />
          </div>
        </div>


      {:else if currentSlide === 9}
        <div class="title">
            <h2 in:fly={{ y: -40, duration: 600 }} style="margin-bottom: 10px;" class="title">
              <strong>Mapa Mundial</strong> de Universidades
            </h2>
            <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
              Veja a distribuição geográfica dos custos educacionais em um mapa interativo.
            </p>
            <p style="margin-bottom: 10px;" >Legenda: Diamante = top 10, Ouro = top 50, Prata = top 300 e Bornze = top 1000 ou Sem rank </p>
            <div class = "mapaInterativo">
              {#if educationData.length}
                <WorldFun2 data={educationData} bind:selectedCountries/>
              {:else}
                <p>Carregando dados...</p>
              {/if}
            </div>
        </div>

      {:else if currentSlide === 10}
        <div class="left-right-container">
          <div class="left">
            <h2 in:fly={{ y: -40, duration: 600 }} class="title">
              Análise por Espaço: <strong>Continente & Custo</strong>
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

      {:else if currentSlide === 11}
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

      {:else if currentSlide === 12}
        <div class="references">
          <h2 in:fly={{ y: -40, duration: 600 }} class="title">Referências</h2>
          <ol>
            <li>[1] Shamim, A. (2024). Cost of International Education [Data set]. Kaggle.</li>
            <li>[2] O’Neill, M. (2020). World University Rankings [Data set]. Kaggle.</li>
          </ol>
        </div>
          <p class="slide-text" in:fly={{ y: 20, delay: 200, duration: 600 }}>
            Abaixo estão disponíveis os <strong>dados utilizados</strong> para o construção dos gráficos desse site em formato json. Qualquer dúvida ou sugestão entrar em contato com:
          </p>
          <div class="emails">
            <h3>Contatos</h3>
            <ul>
              <li><a href="mailto:jogabriel433@gmail.com">jogabriel433@gmail.com</a></li>
              <li><a href="mailto:gu.bianchi.s@gmail.com">gu.bianchi.s@gmail.com</a></li>
              <li><a href="mailto:vinicius.nascimento05@hotmail.com">vinicius.nascimento05@hotmail.com</a></li>
            </ul>
          </div>
          <a class="download-btn" href="./education.json" download>
            📥 Baixar Dados
          </a>
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
            {#each Array(13) as _, i}
                <button
                    role="tab"
                    aria-selected={currentSlide === i}
                    aria-controls={`slide-${i}`}
                    id={`tab-${i}`}
                    class:selected={currentSlide === i}
                    class="dot"
                    on:click={() => goToSlide(i)}
                    on:keydown={(e) => {
                        const totalSlides = 12;
                        if (e.key === 'ArrowRight') goToSlide((i + 1) % totalSlides);
                        if (e.key === 'ArrowLeft') goToSlide((i - 1 + totalSlides) % totalSlides);
                    }}
                    tabindex={currentSlide === i ? '0' : '-1'}
                    title={`Slide ${i}: ${[
                        'Introdução', 'Base de Dados', 'Custo e Distância', '"Get the Money!"',
                        'Comparação Geral', 'Desigualdade...?', 'Ranking de Faculdades',  'Na verdade...',
                        'Análise Geral', 'Faculdades pelo Mundo', 'Por Continente', 'Conclusão', "Referências"
                    ][i]}`}
                >
                    <span class="sr-only">Slide {i + 1}</span>
                </button>
            {/each}
        </div>
    </footer>

    <div class="nav-button-wrapper">
        {#if currentSlide < 12}
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

  .slide-text #level-select {
    margin-bottom: 10px;
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
    flex: 1 1 40%; /* Permite encolher/crescer mantendo a proporção de 40% */
    min-width: 0; /* Evita que o conteúdo force o container a crescer */
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .right {
    flex: 1 1 60%; /* Permite encolher/crescer mantendo a proporção de 60% */
    min-width: 0; /* Garante que o gráfico possa encolher se necessário */
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

.stats-carousel {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding: 1rem 0;
}

.stat-item {
  flex: 0 0 auto;
  background: #fff;
  padding: 0.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  min-width: 180px;
  text-align: center;
}

.stat-title {
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.stat-desc {
  font-size: 0.85rem;
  color: #555;
}

.highlight {
  font-weight: 700;
  color: #007bff;
}

.interactive {
  font-size: 1.1rem;
  font-weight: 600;
  color: #555;
}

.interactive:hover {
  color: #007bff;
  cursor: pointer;
  transition: color 0.3s ease;
}

.references {
  text-align: center;
}
.references h2 {
  font-size: 3rem;
  margin-bottom: 0.8rem;
  color: #333;
}
.references ol {
  list-style-position: inside;
  display: inline-block;
  text-align: left;
  margin-bottom: 1.2rem;
}
.references ol li {
  margin: 0.2rem 0;
  font-size: 1.2rem;
  color: #555;
}

/* estilo para a seção de e-mails */
.emails {
  margin-bottom: 0.4rem;
}
.emails h3 {
  font-size: 1.6rem;
  margin-bottom: 0.4rem;
  color: #333;
}
.emails ul {
  list-style: none;
  padding: 0;
  display: inline-flex;
  gap: 1.2rem;
}
.emails ul li a {
  color: #007acc;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}
.emails ul li a:hover {
  color: #005fa3;
}

/* botão estiloso */
.download-btn {
  display: inline-block;
  background: linear-gradient(135deg, #6b73ff 0%, #000dff 100%);
  color: #fff;
  padding: 0.6rem 1.4rem;
  border-radius: 30px;
  text-decoration: none;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(0, 13, 255, 0.3);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.download-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(0, 13, 255, 0.4);
}

</style>