<script>
  import * as d3 from 'd3';
  import { onMount } from 'svelte';

  export let data = [];
  let container;
  let clicked = false;

  let world;

  async function loadWorld() {
    world = await d3.json('https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson');
  }

  onMount(async () => {
    await loadWorld();
    draw();
  });

  function draw() {
    const width = 600, height = 360;

    const svg = d3.select(container)
      .html('')
      .append('svg')
      .attr('width', width)
      .attr('height', height)
      .style('border', '1px solid #ccc')
      .style('cursor', 'grab')
      .style('user-select', 'none');

    const tooltip = d3.select(container)
      .append('div')
      .attr('class', 'tooltip')
      .style('position', 'absolute')
      .style('padding', '10px')
      .style('background', 'rgba(0, 0, 0, 0.8)')
      .style('color', '#fff')
      .style('border-radius', '4px')
      .style('font-size', '12px')
      .style('pointer-events', 'none')
      .style('z-index', '10')
      .style('opacity', 0);

    const projection = d3.geoNaturalEarth1().scale(150).translate([width / 2, height / 2]);
    const path = d3.geoPath().projection(projection);

    const g = svg.append('g');
    const mapGroup = g.append('g');
    const pointsGroup = g.append('g');

    // Mapa com zoom ao clicar no país
    mapGroup.selectAll('path')
      .data(world.features)
      .enter()
      .append('path')
      .attr('fill', '#d3d3d3')
      .attr('stroke', '#999')
      .attr('stroke-width', 0.5)
      .attr('d', path)
      .on('click', (event, d) => {
        const centroid = d3.geoCentroid(d);
        const [x, y] = projection(centroid);
        const scale = 4;
        const translate = [width / 2 - scale * x, height / 2 - scale * y];

        svg.transition()
          .duration(750)
          .call(
            zoom.transform,
            d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale)
          );
      });

    // Pontos das universidades
    const circles = pointsGroup.selectAll('circle')
      .data(data)
      .enter()
      .append('circle')
      .attr('cx', d => projection([+d.lng, +d.lat])[0])
      .attr('cy', d => projection([+d.lng, +d.lat])[1])
      .attr('r', 4)
      .attr('fill', '#ff5733')
      .attr('opacity', 0.8)
      .style('cursor', 'pointer')
      .on('mousemove', (event, d) => {
        const [x, y] = d3.pointer(event, container);
        tooltip
          .html(`
            <strong>${d.University}</strong><br/>
            ${d.City}, ${d.Country}<br/>
          `)
          .style('left', `${x + 15}px`)
          .style('top', `${y + 15}px`)
          .style('opacity', 1);
      })
      .on('click', (event, d) => {
        clicked = true;

        // Zoom até o ponto clicado
        const [x, y] = projection([+d.lng, +d.lat]);
        const scale = 4;
        const translate = [width / 2 - scale * x, height / 2 - scale * y];

        svg.transition()
          .duration(750)
          .call(
            zoom.transform,
            d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale)
          );

        tooltip
          .html(`
            <strong>${d.University}</strong><br/>
            ${d.City}, ${d.Country}<br/>
            Custo Médio de Curso: $${d.Tuition_USD}<br/>
            Aluguel Mensal: $${d.Rent_USD}<br/>
            Seguro de Saúde Mensal: $${d.Insurance_USD}<br/>
            Câmbio (USD): ${d.Exchange_Rate}
          `)
          .style('left', `${x + 15}px`)
          .style('top', `${y + 15}px`)
          .style('opacity', 1);
      })
      .on('mouseout', () => {
        tooltip.style('opacity', 0);
      });

    // Zoom control
    const zoom = d3.zoom()
      .scaleExtent([1, 8])
      .on('zoom', event => {
        g.attr('transform', event.transform);
        circles.attr('r', 4 / event.transform.k);
      });

    svg.call(zoom);

    // Se clicar fora dos círculos, fecha o tooltip detalhado
    d3.select(container).on('click', (event) => {
      // Se clicou no container mas NÃO em um círculo
      if (event.target.tagName !== 'circle') {
        clicked = false;
        tooltip.style('opacity', 0);
      }
    });
  }
</script>

<style>
  .tooltip {
    max-width: 220px;
    white-space: nowrap;
  }
</style>

<div bind:this={container} style="position: relative;" class="w-full overflow-x-auto"></div>
