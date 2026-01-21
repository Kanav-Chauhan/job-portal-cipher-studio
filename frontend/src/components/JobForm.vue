<template>
  <div class="modal">
    <div class="box">
      <h2>{{ job ? "Edit Job" : "Create Job" }}</h2>

      <form @submit.prevent="submit">

        <!-- Image Upload -->
        <div
          class="upload-box"
          @dragover.prevent
          @drop.prevent="handleDrop"
        >
          <p>Drag & Drop Image or Click</p>
          <input
            type="file"
            ref="fileInput"
            hidden
            @change="handleFile"
          />
          <button type="button" @click="openFile">Choose File</button>

          <img v-if="preview" :src="preview" class="preview" />
        </div>

        <!-- Job Title -->
        <input
          v-model="title"
          placeholder="Job Title"
          required
        />

        <!-- Status -->
        <select v-model="status" multiple required>
          <option>Draft</option>
          <option>Requested</option>
          <option>Posted</option>
          <option>Filled</option>
        </select>

        <!-- Category -->
        <select v-model="category" multiple required>
          <option>Full-time</option>
          <option>Part-time</option>
          <option>Intern</option>
        </select>

        <!-- Location -->
        <input v-model="address" placeholder="Address" />
        <input v-model="city" placeholder="City" />
        <input v-model="state" placeholder="State" />

        <!-- Dates -->
        <input type="date" v-model="start_date" required />
        <input type="date" v-model="end_date" required />

        <!-- Description -->
        <textarea
          v-model="description"
          placeholder="Job Description"
          rows="4"
        ></textarea>

        <!-- Buttons -->
        <div class="actions">
          <button type="submit">
            {{ job ? "Update" : "Save" }}
          </button>
          <button type="button" @click="$emit('close')">
            Cancel
          </button>
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
const category = ref([])
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
    status.value = props.job.status
    category.value = props.job.category
    address.value = props.job.address
    city.value = props.job.city
    state.value = props.job.state
    start_date.value = props.job.start_date
    end_date.value = props.job.end_date
    description.value = props.job.description
    preview.value = props.job.image
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

  if (image.value) {
    form.append("image", image.value)
  }

  if (props.job) {
    await api.put(`jobs/${props.job.id}/`, form)
  } else {
    await api.post("jobs/", form)
  }

  emit("refresh")
  emit("close")
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
  z-index: 1000;
}

.box {
  background: white;
  padding: 20px;
  width: 420px;
  max-height: 90vh;
  overflow-y: auto;
  border-radius: 8px;
}

.upload-box {
  border: 2px dashed #aaa;
  padding: 10px;
  text-align: center;
  margin-bottom: 10px;
}

.preview {
  width: 100%;
  margin-top: 10px;
  border-radius: 6px;
}

input,
select,
textarea {
  width: 100%;
  padding: 6px;
  margin-bottom: 8px;
}

.actions {
  display: flex;
  gap: 10px;
}

.actions button {
  flex: 1;
  padding: 8px;
  border: none;
  border-radius: 4px;
  background: #2563eb;
  color: white;
  cursor: pointer;
}

.actions button:last-child {
  background: #6b7280;
}
</style>
