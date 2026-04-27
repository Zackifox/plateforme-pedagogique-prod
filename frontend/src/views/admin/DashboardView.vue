<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Tableau de bord</h1>
        <p class="text-sm text-gray-500 mt-0.5">Bonjour, {{ auth.user?.username }}</p>
      </div>
      <router-link to="/admin/upload" class="btn-primary">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
        Ajouter une ressource
      </router-link>
    </div>

    <!-- Statistiques -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-10">
      <div v-for="stat in stats" :key="stat.label" class="card p-5">
        <p class="text-sm text-gray-500">{{ stat.label }}</p>
        <p class="text-2xl font-bold text-gray-900 mt-1">{{ stat.value }}</p>
      </div>
    </div>

    <!-- Accès rapides -->
    <h2 class="text-lg font-semibold text-gray-900 mb-4">Accès rapides</h2>
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <router-link
        v-for="link in quickLinks"
        :key="link.to"
        :to="link.to"
        class="card p-5 hover:border-blue-400 group flex items-center gap-4"
      >
        <div class="w-10 h-10 rounded-lg flex items-center justify-center shrink-0" :class="link.bg">
          <component :is="link.icon" class="w-5 h-5" :class="link.color" />
        </div>
        <div>
          <p class="font-semibold text-gray-900 group-hover:text-blue-700">{{ link.label }}</p>
          <p class="text-sm text-gray-400">{{ link.desc }}</p>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, h } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { ressourcesApi } from '@/api/ressources'
import { catalogueApi } from '@/api/catalogue'

const auth = useAuthStore()
const stats = ref([
  { label: 'Ressources', value: '…' },
  { label: 'Instituts', value: '…' },
  { label: 'Filières', value: '…' },
  { label: 'Matières', value: '…' },
])

const UploadIcon = {
  render: () => h('svg', { fill: 'none', stroke: 'currentColor', 'stroke-width': '2', viewBox: '0 0 24 24' },
    [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12' })])
}
const ListIcon = {
  render: () => h('svg', { fill: 'none', stroke: 'currentColor', 'stroke-width': '2', viewBox: '0 0 24 24' },
    [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2' })])
}
const CatalogueIcon = {
  render: () => h('svg', { fill: 'none', stroke: 'currentColor', 'stroke-width': '2', viewBox: '0 0 24 24' },
    [h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', d: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10' })])
}

const quickLinks = [
  { to: '/admin/upload', label: 'Publier un PDF', desc: 'Ajouter cours ou sujet', bg: 'bg-blue-100', color: 'text-blue-700', icon: UploadIcon },
  { to: '/admin/communiques', label: 'Communiqués', desc: 'Publier des annonces', bg: 'bg-orange-100', color: 'text-orange-700', icon: ListIcon },
  { to: '/admin/ressources', label: 'Gérer les ressources', desc: 'Modifier, supprimer', bg: 'bg-green-100', color: 'text-green-700', icon: ListIcon },
  { to: '/admin/catalogue', label: 'Gérer le catalogue', desc: 'Instituts, filières…', bg: 'bg-purple-100', color: 'text-purple-700', icon: CatalogueIcon },
]

onMounted(async () => {
  try {
    const [resData, instData, filData, matData] = await Promise.all([
      ressourcesApi.getRessources({ page_size: 1 }),
      catalogueApi.getInstituts(),
      catalogueApi.getFilieres(),
      catalogueApi.getMatieres(),
    ])
    stats.value[0].value = resData.data.count ?? '—'
    stats.value[1].value = (instData.data.results || instData.data).length
    stats.value[2].value = (filData.data.results || filData.data).length
    stats.value[3].value = (matData.data.results || matData.data).length
  } catch { /* silencieux */ }
})
</script>