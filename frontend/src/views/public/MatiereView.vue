<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <BreadcrumbNav :crumbs="[{ label: matiere?.nom || '…' }]" />
    <template v-if="!loading && matiere">
      <div class="flex items-center justify-between mb-6 flex-wrap gap-3">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">{{ matiere.nom }}</h1>
          <p v-if="matiere.code" class="text-sm text-gray-400 font-mono">{{ matiere.code }}</p>
        </div>
        <div class="flex gap-2">
          <button
            v-for="type in types"
            :key="type.value"
            @click="filtreType = filtreType === type.value ? '' : type.value"
            class="text-xs px-3 py-1.5 rounded-full border transition-colors"
            :class="filtreType === type.value ? 'bg-blue-700 text-white border-blue-700' : 'border-gray-300 text-gray-600 hover:border-blue-400'"
          >
            {{ type.label }}
          </button>
        </div>
      </div>
      <RessourceList :ressources="ressourcesFiltrees" :loading="false" />
    </template>
    <div v-else-if="loading">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="i in 6" :key="i" class="card p-4 h-40 animate-pulse bg-gray-100" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { catalogueApi } from '@/api/catalogue'
import { ressourcesApi } from '@/api/ressources'
import RessourceList from '@/components/ressources/RessourceList.vue'
import BreadcrumbNav from '@/components/layout/BreadcrumbNav.vue'

const route = useRoute()
const matiere = ref(null)
const ressources = ref([])
const filtreType = ref('')
const loading = ref(true)

const types = [
  { value: 'cours', label: 'Cours' },
  { value: 'sujet', label: 'Sujets' },
  { value: 'td', label: 'TD' },
  { value: 'tp', label: 'TP' },
]

const ressourcesFiltrees = computed(() =>
  filtreType.value ? ressources.value.filter((r) => r.type_ressource === filtreType.value) : ressources.value
)

onMounted(async () => {
  try {
    const [matRes, resRes] = await Promise.all([
      catalogueApi.getMatiere(route.params.id),
      ressourcesApi.getRessources({ matiere: route.params.id }),
    ])
    matiere.value = matRes.data
    ressources.value = resRes.data.results || resRes.data
  } finally {
    loading.value = false
  }
})
</script>
