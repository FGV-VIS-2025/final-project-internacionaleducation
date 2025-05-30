<script lang="ts">
  import * as d3 from 'd3';
  import { onMount } from 'svelte';

  export let data = [];
  let container;
  let tooltip;

  function draw() {
    if (!data.length) return;

    const margin = { top: 20, right: 30, bottom: 50, left: 200 },
      width = 600 - margin.left - margin.right;

    // Processa dados
    const processed = data.map(d => ({
      program: `${d.Program} (${d.City})`,
      cost:
        Number(d.Tuition_USD) +
        Number(d.Rent_USD) * 12 * Number(d.Duration_Years) +
        Number(d.Visa_Fee_USD),
      University: d.University,
      City: d.City,
      Country: d.Country,
      total_cost:
        Number(d.Rent_USD) * 12 +
        Number(d.Visa_Fee_USD) +
        Number(d.Insurance_USD)
    }));

    const top10 = processed.sort((a, b) => b.cost - a.cost).slice(0, 1000);

    // Y scale com altura dinâmica (barra altura * número de itens)
    const y = d3.scaleBand()
      .range([0, top10.length * 25])  // 25 px por barra (ajusta se quiser)
      .domain(top10.map(d => d.program))
      .padding(0.2);

    // Altura do SVG = total de barras * altura barra + margens
    const height = y.range()[1];

    // Limpa container e cria svg com altura dinâmica
    const svg = d3.select(container)
      .html('')  // limpa antes de desenhar
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Eixo Y
    svg.append('g')
      .call(d3.axisLeft(y));

    // Eixo X
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

    // Barras
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
            Curso + Custo de Vida: $${d.cost.toLocaleString()}<br/>
            Custo de Vida Anual: $${d.total_cost.toLocaleString()}
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

<!-- Container com altura fixa e scroll vertical -->
<div 
  bind:this={container} 
  class="w-full" 
  style="position: relative; height: 450px; margin: 0 0 20px 0 ; overflow-y: auto; border: 1px solid #ccc;">
</div>
