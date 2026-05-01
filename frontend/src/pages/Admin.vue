<template>
  <MainLayout>
    <div>
      <h2 class="text-2xl font-bold mb-8">{{ t('dashboard.title') }}</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <router-link to="/admin/tools" class="group bg-card rounded-xl border border-border p-6 hover:bg-muted/50 transition-all cursor-pointer">
          <h3 class="text-lg font-semibold">{{ t('dashboard.tools') }}</h3>
          <p class="text-sm text-muted-foreground mt-1">{{ t('dashboard.toolsDesc') }}</p>
        </router-link>
        <div class="bg-card rounded-xl border border-border p-6 hover:bg-muted/50 transition-all">
          <h3 class="text-lg font-semibold">{{ t('dashboard.settings') }}</h3>
          <p class="text-sm text-muted-foreground mt-1">{{ t('dashboard.settingsDesc') }}</p>
          <div class="mt-4">
            <label class="text-xs text-muted-foreground block mb-1">{{ t('dashboard.accessPassword') }}</label>
            <div class="flex gap-2">
              <input v-model="newPassword" type="password" :placeholder="t('dashboard.accessPasswordPlaceholder')" class="flex-1 px-3 py-1.5 text-sm rounded-md border border-border bg-background focus:outline-none focus:ring-1 focus:ring-primary" />
              <button @click="updateAccessPassword" class="px-3 py-1.5 text-sm bg-primary text-primary-foreground rounded-md hover:opacity-90 transition">{{ t('dashboard.update') }}</button>
            </div>
            <p v-if="settingsMsg" :class="settingsOk ? 'text-green-500' : 'text-red-500'" class="text-xs mt-1">{{ settingsMsg }}</p>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import MainLayout from '@/layouts/MainLayout.vue'
import { settings as settingsApi } from '@/api'

const { t } = useI18n()
const newPassword = ref('')
const settingsMsg = ref('')
const settingsOk = ref(false)

const updateAccessPassword = async () => {
  settingsMsg.value = ''
  if (!newPassword.value) return
  try {
    await settingsApi.updateAccessPassword({ password: newPassword.value })
    settingsMsg.value = t('dashboard.passwordUpdated')
    settingsOk.value = true
    newPassword.value = ''
  } catch (e: any) {
    settingsMsg.value = e.response?.data?.detail || t('dashboard.updateFailed')
    settingsOk.value = false
  }
}
</script>
