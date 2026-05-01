import axios from 'axios'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 30000,
})

request.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

request.interceptors.response.use(
  (res) => res.data,
  (err) => {
    if (err.response?.data?.code === 1001 || err.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/admin/login'
    }
    return Promise.reject(err)
  }
)

export const auth = {
  login: (d: { username: string; password: string }) => request.post('/auth/login', d),
  me: () => request.get('/auth/me'),
}

export const tools = {
  listCategories: () => request.get('/categories'),
  createCategory: (d: { name: string; icon?: string; sort_order?: number }) => request.post('/categories', d),
  updateCategory: (id: number, d: any) => request.put(`/categories/${id}`, d),
  deleteCategory: (id: number) => request.delete(`/categories/${id}`),
  list: (params: { page?: number; page_size?: number; search?: string; category_id?: number } = {}) =>
    request.get('/tools', { params }),
  get: (id: number) => request.get(`/tools/${id}`),
  create: (d: any) => request.post('/tools', d),
  update: (id: number, d: any) => request.put(`/tools/${id}`, d),
  delete: (id: number) => request.delete(`/tools/${id}`),
}

export const users = {
  list: (params?: { page?: number; page_size?: number }) => request.get('/users', { params }),
  update: (id: number, d: any) => request.put(`/users/${id}`, d),
  delete: (id: number) => request.delete(`/users/${id}`),
}

export const audit = {
  list: (params?: { page?: number; page_size?: number; action?: string; target_type?: string }) =>
    request.get('/audit-logs', { params }),
}

export const stats = {
  get: () => request.get('/stats'),
}

export const settings = {
  hasAccessPassword: () => request.get('/settings/access-password'),
  verifyAccessPassword: (d: { password: string }) => request.post('/settings/access-password/verify', d),
  updateAccessPassword: (d: { password: string }) => request.put('/settings/access-password', d),
}

export default request
