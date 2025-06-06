<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import * as d3 from 'd3';

  export let data = [];
  export let selected = null;

  const dispatch = createEventDispatcher();

  let container;
  const margin = { top: 20, right: 20, bottom: 70, left: 60 };
  let width, height;
  let colorsHaveBeenDispatched = false; // ADICIONADO: Flag para garantir que o evento dispare apenas uma vez

  function processData(rawData) {
    const counts = d3.rollup(rawData, v => v.length, d => d.Continent);
    return Array.from(counts, ([key, value]) => ({ continent: key, count: value }))
               .sort((a, b) => d3.descending(a.count, b.count));
  }

  function drawChart(chartData) {
    d3.select(container).select('svg').remove();
    const svg = d3.select(container).append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g').attr('transform', `translate(${margin.left}, ${margin.top})`);

    const color = d3.scaleOrdinal(d3.schemeCategory10)
      .domain(chartData.map(d => d.continent));
      
    // ADICIONADO: Criar e despachar o mapa de cores
    if (!colorsHaveBeenDispatched) {
      const colorMap = {};
      chartData.forEach(d => {
        colorMap[d.continent] = color(d.continent);
      });
      dispatch('colorsGenerated', colorMap);
      colorsHaveBeenDispatched = true;
    }

    const x = d3.scaleBand().domain(chartData.map(d => d.continent)).range([0, width]).padding(0.2);
    const y = d3.scaleLinear().domain([0, d3.max(chartData, d => d.count)]).range([height, 0]);

    svg.append('g').attr('transform', `translate(0, ${height})`).call(d3.axisBottom(x))
      .selectAll('text').attr('transform', 'translate(-10,0)rotate(-45)').style('text-anchor', 'end');
    svg.append('g').call(d3.axisLeft(y));

    svg.selectAll('.bar').data(chartData).enter().append('rect')
      .attr('class', 'bar')
      .attr('x', d => x(d.continent))
      .attr('y', d => y(d.count))
      .attr('width', x.bandwidth())
      .attr('height', d => height - y(d.count))
      .attr('fill', d => color(d.continent))
      .style('cursor', 'pointer')
      .style('opacity', d => selected === null || selected === d.continent ? 1 : 0.5)
      .on('click', (event, d) => {
        dispatch('continentSelect', d.continent);
      });

    svg.append('text').attr('text-anchor', 'end').attr('transform', 'rotate(-90)')
      .attr('y', -margin.left + 20).attr('x', -margin.top - height / 2 + 50)
      .text('Nº de Programas');
  }

  $: if (container && data.length) {
    width = container.clientWidth - margin.left - margin.right;
    height = 250 - margin.top - margin.bottom;
    drawChart(processData(data));
  }
  
  $: if(container && data.length) {
    drawChart(processData(data));
  }
</script>

<style>
  .bar:hover { filter: brightness(1.1); }
</style>

<div bind:this={container} style="width: 100%; height: 250px;"></div>