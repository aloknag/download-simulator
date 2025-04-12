<template>
    <div class="row justify-content-center">
        <div>
            <div class="card p-4 shadow-sm">
                <h5 class="mb-3">Download with 4xx Error Simulation</h5>

                <div class="mb-3">
                    <label for="errorCode" class="form-label">Select HTTP Error</label>
                    <select id="errorCode" class="form-select" v-model="selectedCode">
                        <option v-for="code in errorCodes" :key="code" :value="code">
                            {{ code }}
                        </option>
                    </select>
                </div>

                <div v-if="errorMessage" class="alert alert-danger">
                    {{ errorMessage }}
                </div>

                <button class="btn btn-primary w-100 mb-2" :disabled="isLoading" @click="downloadUsingFetch">
                    <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status"></span>
                    {{ isLoading ? 'Trying...' : 'Download using Fetch' }}
                </button>

                <button class="btn btn-secondary w-100" :disabled="isLoading" @click="downloadUsingHref">
                    <span v-if="isLoading" class="spinner-border spinner-border-sm" role="status"></span>
                    {{ isLoading ? 'Starting...' : 'Download using window.location.href' }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import API_SERVER_URL from '../constants';

const selectedCode = ref(401);
const isLoading = ref(false);
const errorMessage = ref('');

const errorCodes = [400, 401, 403, 404, 410, 418]; // Add more if needed

const getUrl = () => `${API_SERVER_URL}/api/download-4xx?code=${selectedCode.value}`;

const downloadUsingFetch = () => {
    isLoading.value = true;
    errorMessage.value = '';

    fetch(getUrl())
        .then(async res => {
            if (!res.ok) {
                const msg = await res.text();
                throw new Error(`HTTP ${res.status}: ${msg}`);
            }
            const blob = await res.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'error-sim.bin';
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url);
        })
        .catch(err => {
            console.error('[Fetch 4xx error]', err);
            errorMessage.value = err.message;
        })
        .finally(() => {
            isLoading.value = false;
        });
};

const downloadUsingHref = () => {
    isLoading.value = true;
    errorMessage.value = '';
    window.location.href = getUrl();
    setTimeout(() => {
        isLoading.value = false;
    }, 1500); // assume browser has taken over
};
</script>

<style scoped>
.card {
    margin-top: 2rem;
}

.form-control,
.form-select {
    font-size: 1.1rem;
    padding: 0.75rem;
}
</style>