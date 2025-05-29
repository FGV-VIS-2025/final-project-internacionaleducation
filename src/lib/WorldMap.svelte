<script>
  import { onMount } from 'svelte';
  import * as d3 from 'd3';

  let map;
  let mapContainer;

  onMount(async () => {
    const L = await import('leaflet');

    const [geoData, costData] = await Promise.all([
      fetch('/countries.geojson').then(r => r.json()),
      fetch('/education.json').then(r => r.json())
    ]);

    const countryNameMap = {
      "usa": "united states of america",
      "uk": "united kingdom",
      "uae": "united arab emirates"
    };

    const countryCosts = {};

    costData.forEach(d => {
      const name = (d.Country || '').toLowerCase().trim();
      const normalized = countryNameMap[name] || name;

      const duration = +d.Duration_Years || 0;
      const tuition = +d.Tuition_USD || 0;
      const rent = (+d.Rent_USD || 0) * 12 * duration;
      const visa = +d.Visa_Fee_USD || 0;
      const insurance = +d.Insurance_USD || 0;
      const totalCost = tuition + rent + visa + insurance;

      if (!countryCosts[normalized]) {
        countryCosts[normalized] = [];
      }
      countryCosts[normalized].push(totalCost);
    });

    const avgCostByCountry = {};
    for (const [country, costs] of Object.entries(countryCosts)) {
      avgCostByCountry[country] = costs.reduce((a, b) => a + b, 0) / costs.length;
    }

    const values = Object.values(avgCostByCountry);
    const min = Math.min(...values);
    const max = Math.max(...values);

    const colorScale = d3.scaleLinear()
      .domain([min, max])
      .range(['#edf8fb', '#006d2c']);

    geoData.features.forEach(f => {
      const name = f.properties.name.toLowerCase();
      f.properties.avgCost = avgCostByCountry[name] || null;
    });

    map = L.map(mapContainer).setView([20, 0], 2);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    function style(feature) {
      const cost = feature.properties.avgCost;
      return {
        fillColor: cost ? colorScale(cost) : '#ccc',
        weight: 0.5,
        opacity: 1,
        color: 'gray',
        fillOpacity: 0.8
      };
    }

    function onEachFeature(feature, layer) {
      const name = feature.properties.name;
      const cost = feature.properties.avgCost;
      const popupContent = `<strong>${name}</strong><br/>
        Custo médio: ${cost ? `$${cost.toLocaleString(undefined, { maximumFractionDigits: 0 })}` : 'N/A'}`;
      layer.bindPopup(popupContent);
    }

    L.geoJSON(geoData, {
      style,
      onEachFeature
    }).addTo(map);
  });
</script>

<style>
  #map {
    width: 100%;
    height: 100vh;
    border-radius: 12px;
  }
</style>

<div id="map" bind:this={mapContainer}></div>
