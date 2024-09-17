<template>
  <div>
    <h1>Data from Backend</h1>
    <div v-if="error">{{ error }}</div>
    <div v-if="data">{{ data }}</div>
    <div v-else>Loading...</div>
  </div>
  <PlotlyChart v-if="data" :data="chartData" :layout="chartLayout" />
</template>

<script lang="ts">
import axios from 'axios'

import PlotlyChart from './components/PlotlyChart.vue'

export default {
  name: 'App',
  components: {
    PlotlyChart
  },
  mounted() {
    const url = '/api/spending/countries/'
    // Make an API call to your backend when the component is mounted
    axios
      .get(url)
      .then((response) => {
        console.log(response)
        // Handle the response and assign it to the data property
        this.data = response.data
        this.chartData[0].x = response.data.country
        this.chartData[0].y = response.data.spending
      })
      .catch((error) => {
        // Handle errors
        this.error = error.message
      })
  },
  data() {
    return {
      data: null,
      error: null,
      chartData: [
        {
          x: null,
          y: null,
          type: 'bar'
        }
      ],
      chartLayout: {
        title: 'Spending'
      }
    }
  }
}
</script>

<style scoped></style>
