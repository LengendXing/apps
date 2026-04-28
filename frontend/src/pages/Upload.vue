<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">{{ t('upload.title') }}</h2>
    <div
      @dragover.prevent
      @drop.prevent="handleDrop"
      class="border-2 border-dashed border-border rounded-xl p-12 text-center hover:bg-muted/30 transition-colors cursor-pointer"
      @click="$refs.fileInput?.click()"
    >
      <p class="text-muted-foreground">{{ t('upload.drop') }}</p>
      <p class="text-sm text-muted-foreground mt-2">({{ t('upload.browse') }})</p>
      <input ref="fileInput" type="file" class="hidden" @change="handleFileSelect" />
    </div>
    <div v-if="uploading" class="mt-4 text-sm text-muted-foreground">Uploading...</div>
    <div v-if="error" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-md text-red-600 text-sm">{{ error }}</div>
    <div v-if="files.length" class="mt-8">
      <h3 class="font-semibold mb-3">{{ t('upload.list') }}</h3>
      <div class="bg-card rounded-lg border border-border overflow-hidden">
        <table class="w-full text-sm">
          <thead class="border-b border-border">
            <tr>
              <th class="px-4 py-3 text-left font-medium text-muted-foreground">File</th>
              <th class="px-4 py-3 text-left font-medium text-muted-foreground">{{ t('upload.size') }}</th>
              <th class="px-4 py-3 text-left font-medium text-muted-foreground">{{ t('upload.expires') }}</th>
              <th class="px-4 py-3 text-right font-medium text-muted-foreground">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="f in files" :key="f.id" class="border-b border-border last:border-0">
              <td class="px-4 py-3"><a :href="f.url" target="_blank" class="hover:underline">{{ f.original_name }}</a></td>
              <td class="px-4 py-3 text-muted-foreground">{{ formatSize(f.size) }}</td>
              <td class="px-4 py-3 text-muted-foreground">{{ f.expires_at }}</td>
              <td class="px-4 py-3 text-right"><button @click="handleDelete(f.id)" class="text-red-500 hover:text-red-700">{{ t('upload.delete') }}</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { uploads } from '@/api'

const { t } = useI18n()
const files = ref<any[]>([])
const uploading = ref(false)
const error = ref('')
const fileInput = ref<HTMLInputElement>()

const handleDrop = (e: DragEvent) => {
  const fileList = e.dataTransfer?.files
  if (fileList?.[0]) uploadFiles([fileList[0]])
}

const handleFileSelect = (e: Event) => {
  const input = e.target as HTMLInputElement
  if (input.files?.[0]) uploadFiles([input.files[0]])
}

const uploadFiles = async (fileList: File[]) => {
  uploading.value = true
  error.value = ''
  try {
    for (const f of fileList) {
      await uploads.upload(f)
    }
    loadFiles()
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Upload failed'
  } finally {
    uploading.value = false
  }
}

const loadFiles = async () => {
  try {
    const res = await uploads.list()
    files.value = res.data
  } catch (_) {}
}

const handleDelete = async (id: number) => {
  await uploads.delete(id)
  loadFiles()
}

const formatSize = (bytes: number) => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1024 / 1024).toFixed(1) + ' MB'
}

onMounted(loadFiles)
</script>
