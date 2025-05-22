<script lang="ts">
  import * as d3 from 'd3';
  import { onMount } from 'svelte';

  export let data = [];
  let container;

  onMount(() => {
    draw();
  });

  function draw() {
    const margin = { top: 20, right: 30, bottom: 50, left: 60 },
          width = 600 - margin.left - margin.right,
          height = 400 - margin.top - margin.bottom;

    const svg = d3.select(container)
      .html('')
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const x = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.Living_Cost_Index) * 1.1])
      .range([0, width]);

    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x));

    const y = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.Tuition_USD) * 1.1])
      .range([height, 0]);

    svg.append('g').call(d3.axisLeft(y));

    svg.append('g')
      .selectAll('dot')
      .data(data)
      .enter()
      .append('circle')
      .attr('cx', d => x(d.Living_Cost_Index))
      .attr('cy', d => y(d.Tuition_USD))
      .attr('r', 4)
      .style('fill', '#4682b4')
      .style('opacity', 0.7);
  }
</script>

<div bind:this={container} class="w-full overflow-x-auto"></div>
