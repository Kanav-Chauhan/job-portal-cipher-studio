<template>
  <div class="container">
    <h1>Job Dashboard</h1>

    <!-- Top Controls -->
    <div class="top-bar">
      <button @click="openCreateForm">Post Job</button>
      <button @click="showAnalytics = true">Analytics</button>

      <input
        v-model="search"
        placeholder="Search by job title..."
      />

      <select v-model="filterStatus">
        <option value="">All Status</option>
        <option>Draft</option>
        <option>Requested</option>
        <option>Posted</option>
        <option>Filled</option>
      </select>
    </div>

    <!-- Loading / Empty -->
    <div v-if="loading">Loading jobs...</div>
    <div v-else-if="filteredJobs.length === 0">
      No Jobs Found
    </div>

    <!-- Job Cards -->
    <div class="grid">
      <div v-for="job in filteredJobs" :key="job.id" class="card">
        <img v-if="job.image" :src="`http://127.0.0.1:8000${job.image}`" />

        <h3>{{ job.title }}</h3>

        <p>{{ job.city }}, {{ job.state }}</p>
        <p>Status: {{ job.status.join(", ") }}</p>
        <p>Category: {{ job.category.join(", ") }}</p>

        <div class="actions">
          <button @click="editJob(job)">Edit</button>
          <button @click="duplicateJob(job.id)">Duplicate</button>
          <button @click="deleteJob(job.id)">Delete</button>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <JobForm
      v-if="showForm"
      :job="selectedJob"
      @close="closeForm"
      @refresh="fetchJobs"
    />

    <AnalyticsDialog
      v-if="showAnalytics"
      @close="showAnalytics = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import api from "../services/api"
import JobForm from "../components/JobForm.vue"
import AnalyticsDialog from "../components/AnalyticsDialog.vue"

const jobs = ref([])
const loading = ref(true)

const showForm = ref(false)
const showAnalytics = ref(false)
const selectedJob = ref(null)

const search = ref("")
const filterStatus = ref("")

// Fetch Jobs
const fetchJobs = async () => {
  loading.value = true
  const res = await api.get("jobs/")
  jobs.value = res.data
  loading.value = false
}

// Filters
const filteredJobs = computed(() => {
  return jobs.value.filter(job => {
    const matchTitle = job.title
      .toLowerCase()
      .includes(search.value.toLowerCase())

    const matchStatus = filterStatus.value
      ? job.status.includes(filterStatus.value)
      : true

    return matchTitle && matchStatus
  })
})

// Actions
const openCreateForm = () => {
  selectedJob.value = null
  showForm.value = true
}

const closeForm = () => {
  showForm.value = false
  selectedJob.value = null
}

const editJob = (job) => {
  selectedJob.value = job
  showForm.value = true
}

const deleteJob = async (id) => {
  if (!confirm("Delete this job?")) return
  await api.delete(`jobs/${id}/`)
  fetchJobs()
}

const duplicateJob = async (id) => {
  const res = await api.post(`jobs/${id}/duplicate/`)
  const newJob = res.data

  const index = jobs.value.findIndex(j => j.id === id)
  jobs.value.splice(index + 1, 0, newJob)
}


onMounted(fetchJobs)
</script>

<style>
.container {
  padding: 20px;
  max-width: 1200px;
  margin: auto;
}

.top-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.top-bar input,
.top-bar select {
  padding: 6px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 260px);
  gap: 16px;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.card img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 6px;
}

.actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}

.actions button {
  flex: 1;
  background: #2563eb;
  color: white;
  border: none;
  padding: 6px;
  border-radius: 4px;
  cursor: pointer;
}

.actions button:last-child {
  background: #dc2626;
}
</style>
