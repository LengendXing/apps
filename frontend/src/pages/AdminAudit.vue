<template>
  <MainLayout>
    <div>
      <h2 class="text-2xl font-bold mb-6">{{ t('adminAudit.title') }}</h2>

      <div class="flex gap-3 mb-4">
        <select v-model="filterAction" @change="page = 1; loadLogs()" class="px-3 py-1.5 text-sm rounded-md border border-border bg-background">
          <option value="">{{ t('adminAudit.filterAction') }}: {{ t('adminAudit.all') }}</option>
          <option value="create">create</option>
          <option value="update">update</option>
          <option value="delete">delete</option>
        </select>
        <select v-model="filterType" @change="page = 1; loadLogs()" class="px-3 py-1.5 text-sm rounded-md border border-border bg-background">
          <option value="">{{ t('adminAudit.filterType') }}: {{ t('adminAudit.all') }}</option>
          <option value="category">category</option>
          <option value="tool">tool</option>
        </select>
      </div>

      <div class="bg-card rounded-lg border border-border overflow-hidden">
        <table class="w-full text-sm">
          <thead class="border-b border-border">
            <tr>
              <th class="px-4 py-3 text-left font-medium text-muted-foreground">ID</th>
              <th class="px-4 py-3 text-left font-medium text-muted-foreground">{{ t('adminAudit.userId') }}</th>
              <th class="px-4 py-3 text-left font-medium text-muted-foreground">{{ t('adminAudit.action') }}</th>
              <th class="px-4 py-3 text-left font-medium text-muted-foreground">{{ t('adminAudit.targetType') }}</th>
              <th class="px-4 py-3 text-left font-medium text-muted-foreground">{{ t('adminAudit.targetId') }}</th>
              <th class="px-4 py-3 text-left font-medium text-muted-foreground">{{ t('adminAudit.details') }}</th>
              <th class="px-4 py-3 text-left font-medium text-muted-foreground">{{ t('adminAudit.time') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in logs" :key="log.id" class="border-b border-border last:border-0">
              <td class="px-4 py-3 text-muted-foreground">{{ log.id }}</td>
              <td class="px-4 py-3">{{ log.user_id }}</td>
              <td class="px-4 py-3">
                <span :class="actionClass(log.action)">{{ log.action }}</span>
              </td>
              <td class="px-4 py-3 text-muted-foreground">{{ log.target_type }}</td>
              <td class="px-4 py-3 text-muted-foreground">{{ log.target_id || '-' }}</td>
              <td class="px-4 py-3 text-muted-foreground max-w-xs truncate">{{ formatDetails(log.details) }}</td>
              <td class="px-4 py-3 text-muted-foreground whitespace-nowrap">{{ log.created_at }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="total > pageSize" class="flex items-center justify-center gap-2 mt-4">
        <button v-for="p in totalPages" :key="p" @click="page = p; loadLogs()"
                :class="p === page ? 'bg-primary text-primary-foreground' : 'border border-border'"
                class="px-3 py-1 text-sm rounded-md">{{ p }}</button>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import MainLayout from '@/layouts/MainLayout.vue'
import { audit as auditApi } from '@/api'

const { t } = useI18n()
const logs = ref<any[]>([])
const page = ref(1)
const pageSize = 20
const total = ref(0)
const filterAction = ref('')
const filterType = ref('')
const totalPages = computed(() => Math.ceil(total.value / pageSize))

const loadLogs = async () => {
  try {
    const params: any = { page: page.value, page_size: pageSize }
    if (filterAction.value) params.action = filterAction.value
    if (filterType.value) params.target_type = filterType.value
    const res = await auditApi.list(params)
    logs.value = res.data.items || []
    total.value = res.data.total || 0
  } catch (_) {}
}

onMounted(loadLogs)

const actionClass = (action: string) => {
  if (action === 'delete') return 'text-red-400'
  if (action === 'create') return 'text-green-500'
  if (action === 'update') return 'text-blue-400'
  return 'text-muted-foreground'
}

const formatDetails = (details: string) => {
  try {
    const d = JSON.parse(details)
    return Object.entries(d).map(([k, v]) => `${k}: ${v}`).join(', ')
  } catch { return details }
}
</script>
