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
    { name: "Algeria", code: "dz" },
    { name: "Argentina", code: "ar" },
    { name: "Australia", code: "au" },
    { name: "Austria", code: "at" },
    { name: "Bahrain", code: "bh" },
    { name: "Bangladesh", code: "bd" },
    { name: "Belgium", code: "be" },
    { name: "Brazil", code: "br" },
    { name: "Bulgaria", code: "bg" },
    { name: "Canada", code: "ca" },
    { name: "China", code: "cn" },
    { name: "Colombia", code: "co" },
    { name: "Croatia", code: "hr" },
    { name: "Cyprus", code: "cy" },
    { name: "Czech Republic", code: "cz" },
    { name: "Denmark", code: "dk" },
    { name: "Dominican Republic", code: "do" },
    { name: "Ecuador", code: "ec" },
    { name: "Egypt", code: "eg" },
    { name: "El Salvador", code: "sv" },
    { name: "Finland", code: "fi" },
    { name: "France", code: "fr" },
    { name: "Germany", code: "de" },
    { name: "Ghana", code: "gh" },
    { name: "Greece", code: "gr" },
    { name: "Hong Kong", code: "hk" },
    { name: "Hungary", code: "hu" },
    { name: "Iceland", code: "is" },
    { name: "India", code: "in" },
    { name: "Indonesia", code: "id" },
    { name: "Ireland", code: "ie" },
    { name: "Israel", code: "il" },
    { name: "Italy", code: "it" },
    { name: "Japan", code: "jp" },
    { name: "Kuwait", code: "kw" },
    { name: "Lebanon", code: "lb" },
    { name: "Luxembourg", code: "lu" },
    { name: "Malaysia", code: "my" },
    { name: "Mexico", code: "mx" },
    { name: "Morocco", code: "ma" },
    { name: "Netherlands", code: "nl" },
    { name: "New Zealand", code: "nz" },
    { name: "Nigeria", code: "ng" },
    { name: "Norway", code: "no" },
    { name: "Panama", code: "pa" },
    { name: "Peru", code: "pe" },
    { name: "Poland", code: "pl" },
    { name: "Portugal", code: "pt" },
    { name: "Romania", code: "ro" },
    { name: "Russia", code: "ru" },
    { name: "Saudi Arabia", code: "sa" },
    { name: "Serbia", code: "rs" },
    { name: "Singapore", code: "sg" },
    { name: "Slovenia", code: "si" },
    { name: "South Africa", code: "za" },
    { name: "Spain", code: "es" },
    { name: "Sweden", code: "se" },
    { name: "Switzerland", code: "ch" },
    { name: "Thailand", code: "th" },
    { name: "Tunisia", code: "tn" },
    { name: "Turkey", code: "tr" },
    { name: "Ukraine", code: "ua" },
    { name: "Uruguay", code: "uy" },
    { name: "USA", code: "us" },
    { name: "Uzbekistan", code: "uz" }
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

    g.selectAll("image.pin")
      .attr("width", pinWidth / transform.k)
      .attr("height", pinHeight / transform.k)
      .attr("x", d => (projection([+d.lng, +d.lat])?.[0] || 0) - (pinWidth / transform.k) / 2)
      .attr("y", d => (projection([+d.lng, +d.lat])?.[1] || 0) - (pinHeight / transform.k));
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

          // Animação de saída dos pins antes de removê-los
          g.selectAll(`image.pin.${countryName}`)
            .transition()
            .duration(400)
            .ease(d3.easeExpIn)  // Efeito de subida (saindo para cima)
            .attr("y", d => (projection([+d.lng, +d.lat])?.[1] || 0) - pinHeight - 100)  // Subir os pins (fora da tela)
            .style("opacity", 0)  // Desaparecer
            .on("end", function() {
              d3.select(this).remove();  // Remove os elementos após a animação
            });

          g.selectAll(`.flag-${countryName.replace(/\s+/g, '-')}`).remove();
          svg.select(`#flag-clip-${countriesISO.find(c => c.name === countryName)?.code}`).remove();
          svg.select(`#flag-pattern-${countriesISO.find(c => c.name === countryName)?.code}`).remove();

          states.transition().style("fill", "#ccc");

          return;
      }

      selectedCountries = [];

      // Animação de saída para todos os pins
      g.selectAll("image.pin")
        .transition()
        .duration(800)
        .ease(d3.easeExpIn)  // Efeito de subida (saindo para cima)
        .attr("y", d => (projection([+d.lng, +d.lat])?.[1] || 0) - pinHeight - 100)  // Subir os pins (fora da tela)
        .style("opacity", 0)  // Desaparecer
        .on("end", function() {
          d3.select(this).remove();  // Remove os elementos após a animação
        });

      g.selectAll(".flag").remove();  // Remove bandeiras restantes
      svg.transition().duration(750).call(
        zoom.transform,
        d3.zoomIdentity
      );

      // Não precisamos de g.selectAll("image.pin").remove() aqui, pois já removemos na transição
  }

  function clicked(event, d) {
    // if (isAnimating) return;
    event.stopPropagation();
    const countryName = d.properties.name;
    
    // Desseleciona se clicar no mesmo país
    if (selectedCountries.includes(countryName)) {
      reset(countryName);
      return;
    }
    
    isAnimating = true;
    // svg.call(zoom.on("zoom", null));
    // svg.style("pointer-events", "none");

    selectedCountries.push(countryName);

    const match = countriesISO.find(c => c.name.toLowerCase() === countryName.toLowerCase());
    if (!match) return;

    svg.select("defs").select(`#flag-clip-${match.code}`).remove();
    svg.select("defs").select(`#flag-pattern-${match.code}`).remove();

    // Calcula área do país
    const [[x0, y0], [x1, y1]] = path.bounds(d);
    const centerX = (x0 + x1) / 2;
    const centerY = (y0 + y1) / 2;
    const viewWidth = (x1 - x0);
    const viewHeight = (y1 - y0);
    const extra = 0.7; // Margem adicional

    // Cria máscara de recorte
    const ClipPath = svg.select("defs")
      .append("clipPath")
      .attr("id", `flag-clip-${match.code}`)
      .append("path")
      .attr("d", path(d));
    

    // Cria padrão da bandeira
    const size = Math.max(viewWidth, viewHeight) * (1 + extra);

    const Pattern = svg.select("defs")
      .append("pattern")
      .attr("class", `pattern flag ${countryName}`)
      .attr("id", `flag-pattern-${match.code}`)
      .attr("patternUnits", "userSpaceOnUse")
      .attr("width", size)
      .attr("height", size)
      .attr("x", centerX - size / 2)
      .attr("y", centerY - size / 2)
      .append("image")
      .attr("xlink:href", `https://flagcdn.com/${match.code}.svg`)
      .attr("width", size)
      .attr("height", size)
      .attr("preserveAspectRatio", "xMidYMid slice");


    // Cria retângulo com a bandeira
    const Flag = g.append("rect")
      .attr("class", `country-flag ${countryName}`)
      .attr("x", centerX - (viewWidth * (1 + extra)) / 2)
      .attr("y", centerY - (viewHeight * (1 + extra)) / 2)
      .attr("width", viewWidth * (1 + extra))
      .attr("height", viewHeight * (1 + extra))
      .attr("clip-path", `url(#flag-clip-${match.code})`)
      .style("fill", `url(#flag-pattern-${match.code})`)
      .style("opacity", 0)
      .style("pointer-events", "none");

    // Adiciona os novos pins com efeito de queda e tooltip
    const newPins = g.selectAll(`image.pin.${countryName}`)
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
      .attr("class", `pin ${countryName}`)
      .attr("href", "images/pinMap.png")
      .attr("width", pinWidth)
      .attr("height", pinHeight)
      .attr("x", d => (projection([+d.lng, +d.lat])?.[0] || 0) - pinWidth / 2)
      .attr("y", d => (projection([+d.lng, +d.lat])?.[1] || 0) - pinHeight - 50) // começa acima
      .style("opacity", 0)
      .style("cursor", "pointer")
      .style("pointer-events", "auto")
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
      Flag.transition()
        .duration(500)
        .style("opacity", 1);

        const fixedTransform = d3.zoomTransform(svg.node());

        // Agora anima os pins com esse transform fixo
        newPins
          .attr("y", d => (projection([+d.lng, +d.lat])?.[1] || 0) - pinHeight - 50) // posição inicial acima
          .style("opacity", 0) // invisível no início
          .transition()
          .delay((_, i) => i * 50)  // cascata entre os pins
          .duration(600)
          .ease(d3.easeExpOut)  // efeito de queda (bounce)
          .attr("y", d => (projection([+d.lng, +d.lat])?.[1] || 0) - (pinHeight / fixedTransform.k)) // posição final
          .style("opacity", 1);
    }); 

    isAnimating = false;
    // svg.call(zoom.on("zoom", zoomed));
    // svg.style("pointer-events", "auto"); 
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
  <button on:click={reset}>
    Resetar Mapa
  </button>
  <div bind:this={container} style="width: 100%; height: auto;"></div>
</div>