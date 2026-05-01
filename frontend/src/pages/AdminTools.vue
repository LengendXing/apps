<template>
  <MainLayout>
    <div>
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold">{{ t('adminTools.title') }}</h2>
        <div class="flex gap-2">
          <button @click="openCategoryForm()" class="px-3 py-1.5 text-sm bg-primary text-primary-foreground rounded-md hover:opacity-90 transition">{{ t('adminTools.addCategory') }}</button>
          <button @click="openToolForm()" class="px-3 py-1.5 text-sm bg-primary text-primary-foreground rounded-md hover:opacity-90 transition">{{ t('adminTools.addTool') }}</button>
        </div>
      </div>

      <!-- Category Form -->
      <div v-if="showCategoryForm" class="mb-6 bg-card rounded-lg border border-border p-4">
        <h3 class="font-semibold mb-3">{{ editingCategory ? t('adminTools.editCategory') : t('adminTools.categoryForm') }}</h3>
        <div class="flex gap-2 items-end">
          <div class="flex-1">
            <label class="text-xs text-muted-foreground block mb-1">{{ t('adminTools.categoryName') }}</label>
            <input v-model="catForm.name" :placeholder="t('adminTools.categoryName')" class="w-full px-3 py-1.5 text-sm rounded-md border border-border bg-background" />
          </div>
          <div class="w-24">
            <label class="text-xs text-muted-foreground block mb-1">{{ t('adminTools.icon') }}</label>
            <input v-model="catForm.icon" :placeholder="t('adminTools.icon')" class="w-full px-3 py-1.5 text-sm rounded-md border border-border bg-background" />
          </div>
          <div class="w-20">
            <label class="text-xs text-muted-foreground block mb-1">{{ t('adminTools.sortOrder') }}</label>
            <input v-model.number="catForm.sort_order" type="number" class="w-full px-3 py-1.5 text-sm rounded-md border border-border bg-background" />
          </div>
          <button @click="saveCategory" class="px-3 py-1.5 text-sm bg-primary text-primary-foreground rounded-md">{{ t('adminTools.save') }}</button>
          <button @click="cancelCategoryForm" class="px-3 py-1.5 text-sm border border-border rounded-md">{{ t('adminTools.cancel') }}</button>
        </div>
      </div>

      <!-- Tool Form -->
      <div v-if="showToolForm" class="mb-6 bg-card rounded-lg border border-border p-4">
        <h3 class="font-semibold mb-3">{{ editingTool ? t('adminTools.editTool') : t('adminTools.toolForm') }}</h3>
        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="text-xs text-muted-foreground block mb-1">{{ t('adminTools.toolName') }}</label>
            <input v-model="toolForm.name" :placeholder="t('adminTools.toolName')" class="w-full px-3 py-1.5 text-sm rounded-md border border-border bg-background" />
          </div>
          <div>
            <label class="text-xs text-muted-foreground block mb-1">{{ t('adminTools.categoryName') }}</label>
            <select v-model="toolForm.category_id" class="w-full px-3 py-1.5 text-sm rounded-md border border-border bg-background">
              <option :value="0">{{ t('adminTools.noCategory') }}</option>
              <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>
          <div class="col-span-2">
            <label class="text-xs text-muted-foreground block mb-1">{{ t('adminTools.toolUrl') }}</label>
            <input v-model="toolForm.url" :placeholder="t('adminTools.toolUrl')" class="w-full px-3 py-1.5 text-sm rounded-md border border-border bg-background" />
          </div>
          <div>
            <label class="text-xs text-muted-foreground block mb-1">{{ t('adminTools.icon') }}</label>
            <input v-model="toolForm.icon" :placeholder="t('adminTools.icon')" class="w-full px-3 py-1.5 text-sm rounded-md border border-border bg-background" />
          </div>
          <div>
            <label class="text-xs text-muted-foreground block mb-1">{{ t('adminTools.description') }}</label>
            <input v-model="toolForm.description" :placeholder="t('adminTools.description')" class="w-full px-3 py-1.5 text-sm rounded-md border border-border bg-background" />
          </div>
          <div>
            <label class="text-xs text-muted-foreground block mb-1">{{ t('adminTools.tags') }}</label>
            <input v-model="toolForm.tagsStr" placeholder="tag1,tag2" class="w-full px-3 py-1.5 text-sm rounded-md border border-border bg-background" />
          </div>
          <div>
            <label class="text-xs text-muted-foreground block mb-1">{{ t('adminTools.platforms') }}</label>
            <input v-model="toolForm.platformsStr" placeholder="mac,windows" class="w-full px-3 py-1.5 text-sm rounded-md border border-border bg-background" />
          </div>
        </div>
        <div class="flex items-center gap-4 mt-3">
          <label class="flex items-center gap-1 text-sm"><input type="checkbox" v-model="toolForm.is_featured" /> {{ t('adminTools.featured') }}</label>
          <div>
            <label class="text-xs text-muted-foreground mr-1">{{ t('adminTools.sortOrder') }}</label>
            <input v-model.number="toolForm.sort_order" type="number" class="w-20 px-3 py-1.5 text-sm rounded-md border border-border bg-background" />
          </div>
          <div class="flex-1"></div>
          <button @click="saveTool" class="px-3 py-1.5 text-sm bg-primary text-primary-foreground rounded-md">{{ t('adminTools.save') }}</button>
          <button @click="cancelToolForm" class="px-3 py-1.5 text-sm border border-border rounded-md">{{ t('adminTools.cancel') }}</button>
        </div>
      </div>

      <!-- Categories & Tools -->
      <div v-for="cat in categories" :key="cat.id" class="mb-8">
        <div class="flex items-center gap-2 mb-3">
          <h3 class="text-lg font-semibold">{{ cat.icon }} {{ cat.name }}</h3>
          <span class="text-xs text-muted-foreground">({{ getTools(cat.id).length }})</span>
          <button @click="openCategoryForm(cat)" class="text-xs text-muted-foreground hover:text-foreground ml-2">{{ t('adminTools.edit') }}</button>
          <button @click="deleteCategory(cat)" class="text-xs text-red-400 hover:text-red-600">{{ t('adminTools.delete') }}</button>
        </div>
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
            <div class="flex gap-1 flex-shrink-0">
              <button @click="openToolForm(tool)" class="text-muted-foreground hover:text-foreground text-sm">{{ t('adminTools.edit') }}</button>
              <button @click="deleteTool(tool)" class="text-red-400 hover:text-red-600 text-sm">{{ t('adminTools.delete') }}</button>
            </div>
          </div>
        </div>
      </div>
      <p v-if="!categories.length" class="text-center text-muted-foreground py-12">{{ t('adminTools.empty') }}</p>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import MainLayout from '@/layouts/MainLayout.vue'
