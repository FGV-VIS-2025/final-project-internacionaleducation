<script lang="ts">
  import * as d3 from 'd3';
  import { onMount } from 'svelte';

  export let data = [];
  let container;
  let tooltip;

  function draw() {
    if (!data.length) return;

    const margin = { top: 20, right: 30, bottom: 50, left: 200 },
      width = 600 - margin.left - margin.right,
      height = 400 - margin.top - margin.bottom;

    const svg = d3.select(container)
      .html('')  // limpa antes de desenhar
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const processed = data.map(d => ({
      program: `${d.Program} (${d.City})`,
      cost:
        Number(d.Tuition_USD) +
        Number(d.Rent_USD) * 12 +
        Number(d.Visa_Fee_USD) +
        Number(d.Insurance_USD),
      University: d.University,
      City: d.City,
      Country: d.Country,
      total_cost:
        Number(d.Tuition_USD) +
        Number(d.Rent_USD) * 12 +
        Number(d.Visa_Fee_USD) +
        Number(d.Insurance_USD)
    }));

    const top10 = processed.sort((a, b) => b.cost - a.cost).slice(0, 20);

    const y = d3.scaleBand()
      .range([0, height])
      .domain(top10.map(d => d.program))
      .padding(0.2);

    svg.append('g')
      .call(d3.axisLeft(y));

    const x = d3.scaleLinear()
      .domain([0, d3.max(top10, d => d.cost) * 1.1])
      .range([0, width]);

    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x));

    // Tooltip div
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
      .style('z-index', '10')
      .style('opacity', 0);

    svg.selectAll('rect')
      .data(top10)
      .enter()
      .append('rect')
      .attr('y', d => y(d.program))
      .attr('x', 0)
      .attr('height', y.bandwidth())
      .attr('width', d => x(d.cost))
      .attr('fill', '#ffa500')
      .on('mouseover', (event, d) => {
        tooltip
          .style('opacity', 1)
          .html(`
            <strong>${d.University || d.program}</strong><br/>
            ${d.City || ''}, ${d.Country || ''}<br/>
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
    draw();
  });

  $: if (data.length) {
    draw();
  }
</script>

<div bind:this={container} class="w-full overflow-x-auto" style="position: relative;"></div>
