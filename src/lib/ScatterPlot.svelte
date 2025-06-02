<script>
  import * as d3 from 'd3';
  import { onMount, afterUpdate } from 'svelte';

  export let data = [];

  let container;
  let initialized = false;

  onMount(() => {
    initialized = true;
  });

  afterUpdate(() => {
    if (initialized && data.length && container) {
      draw();
    }
  });

  function draw() {
    const margin = { top: 20, right: 20, bottom: 60, left: 60 };
    const width = 600 - margin.left - margin.right;
    const height = 360 - margin.top - margin.bottom;

    // Remove existing SVG and tooltip
    d3.select(container).select('svg').remove();
    d3.select(container).selectAll('.tooltip').remove();

    // Create tooltip div (invisible by default)
    const tooltip = d3
      .select(container)
      .append('div')
      .attr('class', 'tooltip')
      .style('opacity', 0);

    const svg = d3
      .select(container)
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const x = d3
      .scaleLinear()
      .domain([0, d3.max(data, d => d.distance) * 1.1])
      .range([0, width]);

    const y = d3
      .scaleLinear()
      .domain([0, d3.max(data, d => d.total_cost) * 1.1])
      .range([height, 0]);

    const xAxisGroup = svg
      .append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x).ticks(6).tickFormat(d3.format('.2f')));

    const yAxisGroup = svg.append('g').call(d3.axisLeft(y));

    xAxisGroup
      .append('text')
      .attr('fill', '#000')
      .attr('x', width / 2)
      .attr('y', 40)
      .attr('text-anchor', 'middle')
      .text('Distância');

    yAxisGroup
      .append('text')
      .attr('fill', '#000')
      .attr('transform', 'rotate(-90)')
      .attr('x', -height / 2)
      .attr('y', -45)
      .attr('text-anchor', 'middle')
      .text('Custo Total (USD)');

    // Draw points with tooltip
    svg
      .selectAll('circle')
      .data(data, d => d.City + d.total_cost)
      .join('circle')
      .attr('r', 5)
      .attr('fill', '#4682b4')
      .style('opacity', 0.7)
      .style('cursor', 'pointer')
      .attr('cx', d => x(d.distance))
      .attr('cy', d => y(d.total_cost))
      .on('mouseenter', (event, d) => {
        tooltip
          .html(
            `<strong>${d.City}, ${d.Country}</strong><br/>
            ${d.University}
            <br/>Custo Total do Curso: USD $${d.total_cost.toLocaleString()}`
          )
          .style('opacity', 1);
      })
      .on('mousemove', event => {
        const [mx, my] = d3.pointer(event, container);
        tooltip.style('left', `${mx + 10}px`).style('top', `${my + 10}px`);
      })
      .on('mouseleave', () => {
        tooltip.style('opacity', 0);
      });
  }
</script>

<style>
  .tooltip {
    position: absolute;
    background: white;
    border: 1px solid #ccc;
    padding: 4px 8px;
    font-size: 0.8rem;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.2s ease-in-out;
    white-space: nowrap;
  }
</style>

<div bind:this={container} class="w-full overflow-x-auto" style="position: relative;"></div>
