<template>
  <div class="row justify-content-center">
    <div>
      <div class="card p-4 shadow-sm">
        <h5 class="mb-3">Download with Abort</h5>
        <div class="mb-3">
          <label for="fileSize" class="form-label">Enter file size (MB):</label>
          <input
            id="fileSize"
            type="number"
            class="form-control"
            v-model.number="fileSize"
            placeholder="e.g., 100"
            min="1"
            aria-describedby="sizeHelp"
          />
          <div id="sizeHelp" class="form-text">Specify the desired file size in Megabytes.</div>
        </div>

        <!-- 🔘 New Checkbox Toggle -->
        <div class="form-check mb-2">
          <input class="form-check-input" type="checkbox" id="enableAbort" v-model="enableAbort" />
          <label class="form-check-label" for="enableAbort"> Abort Download? </label>
        </div>

        <!-- 🧾 Conditionally show input if checkbox is true -->
        <div class="mb-3" v-if="enableAbort">
          <label for="abortAfter" class="form-label">Abort after size (MB):</label>
          <input
            id="abortAfter"
            type="number"
            class="form-control"
            v-model.number="abortAfter"
            placeholder="e.g., 10"
            min="1"
            aria-describedby="abortAfterHelp"
          />
          <div id="abortsizeHelp" class="form-text">Server will abort download after this size</div>
        </div>

        <div v-if="errorMessage" class="alert alert-danger" role="alert">
          {{ errorMessage }}
        </div>

        <button
          @click="downloadUsingFetch"
          :disabled="!isValidSize || isLoading"
          class="btn btn-primary w-100 mb-2"
        >
          <span
            v-if="isLoading"
            class="spinner-border spinner-border-sm"
            role="status"
            aria-hidden="true"
          ></span>
          {{ isLoading ? 'Preparing...' : 'Download using fetch' }}
        </button>

        <button
          @click="downloadUsingHref"
          :disabled="!isValidSize || isLoading"
          class="btn btn-secondary w-100"
        >
          <span
            v-if="isLoading"
            class="spinner-border spinner-border-sm"
            role="status"
            aria-hidden="true"
          ></span>
          {{ isLoading ? 'Preparing...' : 'Download using window.location.href' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import API_SERVER_URL from '../constants'

const fileSize = ref<number | null>(null)
const abortAfter = ref<number | null>(null)
const enableAbort = ref(false)
const errorMessage = ref('')
const isLoading = ref(false)

const isValidSize = computed(() => typeof fileSize.value === 'number' && fileSize.value > 0)
const isValidAbortAfter = computed(
  () => !enableAbort.value || (typeof abortAfter.value === 'number' && abortAfter.value > 0),
)

const getApiUrl = () => {
  let url = `${API_SERVER_URL}/api/download?size=${fileSize.value}`
  if (enableAbort.value && abortAfter.value) {
    url += `&abortAfter=${abortAfter.value}`
  }
  return url
}

const validateInputs = () => {
  errorMessage.value = ''
  if (!isValidSize.value) {
    errorMessage.value = 'Please enter a valid positive number for the size.'
    return false
  }
  if (enableAbort.value && !isValidAbortAfter.value) {
    errorMessage.value = 'Please enter a valid positive number for the abort size.'
    return false
  }
  return true
}

const downloadUsingFetch = () => {
  if (!validateInputs()) return

  isLoading.value = true
  const apiUrl = getApiUrl()
  console.log(`[Fetch] Downloading from: ${apiUrl}`)

  fetch(apiUrl)
    .then(async (response) => {
      if (!response.ok) {
        const text = await response.text()
        throw new Error(text || `Server responded with status: ${response.status}`)
      }

      const contentDisposition = response.headers.get('content-disposition')
      let filename = 'downloaded_file'
      if (contentDisposition) {
        const match = contentDisposition.match(/filename="?(.+?)"?$/i)
        if (match && match[1]) filename = match[1]
      }

      const blob = await response.blob()
      return { blob, filename }
    })
    .then(({ blob, filename }) => {
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      a.style.display = 'none'
      document.body.appendChild(a)
      a.click()
      a.remove()
      URL.revokeObjectURL(url)
    })
    .catch((error) => {
      console.error('[Fetch] Download failed:', error)
      errorMessage.value = `Download failed: ${error.message}`
    })
    .finally(() => {
      isLoading.value = false
    })
}

const downloadUsingHref = () => {
  if (!validateInputs()) return

  isLoading.value = true
  const apiUrl = getApiUrl()
  console.log(`[Href] Initiating download via location.href: ${apiUrl}`)

  try {
    window.location.href = apiUrl
    setTimeout(() => {
      isLoading.value = false
    }, 1500) // Assume browser takes over
  } catch (error) {
    console.error('[Href] Download failed:', error)
    errorMessage.value = 'Could not initiate download.'
    isLoading.value = false
  }
}
</script>

<style scoped>
.card {
  margin-top: 2rem;
}

.form-control {
  padding: 0.75rem 1rem;
  font-size: 1.1rem;
}
</style>
