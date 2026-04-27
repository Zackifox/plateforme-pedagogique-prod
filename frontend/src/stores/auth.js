import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)

  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin = computed(() => user.value?.is_admin || user.value?.is_superuser || false)
  const isSuperAdmin = computed(() => user.value?.is_superuser || false)

  async function login(username, password) {
    const { data } = await api.post('/api/auth/login/', { username, password })
    accessToken.value = data.access
    refreshToken.value = data.refresh
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    await fetchMe()
  }

  async function fetchMe() {
    try {
      const { data } = await api.get('/api/auth/me/')
      user.value = data
    } catch {
      logout()
    }
  }

  function logout() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  // Restaurer l'utilisateur au démarrage si token présent
  if (accessToken.value) fetchMe()

  return { user, accessToken, isAuthenticated, isAdmin, isSuperAdmin, login, logout, fetchMe }
})
