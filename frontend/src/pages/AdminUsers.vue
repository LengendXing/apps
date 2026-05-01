<template>
  <MainLayout>
    <div>
      <h2 class="text-2xl font-bold mb-6">{{ t('adminUsers.title') }}</h2>
      <div class="bg-card rounded-lg border border-border overflow-hidden">
        <table class="w-full text-sm">
          <thead class="border-b border-border">
            <tr>
              <th class="px-4 py-3 text-left font-medium text-muted-foreground">ID</th>
              <th class="px-4 py-3 text-left font-medium text-muted-foreground">{{ t('adminUsers.username') }}</th>
              <th class="px-4 py-3 text-left font-medium text-muted-foreground">{{ t('adminUsers.email') }}</th>
              <th class="px-4 py-3 text-left font-medium text-muted-foreground">{{ t('adminUsers.role') }}</th>
              <th class="px-4 py-3 text-left font-medium text-muted-foreground">{{ t('adminUsers.isActive') }}</th>
              <th class="px-4 py-3 text-right font-medium text-muted-foreground">{{ t('adminUsers.action') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id" class="border-b border-border last:border-0">
              <td class="px-4 py-3 text-muted-foreground">{{ u.id }}</td>
              <td class="px-4 py-3 font-medium">{{ u.username }}</td>
              <td class="px-4 py-3 text-muted-foreground">{{ u.email }}</td>
              <td class="px-4 py-3">
                <span :class="u.role === 'admin' ? 'text-primary font-medium' : 'text-muted-foreground'">
                  {{ u.role === 'admin' ? t('adminUsers.admin') : t('adminUsers.user') }}
                </span>
              </td>
              <td class="px-4 py-3">
                <span :class="u.is_active ? 'text-green-500' : 'text-red-400'">
                  {{ u.is_active ? t('adminUsers.active') : t('adminUsers.inactive') }}
                </span>
              </td>
              <td class="px-4 py-3 text-right space-x-2">
                <button v-if="u.is_active" @click="toggleActive(u, false)" class="text-orange-400 hover:text-orange-600 text-xs">{{ t('adminUsers.disable') }}</button>
                <button v-else @click="toggleActive(u, true)" class="text-green-500 hover:text-green-700 text-xs">{{ t('adminUsers.enable') }}</button>
                <button v-if="u.role !== 'admin'" @click="toggleRole(u)" class="text-muted-foreground hover:text-foreground text-xs">
                  {{ u.role === 'admin' ? '' : t('adminUsers.admin') }}
                </button>
                <button v-if="u.role === 'admin' && u.username !== 'admin'" @click="toggleRole(u)" class="text-muted-foreground hover:text-foreground text-xs">
                  {{ t('adminUsers.user') }}
                </button>
                <button @click="deleteUser(u)" class="text-red-400 hover:text-red-600 text-xs">{{ t('adminUsers.deleteUser') }}</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="total > pageSize" class="flex items-center justify-center gap-2 mt-4">
        <button v-for="p in totalPages" :key="p" @click="page = p; loadUsers()"
                :class="p === page ? 'bg-primary text-primary-foreground' : 'border border-border'"
                class="px-3 py-1 text-sm rounded-md">{{ p }}</button>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import MainLayout from '@/layouts/MainLayout.vue'
import { users as usersApi } from '@/api'

const { t } = useI18n()
const users = ref<any[]>([])
const page = ref(1)
const pageSize = 20
const total = ref(0)
const totalPages = computed(() => Math.ceil(total.value / pageSize))

const loadUsers = async () => {
  try {
    const res = await usersApi.list({ page: page.value, page_size: pageSize })
    users.value = res.data.items || []
    total.value = res.data.total || 0
  } catch (_) {}
}

onMounted(loadUsers)

const toggleActive = async (u: any, active: boolean) => {
  try {
    await usersApi.update(u.id, { is_active: active })
    loadUsers()
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Error')
  }
}

const toggleRole = async (u: any) => {
  const newRole = u.role === 'admin' ? 'user' : 'admin'
  try {
    await usersApi.update(u.id, { role: newRole })
    loadUsers()
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Error')
  }
}

const deleteUser = async (u: any) => {
  if (!confirm(t('adminUsers.confirmDelete'))) return
  try {
    await usersApi.delete(u.id)
    loadUsers()
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Error')
  }
}
</script>
