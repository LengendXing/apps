<template>
  <MainLayout>
    <div>
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold">{{ t('adminTools.title') }}</h2>
        <div class="flex gap-2">
          <button @click="showCategoryForm = true" class="px-3 py-1.5 text-sm bg-primary text-primary-foreground rounded-md hover:opacity-90 transition">{{ t('adminTools.addCategory') }}</button>
          <button @click="showToolForm = true" class="px-3 py-1.5 text-sm bg-primary text-primary-foreground rounded-md hover:opacity-90 transition">{{ t('adminTools.addTool') }}</button>
        </div>
      </div>

      <div v-if="showCategoryForm" class="mb-6 bg-card rounded-lg border border-border p-4">
        <h3 class="font-semibold mb-3">{{ t('adminTools.categoryForm') }}</h3>
        <div class="flex gap-2">
          <input v-model="catForm.name" :placeholder="t('adminTools.categoryName')" class="flex-1 px-3 py-1.5 text-sm rounded-md border border-border bg-background" />
          <input v-model="catForm.icon" :placeholder="t('adminTools.icon')" class="w-24 px-3 py-1.5 text-sm rounded-md border border-border bg-background" />
          <button @click="createCategory" class="px-3 py-1.5 text-sm bg-primary text-primary-foreground rounded-md">{{ t('adminTools.save') }}</button>
          <button @click="showCategoryForm = false" class="px-3 py-1.5 text-sm border border-border rounded-md">{{ t('adminTools.cancel') }}</button>
        </div>
      </div>

      <div v-if="showToolForm" class="mb-6 bg-card rounded-lg border border-border p-4">
        <h3 class="font-semibold mb-3">{{ t('adminTools.toolForm') }}</h3>
        <div class="grid grid-cols-2 gap-3">
          <input v-model="toolForm.name" :placeholder="t('adminTools.toolName')" class="px-3 py-1.5 text-sm rounded-md border border-border bg-background" />
          <select v-model="toolForm.category_id" class="px-3 py-1.5 text-sm rounded-md border border-border bg-background">
            <option :value="0">{{ t('adminTools.noCategory') }}</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
          <input v-model="toolForm.url" :placeholder="t('adminTools.toolUrl')" class="col-span-2 px-3 py-1.5 text-sm rounded-md border border-border bg-background" />
          <input v-model="toolForm.icon" :placeholder="t('adminTools.icon')" class="px-3 py-1.5 text-sm rounded-md border border-border bg-background" />
          <input v-model="toolForm.description" :placeholder="t('adminTools.description')" class="px-3 py-1.5 text-sm rounded-md border border-border bg-background" />
        </div>
        <div class="flex gap-2 mt-3">
          <label class="flex items-center gap-1 text-sm"><input type="checkbox" v-model="toolForm.is_featured" /> {{ t('adminTools.featured') }}</label>
          <button @click="createTool" class="px-3 py-1.5 text-sm bg-primary text-primary-foreground rounded-md">{{ t('adminTools.save') }}</button>
          <button @click="showToolForm = false" class="px-3 py-1.5 text-sm border border-border rounded-md">{{ t('adminTools.cancel') }}</button>
        </div>
      </div>

      <div v-for="cat in categories" :key="cat.id" class="mb-8">
        <h3 class="text-lg font-semibold mb-3">{{ cat.icon }} {{ cat.name }}</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          <div v-for="tool in getTools(cat.id)" :key="tool.id"
               class="bg-card rounded-lg border border-border p-4 hover:bg-muted/50 transition-all flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-muted flex items-center justify-center text-lg flex-shrink-0">
              {{ tool.icon || '🔗' }}
            </div>
            <div class="min-w-0 flex-1">
              <p class="font-medium truncate">{{ tool.name }}</p>
              <p class="text-xs text-muted-foreground truncate">{{ tool.description }}</p>
            </div>
            <button @click="handleDelete(tool.id)" class="text-red-500 hover:text-red-700 text-sm flex-shrink-0">{{ t('adminTools.delete') }}</button>
          </div>
        </div>
      </div>
      <p v-if="!categories.length" class="text-center text-muted-foreground py-12">{{ t('adminTools.empty') }}</p>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import MainLayout from '@/layouts/MainLayout.vue'
import { tools as toolsApi } from '@/api'

const { t } = useI18n()
const categories = ref<any[]>([])
const allTools = ref<any[]>([])
const showCategoryForm = ref(false)
const showToolForm = ref(false)
const catForm = ref({ name: '', icon: '' })
const toolForm = ref({ name: '', category_id: 0, url: '', icon: '', description: '', is_featured: false })

onMounted(async () => {
  try {
    const [catsRes, toolsRes] = await Promise.all([toolsApi.listCategories(), toolsApi.list()])
    categories.value = catsRes.data
    allTools.value = toolsRes.data.items || []
  } catch (_) {}
})

const createCategory = async () => {
  if (!catForm.value.name) return
  const res = await toolsApi.createCategory(catForm.value)
  categories.value.push(res.data)
  showCategoryForm.value = false
  catForm.value = { name: '', icon: '' }
}

const createTool = async () => {
  if (!toolForm.value.name) return
  const res = await toolsApi.create(toolForm.value)
  allTools.value.push(res.data)
  showToolForm.value = false
  toolForm.value = { name: '', category_id: 0, url: '', icon: '', description: '', is_featured: false }
}

const handleDelete = async (id: number) => {
  await toolsApi.delete(id)
  allTools.value = allTools.value.filter(t => t.id !== id)
}

const getTools = (catId: number) => allTools.value.filter(t => t.category_id === catId)
</script>
