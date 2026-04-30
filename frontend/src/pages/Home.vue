<template>
  <div v-if="showPasswordGate" class="min-h-screen bg-background flex items-center justify-center">
    <div class="w-full max-w-md mx-auto p-8">
      <div class="bg-card rounded-xl border border-border p-8 shadow-sm">
        <h2 class="text-2xl font-bold mb-2 text-center">{{ t('home.welcome') }}</h2>
        <p class="text-sm text-muted-foreground text-center mb-6">{{ t('home.hint') }}</p>
        <form @submit.prevent="handleVerify" class="space-y-4">
          <div>
            <label class="text-sm block mb-1 text-muted-foreground">{{ t('home.password') }}</label>
            <input v-model="form.password" type="password" class="w-full px-3 py-2 rounded-md border border-border bg-background focus:outline-none focus:ring-1 focus:ring-primary" required />
          </div>
          <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
          <button type="submit" class="w-full py-2 bg-primary text-primary-foreground rounded-md hover:opacity-90 transition font-medium">{{ t('home.submit') }}</button>
        </form>
      </div>
    </div>
  </div>
  <div v-else>
    <header class="sticky top-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div class="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
        <span class="text-lg font-bold tracking-tight">Apps</span>
        <div class="flex items-center gap-2">
          <button @click="locale = locale === 'zh' ? 'en' : 'zh'" class="px-2 py-1 text-xs rounded border border-border hover:bg-muted transition-colors">
            {{ locale === 'zh' ? '中' : 'EN' }}
          </button>
          <button @click="toggleDark" class="px-2 py-1 text-xs rounded border border-border hover:bg-muted transition-colors">
            {{ isDark ? '☀' : '☾' }}
          </button>
        </div>
      </div>
    </header>
    <main class="max-w-7xl mx-auto px-6 py-8">
      <div class="mb-8">
        <h1 class="text-2xl font-bold mb-4">{{ t('home.tools') }}</h1>
        <input v-model="searchQuery" :placeholder="t('home.search')" class="w-full md:w-96 px-3 py-2 rounded-md border border-border bg-background text-sm" />
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
      <p v-if="!categories.length" class="text-center text-muted-foreground py-12">{{ t('home.empty') }}</p>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { tools as toolsApi, settings } from '@/api'

const { t } = useI18n()
const { locale } = useI18n()
const form = ref({ password: '' })
const error = ref('')
const showPasswordGate = ref(true)
const isDark = ref(localStorage.getItem('dark') === 'true')
const categories = ref<any[]>([])
const allTools = ref<any[]>([])
const searchQuery = ref('')

const toggleDark = () => {
  isDark.value = !isDark.value
  localStorage.setItem('dark', String(isDark.value))
  document.documentElement.classList.toggle('dark')
}

const handleVerify = async () => {
  error.value = ''
  try {
    const res = await settings.verifyAccessPassword({ password: form.value.password })
    if (res.data?.verified) {
      sessionStorage.setItem('access_verified', 'true')
      showPasswordGate.value = false
      loadTools()
    } else {
      error.value = res.message || t('home.wrongPassword')
    }
  } catch (e: any) {
    error.value = e.response?.data?.message || t('home.wrongPassword')
  }
}

const loadTools = async () => {
  try {
    const [catsRes, toolsRes] = await Promise.all([toolsApi.listCategories(), toolsApi.list()])
    categories.value = catsRes.data
    allTools.value = toolsRes.data.items || []
  } catch (_) {}
}

const getTools = (catId: number) => {
  let items = allTools.value.filter((t: any) => t.category_id === catId)
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    items = items.filter((t: any) => t.name.toLowerCase().includes(q) || t.description.toLowerCase().includes(q))
  }
  return items
}

onMounted(() => {
  if (sessionStorage.getItem('access_verified') === 'true') {
    showPasswordGate.value = false
    loadTools()
  }
})
</script>
