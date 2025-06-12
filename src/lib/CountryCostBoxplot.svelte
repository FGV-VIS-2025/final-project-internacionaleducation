<script>
	import { onMount } from 'svelte';
	import * as d3 from 'd3';

	export let data = [];
	// MODIFICADO: Recebe um objeto de cores, não mais uma string
	export let colors = {}; 

	let container;
	const margin = { top: 10, right: 30, bottom: 90, left: 60 };
	let width, height;

	function drawBoxplot() {
		if (!container || data.length === 0) return;
		d3.select(container).select('svg').remove();
		
		width = container.clientWidth - margin.left - margin.right;
		height = 350 - margin.top - margin.bottom;

		const svg = d3.select(container).append('svg')
			.attr('width', width + margin.left + margin.right)
			.attr('height', height + margin.top + margin.bottom)
			.append('g').attr('transform', `translate(${margin.left},${margin.top})`);
		
		const sumstat = d3.group(data, d => d.Country);
		
		// MODIFICADO: Agora guardamos o continente de cada país
		const data_sorted = Array.from(sumstat, ([key, values]) => {
			// Pega o continente do primeiro item (todos os itens de um país terão o mesmo continente)
			const continent = values[0].Continent; 
			const costs = values.map(v => v.total_cost).sort(d3.ascending);
			const q1 = d3.quantile(costs, .25);
			const median = d3.quantile(costs, .5);
			const q3 = d3.quantile(costs, .75);
			const interQuantileRange = q3 - q1;
			const min = q1 - 1.5 * interQuantileRange;
			const max = q3 + 1.5 * interQuantileRange;
			return { key, continent, value: {q1, median, q3, min, max} };
		});
		
		const x = d3.scaleBand()
			.range([0, width])
			.domain(data_sorted.map(d => d.key))
			.paddingInner(1).paddingOuter(.5);
		
		svg.append('g').attr('transform', `translate(0, ${height})`).call(d3.axisBottom(x))
			.selectAll("text").attr("transform", "translate(-10,0)rotate(-45)").style("text-anchor", "end");

		const y = d3.scaleLinear()
			.domain([0, d3.max(data, d => d.total_cost) * 1.1])
			.range([height, 0]);
			
		svg.append('g').call(d3.axisLeft(y).tickFormat(d => `$${d/1000}k`));

		// MODIFICADO: A cor agora é determinada para cada item de dado (país)
		// usando o mapa de cores e o continente do país.

		// Linhas verticais
		svg.selectAll("vertLines").data(data_sorted).enter().append("line")
			.attr("x1", d => x(d.key)).attr("x2", d => x(d.key))
			.attr("y1", d => y(d.value.min)).attr("y2", d => y(d.value.max))
			.attr("stroke", d => colors[d.continent] || '#cccccc') // Usa o mapa de cores
			.style("width", 4);

		// Retângulo do boxplot
		svg.selectAll("boxes").data(data_sorted).enter().append("rect")
			.attr("x", d => x(d.key) - 10).attr("y", d => y(d.value.q3))
			.attr("height", d => y(d.value.q1) - y(d.value.q3))
			.attr("width", 20)
			.attr("stroke", d => colors[d.continent] || '#cccccc') // Usa o mapa de cores
			.style("fill", d => {
				const baseColor = d3.color(colors[d.continent] || '#cccccc');
				return baseColor ? baseColor.copy({opacity: 0.5}) : '#cccccc80';
			});

		// Linha da mediana
		svg.selectAll("medianLines").data(data_sorted).enter().append("line")
			.attr("x1", d => x(d.key) - 10).attr("x2", d => x(d.key) + 10)
			.attr("y1", d => y(d.value.median)).attr("y2", d => y(d.value.median))
			.attr("stroke", d => colors[d.continent] || '#cccccc') // Usa o mapa de cores
			.style("width", 8);
	}
	
	$: if(container && data && Object.keys(colors).length > 0) {
		drawBoxplot();
	}

</script>

<div bind:this={container} style="width: 900px; height: 350px; margin-left: 200px;"></div>