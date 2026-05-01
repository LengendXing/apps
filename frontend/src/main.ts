import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import zhCN from './i18n/locales/zh.json'
import enUS from './i18n/locales/en.json'
import './styles/main.css'

const routes = [
  { path: '/', name: 'Home', component: () => import('./pages/Home.vue') },
  { path: '/admin/login', name: 'Login', component: () => import('./pages/Login.vue') },
  { path: '/admin', name: 'Dashboard', component: () => import('./pages/Dashboard.vue'), meta: { requiresAuth: true } },
  { path: '/admin/tools', name: 'AdminTools', component: () => import('./pages/AdminTools.vue'), meta: { requiresAuth: true } },
  { path: '/admin/users', name: 'AdminUsers', component: () => import('./pages/AdminUsers.vue'), meta: { requiresAuth: true } },
  { path: '/admin/audit', name: 'AdminAudit', component: () => import('./pages/AdminAudit.vue'), meta: { requiresAuth: true } },
]

const router = createRouter({ history: createWebHistory(), routes })
const i18n = createI18n({ legacy: false, locale: 'zh', fallbackLocale: 'en', messages: { zh: zhCN, en: enUS } })

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) next('/admin/login')
  else next()
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(i18n)
app.mount('#app')
