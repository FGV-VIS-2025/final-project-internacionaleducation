<script lang="ts">
  import * as d3 from 'd3';
  import { onMount } from 'svelte';

  export let data = [];
  let container;

  onMount(() => {
    draw();
  });

  async function draw() {
    const width = 800, height = 400;

    const projection = d3.geoNaturalEarth1().scale(150).translate([width / 2, height / 2]);
    const path = d3.geoPath().projection(projection);

    const svg = d3.select(container)
      .html('')
      .append('svg')
      .attr('width', width)
      .attr('height', height);

    const world = await d3.json('https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson');

    svg.append('g')
      .selectAll('path')
      .data(world.features)
      .enter()
      .append('path')
      .attr('fill', '#d3d3d3')
      .attr('d', path)
      .style('stroke', 'none');

    svg.selectAll('circle')
      .data(data)
      .enter()
      .append('circle')
      .attr('cx', d => projection([+d.lng, +d.lat])[0])
      .attr('cy', d => projection([+d.lng, +d.lat])[1])
      .attr('r', 3)
      .attr('fill', '#ff5733')
      .attr('opacity', 0.7);
  }
</script>

<div bind:this={container} class="w-full overflow-x-auto"></div>
