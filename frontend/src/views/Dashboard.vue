<template>
  <div class="min-h-screen bg-gray-50 p-8">

    <!-- Header -->
    <h1 class="text-4xl font-bold text-gray-900 mb-6 text-center">
      Job Dashboard
    </h1>

    <!-- Top Controls -->
    <div class="flex flex-wrap items-center justify-between gap-4 mb-8">

  <!-- Left: Actions -->
  <div class="flex gap-3">
    <button
      @click="openCreateForm"
      class="flex items-center gap-2 px-5 py-2 rounded-lg
             bg-blue-600 text-white font-semibold
             hover:bg-blue-700
             shadow-md hover:shadow-[0_0_20px_rgba(37,99,235,0.8)]
             transition-all"
    >
      <span>➕</span>
      Post Job
    </button>

    <button
      @click="showAnalytics = true"
      class="px-5 py-2 rounded-lg
             border border-blue-600 text-blue-600 font-semibold
             hover:bg-blue-50
             transition"
    >
      Analytics
    </button>
  </div>

  <!-- Right: Search + Filter -->
  <div class="flex gap-3 flex-wrap">

    <div class="relative">
      <input
        v-model="search"
        placeholder="Search jobs..."
        class="pl-10 pr-4 py-2 rounded-lg border border-gray-300
               focus:ring-2 focus:ring-blue-500 outline-none"
      />
      <span class="absolute left-3 top-2.5 text-gray-400">🔍</span>
    </div>

    <select
      v-model="filterStatus"
      class="px-4 py-2 rounded-lg border border-gray-300
             focus:ring-2 focus:ring-blue-500 outline-none
             bg-white"
    >
      <option value="">All Status</option>
      <option>Draft</option>
      <option>Requested</option>
      <option>Posted</option>
      <option>Filled</option>
    </select>

  </div>
</div>


    <!-- Loading / Empty -->
    <div v-if="loading" class="text-center text-gray-500">
      Loading jobs...
    </div>

    <div v-else-if="filteredJobs.length === 0" class="text-center text-gray-500">
      No Jobs Found
    </div>

    <!-- Job Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">

      <div
        v-for="job in filteredJobs"
        :key="job.id"
        class="bg-white border border-gray-200 rounded-xl p-4 shadow-sm
               hover:shadow-[0_0_25px_rgba(37,99,235,0.8)]
               hover:border-blue-500 transition-all duration-300"
      >
        <img
          v-if="job.image"
          :src="`http://127.0.0.1:8000${job.image}`"
          class="w-full h-40 object-cover rounded-lg mb-3"
        />

        <h3 class="text-lg font-semibold text-gray-900">
          {{ job.title }}
        </h3>

        <p class="text-sm text-gray-600">
          {{ job.city }}, {{ job.state }}
        </p>

        <p class="text-sm mt-2">
          <span class="font-medium">Status:</span>
          {{ job.status.join(", ") }}
        </p>

        <p class="text-sm">
          <span class="font-medium">Category:</span>
          {{ job.category.join(", ") }}
        </p>

        <div class="flex gap-2 mt-4">
          <button
            @click="editJob(job)"
            class="flex-1 bg-blue-600 text-white py-1 rounded-lg
                   hover:bg-blue-700 transition"
          >
            Edit
          </button>

          <button
            @click="duplicateJob(job.id)"
            class="flex-1 bg-green-600 text-white py-1 rounded-lg
                   hover:bg-green-700 transition"
          >
            Duplicate
          </button>

          <button
            @click="deleteJob(job.id)"
            class="flex-1 bg-red-600 text-white py-1 rounded-lg
                   hover:bg-red-700 transition"
          >
            Delete
          </button>
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

const fetchJobs = async () => {
  loading.value = true
  const res = await api.get("jobs/")
  jobs.value = res.data
  loading.value = false
}

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
  Swal.fire({
    title: "Delete this job?",
    text: "This action cannot be undone!",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#2563eb",   // Blue
    cancelButtonColor: "#94a3b8",    // Gray
    confirmButtonText: "Yes, delete it",
    cancelButtonText: "Cancel"
  }).then(async (result) => {
    if (result.isConfirmed) {
      await api.delete(`jobs/${id}/`)
      fetchJobs()

      Swal.fire({
        icon: "success",
        title: "Deleted!",
        text: "The job has been removed.",
        timer: 2000,
        showConfirmButton: false
      })
    }
  })
}

const duplicateJob = async (id) => {
  const res = await api.post(`jobs/${id}/duplicate/`)
  fetchJobs()

  Swal.fire({
    icon: "success",
    title: "Job Duplicated",
    text: "A copy of the job has been created successfully!",
    timer: 2000,
    showConfirmButton: false
  })
}


onMounted(fetchJobs)
</script>
