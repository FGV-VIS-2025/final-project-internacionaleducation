<script lang="ts">
  import Boxplot from '$lib/Boxplot.svelte';
  import WorldMap from '$lib/WorldMap.svelte';
  import ScatterPlot from '$lib/ScatterPlot.svelte';
  import BarChart from '$lib/BarChart.svelte';
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  let data = [];

  onMount(async () => {
    const response = await fetch('/education.csv');
    const text = await response.text();
    const parsed = d3.csvParse(text, d => ({
      Country: d.Country,
      City: d.City,
      University: d.University,
      Program: d.Program,
      Level: d.Level,
      Duration_Years: +d.Duration_Years,
      Tuition_USD: +d.Tuition_USD,
      Living_Cost_Index: +d.Living_Cost_Index,
      Rent_USD: +d.Rent_USD,
      Visa_Fee_USD: +d.Visa_Fee_USD,
      Insurance_USD: +d.Insurance_USD,
      Exchange_Rate: +d.Exchange_Rate
    }));
    
    data = parsed;
  });
</script>

<div class="container mx-auto px-4 py-8 space-y-12">
  <h1 class="text-4xl font-bold text-center mb-8">🌍 Educação pelo Mundo</h1>
  <p class="text-center text-lg mb-12">
    Explore os custos de estudar em diferentes países e programas acadêmicos.
    Compare taxas, custo de vida e veja insights visuais!
  </p>

  {#if data.length > 0}
    <section>
      <h2 class="text-2xl font-semibold mb-4">Boxplot: Custo Total por Nível</h2>
      <Boxplot {data} />
      <p class="text-sm text-gray-500 mt-2">
        Análise das diferenças de custo total considerando mensalidades, aluguel e taxas.
      </p>
    </section>

    <section>
      <h2 class="text-2xl font-semibold mb-4">Distribuição Global: Onde Estudar?</h2>
      <WorldMap {data} />
      <p class="text-sm text-gray-500 mt-2">
        Veja a distribuição geográfica das universidades no mundo.
      </p>
    </section>

    <section>
      <h2 class="text-2xl font-semibold mb-4">Relação entre Custo de Vida e Mensalidade</h2>
      <ScatterPlot {data} />
      <p class="text-sm text-gray-500 mt-2">
        Relação entre custo de vida no país e as mensalidades cobradas.
      </p>
    </section>

    <section>
      <h2 class="text-2xl font-semibold mb-4">Top 10 Programas Mais Caros</h2>
      <BarChart {data} />
      <p class="text-sm text-gray-500 mt-2">
        Ranking dos programas mais caros considerando todas as taxas.
      </p>
    </section>
  {:else}
    <p class="text-center text-gray-600">Carregando dados...</p>
  {/if}
</div>
