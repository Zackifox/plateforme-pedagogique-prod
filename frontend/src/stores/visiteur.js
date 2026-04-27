import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/axios'

export const useVisiteurStore = defineStore('visiteur', () => {
  const user = ref(JSON.parse(localStorage.getItem('visiteur_user') || 'null'))
  const accessToken = ref(localStorage.getItem('visiteur_access') || null)

  const isConnecte = computed(() => !!accessToken.value)

  async function inscrire(username, email, password, password2) {
    const { data } = await api.post('/api/auth/inscription/', { username, email, password, password2 })
    _sauvegarder(data)
  }

  async function login(username, password) {
    const { data } = await api.post('/api/auth/login/', { username, password })
    _sauvegarder(data)
  }

  async function loginGoogle(googleToken) {
    const { data } = await api.post('/api/auth/login-google/', { token: googleToken })
    _sauvegarder(data)
    return data
  }

  function _sauvegarder(data) {
    accessToken.value = data.access
    user.value = {
      username: data.username,
      email: data.email || '',
    }
    localStorage.setItem('visiteur_access', data.access)
    localStorage.setItem('visiteur_refresh', data.refresh || '')
    localStorage.setItem('visiteur_user', JSON.stringify(user.value))
    api.defaults.headers.common['Authorization'] = `Bearer ${data.access}`
  }

  function logout() {
    user.value = null
    accessToken.value = null
    localStorage.removeItem('visiteur_access')
    localStorage.removeItem('visiteur_refresh')
    localStorage.removeItem('visiteur_user')
    delete api.defaults.headers.common['Authorization']
  }

  if (accessToken.value) {
    api.defaults.headers.common['Authorization'] = `Bearer ${accessToken.value}`
  }

  return { user, accessToken, isConnecte, inscrire, login, loginGoogle, logout }
})