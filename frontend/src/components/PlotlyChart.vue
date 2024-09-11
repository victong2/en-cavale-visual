<template>
  <div ref="plotElement"></div>
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
      Plotly.newPlot(this.$refs.plotElement as HTMLElement, this.data, this.layout)
    }
  },
  watch: {
    data: 'renderChart',
    layout: 'renderChart'
  }
}
</script>
