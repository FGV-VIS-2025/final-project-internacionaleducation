<script>
	import { onMount } from 'svelte';
	import * as d3 from 'd3';

	export let data = [];
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

		const tooltip = d3.select("#tooltip");

		const sumstat = d3.group(data, d => d.Country);
		
		const data_sorted = Array.from(sumstat, ([key, values]) => {
			const continent = values[0].Continent; 
			const costs = values.map(v => v.total_cost).sort(d3.ascending);
			const q1 = d3.quantile(costs, .25);
			const median = d3.quantile(costs, .5);
			const q3 = d3.quantile(costs, .75);
			const min = d3.min(costs); 
			const max = d3.max(costs);
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

		const boxGroups = svg.selectAll("boxGroup")
			.data(data_sorted)
			.enter()
			.append("g")
			.attr("class", "box-group");

		boxGroups.append("line")
			.attr("x1", d => x(d.key)).attr("x2", d => x(d.key))
			.attr("y1", d => y(d.value.min)).attr("y2", d => y(d.value.max))
			.attr("stroke", d => colors[d.continent] || '#cccccc');

		boxGroups.append("rect")
			.attr("x", d => x(d.key) - 10)
			.attr("y", d => y(d.value.q3))
			.attr("height", d => y(d.value.q1) - y(d.value.q3))
			.attr("width", 20)
			.attr("stroke", d => colors[d.continent] || '#cccccc')
			.style("fill", d => {
				const baseColor = d3.color(colors[d.continent] || '#cccccc');
				return baseColor ? baseColor.copy({opacity: 0.5}) : '#cccccc80';
			});

		boxGroups.append("line")
			.attr("x1", d => x(d.key) - 10).attr("x2", d => x(d.key) + 10)
			.attr("y1", d => y(d.value.median)).attr("y2", d => y(d.value.median))
			.attr("stroke", d => colors[d.continent] || '#cccccc')
			.style("stroke-width", 2);

		boxGroups
			.on("mouseover", function(event, d) {
				tooltip
					.style("opacity", 1)
					// MODIFICADO: A posição 'left' e 'top' agora aponta diretamente para o cursor.
					.style("left", event.pageX + "px")
					.style("top", event.pageY + "px")
					.html(`
						<strong>${d.key}</strong><br>
						Continente: ${d.continent}<br>
						Máximo: $${d.value.max.toFixed(2)}<br>
						Q3: $${d.value.q3.toFixed(2)}<br>
						Mediana: $${d.value.median.toFixed(2)}<br>
						Q1: $${d.value.q1.toFixed(2)}<br>
						Mínimo: $${d.value.min.toFixed(2)}
					`);
				
				d3.select(this).selectAll('line, rect')
					.style('stroke-width', 2.5);
			})
			.on("mouseout", function(d) {
				tooltip.style("opacity", 0);
				
				d3.select(this).selectAll('line, rect')
					.style('stroke-width', null);
				d3.select(this).select('line[y1*="median"]')
					.style('stroke-width', 2);
			});
	}
	
	$: if(container && data && Object.keys(colors).length > 0) {
		drawBoxplot();
	}

</script>

<style>
	#tooltip {
		position: absolute;
		text-align: left;
		padding: 8px;
		font: 12px sans-serif;
		background: lightsteelblue;
		border: 0px;
		border-radius: 8px;
		pointer-events: none;
		opacity: 0;
		transition: opacity 0.2s;
		
		/* Mágica do posicionamento:
		  - translate(-50%, -110%) move o tooltip:
		    - 50% de sua própria largura para a esquerda (centralizando-o horizontalmente no cursor)
		    - 110% de sua própria altura para cima (colocando-o acima do cursor com uma pequena margem)
		*/
		transform: translate(-350%, -150%);
	}
</style>

<div id="tooltip"></div>
<div bind:this={container} style="width: 900px; height: 350px; margin-left: 200px;"></div>