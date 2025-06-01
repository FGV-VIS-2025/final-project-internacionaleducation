<script>
  export let text = "";
</script>

<span class="tooltip-container">
  <slot></slot>
  <span class="tooltip-text">{text}</span>
</span>

<style>
.tooltip-container {
  position: relative;
  cursor: help;
  border-bottom: 1px dotted #555;
}

.tooltip-text {
  visibility: hidden;
  width: max-content;
  background-color: rgba(0, 0, 0, 0.75);
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 8px;
  position: absolute;
  z-index: 1;
  bottom: 125%; /* posiciona acima do texto */
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 0.75rem;
  white-space: nowrap;
}

.tooltip-container:hover .tooltip-text {
  visibility: visible;
  opacity: 1;
}
</style>
