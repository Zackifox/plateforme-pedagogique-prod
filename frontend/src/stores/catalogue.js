import { defineStore } from 'pinia'
import { ref } from 'vue'
import { catalogueApi } from '@/api/catalogue'

export const useCatalogueStore = defineStore('catalogue', () => {
  const instituts = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchInstituts() {
    loading.value = true
    error.value = null
    try {
      const { data } = await catalogueApi.getInstituts()
      instituts.value = data.results || data
    } catch (e) {
      error.value = 'Impossible de charger les instituts.'
    } finally {
      loading.value = false
    }
  }

  async function fetchFilieres(institutId) {
    const { data } = await catalogueApi.getInstitutFilieres(institutId)
    return data
  }

  async function fetchNiveaux(filiereId) {
    const { data } = await catalogueApi.getFilierNiveaux(filiereId)
    return data
  }

  async function fetchMatieres(niveauId) {
    const { data } = await catalogueApi.getNiveauMatieres(niveauId)
    return data
  }

  return { instituts, loading, error, fetchInstituts, fetchFilieres, fetchNiveaux, fetchMatieres }
})
