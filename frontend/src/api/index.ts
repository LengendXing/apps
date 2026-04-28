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
      window.location.href = '/login'
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
  createCategory: (d: { name: string; icon?: string }) => request.post('/categories', d),
  list: (params: { page?: number; page_size?: number; search?: string; category_id?: number } = {}) =>
    request.get('/tools', { params }),
  create: (d: any) => request.post('/tools', d),
  update: (id: number, d: any) => request.put(`/tools/${id}`, d),
  delete: (id: number) => request.delete(`/tools/${id}`),
}

export const uploads = {
  upload: (file: File) => {
    const fd = new FormData()
    fd.append('file', file)
    return request.post('/uploads', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
  },
  list: () => request.get('/uploads'),
  delete: (id: number) => request.delete(`/uploads/${id}`),
}

export default request
