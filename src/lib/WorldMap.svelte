<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  let map;

  onMount(async () => {
    if (typeof window === 'undefined') return;

    const L = await import('leaflet');

    const geoData = await (await fetch('/countries.geojson')).json();
    const costData = await (await fetch('/education.json')).json();

    const costByCountry = {};
    costData.forEach(d => {
      costByCountry[d.Country.toLowerCase()] = +d.Total_Cost_USD;
    });

    const values = Object.values(costByCountry);
    const colorScale = d3.scaleQuantize()
      .domain([d3.min(values), d3.max(values)])
      .range(d3.schemeBlues[7]);

    map = L.map('map').setView([20, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    L.geoJSON(geoData, {
      style: feature => {
        const name = feature.properties.name.toLowerCase();
        const cost = costByCountry[name];
        return {
          fillColor: cost ? colorScale(cost) : '#ccc',
          color: 'white',
          weight: 1,
          fillOpacity: 0.7
        };
      },
      onEachFeature: (feature, layer) => {
        const name = feature.properties.name;
        const cost = costByCountry[name.toLowerCase()];
        layer.bindTooltip(`${name}<br>Custo: ${cost ? `$${cost.toLocaleString()}` : 'N/A'}`);
      }
    }).addTo(map);
  });
</script>

<style>
  #map {
    height: 600px;
    width: 100%;
    border-radius: 12px;
  }
</style>

<div id="map"></div>
