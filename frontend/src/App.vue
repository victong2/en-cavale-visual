<!-- <script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script> -->

<!-- <template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template> -->

<template>
  <div>
    <h1>Data from Backend</h1>
    <div v-if="error">{{ error }}</div>
    <div v-else>Loading...</div>
  </div>
  <PlotlyChart v-if="data" :data="chartData" :layout="chartLayout" />
</template>

<script lang="ts">
import axios from 'axios'
// import HelloWorld from './components/HelloWorld.vue'

import PlotlyChart from './components/PlotlyChart.vue'

export default {
  name: 'App',
  components: {
    PlotlyChart
  },
  methods: {
    changeName(event: Event) {
      this.name = 'Batman'
      console.log('Event', event)
    },
    add(a: number, b: number, c: number) {
      return a + b + c
    },
    increment(num: number, event: Event) {
      this.count += num
      console.log('Event', event)
    },
    decrement(num: number) {
      this.count -= num
    }
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
      count: 0,
      name: 'Victor',
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
