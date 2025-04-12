<template>
    <div class="row justify-content-center">
        <div>
            <div class="card p-4 shadow-sm">
                <h5 class="mb-3">Download without Content-Length</h5>

                <div class="mb-3">
                    <label for="fileSize" class="form-label">File Size (MB)</label>
                    <input id="fileSize" type="number" class="form-control" v-model.number="fileSize" min="1"
                        placeholder="e.g., 50" />
                </div>

                <div v-if="errorMessage" class="alert alert-danger">
                    {{ errorMessage }}
                </div>

                <button class="btn btn-primary w-100 mb-2" :disabled="!isValid || isLoading"
                    @click="downloadUsingFetch">
                    <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status"
                        aria-hidden="true"></span>
                    {{ isLoading ? 'Fetching...' : 'Download using Fetch' }}
                </button>

                <button class="btn btn-secondary w-100" :disabled="!isValid || isLoading" @click="downloadUsingHref">
                    <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status"
                        aria-hidden="true"></span>
                    {{ isLoading ? 'Starting...' : 'Download using window.location.href' }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import API_SERVER_URL from '../constants';

const fileSize = ref<number | null>(null);
const isLoading = ref(false);
const errorMessage = ref('');

const isValid = computed(() => {
    return typeof fileSize.value === 'number' && fileSize.value > 0;
});

const getUrl = () => {
    return `${API_SERVER_URL}/api/download-no-length?size=${fileSize.value}`;
};

const downloadUsingFetch = () => {
    if (!isValid.value) {
        errorMessage.value = 'Please enter a valid size.';
        return;
    }

    isLoading.value = true;
    errorMessage.value = '';

    fetch(getUrl())
        .then(async res => {
            if (!res.ok) {
                const msg = await res.text();
                throw new Error(msg || `Status ${res.status}`);
            }

            const blob = await res.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'file-no-length.bin';
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
        })
        .catch(err => {
            console.error('[NoContentLength Fetch Error]', err);
            errorMessage.value = `Download failed: ${err.message}`;
        })
        .finally(() => {
            isLoading.value = false;
        });
};

const downloadUsingHref = () => {
    if (!isValid.value) {
        errorMessage.value = 'Please enter a valid size.';
        return;
    }

    isLoading.value = true;
    errorMessage.value = '';
    window.location.href = getUrl();
    setTimeout(() => {
        isLoading.value = false;
    }, 2000);
};
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