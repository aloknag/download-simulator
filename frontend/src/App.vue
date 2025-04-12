<script setup lang="ts">
import DownloadBasic from './components/DownloadBasic.vue'
import DownloadRedirect from './components/DownloadRedirect.vue'
import DownloadNoContentLength from './components/DownloadNoContentLength.vue'
import DownloadHttpError from './components/DownloadHttpError.vue'
import DownloadNewTab from './components/DownloadNewTab.vue'
</script>

<template>
  <div class="container" id="app">
    <h1 class="text-center mb-4">File Downloader</h1>

    <!-- First row with two components -->
    <div class="row mb-4">
      <div class="col-md-6 d-flex align-items-stretch">
        <DownloadBasic class="w-100" />
      </div>
      <div class="col-md-6 d-flex align-items-stretch">
        <DownloadRedirect class="w-100" />
      </div>
    </div>

    <!-- Second row with two components -->
    <div class="row mb-4">
      <div class="col-md-6 d-flex align-items-stretch">
        <DownloadNoContentLength class="w-100" />
      </div>
      <div class="col-md-6 d-flex align-items-stretch">
        <DownloadHttpError class="w-100" />
      </div>
    </div>

    <!-- Third row with one component -->
    <div class="row mb-4">
      <div class="col-md-12 d-flex justify-content-center">
        <DownloadNewTab class="w-100" />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Ensures that each component inside the columns stretches to the same height */
.d-flex.align-items-stretch {
  display: flex;
  align-items: stretch;
}

/* Optional: Adds margin for uniform spacing between rows */
.mb-4 {
  margin-bottom: 1.5rem;
}

/* Ensure each component doesn't overflow */
.w-100 {
  width: 100%;
}
</style>
