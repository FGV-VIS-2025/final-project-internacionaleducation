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
      const country = d.Country.toLowerCase();
      costByCountry[country] = {
        total: +d.Total_Cost_USD,
        living: +d.Living_Cost_Index
      };
    });

    const values = Object.values(costByCountry).map(d => d.total);
    const colorScale = d3.scaleQuantize()
      .domain([d3.min(values), d3.max(values)])
      .range(d3.schemeBlues[7]);

    map = L.map('map').setView([20, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    function highlightFeature(e) {
      const layer = e.target;
      layer.setStyle({
        weight: 3,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.9
      });

      layer.bringToFront();
    }

    function resetHighlight(e) {
      geojson.resetStyle(e.target);
    }

    function zoomToFeature(e) {
      map.fitBounds(e.target.getBounds());
    }

    function onEachFeature(feature, layer) {
      const name = feature.properties.name;
      const countryData = costByCountry[name.toLowerCase()];
      const total = countryData?.total;
      const living = countryData?.living;

      const tooltipContent = `
        <strong>${name}</strong><br>
        Custo Total: ${total ? `$${total.toLocaleString()}` : 'N/A'}<br>
        Índice de Custo de Vida: ${living ?? 'N/A'}
      `;
      layer.bindTooltip(tooltipContent);

      layer.on({
        mouseover: highlightFeature,
        mouseout: resetHighlight,
        click: zoomToFeature
      });
    }

    const geojson = L.geoJSON(geoData, {
      style: feature => {
        const name = feature.properties.name.toLowerCase();
        const cost = costByCountry[name]?.total;
        return {
          fillColor: cost ? colorScale(cost) : '#ccc',
          color: 'white',
          weight: 1,
          fillOpacity: 0.7
        };
      },
      onEachFeature
    }).addTo(map);

    // 🎨 Legenda
    const legend = L.control({ position: 'bottomright' });
    legend.onAdd = () => {
      const div = L.DomUtil.create('div', 'info legend');
      const grades = colorScale.range().map(color => {
        const extent = colorScale.invertExtent(color);
        return { color, from: Math.round(extent[0]), to: Math.round(extent[1]) };
      });

      div.innerHTML = '<strong>Custo Total (USD)</strong><br>';
      grades.forEach(({ color, from, to }) => {
        div.innerHTML +=
          `<i style="background:${color}"></i> $${from.toLocaleString()} &ndash; $${to.toLocaleString()}<br>`;
      });

      return div;
    };
    legend.addTo(map);
  });
</script>

<style>
  #map {
    height: 400px;
    width: 100%;
    border-radius: 12px;
    margin-bottom: 1rem;
  }

  .legend {
    line-height: 18px;
    color: #555;
    background: white;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
    font-size: 14px;
  }

  .legend i {
    width: 18px;
    height: 18px;
    float: left;
    margin-right: 8px;
    opacity: 0.7;
    border: 1px solid #ccc;
  }
</style>

<div id="map"></div>
