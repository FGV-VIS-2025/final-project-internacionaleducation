<script>
  import * as d3 from 'd3';
  import { onMount } from 'svelte';

  export let data = [];
  
  console.log(data);

  let container;
  let tooltip;

  let selectedPoint = [0, 0];

  let scatterData = [];

  function getDistance(datum, point) {
    const [latPoint, lngPoint] = point;
    const lat = Number(datum.lat);
    const lng = Number(datum.lng);
    return Math.sqrt((latPoint - lat) ** 2 + (lngPoint - lng) ** 2);
  }

  function updateScatterData() {
    scatterData = data.map(d => ({
      distance: getDistance(d, selectedPoint),
      total_cost: Number(d.total_cost),
      City: d.City,
      Country: d.Country,
      University: d.University
    }));
  }

  $: updateScatterData();
  $: if (scatterData.length) draw();

  function draw() {
    const margin = { top: 20, right: 30, bottom: 50, left: 70 };
    const width = 600 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // APAGA SÓ O SVG, mantém o tooltip intacto
    d3.select(container).select('svg').remove();

    const svg = d3.select(container)
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const x = d3.scaleLinear()
      .domain([0, d3.max(scatterData, d => d.distance) * 1.1])
      .range([0, width]);

    const y = d3.scaleLinear()
      .domain([0, d3.max(scatterData, d => d.total_cost) * 1.1])
      .range([height, 0]);

    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x).ticks(6).tickFormat(d3.format(".2f")))
      .append("text")
      .attr("fill", "#000")
      .attr("x", width / 2)
      .attr("y", 40)
      .attr("text-anchor", "middle")
      .text("Distância");

    svg.append('g')
      .call(d3.axisLeft(y))
      .append("text")
      .attr("fill", "#000")
      .attr("transform", "rotate(-90)")
      .attr("x", -height / 2)
      .attr("y", -50)
      .attr("text-anchor", "middle")
      .text("Custo Total (USD)");

    svg.append('g')
      .selectAll('circle')
      .data(scatterData)
      .enter()
      .append('circle')
      .attr('cx', d => x(d.distance))
      .attr('cy', d => y(d.total_cost))
      .attr('r', 5)
      .style('fill', '#4682b4')
      .style('opacity', 0.7)
      .style('cursor', 'pointer')
      .on('mouseover', (event, d) => {
        tooltip
          .style('opacity', 1)
          .html(`
            <strong>${d.University}</strong><br/>
            ${d.City}, ${d.Country}<br/>
            Custo: $${d.total_cost.toLocaleString()}
          `);
      })
      .on('mousemove', (event) => {
        tooltip
          .style('left', (event.offsetX + 10) + 'px')
          .style('top', (event.offsetY + 10) + 'px');
      })
      .on('mouseout', () => {
        tooltip.style('opacity', 0);
      });
  }

  onMount(() => {
    // cria o tooltip 1x só, fora do svg
    tooltip = d3.select(container)
      .append('div')
      .attr('class', 'tooltip')
      .style('position', 'absolute')
      .style('background', 'rgba(0, 0, 0, 0.7)')
      .style('color', '#fff')
      .style('padding', '6px 10px')
      .style('border-radius', '4px')
      .style('font-size', '12px')
      .style('pointer-events', 'none')
      .style('opacity', 0);

    updateScatterData();
  });
</script>

<style>
  .tooltip {
    font-size: 12px;
  }
</style>

<div bind:this={container} class="w-full overflow-x-auto" style="position: relative;"></div>
