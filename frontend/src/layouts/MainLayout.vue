<template>
  <div class="min-h-screen bg-background text-foreground">
    <header class="sticky top-0 z-50 bg-background/80 backdrop-blur-md border-b border-border">
      <div class="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
        <router-link to="/dashboard" class="text-lg font-bold tracking-tight">Apps</router-link>
        <nav class="flex items-center gap-1">
          <router-link to="/dashboard" class="px-3 py-1.5 text-sm rounded-md hover:bg-muted transition-colors">{{ t('nav.dashboard') }}</router-link>
          <router-link to="/tools" class="px-3 py-1.5 text-sm rounded-md hover:bg-muted transition-colors">{{ t('nav.tools') }}</router-link>
          <router-link to="/upload" class="px-3 py-1.5 text-sm rounded-md hover:bg-muted transition-colors">{{ t('nav.upload') }}</router-link>
        </nav>
        <div class="flex items-center gap-2">
          <button @click="locale = locale === 'zh' ? 'en' : 'zh'" class="px-2 py-1 text-xs rounded border border-border hover:bg-muted transition-colors">
            {{ locale === 'zh' ? '中' : 'EN' }}
          </button>
          <button @click="toggleDark" class="px-2 py-1 text-xs rounded border border-border hover:bg-muted transition-colors">
            {{ isDark ? '☀' : '☾' }}
          </button>
          <button @click="handleLogout" class="px-2 py-1 text-xs rounded border border-border hover:bg-muted transition-colors">{{ t('nav.logout') }}</button>
        </div>
      </div>
    </header>
    <main class="max-w-7xl mx-auto px-6 py-8">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()
const { locale } = useI18n()
const router = useRouter()
const authStore = useAuthStore()
const isDark = ref(localStorage.getItem('dark') === 'true')

const toggleDark = () => {
  isDark.value = !isDark.value
  localStorage.setItem('dark', String(isDark.value))
  document.documentElement.classList.toggle('dark')
}

const handleLogout = () => { authStore.logout(); router.push('/login') }
</script>
