<script>
  import * as d3 from 'd3';
  import { createEventDispatcher, onMount } from 'svelte';

  const dispatch = createEventDispatcher();
  let container;
  const width = 600;
  const height = 400;
  let worldData = null;

  const projection = d3.geoNaturalEarth1().scale(150).translate([width/2, height/2]);
  const path = d3.geoPath().projection(projection);

  async function loadWorld() {
    worldData = await d3.json('https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson');
  }

  function draw() {
    if (!worldData) return;

    const svg = d3.select(container).html('').append('svg')
      .attr('width', width)
      .attr('height', height);

    svg.append('g')
      .selectAll('path')
      .data(worldData.features)
      .enter()
      .append('path')
      .attr('d', path)
      .attr('fill', '#ccc')
      .attr('stroke', '#333');

    svg.on('click', (event) => {
      const [x, y] = d3.pointer(event);
      const coords = projection.invert([x, y]);
      if (coords) {
        const [lng, lat] = coords;
        dispatch('selectpoint', { lat, lng });
      }
    });
  }

  onMount(async () => {
    await loadWorld();
    draw();
  });
</script>

<div bind:this={container} style="cursor:pointer;"></div>
