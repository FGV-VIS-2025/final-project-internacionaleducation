<script>
  import { onMount, afterUpdate } from 'svelte';
  import * as d3 from 'd3';
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  export let data = [];
  export let selectedCountries = [];

  let container;
  let chartHeight = 500;

  $: rankedData = getRankedData(data, selectedCountries);

  function getRankedData(allData, countries) {
    const filtered = countries.length === 0
      ? allData
      : allData.filter(d => countries.includes(d.Country));

    const withRank = filtered
      .filter(d => d.world_rank !== "Unknown")
      .sort((a, b) => a.world_rank - b.world_rank);

    const withoutRank = filtered.filter(d => d.world_rank === "Unknown");

    return [...withRank, ...withoutRank]
    .map((d, i) => ({
      ...d,
      scopeRank: i + 1,
      isRanked: d.world_rank !== "Unknown"
    }))
    .slice(0, 15); 
  }

  function drawChart() {
    const width = 600;
    const margin = { top: 40, right: 40, bottom: 40, left: 200 };
    const barHeight = 30;
    const innerHeight = Math.max(chartHeight, rankedData.length * barHeight);

    d3.select(container).selectAll('*').remove();

    const svg = d3.select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', chartHeight)
      .attr('viewBox', [0, 0, width, chartHeight])
      .attr('style', 'max-width: 100%; height: auto; background: #f9f9f9; border-radius: 15px;');

    const defs = svg.append('defs');
    defs.append('filter')
      .attr('id', 'cartoonEffect')
      .append('feDropShadow')
      .attr('dx', 2)
      .attr('dy', 2)
      .attr('stdDeviation', 2)
      .attr('flood-color', 'rgba(0,0,0,0.3)');

    const chart = svg.append('g')
      .attr('transform', `translate(${margin.left}, ${margin.top})`);

    const x = d3.scaleLinear()
      .domain([0, 1])
      .range([0, width - margin.left - margin.right - 50]);

    const y = d3.scaleBand()
      .domain(rankedData.map(d => d.University))
      .range([0, innerHeight - margin.top - margin.bottom])
      .padding(0.3);

    const maxWidth = x(1);
    const barWidths = d => {
      if (d.scopeRank <= 10) {
        return maxWidth * (1 - (d.scopeRank - 1) * 0.07);
      } else {
        const rest = rankedData.length - 10;
        const idx = d.scopeRank - 11;
        return maxWidth * 0.3 * (1 - idx / rest);
      }
    };

    chart.selectAll('rect')
      .data(rankedData, d => d.University)
      .join(
        enter => enter.append('rect')
          .attr('x', 0)
          .attr('y', d => y(d.University))
          .attr('height', y.bandwidth())
          .attr('width', 0)
          .attr('rx', 8)
          .attr('ry', 8)
          .attr('fill', d => {
            const rank = d.world_rank;
            if (rank <= 10) return '#00c2ff';   // Diamante
            if (rank <= 100) return '#ffd700';  // Ouro
            if (rank <= 400) return '#c0c0c0';  // Prata
            return '#cd7f32';                   // Bronze
          })
          .attr('stroke', '#333')
          .attr('stroke-width', 1.5)
          .attr('filter', 'url(#cartoonEffect)')
          .on('click', (event, d) => {
            if (selectedCountries.length === 0) {
              dispatch('zoomToCountry', d.Country);
            } else {
              dispatch('selectUniversity', d);
            }
          })
            .on('mouseover', function(event, d) {
            const bar = d3.select(this);
    
            // Guarda a cor original (se precisar restaurar depois)
            bar.attr('data-original-fill', bar.attr('fill'));
            
            bar.transition()
                .duration(200)
                .attr('fill', d3.color(bar.attr('fill')).brighter(0.6)) // Clareia a cor
                .attr('fill-opacity', 0.9)
                .attr('stroke-width', 3);

            const pin = d3.select(`image.pin[data-uni-id='${d.University.replace(/\s+/g, '-')}']`);
            if (!pin.empty()) {
              const originalY = parseFloat(pin.attr('y'));

              pin.raise();

              pin.transition()
                .duration(100)
                .attr('y', originalY - 10)
                .transition()
                .duration(100)
                .attr('y', originalY);
            }
          })

          .on('mouseout', function () {
            const bar = d3.select(this);
            bar.transition()
                .duration(200)
                .attr('fill', bar.attr('data-original-fill')) // Volta para a cor original
                .attr('fill-opacity', 1)
                .attr('stroke-width', 1);
                  })
          .transition()
          .duration(800)
          .attr('width', d => barWidths(d)),

        update => update
          .transition()
          .duration(800)
          .attr('y', d => y(d.University))
          .attr('width', d => barWidths(d)),

        exit => exit
          .transition()
          .duration(500)
          .attr('width', 0)
          .remove()
      );

    chart.selectAll('.university-label')
      .data(rankedData, d => d.University)
      .join(
        enter => enter.append('text')
          .attr('class', 'university-label')
          .attr('x', -10)
          .attr('y', d => y(d.University) + y.bandwidth() / 2)
          .attr('text-anchor', 'end')
          .attr('alignment-baseline', 'middle')
          .attr('font-size', '12px')
          .attr('font-weight', 'bold')
          .attr('fill', '#333')
          .attr('stroke', 'white')
          .attr('stroke-width', '2px')
          .attr('paint-order', 'stroke')
          .text(d => d.University.length > 25 ? d.University.slice(0, 25) + '...' : d.University)
          .style('opacity', 0)
          .transition().duration(800).style('opacity', 1),

        update => update
          .transition()
          .duration(800)
          .attr('y', d => y(d.University) + y.bandwidth() / 2),

        exit => exit
          .transition().duration(300)
          .style('opacity', 0)
          .remove()
      );

    svg.append('text')
      .attr('x', width / 2)
      .attr('y', 30)
      .attr('text-anchor', 'middle')
      .attr('font-size', '18px')
      .attr('font-weight', 'bold')
      .attr('fill', '#4a90e2')
      .text(selectedCountries.length
        ? `top 15 universidades da seleção`
        : `Top universidades Globais`);
  }

  afterUpdate(drawChart);
</script>

<style>
  .chart-container {
    width: 100%;
    overflow-y: auto;
    border-radius: 15px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  }
</style>

<div class="chart-container" bind:this={container}></div>
