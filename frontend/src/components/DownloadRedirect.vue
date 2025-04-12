<template>
  <div class="row justify-content-center">
    <div>
      <div class="card p-4 shadow-sm">
        <h5 class="mb-3">Redirect Download Test</h5>

        <div class="mb-3">
          <label for="redirects" class="form-label">Redirect Count</label>
          <input
            id="redirects"
            type="number"
            class="form-control"
            v-model.number="redirectCount"
            min="0"
            max="5"
            placeholder="e.g., 2"
          />
        </div>

        <div class="mb-3">
          <label for="fileSize" class="form-label">Final File Size (MB)</label>
          <input
            id="fileSize"
            type="number"
            class="form-control"
            v-model.number="fileSize"
            min="1"
            placeholder="e.g., 10"
          />
        </div>

        <div v-if="errorMessage" class="alert alert-danger">
          {{ errorMessage }}
        </div>

        <button
          class="btn btn-primary w-100 mb-2"
          :disabled="!isValidInput || isLoading"
          @click="downloadUsingFetch"
        >
          <span
            v-if="isLoading"
            class="spinner-border spinner-border-sm"
            role="status"
            aria-hidden="true"
          ></span>
          {{ isLoading ? 'Redirecting...' : 'Download using Fetch' }}
        </button>

        <button
          class="btn btn-secondary w-100"
          :disabled="!isValidInput || isLoading"
          @click="downloadUsingHref"
        >
          <span
            v-if="isLoading"
            class="spinner-border spinner-border-sm"
            role="status"
            aria-hidden="true"
          ></span>
          {{ isLoading ? 'Redirecting...' : 'Download using window.location.href' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import API_SERVER_URL from '../constants'

const fileSize = ref<number | null>(null)
const redirectCount = ref<number>(0)
const isLoading = ref(false)
const errorMessage = ref('')

const isValidInput = computed(() => {
  return (
    typeof fileSize.value === 'number' &&
    fileSize.value > 0 &&
    typeof redirectCount.value === 'number' &&
    redirectCount.value >= 0 &&
    redirectCount.value <= 5
  )
})

const getUrl = () => {
  return `${API_SERVER_URL}/api/redirect-download?redirects=${redirectCount.value}&size=${fileSize.value}`
}

const downloadUsingFetch = () => {
  if (!isValidInput.value) {
    errorMessage.value = 'Please provide valid inputs.'
    return
  }

  isLoading.value = true
  const url = getUrl()

  fetch(url, { redirect: 'follow' }) // could also try 'manual' to test stricter scenarios
    .then(async (response) => {
      if (!response.ok) {
        const msg = await response.text()
        throw new Error(msg || `Status ${response.status}`)
      }

      const blob = await response.blob()
      const blobUrl = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = blobUrl
      a.download = 'redirected_file.bin'
      a.click()
      URL.revokeObjectURL(blobUrl)
    })
    .catch((err) => {
      console.error('[Redirect Fetch Error]', err)
      errorMessage.value = `Download failed: ${err.message}`
    })
    .finally(() => {
      isLoading.value = false
    })
}

const downloadUsingHref = () => {
  if (!isValidInput.value) {
    errorMessage.value = 'Please provide valid inputs.'
    return
  }

  isLoading.value = true
  window.location.href = getUrl()
  setTimeout(() => {
    isLoading.value = false
  }, 2000)
}
</script>

<style scoped>
.card {
  margin-top: 2rem;
}

.form-control {
  font-size: 1.1rem;
  padding: 0.75rem;
}
</style>
