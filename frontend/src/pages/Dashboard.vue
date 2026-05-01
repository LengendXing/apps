<template>
  <MainLayout>
    <div>
      <h2 class="text-2xl font-bold mb-8">{{ t('dashboard.title') }}</h2>

      <div v-if="statData" class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
        <div class="bg-card rounded-xl border border-border p-5">
          <p class="text-sm text-muted-foreground">{{ t('dashboard.statUsers') }}</p>
          <p class="text-2xl font-bold mt-1">{{ statData.users }}</p>
          <p class="text-xs text-muted-foreground mt-1">{{ statData.active_users }} {{ t('adminUsers.active') }}</p>
        </div>
        <div class="bg-card rounded-xl border border-border p-5">
          <p class="text-sm text-muted-foreground">{{ t('dashboard.statCategories') }}</p>
          <p class="text-2xl font-bold mt-1">{{ statData.categories }}</p>
        </div>
        <div class="bg-card rounded-xl border border-border p-5">
          <p class="text-sm text-muted-foreground">{{ t('dashboard.statTools') }}</p>
          <p class="text-2xl font-bold mt-1">{{ statData.tools }}</p>
          <p class="text-xs text-muted-foreground mt-1">{{ statData.featured_tools }} {{ t('tools.featured') }}</p>
        </div>
      </div>

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

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <router-link to="/admin/users" class="bg-card rounded-xl border border-border p-6 hover:bg-muted/50 transition-all cursor-pointer">
          <h3 class="text-lg font-semibold">{{ t('dashboard.users') }}</h3>
          <p class="text-sm text-muted-foreground mt-1">{{ t('dashboard.usersDesc') }}</p>
        </router-link>
        <router-link to="/admin/audit" class="bg-card rounded-xl border border-border p-6 hover:bg-muted/50 transition-all cursor-pointer">
          <h3 class="text-lg font-semibold">{{ t('dashboard.audit') }}</h3>
          <p class="text-sm text-muted-foreground mt-1">{{ t('dashboard.auditDesc') }}</p>
        </router-link>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import MainLayout from '@/layouts/MainLayout.vue'
import { stats as statsApi, settings as settingsApi } from '@/api'

const { t } = useI18n()
const statData = ref<any>(null)
const newPassword = ref('')
const settingsMsg = ref('')
const settingsOk = ref(false)

onMounted(async () => {
  try {
    const res = await statsApi.get()
    statData.value = res.data
  } catch (_) {}
})

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
