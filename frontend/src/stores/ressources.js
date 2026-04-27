import { defineStore } from 'pinia'
import { ref } from 'vue'
import { ressourcesApi } from '@/api/ressources'

export const useRessourcesStore = defineStore('ressources', () => {
  const ressources = ref([])
  const total = ref(0)
  const loading = ref(false)
  const error = ref(null)

  async function fetchRessources(params = {}) {
    loading.value = true
    error.value = null
    try {
      const { data } = await ressourcesApi.getRessources(params)
      ressources.value = data.results || data
      total.value = data.count || ressources.value.length
    } catch (e) {
      error.value = 'Impossible de charger les ressources.'
    } finally {
      loading.value = false
    }
  }

  async function deleteRessource(id) {
    await ressourcesApi.deleteRessource(id)
    ressources.value = ressources.value.filter((r) => r.id !== id)
    total.value--
  }

  return { ressources, total, loading, error, fetchRessources, deleteRessource }
})
