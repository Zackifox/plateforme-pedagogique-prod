<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <BreadcrumbNav :crumbs="[{ label: niveau?.nom || '…' }]" />
    <template v-if="!loading && niveau">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">{{ niveau.nom }}</h1>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <router-link
          v-for="matiere in matieres"
          :key="matiere.id"
          :to="{ name: 'Matiere', params: { id: matiere.id } }"
          class="card p-5 hover:border-blue-400 group flex items-center justify-between"
        >
          <div>
            <p v-if="matiere.code" class="text-xs text-gray-400 font-mono mb-0.5">{{ matiere.code }}</p>
            <span class="font-semibold text-gray-900 group-hover:text-blue-700">{{ matiere.nom }}</span>
            <p class="text-sm text-gray-400 mt-0.5">{{ matiere.nb_ressources }} ressource(s)</p>
          </div>
          <svg class="w-5 h-5 text-gray-300 group-hover:text-blue-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
          </svg>
        </router-link>
      </div>
    </template>
    <div v-else-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <div v-for="i in 6" :key="i" class="card p-5 h-24 animate-pulse bg-gray-100" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { catalogueApi } from '@/api/catalogue'
import BreadcrumbNav from '@/components/layout/BreadcrumbNav.vue'

const route = useRoute()
const niveau = ref(null)
const matieres = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const [nivRes, matRes] = await Promise.all([
      catalogueApi.getNiveau(route.params.id),
      catalogueApi.getNiveauMatieres(route.params.id),
    ])
    niveau.value = nivRes.data
    matieres.value = matRes.data
  } finally {
    loading.value = false
  }
})
</script>
