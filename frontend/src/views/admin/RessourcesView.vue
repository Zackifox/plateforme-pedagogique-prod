<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Ressources</h1>
      <router-link to="/admin/upload" class="btn-primary text-sm">+ Ajouter</router-link>
    </div>

    <!-- Filtres -->
    <div class="card p-4 mb-6 flex flex-wrap gap-3">
      <input v-model="search" @input="debouncedFetch" type="search" placeholder="Rechercher…" class="input max-w-xs text-sm" />
      <select v-model="filtreType" @change="fetchData" class="input max-w-xs text-sm">
        <option value="">Tous les types</option>
        <option value="cours">Cours</option>
        <option value="sujet">Sujets</option>
        <option value="td">TD</option>
        <option value="tp">TP</option>
        <option value="autre">Autre</option>
      </select>
      <span class="text-sm text-gray-400 self-center ml-auto">{{ store.total }} résultat(s)</span>
    </div>

    <!-- Tableau -->
    <div class="card overflow-hidden">
      <div v-if="store.loading" class="p-8 text-center text-gray-400">Chargement…</div>
      <div v-else-if="store.ressources.length === 0" class="p-8 text-center text-gray-400">Aucune ressource trouvée.</div>
      <table v-else class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th class="text-left px-4 py-3 font-medium text-gray-600">Titre</th>
            <th class="text-left px-4 py-3 font-medium text-gray-600 hidden sm:table-cell">Type</th>
            <th class="text-left px-4 py-3 font-medium text-gray-600 hidden md:table-cell">Matière</th>
            <th class="text-left px-4 py-3 font-medium text-gray-600 hidden lg:table-cell">Année</th>
            <th class="text-left px-4 py-3 font-medium text-gray-600 hidden lg:table-cell">DL</th>
            <th class="px-4 py-3"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="r in store.ressources" :key="r.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 font-medium text-gray-900 max-w-xs truncate">{{ r.titre }}</td>
            <td class="px-4 py-3 hidden sm:table-cell">
              <span :class="badgeClass(r.type_ressource)">{{ r.type_label }}</span>
            </td>
            <td class="px-4 py-3 text-gray-500 hidden md:table-cell">{{ r.matiere_nom }}</td>
            <td class="px-4 py-3 text-gray-400 hidden lg:table-cell">{{ r.annee || '—' }}</td>
            <td class="px-4 py-3 text-gray-400 hidden lg:table-cell">{{ r.nb_telechargements }}</td>
            <td class="px-4 py-3 text-right">
              <button
                @click="confirmerSuppression(r)"
                class="text-red-500 hover:text-red-700 text-xs px-2 py-1 rounded hover:bg-red-50 transition-colors"
              >
                Supprimer
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div v-if="store.total > pageSize" class="flex justify-center gap-2 mt-6">
      <button @click="page--; fetchData()" :disabled="page <= 1" class="btn-secondary text-sm py-1.5 px-3" :class="{ 'opacity-40': page <= 1 }">Précédent</button>
      <span class="text-sm text-gray-500 self-center">Page {{ page }}</span>
      <button @click="page++; fetchData()" :disabled="page * pageSize >= store.total" class="btn-secondary text-sm py-1.5 px-3" :class="{ 'opacity-40': page * pageSize >= store.total }">Suivant</button>
    </div>

    <!-- Modal confirmation suppression -->
    <div v-if="aSupprimer" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4">
      <div class="bg-white rounded-xl p-6 max-w-sm w-full shadow-xl">
        <h2 class="font-semibold text-gray-900 mb-2">Confirmer la suppression</h2>
        <p class="text-sm text-gray-500 mb-6">Voulez-vous supprimer <strong>{{ aSupprimer.titre }}</strong> ? Cette action est irréversible.</p>
        <div class="flex gap-3 justify-end">
          <button @click="aSupprimer = null" class="btn-secondary text-sm">Annuler</button>
          <button @click="supprimer" class="btn-danger text-sm">Supprimer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRessourcesStore } from '@/stores/ressources'

const store = useRessourcesStore()
const search = ref('')
const filtreType = ref('')
const page = ref(1)
const pageSize = 20
const aSupprimer = ref(null)
let debounceTimer = null

const badgeMap = { cours: 'badge-cours', sujet: 'badge-sujet', td: 'badge-td', tp: 'badge-tp', autre: 'badge-autre' }
const badgeClass = (type) => badgeMap[type] || 'badge-autre'

function fetchData() {
  const params = { page: page.value, page_size: pageSize }
  if (search.value) params.search = search.value
  if (filtreType.value) params.type_ressource = filtreType.value
  store.fetchRessources(params)
}

function debouncedFetch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => { page.value = 1; fetchData() }, 350)
}

function confirmerSuppression(r) { aSupprimer.value = r }

async function supprimer() {
  if (!aSupprimer.value) return
  await store.deleteRessource(aSupprimer.value.id)
  aSupprimer.value = null
}

onMounted(fetchData)
</script>
