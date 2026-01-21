<template>
  <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">

    <div class="frost-modal w-full max-w-xl rounded-2xl p-6 shadow-xl max-h-[90vh] flex flex-col">

      <!-- Header -->
      <h2 class="frost-title mb-4">
        {{ job ? "Edit Job" : "Create Job" }}
      </h2>

      <!-- Scrollable Form -->
      <form @submit.prevent="submit" class="space-y-4 overflow-y-auto pr-2 flex-1">

        <!-- Image Upload -->
        <div
          class="frost-upload"
          @dragover.prevent
          @drop.prevent="handleDrop"
          @click="openFile"
        >
          <p class="text-muted">Drag & Drop Image or Click</p>

          <input type="file" ref="fileInput" hidden @change="handleFile" />

          <img
            v-if="preview"
            :src="preview"
            class="w-full h-40 object-cover rounded-lg mt-3"
          />
        </div>

        <!-- Job Title -->
        <input v-model="title" placeholder="Job Title" required class="frost-input" />

        <!-- Status (Multi-select) -->
        <div>
          <p class="frost-label">Status</p>
          <div class="frost-checkbox-group">
            <label v-for="s in ['Draft','Requested','Posted','Filled']" :key="s" class="frost-checkbox">
              <input type="checkbox" :value="s" v-model="status" />
              <span>{{ s }}</span>
            </label>
          </div>
        </div>

        <!-- Category (Multi-select) -->
        <div>
          <p class="frost-label">Category</p>
          <div class="frost-checkbox-group">
            <label v-for="c in ['Full-time','Part-time','Intern']" :key="c" class="frost-checkbox">
              <input type="checkbox" :value="c" v-model="category" />
              <span>{{ c }}</span>
            </label>
          </div>
        </div>

        <!-- Location -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <input v-model="address" placeholder="Address" class="frost-input" />
          <input v-model="city" placeholder="City" class="frost-input" />
          <input v-model="state" placeholder="State" class="frost-input" />
        </div>

        <!-- Dates -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <input type="date" v-model="start_date" required class="frost-input" />
          <input type="date" v-model="end_date" required class="frost-input" />
        </div>

        <!-- Description -->
        <textarea
          v-model="description"
          placeholder="Job Description"
          rows="4"
          class="frost-input"
        ></textarea>

        <!-- Sticky Buttons INSIDE Form -->
        <div class="sticky bottom-0 bg-[rgba(20,40,80,0.9)] backdrop-blur-md pt-3">
          <div class="flex gap-3">
            <button type="submit" class="frost-btn-primary">
              {{ job ? "Update" : "Save" }}
            </button>

            <button type="button" @click="$emit('close')" class="frost-btn-secondary">
              Cancel
            </button>
          </div>
        </div>

      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"

const props = defineProps({ job: Object })
const emit = defineEmits(["close", "refresh"])

const title = ref("")
const status = ref([])
const category = ref([])   // MULTI-SELECT
const address = ref("")
const city = ref("")
const state = ref("")
const start_date = ref("")
const end_date = ref("")
const description = ref("")
const image = ref(null)
const preview = ref(null)
const fileInput = ref(null)

onMounted(() => {
  if (props.job) {
    title.value = props.job.title
    status.value = props.job.status || []
    category.value = props.job.category || []
    address.value = props.job.address
    city.value = props.job.city
    state.value = props.job.state
    start_date.value = props.job.start_date
    end_date.value = props.job.end_date
    description.value = props.job.description

    if (props.job.image) {
      preview.value = `http://127.0.0.1:8000${props.job.image}`
    }
  }
})

const openFile = () => fileInput.value.click()

const handleFile = (e) => {
  image.value = e.target.files[0]
  preview.value = URL.createObjectURL(image.value)
}

const handleDrop = (e) => {
  image.value = e.dataTransfer.files[0]
  preview.value = URL.createObjectURL(image.value)
}

const submit = async () => {
  if (end_date.value < start_date.value) {
    alert("End date cannot be before start date.")
    return
  }

  const form = new FormData()

  form.append("title", title.value)
  form.append("status", JSON.stringify(status.value))
  form.append("category", JSON.stringify(category.value))
  form.append("address", address.value)
  form.append("city", city.value)
  form.append("state", state.value)
  form.append("start_date", start_date.value)
  form.append("end_date", end_date.value)
  form.append("description", description.value)

  if (image.value) form.append("image", image.value)

  if (props.job) {
    await api.put(`jobs/${props.job.id}/`, form)
    Swal.fire({
  icon: "success",
  title: "Job Updated",
  text: "Changes saved successfully!",
  timer: 2000,
  showConfirmButton: false
})
  } else {
    await api.post("jobs/", form)
    Swal.fire({
  icon: "success",
  title: "Job Created",
  text: "The job has been saved successfully!",
  timer: 2000,
  showConfirmButton: false
})
  }

  emit("refresh")
  emit("close")
}
</script>

<style>
  .frost-modal {
  background: #f8fbff;
  border: 1px solid #dbeafe;
  color: #1e3a8a;
}

.frost-title {
  font-size: 24px;
  font-weight: 700;
  color: #2563eb;
}

.text-muted {
  color: #64748b;
}

.frost-upload {
  border: 2px dashed #93c5fd;
  border-radius: 12px;
  padding: 16px;
  text-align: center;
  cursor: pointer;
  background: #eff6ff;
  transition: 0.3s;
}

.frost-upload:hover {
  background: #dbeafe;
}

.frost-input {
  width: 100%;
  background: #ffffff;
  border: 1px solid #bfdbfe;
  color: #1e3a8a;
  padding: 10px 14px;
  border-radius: 10px;
  outline: none;
}

.frost-input::placeholder {
  color: #94a3b8;
}

.frost-label {
  font-weight: 600;
  color: #1e3a8a;
  margin-bottom: 6px;
}

.frost-checkbox-group {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.frost-checkbox {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  padding: 8px 12px;
  border-radius: 10px;
  cursor: pointer;
  color: #1e3a8a;
  transition: 0.25s ease;
}

.frost-checkbox:hover {
  background: #dbeafe;
}

.frost-checkbox input {
  accent-color: #2563eb;
}

.frost-btn-primary {
  flex: 1;
  background: #2563eb;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 12px;
  font-weight: 600;
  transition: 0.3s;
}

.frost-btn-primary:hover {
  background: #1d4ed8;
}

.frost-btn-secondary {
  flex: 1;
  background: #e5e7eb;
  color: #1e3a8a;
  border: 1px solid #cbd5f5;
  padding: 10px;
  border-radius: 12px;
}

.sticky {
  background: #f8fbff;
}

</style>
