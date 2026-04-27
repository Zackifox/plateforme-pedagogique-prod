<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <BreadcrumbNav :crumbs="crumbs" />

    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <div v-for="i in 4" :key="i" class="card p-5 h-24 animate-pulse bg-gray-100" />
    </div>

    <div v-else-if="erreur" class="text-center py-16 text-red-500">
      <p>{{ erreur }}</p>
      <button @click="charger" class="btn-secondary mt-4">Réessayer</button>
    </div>

    <template v-else-if="filiere">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">{{ filiere.nom }}</h1>

      <div v-if="niveaux.length === 0" class="text-center py-16 text-gray-400">
        Aucun niveau disponible pour cette filière.
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <router-link
          v-for="niveau in niveaux"
          :key="niveau.id"
          :to="{ name: 'Niveau', params: { id: niveau.id } }"
          class="card p-5 hover:border-blue-400 group flex items-center justify-between"
        >
          <div>
            <span class="font-semibold text-gray-900 group-hover:text-blue-700">
              {{ niveau.nom }}
            </span>
            <p class="text-sm text-gray-400 mt-0.5">{{ niveau.nb_matieres ?? 0 }} matière(s)</p>
          </div>
          <svg class="w-5 h-5 text-gray-300 group-hover:text-blue-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </router-link>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { catalogueApi } from '@/api/catalogue'
import BreadcrumbNav from '@/components/layout/BreadcrumbNav.vue'

const route = useRoute()
const filiere = ref(null)
const niveaux = ref([])
const loading = ref(true)
const erreur = ref(null)

const crumbs = computed(() => [
  filiere.value?.institut
    ? { label: 'Institut', to: { name: 'Institut', params: { id: filiere.value.institut } } }
    : null,
  { label: filiere.value?.nom || '…' },
].filter(Boolean))

async function charger() {
  loading.value = true
  erreur.value = null
  try {
    const id = route.params.id
    const [filRes, nivRes] = await Promise.all([
      catalogueApi.getFiliere(id),
      catalogueApi.getFiliereNiveaux(id),
    ])
    filiere.value = filRes.data
    niveaux.value = nivRes.data.results || nivRes.data
  } catch (e) {
    erreur.value = 'Impossible de charger les données.'
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(charger)
</script>