<script lang="ts">
  import * as d3 from 'd3';
  import { onMount } from 'svelte';

  export let data = [];
  let container;
  let tooltip;

  function draw() {
    if (!data.length) return;

    const margin = { top: 5, right: 30, bottom: 40, left: 10 },
      width = 600 - margin.left - margin.right;

    // Processa os dados
    const processed = Array.from(
      new Map(
        data.filter(d => d) 
          .map(d => ({
            program: `${d.Program} (${d.University})`,  // Combina Program com University
            cost:
              Number(d.Tuition_USD) +
              Number(d.Rent_USD) * 12 * Number(d.Duration_Years) +
              Number(d.Visa_Fee_USD),
            Program: d.Program,
            University: d.University,
            City: d.City,
            Country: d.Country,
            Duration_Years: d.Duration_Years,
            total_cost:
              Number(d.Rent_USD) * 12 +
              Number(d.Visa_Fee_USD) +
              Number(d.Insurance_USD),
          }))
          .map(item => [`${item.Program}-${item.University}`, item])  // Usa a chave combinando Program e University
      ).values()
    );

    const top10 = processed.sort((a, b) => b.cost - a.cost).slice(0, 1000);

    const barHeight = Math.max(30, 400 / top10.length);

    const y = d3.scaleBand()
      .range([0, top10.length * barHeight])
      .domain(top10.map(d => d.program))  // Alterado para combinar Program e University
      .padding(0.2);

    const height = Math.max(400, y.range()[1]);

    const svg = d3.select(container)
      .html('')
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Eixo Y
    svg.append('g')
      .call(d3.axisLeft(y))
      .style('visibility', 'hidden');  // Removemos os rótulos do eixo Y

    // Eixo X
    const x = d3.scaleLinear()
      .domain([0, d3.max(top10, d => d.cost) * 1.1])
      .range([0, width]);

    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x).ticks(6));

    // Adicionando título para o eixo X
    svg.append('text')
      .attr('transform', `translate(${width / 2}, ${height + margin.bottom - 10})`)
      .style('text-anchor', 'middle')
      .style('font-size', '14px')
      .style('font-weight', 'bold')
      .text('Custo Total (USD)');

    // Tooltip div
    tooltip = d3.select(container)
      .append('div')
      .attr('class', 'tooltip')
      .style('position', 'absolute')
      .style('background', 'rgba(0, 0, 0, 0.7)')
      .style('color', '#f5f4f1')
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
      .attr('rx', 5)  // Bordas arredondadas para as barras
      .on('mouseover', (event, d) => {
        tooltip
          .style('opacity', 1)
          .html(`
            <strong>${d.program}</strong><br/>
            ${d.City || ''}, ${d.Country || ''}<br/>
            Custo Total: $${d.cost.toLocaleString()}<br/>
            Custo de Vida Anual: $${d.total_cost.toLocaleString()}<br>
            Anos de Duração: ${d.Duration_Years.toLocaleString()}
          `);

        // Efeito de hover nas barras
        d3.select(event.target)
          .transition()
          .duration(200)
          .attr('fill', '#ff7f00') // A cor muda ao passar o mouse
          .attr('width', d => x(d.cost) * 1.1);  // Aumenta ligeiramente o tamanho
      })
      .on('mousemove', (event) => {
        tooltip
          .style('left', (event.offsetX + 10) + 'px')
          .style('top', (event.offsetY + 10) + 'px');
      })
      .on('mouseout', (event) => {
        tooltip.style('opacity', 0);
        
        // Reverte a barra ao seu estado normal
        d3.select(event.target)
          .transition()
          .duration(200)
          .attr('fill', '#ffa500')
          .attr('width', d => x(d.cost));
      });

    // Adiciona o nome do programa dentro da barra
    svg.selectAll('text.bar-label')
      .data(top10)
      .enter()
      .append('text')
      .attr('class', 'bar-label')
      .attr('y', d => y(d.program) + y.bandwidth() / 2)
      .attr('x', d => Math.min(x(d.cost) - 10, width - 10))  // Posiciona dentro da barra
      .attr('dy', '.35em')
      .style('text-anchor', 'end')
      .style('font-size', '12px')
      .style('fill', '#f5f4f1')
      .style('font-weight', 'bold')
      .text(d => {
        const maxLength = 50;  // Limite de caracteres
        return d.program.length > maxLength ? `${d.program.slice(0, maxLength)}...` : d.program;  // Adiciona '...' se o nome for muito longo
      });
  }

  onMount(() => {
    draw();
  });

  $: if (data.length) {
    draw();
  }
</script>

<style>
  /* Estilos para a barra de ferramentas */
  .tooltip {
    position: absolute;
    background: rgba(0, 0, 0, 0.7);
    color: #f5f4f1;
    padding: 8px;
    border-radius: 5px;
    font-size: 12px;
    pointer-events: none;
    opacity: 0;
  }

  .bar-label {
    font-size: 12px;
    fill: #f5f4f1;
    font-weight: bold;
  }

  svg rect {
    transition: all 0.3s ease-in-out;
  }
</style>

<!-- Container com altura fixa e scroll vertical -->
<div 
  bind:this={container} 
  class="w-full" 
  style="position: relative; height: 450px; margin: 0 0 20px 0 ; overflow-y: auto; border: 1px solid #ccc;">
</div>
