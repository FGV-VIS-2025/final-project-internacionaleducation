<script lang="ts">
  import * as d3 from 'd3';

  export let data = [];

  // Preprocess data
  let grouped = d3.group(data, d => d.Level);

  let boxData = Array.from(grouped, ([level, items]) => {
    let totalCosts = items.map(d => 
      d.Tuition_USD * d.Duration_Years +
      d.Rent_USD * d.Duration_Years * 12 +
      d.Insurance_USD +
      d.Visa_Fee_USD
    );

    return {
      level,
      q1: d3.quantile(totalCosts, 0.25),
      median: d3.median(totalCosts),
      q3: d3.quantile(totalCosts, 0.75),
      min: d3.min(totalCosts),
      max: d3.max(totalCosts)
    };
  });
</script>

<svg width="600" height="400">
  {#each boxData as box, i}
    <g transform={`translate(${100 + i * 150}, 0)`}>
      <!-- Box -->
      <rect 
        x="-20" 
        y={400 - box.q3 / 500} 
        width="40" 
        height={(box.q3 - box.q1) / 500} 
        fill="lightblue"
        stroke="black" />
      
      <!-- Median line -->
      <line 
        x1="-20" 
        x2="20" 
        y1={400 - box.median / 500} 
        y2={400 - box.median / 500} 
        stroke="black" />
      
      <!-- Whiskers -->
      <line 
        x1="0" 
        x2="0" 
        y1={400 - box.max / 500} 
        y2={400 - box.q3 / 500} 
        stroke="black" />
      <line 
        x1="0" 
        x2="0" 
        y1={400 - box.q1 / 500} 
        y2={400 - box.min / 500} 
        stroke="black" />
      
      <!-- Min/Max lines -->
      <line 
        x1="-10" 
        x2="10" 
        y1={400 - box.max / 500} 
        y2={400 - box.max / 500} 
        stroke="black" />
      <line 
        x1="-10" 
        x2="10" 
        y1={400 - box.min / 500} 
        y2={400 - box.min / 500} 
        stroke="black" />
      
      <!-- Labels -->
      <text 
        x="0" 
        y="390" 
        text-anchor="middle">
        {box.level}
      </text>
    </g>
  {/each}
</svg>
