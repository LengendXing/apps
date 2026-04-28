<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold">{{ t('tools.title') }}</h2>
      <input v-model="searchQuery" :placeholder="t('tools.search')" class="px-3 py-2 rounded-md border border-border bg-background text-sm w-64" />
    </div>
    <div v-for="cat in categories" :key="cat.id" class="mb-8">
      <h3 class="text-lg font-semibold mb-3">{{ cat.icon }} {{ cat.name }}</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        <a v-for="tool in getTools(cat.id)" :key="tool.id" :href="tool.url" target="_blank"
           class="bg-card rounded-lg border border-border p-4 hover:bg-muted/50 transition-all flex items-center gap-3">
          <div class="w-10 h-10 rounded-lg bg-muted flex items-center justify-center text-lg flex-shrink-0">
            {{ tool.icon || '🔗' }}
          </div>
          <div class="min-w-0">
            <p class="font-medium truncate">{{ tool.name }}</p>
            <p class="text-xs text-muted-foreground truncate">{{ tool.description }}</p>
          </div>
        </a>
      </div>
    </div>
    <p v-if="!categories.length" class="text-center text-muted-foreground py-12">No tools yet. Add them from the admin panel.</p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { tools } from '@/api'

const { t } = useI18n()
const categories = ref<any[]>([])
const allTools = ref<any[]>([])
const searchQuery = ref('')

onMounted(async () => {
  try {
    const [catsRes, toolsRes] = await Promise.all([tools.listCategories(), tools.list()])
    categories.value = catsRes.data
    allTools.value = toolsRes.data.items || []
  } catch (_) {}
})

const getTools = (catId: number) => {
  let items = allTools.value.filter(t => t.category_id === catId)
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    items = items.filter(t => t.name.toLowerCase().includes(q) || t.description.toLowerCase().includes(q))
  }
  return items
}
</script>
