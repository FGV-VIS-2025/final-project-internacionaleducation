<script>
  import * as d3 from 'd3';
  import { onMount } from 'svelte';

  export let data = [];
  
  let container;
  let tooltip;

  let selectedPoint = [0, 0];
  let scatterData = [];

  function getDistance(datum, point) {
    const [latPoint, lngPoint] = point;
    const lat = Number(datum.lat);
    const lng = Number(datum.lng);
    return Math.sqrt((latPoint - lat) ** 2 + (lngPoint - lng) ** 2);
  }

  function updateScatterData() {
    scatterData = data.map(d => ({
      distance: getDistance(d, selectedPoint),
      total_cost: Number(d.total_cost),
      City: d.City,
      Country: d.Country,
      University: d.University
    }));
  }

  $: updateScatterData();
  $: if (scatterData.length) draw();

  function draw() {
    const margin = { top: 20, right: 70, bottom: 100, left: 70 };
    const width = 600 - margin.left - margin.right;
    const height = 360 - margin.top - margin.bottom;
    const brushHeight = 50;
    const brushWidth = 50;

    d3.select(container).select('svg').remove();

    const svg = d3.select(container)
      .append('svg')
      .attr('width', width + margin.left + margin.right + brushWidth)
      .attr('height', height + margin.top + margin.bottom + brushHeight)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    svg.append("defs")
      .append("clipPath")
      .attr("id", "clip")
      .append("rect")
      .attr("width", width)
      .attr("height", height);

    let x = d3.scaleLinear()
      .domain([0, d3.max(scatterData, d => d.distance) * 1.1])
      .range([0, width]);

    let y = d3.scaleLinear()
      .domain([0, d3.max(scatterData, d => d.total_cost) * 1.1])
      .range([height, 0]);

    const xAxisGroup = svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x).ticks(6).tickFormat(d3.format(".2f")));

    const yAxisGroup = svg.append('g')
      .call(d3.axisLeft(y));

    xAxisGroup.append("text")
      .attr("fill", "#000")
      .attr("x", width / 2)
      .attr("y", 30)
      .attr("text-anchor", "middle")
      .text("Distância");

    yAxisGroup.append("text")
      .attr("fill", "#000")
      .attr("transform", "rotate(-90)")
      .attr("x", -height / 2)
      .attr("y", -50)
      .attr("text-anchor", "middle")
      .text("Custo Total (USD)");

    const pointsGroup = svg.append('g')
      .attr("clip-path", "url(#clip)");

    let xSelection = x.domain();
    let ySelection = y.domain();

    function updatePoints() {
      const filtered = scatterData.filter(d =>
        d.distance >= xSelection[0] && d.distance <= xSelection[1] &&
        d.total_cost >= ySelection[0] && d.total_cost <= ySelection[1]
      );

      const circles = pointsGroup.selectAll('circle').data(filtered, d => d.City + d.total_cost);

      circles.exit().remove();

      circles.enter()
        .append('circle')
        .attr('r', 5)
        .attr('fill', '#4682b4')
        .style('opacity', 0.7)
        .style('cursor', 'pointer')
        .merge(circles)
        .attr('cx', d => x(d.distance))
        .attr('cy', d => y(d.total_cost))
        .on('mouseover', (event, d) => {
          tooltip
            .style('opacity', 1)
            .html(`
              <strong>${d.University}</strong><br/>
              ${d.City}, ${d.Country}<br/>
              Custo: $${d.total_cost.toLocaleString()}
            `);
        })
        .on('mousemove', (event) => {
          // Pega posição com scroll para não errar no posicionamento
          tooltip
            .style('left', (event.clientX + window.scrollX + 10) + 'px')
            .style('top', (event.clientY + window.scrollY + 10) + 'px');
        })
        .on('mouseout', () => {
          tooltip.style('opacity', 0);
        });
    }

    updatePoints();

    const xBrush = d3.scaleLinear().domain(x.domain()).range(x.range());
    const yBrush = d3.scaleLinear().domain(y.domain()).range(y.range());

    const brushGroupX = svg.append('g')
      .attr('transform', `translate(0,${height + 40})`);

    brushGroupX.append('g').call(d3.axisBottom(xBrush));

    const brushX = d3.brushX()
      .extent([[0, 0], [width, brushHeight]])
      .on('brush end', (event) => {
        if (!event.selection) {
          xSelection = x.domain();
        } else {
          xSelection = event.selection.map(xBrush.invert);
        }
        updatePoints();
      });

    brushGroupX.append('g').attr('class', 'brush').call(brushX);

    const brushGroupY = svg.append('g')
      .attr('transform', `translate(${width + 40}, 0)`);

    brushGroupY.append('g').call(d3.axisRight(yBrush));

    const brushY = d3.brushY()
      .extent([[0, 0], [brushWidth, height]])
      .on('brush end', (event) => {
        if (!event.selection) {
          ySelection = y.domain();
        } else {
          ySelection = event.selection.map(yBrush.invert).sort((a,b) => a - b);
        }
        updatePoints();
      });

    brushGroupY.append('g').attr('class', 'brush').call(brushY);

    const zoom = d3.zoom()
      .scaleExtent([1, 10])
      .translateExtent([[0, 0], [width, height]])
      .extent([[0, 0], [width, height]])
      .on('zoom', (event) => {
        const transform = event.transform;
        const zx = transform.rescaleX(x);
        const zy = transform.rescaleY(y);

        xAxisGroup.call(d3.axisBottom(zx).ticks(6).tickFormat(d3.format(".2f")));
        yAxisGroup.call(d3.axisLeft(zy));

        pointsGroup.selectAll('circle')
          .attr('cx', d => zx(d.distance))
          .attr('cy', d => zy(d.total_cost));
      });

    svg.append('rect')
      .attr('width', width)
      .attr('height', height)
      .style('fill', 'none')
      .style('pointer-events', 'all')
      .call(zoom);
  }

  onMount(() => {
    // Coloca tooltip no body para evitar corte e problemas de overflow
    tooltip = d3.select(document.body)
      .append('div')
      .attr('class', 'tooltip')
      .style('position', 'absolute')
      .style('background', 'rgba(0, 0, 0, 0.7)')
      .style('color', '#fff')
      .style('padding', '6px 10px')
      .style('border-radius', '4px')
      .style('font-size', '12px')
      .style('pointer-events', 'none')
      .style('z-index', '9999')
      .style('opacity', 0);

    updateScatterData();
  });
</script>

<style>
  .tooltip {
    font-size: 12px;
    pointer-events: none;
    position: absolute;
  }
</style>

<div bind:this={container} class="w-full overflow-x-auto" style="position: relative;"></div>
