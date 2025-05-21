<script lang="ts">
  import Test from '$lib/Test.svelte';
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
      Exchange_Rate: +d.Exchange_Rate
    }));
    
    data = parsed;
  });
</script>

<h1 class="text-2xl font-bold mb-4">Boxplot: Custo Total por Nível</h1>

{#if data.length > 0}
  <Test {data} />
{:else}
  <p>Carregando dados...</p>
{/if}
