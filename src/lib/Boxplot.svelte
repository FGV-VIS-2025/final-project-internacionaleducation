<script lang="ts">
  import * as d3 from 'd3';
  import { onMount } from 'svelte';

  export let data = [];

  let container;

  onMount(() => {
    draw();
  });

  function draw() {
    const margin = { top: 20, right: 30, bottom: 50, left: 50 },
          width = 600 - margin.left - margin.right,
          height = 400 - margin.top - margin.bottom;

    const svg = d3.select(container)
      .html('')
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const grouped = d3.groups(data, d => d.Level);

    const sumStats = grouped.map(([level, values]) => {
      const costs = values.map(d => d.Tuition_USD + d.Rent_USD * 12 + d.Visa_Fee_USD + d.Insurance_USD);
      costs.sort(d3.ascending);
      const q1 = d3.quantile(costs, 0.25);
      const median = d3.quantile(costs, 0.5);
      const q3 = d3.quantile(costs, 0.75);
      const interQuantileRange = q3 - q1;
      const min = q1 - 1.5 * interQuantileRange;
      const max = q3 + 1.5 * interQuantileRange;
      return { level, q1, median, q3, min, max };
    });

    const x = d3.scaleBand()
      .range([0, width])
      .domain(sumStats.map(d => d.level))
      .padding(0.4);

    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x));

    const y = d3.scaleLinear()
      .domain([0, d3.max(sumStats, d => d.max) * 1.1])
      .range([height, 0]);

    svg.append('g').call(d3.axisLeft(y));

    svg.selectAll('boxes')
      .data(sumStats)
      .enter()
      .append('rect')
      .attr('x', d => x(d.level))
      .attr('y', d => y(d.q3))
      .attr('height', d => y(d.q1) - y(d.q3))
      .attr('width', x.bandwidth())
      .attr('stroke', 'black')
      .style('fill', '#69b3a2');

    svg.selectAll('medianLines')
      .data(sumStats)
      .enter()
      .append('line')
      .attr('x1', d => x(d.level))
      .attr('x2', d => x(d.level) + x.bandwidth())
      .attr('y1', d => y(d.median))
      .attr('y2', d => y(d.median))
      .attr('stroke', 'black');
  }
</script>

<div bind:this={container} class="w-full overflow-x-auto"></div>
