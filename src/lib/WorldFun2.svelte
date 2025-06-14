<script>
  import * as d3 from 'd3';
  import { onMount } from 'svelte';

  export let data = []; // Universidades
  
  let container;
  let search = '';
  let selectedCountries = [];
  let circlesSize = 4;
  let circlesColor = '#ff5733';
  let circlesOpacity = 0.8;
  let pinWidth = 50;
  let pinHeight = 50;
  let tooltip;
  let isAnimating = false;

  let svg, g, states, path, projection, zoom, circles;
  let world;

  const countriesISO = [
    { name: "Algeria", code: "dz", patternLoaded: false },
    { name: "Argentina", code: "ar", patternLoaded: false },
    { name: "Australia", code: "au", patternLoaded: false },
    { name: "Austria", code: "at", patternLoaded: false },
    { name: "Bahrain", code: "bh", patternLoaded: false },
    { name: "Bangladesh", code: "bd", patternLoaded: false },
    { name: "Belgium", code: "be", patternLoaded: false },
    { name: "Brazil", code: "br", patternLoaded: false },
    { name: "Bulgaria", code: "bg", patternLoaded: false },
    { name: "Canada", code: "ca", patternLoaded: false },
    { name: "China", code: "cn", patternLoaded: false },
    { name: "Colombia", code: "co", patternLoaded: false },
    { name: "Croatia", code: "hr", patternLoaded: false },
    { name: "Cyprus", code: "cy", patternLoaded: false },
    { name: "Czech Republic", code: "cz", patternLoaded: false },
    { name: "Denmark", code: "dk", patternLoaded: false },
    { name: "Dominican Republic", code: "do", patternLoaded: false },
    { name: "Ecuador", code: "ec", patternLoaded: false },
    { name: "Egypt", code: "eg", patternLoaded: false },
    { name: "El Salvador", code: "sv", patternLoaded: false },
    { name: "Finland", code: "fi", patternLoaded: false },
    { name: "France", code: "fr", patternLoaded: false },
    { name: "Germany", code: "de", patternLoaded: false },
    { name: "Ghana", code: "gh", patternLoaded: false },
    { name: "Greece", code: "gr", patternLoaded: false },
    { name: "Hong Kong", code: "hk", patternLoaded: false },
    { name: "Hungary", code: "hu", patternLoaded: false },
    { name: "Iceland", code: "is", patternLoaded: false },
    { name: "India", code: "in", patternLoaded: false },
    { name: "Indonesia", code: "id", patternLoaded: false },
    { name: "Ireland", code: "ie", patternLoaded: false },
    { name: "Israel", code: "il", patternLoaded: false },
    { name: "Italy", code: "it", patternLoaded: false },
    { name: "Japan", code: "jp", patternLoaded: false },
    { name: "Kuwait", code: "kw", patternLoaded: false },
    { name: "Lebanon", code: "lb", patternLoaded: false },
    { name: "Luxembourg", code: "lu", patternLoaded: false },
    { name: "Malaysia", code: "my", patternLoaded: false },
    { name: "Mexico", code: "mx", patternLoaded: false },
    { name: "Morocco", code: "ma", patternLoaded: false },
    { name: "Netherlands", code: "nl", patternLoaded: false },
    { name: "New Zealand", code: "nz", patternLoaded: false },
    { name: "Nigeria", code: "ng", patternLoaded: false },
    { name: "Norway", code: "no", patternLoaded: false },
    { name: "Panama", code: "pa", patternLoaded: false },
    { name: "Peru", code: "pe", patternLoaded: false },
    { name: "Poland", code: "pl", patternLoaded: false },
    { name: "Portugal", code: "pt", patternLoaded: false },
    { name: "Romania", code: "ro", patternLoaded: false },
    { name: "Russia", code: "ru", patternLoaded: false },
    { name: "Saudi Arabia", code: "sa", patternLoaded: false },
    { name: "Serbia", code: "rs", patternLoaded: false },
    { name: "Singapore", code: "sg", patternLoaded: false },
    { name: "Slovenia", code: "si", patternLoaded: false },
    { name: "South Africa", code: "za", patternLoaded: false },
    { name: "Spain", code: "es", patternLoaded: false },
    { name: "Sweden", code: "se", patternLoaded: false },
    { name: "Switzerland", code: "ch", patternLoaded: false },
    { name: "Thailand", code: "th", patternLoaded: false },
    { name: "Tunisia", code: "tn", patternLoaded: false },
    { name: "Turkey", code: "tr", patternLoaded: false },
    { name: "Ukraine", code: "ua", patternLoaded: false },
    { name: "Uruguay", code: "uy", patternLoaded: false },
    { name: "USA", code: "us", patternLoaded: false },
    { name: "Uzbekistan", code: "uz", patternLoaded: false }
  ];

  async function loadWorld() {
    world = await d3.json('https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson');
  }
  
  function zoomed(event) {
    const { transform } = event;
    g.attr("transform", transform);
    g.attr("stroke-width", 1 / transform.k);
    
    if (circles) {
      circles.attr("r", circlesSize / transform.k);
    }

    const maxPinSize = 13;

    g.selectAll("image.pin")
      .attr("width", d => Math.min(pinWidth / transform.k, maxPinSize))
      .attr("height", d => Math.min(pinHeight / transform.k, maxPinSize))
      .attr("x", d => (projection([+d.lng, +d.lat])?.[0] || 0) - Math.min(pinWidth / transform.k, maxPinSize) / 2)
      .attr("y", d => (projection([+d.lng, +d.lat])?.[1] || 0) - Math.min(pinHeight / transform.k, maxPinSize));
    }

  function draw() {
    const width = container.clientWidth;
    const height = Math.min(width * 0.6, 800);

    projection = d3.geoNaturalEarth1()
      .scale(width / 5.8)
      .translate([width / 2, height / 2]);

    path = d3.geoPath(projection);

    zoom = d3.zoom()
      .scaleExtent([1, 12])
      .on("zoom", zoomed);

    // svg = d3.select(container)
    //   .html('')
    //   .append("svg")
    //   .attr("width", width)
    //   .attr("height", height)
    //   .attr("viewBox", [0, 0, width, height])
    //   .attr("style", "max-width: 100%; height: auto;")
    //   .call(zoom);

    d3.select(container).select("svg").remove();

    svg = d3.select(container)
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .attr("viewBox", [0, 0, width, height])
      .attr("style", "max-width: 100%; height: auto;")
      .call(zoom);

    g = svg.append("g");
    svg.append("defs");

    states = g.append("g")
      .attr("fill", "#ccc")
      .selectAll("path")
      .data(world.features)
      .join("path")
      .attr("d", path)
      .attr("stroke", "#999")
      .attr("stroke-width", 0.5)
      .on("click", clicked)
      .on("mouseover", function() {
        d3.select(this).attr("fill", "#aaa");
      })
      .on("mouseout", function() {
        d3.select(this).attr("fill", "#ccc");
      });

    states.append("title").text(d => d.properties.name);

    if (data.length > 0) {
      circles = g.append("g")
        .selectAll("circle")
        .data(data)
        .join("circle")
        .attr("cx", d => projection([+d.lng, +d.lat])?.[0] || 0)
        .attr("cy", d => projection([+d.lng, +d.lat])?.[1] || 0)
        .attr("r", circlesSize)
        .attr("fill", circlesColor)
        .attr("opacity", circlesOpacity)
        .style("cursor", "pointer")
        .on("mousemove", (event, d) => {
          const [x, y] = d3.pointer(event, container);
          tooltip
            .html(`
              <strong>${d.University}</strong><br/>
              ${d.City}, ${d.Country}<br/>
              Tuition (média): $${d.Tuition_USD}<br/>
              Aluguel: $${d.Rent_USD}<br/>
              Seguro: $${d.Insurance_USD}<br/>
              Câmbio (USD): ${d.Exchange_Rate}<br/>
              Ranking Mundial: ${d.world_rank}
            `)
            .style("left", `${x + 15}px`)
            .style("top", `${y + 15}px`)
            .style("opacity", 1);
        })
        .on("mouseout", () => {
          tooltip.style("opacity", 0);
        })
        .on("click", (event, d) => {
          event.stopPropagation(); // Evita conflito com clique no país
          const [x, y] = projection([+d.lng, +d.lat]);
          const scale = 4;
          const translate = [width / 2 - scale * x, height / 2 - scale * y];

          svg.transition()
            .duration(1000)
            .call(
              zoom.transform,
              d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale)
            );
        });
    }
    
  }

  function reset(countryName) {
    if (countryName) {
      let indexToRemove = selectedCountries.findIndex(element => element === countryName);
      selectedCountries.splice(indexToRemove, 1);

      const className = countryName.replace(/\s+/g, '-');

      // Animação de saída dos pins antes de removê-los
      g.selectAll(`image.pin.${className}`)
        .transition()
        .duration(400)
        .ease(d3.easeExpIn)
        .attr("y", d => (projection([+d.lng, +d.lat])?.[1] || 0) - pinHeight - 100)
        .style("opacity", 0)
        .on("end", function() {
          d3.select(this).remove();
        });

      // Esconde o retângulo da bandeira (não remove)
      g.selectAll(`.flag-${className}`)
        .transition()
        .duration(300)
        .style("opacity", 0);
      
      g.selectAll(`.border-${className}`)
        .transition()
        .duration(300)
        .style("opacity", 0);

      states.transition().attr("fill", "#ccc");
      return;
    }

    selectedCountries.forEach(country => {
    const className = country.replace(/\s+/g, '-');

    g.selectAll(`image.pin.${className}`)
      .transition()
      .duration(400)
      .ease(d3.easeExpIn)
      .attr("y", d => (projection([+d.lng, +d.lat])?.[1] || 0) - pinHeight - 100)
      .style("opacity", 0)
      .on("end", function () {
        d3.select(this).remove();
      });

    g.selectAll(`.flag-${className}`)
      .transition()
      .duration(300)
      .style("opacity", 0);

    g.selectAll(`.border-${className}`)
      .transition()
      .duration(300)
      .style("opacity", 0);
  });

  selectedCountries = [];

  setTimeout(() => {
    svg.transition().duration(750).call(
      zoom.transform,
      d3.zoomIdentity
    );
  }, 500);
  }

  function clicked(event, d) {
    event.stopPropagation();
    const countryName = d.properties.name;

    // Desseleciona se clicar no mesmo país
    if (selectedCountries.includes(countryName)) {
      reset(countryName);
      return;
    }

    isAnimating = true;
    selectedCountries.push(countryName);

    const match = countriesISO.find(c => c.name.toLowerCase() === countryName.toLowerCase());
    if (!match) return;
    const code = match.code.toLowerCase();

    // Calcula área do país
    const [[x0, y0], [x1, y1]] = path.bounds(d);
    const centerX = (x0 + x1) / 2;
    const centerY = (y0 + y1) / 2;
    const viewWidth = (x1 - x0);
    const viewHeight = (y1 - y0);
    const extra = 0.7;
    const size = Math.max(viewWidth, viewHeight) * (1 + extra);

    // Só cria padrão e máscara se ainda não estiver criado
    if (!match.patternLoaded) {
      svg.select("defs")
        .append("clipPath")
        .attr("id", `flag-clip-${code}`)
        .append("path")
        .attr("d", path(d))
        .attr("fill", "transparent")
        .style("pointer-events", "visible");

      svg.select("defs")
        .append("pattern")
        .attr("id", `flag-pattern-${code}`)
        .attr("patternUnits", "userSpaceOnUse")
        .attr("x", centerX - size / 2)
        .attr("y", centerY - size / 2)
        .attr("width", size)
        .attr("height", size)
        .append("image")
        .attr("xlink:href", `https://flagcdn.com/${code}.svg`)
        .attr("width", size)
        .attr("height", size)
        .attr("preserveAspectRatio", "xMidYMid slice");

      match.patternLoaded = true;
    }

    // Reutiliza ou cria a flag
    let flagId = `flag-${code}`;
    let borderId = `border-${code}`;
    let existingFlag = g.select(`#${flagId}`);
    let existingBorder = g.select(`#${borderId}`);

    const countryClass = countryName.replace(/\s+/g, '-');

    if (existingFlag.empty()) {
      g.append("rect")
        .attr("id", flagId)
        .attr("class", `country-flag flag-${countryClass}`)
        .attr("x", centerX - (viewWidth * (1 + extra)) / 2)
        .attr("y", centerY - (viewHeight * (1 + extra)) / 2)
        .attr("width", viewWidth * (1 + extra))
        .attr("height", viewHeight * (1 + extra))
        .attr("clip-path", `url(#flag-clip-${code})`)
        .style("fill", `url(#flag-pattern-${code})`)
        .style("opacity", 0)
        .style("pointer-events", "none")
        .transition()
        .duration(500)
        .style("opacity", 1);

      g.append("path")
        .attr("id", borderId)
        .attr("class", `flag-border border-${countryClass}`)
        .attr("d", path(d))
        .attr("fill", "none")
        .attr("stroke", "#333")         // cor da borda
        .attr("stroke-width", 0.7)      // espessura da borda
        .style("pointer-events", "none")
        .style("opacity", 0)
        .transition()
        .duration(500)
        .style("opacity", 1);
      
      g.append("path")
        .attr("class", `hover-area hover-${countryClass}`)
        .attr("d", path(d))
        .attr("fill", "transparent")
        .style("pointer-events", "visible")
        .style("opacity", 0.7) 
        .attr("clip-path", `url(#flag-hover-${code})`)
        .on("mouseover", function() {
          d3.select(this).style("opacity", 1);
          d3.select(`#${borderId}`)
            .attr("stroke", "red")
            .attr("stroke-width", 1.0)
            .raise();
        })
        .on("mouseout", function() {
          d3.select(this).style("opacity", 0.7);
          d3.select(`#${borderId}`)
            .attr("stroke", "#333")
            .attr("stroke-width", 0.7);
        })
        .on("click", function(event) {
          event.stopPropagation();
          clicked(event, d); 
        });
    } else {
      existingFlag
        .transition()
        .duration(400)
        .style("opacity", 1);
      existingBorder
        .transition()
        .duration(400)
        .style("opacity", 1);
    }

    g.select(`#${borderId}`).each(function() {
      this.parentNode.appendChild(this);
    });
    
    g.selectAll("image.pin").each(function () {
        this.parentNode.appendChild(this);
      });

    // Adiciona os novos pins com efeito de queda e tooltip
    const newPins = g.selectAll(`image.pin.${countryClass}`)
      .data(
        Array.from(
          d3.group(
            data.filter(d => d.Country === countryName),
            d => d.University
          ).values(),
          v => v[0]
        )
      )
      .join("image")
      .attr("class", `pin ${countryClass}`)
      .attr("href", "images/pinMap.png")
      .attr("width", pinWidth)
      .attr("height", pinHeight)
      .attr("x", d => (projection([+d.lng, +d.lat])?.[0] || 0) - pinWidth / 2)
      .attr("y", d => (projection([+d.lng, +d.lat])?.[1] || 0) - pinHeight - 50)
      .style("opacity", 0)
      .style("cursor", "pointer")
      .style("pointer-events", "auto")
      .on("mousemove", function(event, d) {
        d3.select(this).raise(); 

        const [x, y] = d3.pointer(event, container);
        tooltip
          .html(`
            <strong>${d.University}</strong><br/>
            ${d.City}, ${d.Country}<br/>
            Tuition (média): $${d.Tuition_USD}<br/>
            Aluguel: $${d.Rent_USD}<br/>
            Seguro: $${d.Insurance_USD}<br/>
            Câmbio (USD): ${d.Exchange_Rate}<br/>
            Ranking Mundial: ${d.world_rank}
          `)
          .style("left", `${x + 15}px`)
          .style("top", `${y + 15}px`)
          .style("opacity", 1);
      })
      .on("mouseout", () => tooltip.style("opacity", 0))
      .on("click", (event, d) => {
        event.stopPropagation();
        const [x, y] = projection([+d.lng, +d.lat]);
        const scale = 4;
        const translate = [svg.attr("width") / 2 - scale * x, svg.attr("height") / 2 - scale * y];

        svg.transition()
          .duration(500)
          .call(
            zoom.transform,
            d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale)
          );
      });

    // Aplica zoom e animação
    svg.transition().duration(700).call(
      zoom.transform,
      d3.zoomIdentity
        .translate(svg.attr("width") / 2, svg.attr("height") / 2)
        .scale(Math.min(8, 0.9 / Math.max(
          viewWidth / svg.attr("width"), 
          viewHeight / svg.attr("height")
        )))
        .translate(-centerX, -centerY)
    ).on("end", () => {
      const fixedTransform = d3.zoomTransform(svg.node());

      newPins
        .attr("y", d => (projection([+d.lng, +d.lat])?.[1] || 0) - pinHeight - 50)
        .style("opacity", 0)
        .transition()
        .delay((_, i) => i * 50)
        .duration(600)
        .ease(d3.easeExpOut)
        .attr("y", d => (projection([+d.lng, +d.lat])?.[1] || 0) - (pinHeight / fixedTransform.k))
        .style("opacity", 1);
    });

    isAnimating = false;
  }


  function zoomToCountry(name) {
    const match = countriesISO.find(c => c.name.toLowerCase() === name.toLowerCase());
    if (!match) return;

    const country = world.features.find(f => 
      f.properties.name.toLowerCase() === name.toLowerCase()
    );
    if (!country) return;

    const event = { stopPropagation: () => {} };
    clicked(event, country);
  }

  onMount(async () => {
    await loadWorld();
    tooltip = d3.select(container)
      .append("div")
      .attr("class", "tooltip")
      .style("position", "absolute")
      .style("padding", "10px")
      .style("background", "rgba(0, 0, 0, 0.8)")
      .style("color", "#fff")
      .style("border-radius", "4px")
      .style("font-size", "12px")
      .style("pointer-events", "none")
      .style("z-index", "10")
      .style("opacity", 0);

    draw();
    
    window.addEventListener('resize', () => {
      if (world) draw();
    });
  });
</script>

<style>
  input {
    margin-bottom: 10px;
    padding: 8px 12px;
    width: 100%;
    max-width: 400px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
  }
  .map-container {
    position: relative;
    width: 100%;
    margin: 0 auto;
    overflow: hidden;
    border: 1px solid #eee;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  }
  button {
    margin-left: 10px;
    padding: 8px 12px;
    background: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.2s;
  }
  button:hover {
    background: #e0e0e0;
  }
  .flag-border:hover {
    stroke: red;
    stroke-width: 1.1;
    opacity: 1 !important;
  }
</style>

<div class="map-container">
  <input
    list="countries"
    bind:value={search}
    placeholder="Digite ou selecione um país"
    on:keydown={(e) => {
      if (e.key === 'Enter') {
        zoomToCountry(search);
      }
    }}
  />
  <datalist id="countries">
    {#each countriesISO as c}
      <option value={c.name} />
    {/each}
  </datalist>
  <button on:click={() => reset()}>
    Resetar Mapa
  </button>
  <div bind:this={container} style="width: 100%; height: auto;"></div>
</div>