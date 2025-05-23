<script lang="ts">
  import * as d3 from 'd3';
  import { onMount } from 'svelte';

  export let data = [];
  let container;

  function draw() {
    if (!data.length) return;

    const margin = { top: 20, right: 30, bottom: 100, left: 80 },
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
        Number(d.Insurance_USD)
    }));

    const top10 = processed.sort((a, b) => b.cost - a.cost).slice(0, 10);

    const x = d3.scaleBand()
      .range([0, width])
      .domain(top10.map(d => d.program))
      .padding(0.2);

    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x))
      .selectAll("text")
      .attr("transform", "rotate(-45)")
      .style("text-anchor", "end");

    const y = d3.scaleLinear()
      .domain([0, d3.max(top10, d => d.cost) * 1.1])
      .range([height, 0]);

    svg.append('g').call(d3.axisLeft(y));

    svg.selectAll('rect')
      .data(top10)
      .enter()
      .append('rect')
      .attr('x', d => x(d.program))
      .attr('y', d => y(d.cost))
      .attr('width', x.bandwidth())
      .attr('height', d => height - y(d.cost))
      .attr('fill', '#ffa500');
  }

  onMount(() => {
    draw();
  });

  $: if (data.length) {
    draw();
  }
</script>

<div bind:this={container} class="w-full overflow-x-auto"></div>
