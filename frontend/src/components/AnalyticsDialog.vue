<template>
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">

    <div class="bg-white w-full max-w-5xl rounded-2xl p-8 shadow-2xl relative">

      <!-- Header -->
      <div class="flex justify-between items-center mb-8">
        <h2 class="text-3xl font-bold text-gray-900">
          Analytics Overview
        </h2>

        <button
          @click="$emit('close')"
          class="text-gray-400 hover:text-red-500 text-2xl font-bold"
        >
          ✕
        </button>
      </div>

      <!-- Charts Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">

        <!-- Status Chart -->
        <div class="bg-gray-50 rounded-2xl p-6 shadow-md hover:shadow-xl transition">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">
            Status Distribution
          </h3>
          <div class="h-80">
            <canvas ref="statusChart"></canvas>
          </div>
        </div>

        <!-- City Chart -->
        <div class="bg-gray-50 rounded-2xl p-6 shadow-md hover:shadow-xl transition">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">
            Jobs by City
          </h3>
          <div class="h-80">
            <canvas ref="cityChart"></canvas>
          </div>
        </div>

        <!-- State Chart -->
        <div class="bg-gray-50 rounded-2xl p-6 shadow-md hover:shadow-xl transition">
          <h3 class="text-lg font-semibold text-gray-800 mb-4">
            Jobs by State
          </h3>
          <div class="h-80">
            <canvas ref="stateChart"></canvas>
          </div>
        </div>

      </div>

      <!-- Footer -->
      <div class="flex justify-end mt-8">
        <button
          @click="$emit('close')"
          class="px-6 py-2.5 rounded-lg bg-blue-600 text-white font-semibold
                 hover:bg-blue-700 shadow-lg transition"
        >
          Close
        </button>
      </div>

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

  createChart(statusChart.value, res.data.status, "status")
  createChart(cityChart.value, res.data.city, "city")
  createChart(stateChart.value, res.data.state, "state")
})

const createChart = (canvas, data, key) => {
  new Chart(canvas, {
    type: "pie",
    data: {
      labels: data.map(d => d[key]),
      datasets: [{
        data: data.map(d => d.count),
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "right",
          align: "start",
          labels: {
            boxWidth: 12,
            padding: 10,
            font: { size: 11 },
            usePointStyle: true
          }
        }
      },
      layout: {
        padding: {
          right: 20
        }
      }
    }
  })
}
</script>
