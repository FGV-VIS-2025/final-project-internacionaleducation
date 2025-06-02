<script>
  import { onMount, createEventDispatcher } from 'svelte';
  import * as d3 from 'd3';

  const dispatch = createEventDispatcher();

  let map;
  let mapContainer;
  let marker;  // Novo: referência ao marcador

  let cityInput = '';
  let suggestions = [];
  const MAPBOX_TOKEN = 'pk.eyJ1IjoidmluYXNxdWUiLCJhIjoiY21iZHNiaG9uMW5rejJpcHY3Y3Rwem9zbyJ9.GM-u07CTOXFnKXA_N99aoQ';

  async function searchCities() {
    if (cityInput.length < 3) {
      suggestions = [];
      return;
    }

    const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(cityInput)}.json?access_token=${MAPBOX_TOKEN}&types=place&language=pt&limit=5`;
    const res = await fetch(url);
    const data = await res.json();

    suggestions = data.features.map(f => ({
      name: f.text,
      place_name: f.place_name,
      center: f.center  // [lng, lat]
    }));
  }

  function goToCity(suggestion) {
    cityInput = suggestion.place_name;
    const [lng, lat] = suggestion.center;

    map.setView([lat, lng], 8);

    // Novo: adiciona ou move marcador
    if (marker) {
      marker.setLatLng([lat, lng]);
    } else {
      marker = L.marker([lat, lng]).addTo(map);
    }

    dispatch('select', { lat, lng });
    suggestions = [];
  }

  function clearSearch() {
    cityInput = '';
    suggestions = [];
    if (marker) {
      map.removeLayer(marker);
      marker = null;
    }
  }

  onMount(async () => {
    const L = await import('leaflet');

    const [geoData, costData] = await Promise.all([
      fetch('./countries.geojson').then(r => r.json()),
      fetch('./education.json').then(r => r.json())
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

    L.geoJSON(geoData, { style }).addTo(map);

    map.on('click', e => {
      const { lat, lng } = e.latlng;
      dispatch('select', { lat, lng });
    });
  });
</script>

<style>
  #map {
    width: 100%;
    height: 30vh;
    border-radius: 12px;
  }

  .search-container {
    margin-bottom: 0.5rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .input-group {
    display: flex;
    gap: 0.25rem;
  }

  input[type="text"] {
    flex: 1;
    padding: 0.4rem;
    border-radius: 6px;
    border: 1px solid #ccc;
  }

  button.clear-btn {
    padding: 0.4rem 0.6rem;
    border: none;
    background: #e0e0e0;
    border-radius: 6px;
    cursor: pointer;
  }

  button.clear-btn:hover {
    background: #d0d0d0;
  }

  .suggestions {
    border: 1px solid #ccc;
    border-radius: 4px;
    background: white;
    list-style: none;
    padding: 0;
    margin: 0;
    max-height: 150px;
    overflow-y: auto;
  }

  .suggestions li {
    padding: 0.5rem;
    cursor: pointer;
  }

  .suggestions li:hover {
    background: #f0f0f0;
  }
</style>

<div class="search-container">
  <label>
    Pesquisar cidade:
    <div class="input-group">
      <input
        type="text"
        bind:value={cityInput}
        on:input={searchCities}
        placeholder="Digite o nome da cidade..."
      />
      <button class="clear-btn" on:click={clearSearch}>Limpar</button>
    </div>
  </label>

  {#if suggestions.length}
    <ul class="suggestions">
      {#each suggestions as suggestion}
        <li on:click={() => goToCity(suggestion)}>
          {suggestion.place_name}
        </li>
      {/each}
    </ul>
  {/if}
</div>

<div id="map" bind:this={mapContainer}></div>
