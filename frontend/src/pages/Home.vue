<template>
  <!-- Password Gate -->
  <div v-if="showPasswordGate" class="h-screen bg-background flex items-center justify-center">
    <div class="w-full max-w-md mx-auto p-8">
      <div class="bg-card rounded-2xl border border-border p-10 shadow-sm">
        <h2 class="text-3xl font-bold mb-2 text-center">{{ t('home.welcome') }}</h2>
        <p class="text-sm text-muted-foreground text-center mb-8">{{ t('home.hint') }}</p>
        <form @submit.prevent="handleVerify" class="space-y-4">
          <input v-model="form.password" type="password" :placeholder="t('home.password')"
                 class="w-full px-4 py-3 rounded-lg border border-border bg-background focus:outline-none focus:ring-2 focus:ring-primary/50 text-center text-lg tracking-widest" required />
          <p v-if="error" class="text-red-500 text-sm text-center">{{ error }}</p>
          <button type="submit" class="w-full py-3 bg-primary text-primary-foreground rounded-lg hover:opacity-90 transition font-medium">{{ t('home.submit') }}</button>
        </form>
      </div>
    </div>
  </div>

  <!-- Main Layout -->
  <div v-else class="h-screen flex flex-col overflow-hidden">

    <!-- Fixed Top Bar -->
    <header class="flex-shrink-0 h-12 bg-background/90 backdrop-blur-md border-b border-border z-50">
      <div class="max-w-[1400px] mx-auto h-full flex items-center justify-between px-2">
        <span class="text-base font-bold tracking-tight pl-1">Apps</span>
        <div class="flex items-center gap-2">
          <button @click="locale = locale === 'zh' ? 'en' : 'zh'" class="px-2 py-0.5 text-xs rounded border border-border hover:bg-muted transition-colors">
            {{ locale === 'zh' ? '中' : 'EN' }}
          </button>
          <button @click="toggleDark" class="px-2 py-0.5 text-xs rounded border border-border hover:bg-muted transition-colors">
            {{ isDark ? '☀' : '☾' }}
          </button>
        </div>
      </div>
    </header>

    <!-- Body: centered container wrapping sidebar + content -->
    <div class="flex-1 flex justify-center overflow-hidden">
      <div class="w-full max-w-[1400px] flex overflow-hidden">

        <!-- Left Category Panel -->
        <aside class="flex-shrink-0 w-44 border-r border-border overflow-y-auto py-3 px-2">
          <button @click="selectedCategoryId = 0"
                  :class="selectedCategoryId === 0 ? 'bg-primary text-primary-foreground font-medium' : 'text-muted-foreground hover:bg-muted'"
                  class="w-full text-left px-3 py-2 rounded-lg text-sm transition-colors truncate mb-0.5">
            {{ t('home.all') }}
          </button>
          <button v-for="cat in categories" :key="cat.id" @click="selectedCategoryId = cat.id"
                  :class="selectedCategoryId === cat.id ? 'bg-primary text-primary-foreground font-medium' : 'text-muted-foreground hover:bg-muted'"
                  class="w-full text-left px-3 py-2 rounded-lg text-sm transition-colors truncate mb-0.5">
            {{ cat.icon }} {{ cat.name }}
          </button>
        </aside>

        <!-- Main Content: Card Grid (scrollable) -->
        <main class="flex-1 overflow-y-auto p-5">
          <!-- Search -->
          <div class="mb-4">
            <input v-model="searchQuery" :placeholder="t('home.search')"
                   class="w-full max-w-md px-4 py-2 rounded-lg border border-border bg-background text-sm focus:outline-none focus:ring-2 focus:ring-primary/30" />
          </div>
          <!-- Card Grid -->
          <div v-if="filteredTools.length" class="grid grid-cols-7 gap-3">
            <a v-for="tool in filteredTools" :key="tool.id" :href="tool.url" target="_blank"
               class="group aspect-square bg-card rounded-xl border border-border p-3 flex flex-col items-center justify-center gap-2 hover:bg-muted/60 hover:border-primary/30 transition-all cursor-pointer no-underline text-foreground">
              <div class="w-11 h-11 rounded-lg bg-muted flex items-center justify-center text-xl flex-shrink-0 group-hover:scale-110 transition-transform">
                {{ tool.icon || '🔗' }}
              </div>
              <span class="text-xs font-medium text-center leading-tight line-clamp-2 w-full">{{ tool.name }}</span>
            </a>
          </div>
          <p v-else-if="!loading" class="text-center text-muted-foreground py-20 text-sm">{{ t('home.empty') }}</p>
          <p v-else class="text-center text-muted-foreground py-20 text-sm">Loading...</p>
        </main>

      </div>
    </div>

    <!-- Fixed Bottom Bar -->
    <footer class="flex-shrink-0 h-9 bg-background/90 backdrop-blur-md border-t border-border z-50">
      <div class="max-w-[1400px] mx-auto h-full flex items-center justify-center gap-4 text-xs text-muted-foreground">
        <span>Powered by Apps Startpage</span>
        <span>&copy; {{ new Date().getFullYear() }}</span>
      </div>
    </footer>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
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
const selectedCategoryId = ref(0)
const loading = ref(false)

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
      await nextTick()
      loadTools()
    } else {
      error.value = t('home.wrongPassword')
    }
  } catch (e: any) {
    const msg = e.response?.data?.message
    error.value = msg || t('home.wrongPassword')
  }
}

const loadTools = async () => {
  loading.value = true
  try {
    const [catsRes, toolsRes] = await Promise.all([
      toolsApi.listCategories(),
      toolsApi.list({ page_size: 100 }),
    ])
    categories.value = catsRes.data || []
    allTools.value = toolsRes.data?.items || []
  } catch (e) {
    console.error('Failed to load tools:', e)
  } finally {
    loading.value = false
  }
}

const filteredTools = computed(() => {
  let items = allTools.value
  if (selectedCategoryId.value) {
    items = items.filter((t: any) => t.category_id === selectedCategoryId.value)
  }
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    items = items.filter((t: any) => t.name.toLowerCase().includes(q) || (t.description || '').toLowerCase().includes(q))
  }
  return items
})

onMounted(() => {
  if (isDark.value) document.documentElement.classList.add('dark')
  if (sessionStorage.getItem('access_verified') === 'true') {
    showPasswordGate.value = false
    loadTools()
  }
})
</script>