import { tools as toolsApi } from '@/api'

const { t } = useI18n()
const categories = ref<any[]>([])
const allTools = ref<any[]>([])

const showCategoryForm = ref(false)
const showToolForm = ref(false)
const editingCategory = ref<any>(null)
const editingTool = ref<any>(null)

const emptyCatForm = () => ({ name: '', icon: '', sort_order: 0 })
const emptyToolForm = () => ({ name: '', category_id: 0, url: '', icon: '', description: '', is_featured: false, sort_order: 0, tagsStr: '', platformsStr: '' })

const catForm = ref(emptyCatForm())
const toolForm = ref(emptyToolForm())

const loadData = async () => {
  try {
    const [catsRes, toolsRes] = await Promise.all([toolsApi.listCategories(), toolsApi.list()])
    categories.value = catsRes.data
    allTools.value = toolsRes.data.items || []
  } catch (_) {}
}

onMounted(loadData)

const getTools = (catId: number) => allTools.value.filter((t: any) => t.category_id === catId)

const openCategoryForm = (cat?: any) => {
  editingCategory.value = cat || null
  catForm.value = cat ? { name: cat.name, icon: cat.icon, sort_order: cat.sort_order || 0 } : emptyCatForm()
  showCategoryForm.value = true
}

const cancelCategoryForm = () => { showCategoryForm.value = false; editingCategory.value = null }

const saveCategory = async () => {
  if (!catForm.value.name) return
  try {
    if (editingCategory.value) {
      await toolsApi.updateCategory(editingCategory.value.id, catForm.value)
    } else {
      await toolsApi.createCategory(catForm.value)
    }
    showCategoryForm.value = false
    editingCategory.value = null
    loadData()
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Error')
  }
}

const deleteCategory = async (cat: any) => {
  if (!confirm(t('adminTools.confirmDelete'))) return
  try {
    await toolsApi.deleteCategory(cat.id)
    loadData()
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Error')
  }
}

const openToolForm = (tool?: any) => {
  editingTool.value = tool || null
  if (tool) {
    toolForm.value = {
      name: tool.name, category_id: tool.category_id, url: tool.url, icon: tool.icon,
      description: tool.description, is_featured: tool.is_featured, sort_order: tool.sort_order || 0,
      tagsStr: (tool.tags || []).join(','), platformsStr: (tool.platforms || []).join(','),
    }
  } else {
    toolForm.value = emptyToolForm()
  }
  showToolForm.value = true
}

const cancelToolForm = () => { showToolForm.value = false; editingTool.value = null }

const saveTool = async () => {
  if (!toolForm.value.name) return
  const payload: any = {
    name: toolForm.value.name, category_id: toolForm.value.category_id, url: toolForm.value.url,
    icon: toolForm.value.icon, description: toolForm.value.description,
    is_featured: toolForm.value.is_featured, sort_order: toolForm.value.sort_order,
    tags: toolForm.value.tagsStr ? toolForm.value.tagsStr.split(',').map((s: string) => s.trim()).filter(Boolean) : [],
    platforms: toolForm.value.platformsStr ? toolForm.value.platformsStr.split(',').map((s: string) => s.trim()).filter(Boolean) : [],
  }
  try {
    if (editingTool.value) {
      await toolsApi.update(editingTool.value.id, payload)
    } else {
      await toolsApi.create(payload)
    }
    showToolForm.value = false
    editingTool.value = null
    loadData()
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Error')
  }
}

const deleteTool = async (tool: any) => {
  if (!confirm(t('adminTools.confirmDelete'))) return
  try {
    await toolsApi.delete(tool.id)
    loadData()
  } catch (_) {}
}
</script>
