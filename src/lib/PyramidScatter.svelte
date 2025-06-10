<script lang="ts">
  import * as d3 from 'd3';
  import { onMount } from 'svelte';

  export let data = [];  // Dados das universidades

  let container;
  let tooltip;

  // Camadas definidas com base no ranking
  const rankLayers = [
    { min: 1, max: 1 },
    { min: 2, max: 5 },
    { min: 6, max: 15 },
    { min: 16, max: 30 },
    { min: 31, max: 50 },
    { min: 51, max: 75 },
    { min: 76, max: 100 }
  ];

  // Função para organizar dados nas camadas de ranking e filtrar "Bachelor", mas com fallback
  function organizeData(data) {
    // Primeiramente, tenta filtrar dados de "Bachelor"
    const bachelorData = data.filter(d => d.Level === "Bachelor");

    // Para as faculdades que não têm "Bachelor", pega o primeiro dado disponível
    const fallbackData = data.filter(d => !bachelorData.some(item => item.University === d.University));

    // Combina os dados, dando prioridade para "Bachelor" e adicionando os outros casos
    const uniqueUniversities = new Map();

    // Adiciona os dados de "Bachelor"
    bachelorData.forEach(d => {
      if (!uniqueUniversities.has(d.University)) {
        uniqueUniversities.set(d.University, d);  // Adiciona "Bachelor"
      }
    });

    // Para as faculdades que não têm "Bachelor", pega o primeiro dado
    fallbackData.forEach(d => {
      if (!uniqueUniversities.has(d.University)) {
        uniqueUniversities.set(d.University, d);  // Adiciona qualquer nível disponível
      }
    });

    // Organiza os dados nas camadas de ranking
    return rankLayers.map(layer => {
      return Array.from(uniqueUniversities.values())
        .filter(d => d.Rank >= layer.min && d.Rank <= layer.max)
        .map(d => ({
          ...d,
          rankLayer: `${layer.min}-${layer.max}`,
          cost: d.total_cost,
          programUniversity: `${d.Program} (${d.University})`,
        }));
    });
  }

  // Função para desenhar o gráfico
  function draw() {
    if (!data.length) return;

    const margin = { top: 10, right: 30, bottom: 10, left: 80 },
          width = 1000 - margin.left - margin.right,
          height = 350 - margin.top - margin.bottom;

    const svg = d3.select(container)
      .html('')  // Limpa o container antes de desenhar
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const color = d3.scaleOrdinal(d3.schemeCategory10);  // Escala de cores para os países

    // Organizando os dados nas camadas
    const layeredData = organizeData(data);

    // Escala para o eixo X (ranking)
    const xScale = d3.scaleLinear()
      .domain([1, 100])
      .range([0, width]);

    // Escala para o eixo Y (posição dentro da camada, para evitar sobreposição)
    const yScale = d3.scaleLinear()
      .domain([0, 10])  // Máximo de 10 camadas por "faixa" de ranking, ajustável
      .range([0, height]);

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
      .style('opacity', 0)
      .style('transform', 'scale(0.5)')  // Inicialmente, um tamanho reduzido para animação
      .style('transition', 'transform 0.3s, opacity 0.3s');

    // Ajuste para centralizar as camadas
    const middleY = height / 2; // Centraliza a camada de rank 1

    // Criando as bolhas para cada camada
    let yOffset = 0;  // Para ajustar a posição de cada camada no eixo Y

    layeredData.forEach((layerData, i) => {
      const layerHeight = layerData.length; // Quantidade de pontos na camada

      // Calcula a posição Y de forma que as camadas sejam distribuídas
      const layerY = middleY + (i - 3) * (height / 8);  // Aumenta a distância entre as camadas, ajustando a pirâmide

      svg.selectAll(`circle.layer${i}`)
        .data(layerData)
        .enter()
        .append('circle')
        .attr('cx', d => xScale(d.Rank) * (2.7 - layerHeight/6))  // Posição no eixo X de acordo com o ranking
        .attr('cy', (d, index) => layerY + (index - Math.floor(layerHeight)) * (50 - layerHeight * 1.5) + 220 - layerY * 0.3)  // Ajuste Y para cada ponto
        .attr('r', d => d.cost * 0.0002)  
        .attr('fill', d => d.Country === 'USA' ? 'blue' : 'gray') 
        .attr('opacity', 0.7)
        .on('mouseover', (event, d) => {
          tooltip
            .style('opacity', 1)
            .style('transform', 'scale(1)')  // Aumenta a escala do tooltip com animação
            .html(`
              <strong>${d.programUniversity}</strong><br/>
              ${d.City || ''}, ${d.Country || ''}<br/>
              Custo Total: $${d.cost.toLocaleString()}<br/>
              Rank: ${d.Rank}
            `);

          // Aumenta a bolha ao passar o mouse
          d3.select(event.target)
            .transition()
            .duration(300)
            .attr('r', d => d.cost * 0.00025)  // Aumenta o tamanho da bolha
            .attr('opacity', 1);
        })
        .on('mousemove', (event) => {
          tooltip
            .style('left', (event.offsetX + 10) + 'px')
            .style('top', (event.offsetY + 10) + 'px');
        })
        .on('mouseout', (event) => {
          tooltip.style('opacity', 0)
            .style('transform', 'scale(0.5)');  // Animação de desaparecimento

          // Reverte a bolha ao tamanho normal
          d3.select(event.target)
            .transition()
            .duration(300)
            .attr('r', d => d.cost * 0.0002)
            .attr('opacity', 0.7);
        });

      yOffset += layerHeight / 10;  // Incrementa o Y para a próxima camada
    });

    // Remover eixos X e Y
    svg.selectAll('.axis').remove();

    // Adicionando a legenda para USA (Azul) e NOT-USA (Cinza)
    const legend = svg.append('g')
      .attr('transform', `translate(${width - 160}, 20)`);

    // Adicionando fundo para a legenda
    legend.append('rect')
      .attr('x', -10)
      .attr('y', -10)
      .attr('width', 120)
      .attr('height', 60)
      .attr('fill', '#fff')
      .attr('stroke', '#000')
      .attr('stroke-width', 1);

    legend.append('circle')
      .attr('cx', 10)
      .attr('cy', 10)
      .attr('r', 6)
      .attr('fill', 'blue');
    
    legend.append('text')
      .attr('x', 25)
      .attr('y', 15)
      .style('font-size', '12px')
      .text('USA');

    legend.append('circle')
      .attr('cx', 10)
      .attr('cy', 30)
      .attr('r', 6)
      .attr('fill', 'gray');
    
    legend.append('text')
      .attr('x', 25)
      .attr('y', 35)
      .style('font-size', '12px')
      .text('Not USA');
  }

  onMount(() => {
    draw();
  });

  $: if (data.length) {
    draw();
  }
</script>

<style>
  .tooltip {
    position: absolute;
    background: rgba(0, 0, 0, 0.7);
    color: #fff;
    padding: 8px;
    border-radius: 5px;
    font-size: 12px;
    pointer-events: none;
    opacity: 0;
    transition: opacity 0.3s, transform 0.3s;
  }
</style>

<!-- Container para o gráfico -->
<div 
  bind:this={container} 
  style="position: relative; width: 100%; border: 1px solid #ccc;">
</div>
