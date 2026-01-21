<template>
  <div class="modal">
    <div class="box">
      <h2>Analytics Dashboard</h2>

      <h3>Status Distribution</h3>
      <canvas ref="statusChart"></canvas>

      <h3>Jobs by City</h3>
      <canvas ref="cityChart"></canvas>

      <h3>Jobs by State</h3>
      <canvas ref="stateChart"></canvas>

      <button @click="$emit('close')">Close</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"
import Chart from "chart.js/auto"

const statusChart = ref(null)
const cityChart = ref(null)
const stateChart = ref(null)

onMounted(async () => {
  const res = await api.get("analytics/")

  createChart(statusChart.value, res.data.status, "Status")
  createChart(cityChart.value, res.data.city, "City")
  createChart(stateChart.value, res.data.state, "State")
})

const createChart = (canvas, data, label) => {
  new Chart(canvas, {
    type: "pie",
    data: {
      labels: data.map(d => d[label.toLowerCase()]),
      datasets: [{
        data: data.map(d => d.count),
      }]
    }
  })
}
</script>

<style>
.modal {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.box {
  background: white;
  padding: 20px;
  width: 450px;
  border-radius: 8px;
  text-align: center;
}
</style>
