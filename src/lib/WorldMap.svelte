<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  let container;
  let width, height;

  onMount(async () => {
    const geoData = await (await fetch('/countries.geojson')).json();
    const costData = await (await fetch('/education.json')).json();

    const countryCosts = {};

    costData.forEach(d => {
      const duration = +d.Duration_Years || 0;
      const tuition = +d.Tuition_USD || 0;
      const rent = (+d.Rent_USD || 0) * 12 * duration;
      const visa = +d.Visa_Fee_USD || 0;
      const insurance = +d.Insurance_USD || 0;
      const totalCost = tuition + rent + visa + insurance;

      const country = d.Country.toLowerCase();

      if (!countryCosts[country]) {
        countryCosts[country] = [];
      }
      countryCosts[country].push(totalCost);
    });

    // calcular média por país
    const avgCostByCountry = {};
    for (const [country, costs] of Object.entries(countryCosts)) {
      avgCostByCountry[country] = d3.mean(costs);
    }

    const values = Object.values(avgCostByCountry);
    const colorScale = d3.scaleQuantize()
      .domain([d3.min(values), d3.max(values)])
      .range(d3.schemeBlues[7]);

    const svg = d3.select(container)
      .append('svg')
      .attr('width', '100%')
      .attr('height', '100%')
      .attr('viewBox', '0 0 960 500')
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
        const value = avgCostByCountry[name];
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
        const value = avgCostByCountry[name.toLowerCase()];
        return `${name}\nCusto médio total: ${value ? `$${value.toLocaleString(undefined, { maximumFractionDigits: 0 })}` : 'N/A'}`;
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
