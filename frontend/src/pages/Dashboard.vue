<template>
  <div>
    <h2 class="text-2xl font-bold mb-8">{{ t('dashboard.title') }}</h2>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <router-link to="/tools" class="group bg-card rounded-xl border border-border p-6 hover:bg-muted/50 transition-all cursor-pointer">
        <h3 class="text-lg font-semibold">{{ t('dashboard.tools') }}</h3>
        <p class="text-sm text-muted-foreground mt-1">Manage your development tools and resources</p>
      </router-link>
      <router-link to="/upload" class="group bg-card rounded-xl border border-border p-6 hover:bg-muted/50 transition-all cursor-pointer">
        <h3 class="text-lg font-semibold">{{ t('dashboard.quickUpload') }}</h3>
        <p class="text-sm text-muted-foreground mt-1">Upload and share temporary files</p>
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>
