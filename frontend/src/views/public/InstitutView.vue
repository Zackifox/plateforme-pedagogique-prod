<template>
  <div class="max-w-6xl mx-auto px-4 py-8">

    <BreadcrumbNav :crumbs="[{ label: institut?.nom || '…' }]" />

    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <div v-for="i in 4" :key="i" class="card p-5 h-28 animate-pulse bg-gray-100" />
    </div>

    <div v-else-if="erreur" class="text-center py-16 text-red-500">
      <p>{{ erreur }}</p>
      <button @click="charger" class="btn-secondary mt-4">Réessayer</button>
    </div>

    <template v-else-if="institut">
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-gray-900">{{ institut.nom }}</h1>
        <p v-if="institut.sigle" class="text-sm text-gray-400 mt-0.5">{{ institut.sigle }}</p>
        <p v-if="institut.description" class="text-gray-500 mt-1">{{ institut.description }}</p>
      </div>

      <div v-if="filieres.length === 0" class="text-center py-16 text-gray-400">
        <p>Aucune filière disponible pour cet institut.</p>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <router-link
          v-for="filiere in filieres"
          :key="filiere.id"
          :to="{ name: 'Filiere', params: { id: filiere.id } }"
          class="card p-5 hover:border-blue-400 group"
        >
          <div class="flex items-center justify-between mb-2">
            <span class="font-semibold text-gray-900 group-hover:text-blue-700">
              {{ filiere.nom }}
            </span>
            <span class="text-xs text-gray-400">{{ filiere.nb_niveaux ?? 0 }} niveau(x)</span>
          </div>
          <p v-if="filiere.sigle" class="text-sm text-gray-400">{{ filiere.sigle }}</p>
          <p v-if="filiere.description" class="text-sm text-gray-500 mt-1 line-clamp-2">
            {{ filiere.description }}
          </p>
        </router-link>
      </div>
    </template>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/axios'
import BreadcrumbNav from '@/components/layout/BreadcrumbNav.vue'

const route = useRoute()
const institut = ref(null)
const filieres = ref([])
const loading = ref(true)
const erreur = ref(null)

async function charger() {
  loading.value = true
  erreur.value = null
  try {
    const id = route.params.id
    const [instRes, filRes] = await Promise.all([
      api.get(`/api/catalogue/instituts/${id}/`),
      api.get(`/api/catalogue/instituts/${id}/filieres/`),
    ])
    institut.value = instRes.data
    filieres.value = filRes.data.results || filRes.data
  } catch (e) {
    erreur.value = 'Impossible de charger les données. Vérifiez que le serveur Django tourne.'
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(charger)
</script>