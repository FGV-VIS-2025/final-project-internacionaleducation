<script lang="ts">
  import Boxplot from '$lib/Boxplot.svelte';
  import WorldMap from '$lib/WorldMap.svelte';
  import ScatterPlot from '$lib/ScatterPlot.svelte';
  import BarChart from '$lib/BarChart.svelte';

  import * as d3 from 'd3';
  import { onMount } from 'svelte';

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
      Exchange_Rate: +d.Exchange_Rate,
      lat: +d.lat,
      lng: +d.lng
    }));

    data = parsed;
  });
</script>

{#if data.length > 0}
  <div class="flex flex-col">

    <!-- Boxplot Section -->
    <section class="h-screen flex items-center justify-center bg-gradient-to-br from-green-100 to-green-300">
      <div class="w-full max-w-6xl">
        <h1 class="text-4xl font-bold mb-6 text-center">
          Boxplot: Custo Total por Nível
        </h1>
        <Boxplot {data} />
      </div>
    </section>

    <!-- World Map Section -->
    <section class="h-screen flex items-center justify-center bg-gradient-to-br from-blue-100 to-blue-300">
      <div class="w-full max-w-6xl">
        <h1 class="text-4xl font-bold mb-6 text-center">
          Mapa Mundial: Localização das Universidades
        </h1>
        <WorldMap {data} />
      </div>
    </section>

    <!-- Scatter Plot Section -->
    <section class="h-screen flex items-center justify-center bg-gradient-to-br from-purple-100 to-purple-300">
      <div class="w-full max-w-6xl">
        <h1 class="text-4xl font-bold mb-6 text-center">
          Relação: Custo de Vida x Anuidade
        </h1>
        <ScatterPlot {data} />
      </div>
    </section>

    <!-- Bar Chart Section -->
    <section class="h-screen flex items-center justify-center bg-gradient-to-br from-yellow-100 to-yellow-300">
      <div class="w-full max-w-6xl">
        <h1 class="text-4xl font-bold mb-6 text-center">
          Top 10 Programas Mais Caros
        </h1>
        <BarChart {data} />
      </div>
    </section>

  </div>
{:else}
  <div class="h-screen flex items-center justify-center">
    <p class="text-xl">Carregando dados...</p>
  </div>
{/if}
