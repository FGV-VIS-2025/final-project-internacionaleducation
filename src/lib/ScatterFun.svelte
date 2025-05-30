<script>
  import { onMount } from "svelte";
  import * as d3 from "d3";

  export let scatterInteractiveData = [];

  let container;

  // Dimensões básicas do gráfico
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  let width = 600;
  let height = 360;

  onMount(() => {
    // Limpa o container
    d3.select(container).select("svg").remove();

    // Cria o SVG
    const svg = d3
      .select(container)
      .append("svg")
      .attr("width", width)
      .attr("height", height);

    // Define escala X
    const x = d3
      .scaleLinear()
      .domain(d3.extent(scatterInteractiveData, d => d.x))
      .nice()
      .range([margin.left, width - margin.right]);

    // Define escala Y
    const y = d3
      .scaleLinear()
      .domain(d3.extent(scatterInteractiveData, d => d.y))
      .nice()
      .range([height - margin.bottom, margin.top]);

    // Eixo X
    svg
      .append("g")
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x));

    // Eixo Y
    svg
      .append("g")
      .attr("transform", `translate(${margin.left},0)`)
      .call(d3.axisLeft(y));

    // Desenha os pontos
    svg
      .append("g")
      .attr("stroke", "black")
      .attr("stroke-width", 1)
      .selectAll("circle")
      .data(scatterInteractiveData)
      .join("circle")
      .attr("cx", d => x(d.x))
      .attr("cy", d => y(d.y))
      .attr("r", 5)
      .attr("fill", "steelblue");
  });
</script>

<div bind:this={container} class="w-full overflow-x-auto"></div>
