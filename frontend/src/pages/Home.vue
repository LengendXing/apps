<template>
  <!-- Password Gate (only when backend API is available) -->
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

    <!-- Body: centered container wrapping sidebar + content + drawer -->
    <div class="flex-1 flex justify-center overflow-hidden">
      <div class="w-full max-w-[1400px] flex overflow-hidden relative">

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
            <div v-for="tool in filteredTools" :key="tool.id"
                 class="group aspect-square bg-card rounded-xl border border-border p-3 flex flex-col items-center justify-center gap-2 hover:bg-muted/60 hover:border-primary/30 transition-all cursor-pointer relative">
              <!-- Info icon top-right -->
              <button @click.stop="openDrawer(tool)" class="absolute top-2 right-2 w-5 h-5 rounded-full bg-muted text-muted-foreground flex items-center justify-center text-[10px] hover:bg-primary hover:text-primary-foreground transition-colors z-10" title="Detail">
                i
              </button>
              <!-- Card body: click goes to main URL -->
              <a :href="tool.url" target="_blank" @click.stop class="flex flex-col items-center justify-center gap-2 w-full h-full no-underline text-foreground">
                <div class="w-11 h-11 rounded-lg bg-muted flex items-center justify-center text-xl flex-shrink-0 group-hover:scale-110 transition-transform overflow-hidden">
                  <img v-if="isIconUrl(tool.icon)" :src="tool.icon" class="w-full h-full object-cover rounded-lg" alt="" />
                  <span v-else>{{ tool.icon || '🔗' }}</span>
                </div>
                <span class="text-xs font-medium text-center leading-tight line-clamp-2 w-full">{{ tool.name }}</span>
              </a>
            </div>
          </div>
          <p v-else-if="!loading" class="text-center text-muted-foreground py-20 text-sm">{{ t('home.empty') }}</p>
          <p v-else class="text-center text-muted-foreground py-20 text-sm">Loading...</p>
        </main>

        <!-- Right Drawer -->
        <transition name="drawer">
          <div v-if="drawerTool" class="absolute top-0 right-0 bottom-0 w-80 bg-card border-l border-border overflow-y-auto z-40 shadow-lg">
            <div class="p-5">
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-bold">{{ drawerTool.name }}</h3>
                <button @click="drawerTool = null" class="w-6 h-6 rounded-full bg-muted flex items-center justify-center text-xs hover:bg-primary hover:text-primary-foreground transition-colors">✕</button>
              </div>
              <!-- Icon -->
              <div class="w-16 h-16 rounded-xl bg-muted flex items-center justify-center text-3xl mb-4 overflow-hidden">
                <img v-if="isIconUrl(drawerTool.icon)" :src="drawerTool.icon" class="w-full h-full object-cover rounded-xl" alt="" />
                <span v-else>{{ drawerTool.icon || '🔗' }}</span>
              </div>
              <!-- Description -->
              <p v-if="drawerTool.description" class="text-sm text-muted-foreground mb-4">{{ drawerTool.description }}</p>
              <!-- Main URL -->
              <div v-if="drawerTool.url" class="mb-4">
                <a :href="drawerTool.url" target="_blank" class="text-sm text-primary hover:underline break-all">{{ drawerTool.url }}</a>
              </div>
              <!-- Tags & Platforms -->
              <div v-if="drawerTool.tags?.length" class="flex flex-wrap gap-1 mb-3">
                <span v-for="tag in drawerTool.tags" :key="tag" class="px-2 py-0.5 text-xs rounded bg-muted text-muted-foreground">{{ tag }}</span>
              </div>
              <div v-if="drawerTool.platforms?.length" class="flex flex-wrap gap-1 mb-4">
                <span v-for="p in drawerTool.platforms" :key="p" class="px-2 py-0.5 text-xs rounded bg-muted text-muted-foreground">{{ p }}</span>
              </div>
              <!-- Versions -->
              <div v-if="drawerTool.versions?.length">
                <h4 class="text-sm font-semibold mb-2">{{ t('home.versions') }}</h4>
                <div class="space-y-1">
                  <div v-for="(v, idx) in drawerTool.versions" :key="idx" class="flex items-center gap-2 text-sm">
                    <span class="text-muted-foreground w-6 text-right flex-shrink-0">{{ idx + 1 }}.</span>
                    <a v-if="v.url" :href="v.url" target="_blank" class="text-primary hover:underline">{{ v.version }}</a>
                    <span v-else>{{ v.version }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </transition>

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
import { ref, computed, onMounted, nextTick } from 'vue'
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
const drawerTool = ref<any>(null)
const isStaticMode = ref(false)

const isIconUrl = (icon: string) => icon && (icon.startsWith('http://') || icon.startsWith('https://'))

const toggleDark = () => {
  isDark.value = !isDark.value
  localStorage.setItem('dark', String(isDark.value))
  document.documentElement.classList.toggle('dark')
}

const openDrawer = (tool: any) => {
  drawerTool.value = tool
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

const loadToolsFromStatic = async () => {
  loading.value = true
  try {
    const res = await fetch('/data.json')
    const data = await res.json()
    categories.value = data.categories || []
    allTools.value = data.tools || []
  } catch (e) {
    console.error('Failed to load static data:', e)
  } finally {
    loading.value = false
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
    // Backend unavailable, fall back to static data
    isStaticMode.value = true
    await loadToolsFromStatic()
  } finally {
    if (!isStaticMode.value) loading.value = false
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
  if (isStaticMode.value || sessionStorage.getItem('access_verified') === 'true') {
    showPasswordGate.value = false
    if (isStaticMode.value) {
      loadToolsFromStatic()
    } else {
      loadTools()
    }
  } else {
    // Try API first, if unreachable skip password gate and use static data
    loadTools().then(() => {
      if (isStaticMode.value) {
        showPasswordGate.value = false
      }
    })
  }
})
</script>

<style scoped>
.drawer-enter-active,
.drawer-leave-active {
  transition: transform 0.2s ease;
}
.drawer-enter-from,
.drawer-leave-to {
  transform: translateX(100%);
}
</style>
