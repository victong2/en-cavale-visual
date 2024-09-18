<template>
  <div ref="plotElement" class="full-screen-component"></div>
</template>

<script lang="ts">
import Plotly from 'plotly.js-dist-min'

export default {
  name: 'PlotlyChart',
  props: {
    data: Array,
    layout: Object
  },
  mounted() {
    this.renderChart()
  },
  methods: {
    renderChart() {
      // @ts-ignore
      Plotly.newPlot(this.$refs.plotElement as HTMLElement, this.data, this.layout)
    }
  },
  watch: {
    data: 'renderChart',
    layout: 'renderChart'
  }
}
</script>

<style scoped>
.full-screen-component {
  height: 95vh; /* 100% of the viewport height */
  width: 95vw; /* 100% of the viewport width */
  display: flex; /* Optionally use flexbox to center content */
  justify-content: center;
  align-items: center;
}
</style>
