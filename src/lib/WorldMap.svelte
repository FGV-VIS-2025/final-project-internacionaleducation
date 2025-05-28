<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  let container;
  let width, height;

  onMount(async () => {
    const geoData = await (await fetch('/countries.geojson')).json();
    const costData = await (await fetch('/education.json')).json();

    const costByCountry = {};
    costData.forEach(d => {
      costByCountry[d.Country.toLowerCase()] = +d.Total_Cost_USD;
    });

    const values = Object.values(costByCountry);
    const colorScale = d3.scaleQuantize()
      .domain([d3.min(values), d3.max(values)])
      .range(d3.schemeBlues[7]);

    const svg = d3.select(container)
      .append('svg')
      .attr('width', '100%')
      .attr('height', '100%')
      .attr('viewBox', '0 0 960 500') // escala adaptável
      .style('border-radius', '12px');

    const projection = d3.geoNaturalEarth1().scale(160).translate([480, 250]);
    const path = d3.geoPath().projection(projection);

    svg.append('g')
      .selectAll('path')
      .data(geoData.features)
      .join('path')
      .attr('d', path)
      .attr('fill', d => {
        const name = d.properties.name.toLowerCase();
        const value = costByCountry[name];
        return value ? colorScale(value) : '#ccc';
      })
      .attr('stroke', '#fff')
      .attr('stroke-width', 0.5)
      .on('mouseover', function (event, d) {
        d3.select(this)
          .attr('stroke', '#000')
          .attr('stroke-width', 1.5);
      })
      .on('mouseout', function () {
        d3.select(this)
          .attr('stroke', '#fff')
          .attr('stroke-width', 0.5);
      })
      .append('title')
      .text(d => {
        const name = d.properties.name;
        const value = costByCountry[name.toLowerCase()];
        return `${name}\nCusto total: ${value ? `$${value.toLocaleString()}` : 'N/A'}`;
      });
  });
</script>

<style>
  .map-container {
    width: 100%;
    height: 100vh;
  }

  svg {
    display: block;
  }
</style>

<div bind:this={container} class="map-container"></div>
