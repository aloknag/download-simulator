<template>
    <div class="row justify-content-center">
        <div>
            <div class="card p-4 shadow-sm">
                <h5 class="mb-3">Download in New Tab</h5>

                <div class="mb-3">
                    <label for="ntFileSize" class="form-label">File Size (MB)</label>
                    <input id="ntFileSize" type="number" class="form-control" v-model.number="ntFileSize"
                        placeholder="e.g., 100" min="1" />
                </div>

                <div class="mb-3 form-check">
                    <input type="checkbox" class="form-check-input" id="ntEnableAbort" v-model="ntEnableAbortAfter" />
                    <label class="form-check-label" for="ntEnableAbort">Abort after certain size</label>
                </div>

                <div class="mb-3" v-if="ntEnableAbortAfter">
                    <label for="ntAbortAfter" class="form-label">Abort After (MB)</label>
                    <input id="ntAbortAfter" type="number" class="form-control" v-model.number="ntAbortAfter" min="1" />
                </div>

                <div v-if="ntErrorMessage" class="alert alert-danger">
                    {{ ntErrorMessage }}
                </div>

                <button class="btn btn-primary w-100" :disabled="!ntFileSize || (ntEnableAbortAfter && !ntAbortAfter)"
                    @click="ntDownloadInNewTab">
                    Open Download in New Tab
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import API_SERVER_URL from '../constants';

const ntFileSize = ref<number | null>(100);
const ntAbortAfter = ref<number | null>(null);
const ntEnableAbortAfter = ref(false);
const ntErrorMessage = ref('');

const ntDownloadInNewTab = () => {
    if (!ntFileSize.value || ntFileSize.value <= 0) {
        ntErrorMessage.value = 'Please enter a valid file size.';
        return;
    }
    if (ntEnableAbortAfter.value && (!ntAbortAfter.value || ntAbortAfter.value <= 0)) {
        ntErrorMessage.value = 'Please enter a valid abort size.';
        return;
    }

    const params = new URLSearchParams({
        size: String(ntFileSize.value),
    });

    if (ntEnableAbortAfter.value) {
        params.append('abortAfter', String(ntAbortAfter.value));
    }

    const ntUrl = `${API_SERVER_URL}/api/download?${params.toString()}`;

    // Open in a new tab
    window.open(ntUrl, '_blank');
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