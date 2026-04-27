<template>
  <div class="max-w-6xl mx-auto px-4 py-10">
    <div class="text-center mb-10">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Ressources pédagogiques</h1>
      <p class="text-gray-500">Téléchargez gratuitement vos cours et sujets d'examen par Institut, Filière et Niveau</p>
    </div>

    <div v-if="store.loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <div v-for="i in 6" :key="i" class="card p-5 h-32 animate-pulse bg-gray-100" />
    </div>

    <div v-else-if="store.error" class="text-center text-red-500 py-10">{{ store.error }}</div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <router-link
        v-for="institut in store.instituts"
        :key="institut.id"
        :to="{ name: 'Institut', params: { id: institut.id } }"
        class="card p-5 hover:border-blue-400 group"
      >
        <div class="flex items-start justify-between mb-3">
          <span class="inline-flex items-center justify-center w-10 h-10 rounded-lg bg-blue-100 text-blue-700 font-bold text-sm">
            {{ (institut.sigle || institut.nom).substring(0, 2).toUpperCase() }}
          </span>
          <span class="text-xs text-gray-400">{{ institut.nb_filieres }} filière(s)</span>
        </div>
        <h2 class="font-semibold text-gray-900 group-hover:text-blue-700 transition-colors">{{ institut.nom }}</h2>
        <p v-if="institut.sigle" class="text-sm text-gray-400 mt-0.5">{{ institut.sigle }}</p>
        <p v-if="institut.description" class="text-sm text-gray-500 mt-2 line-clamp-2">{{ institut.description }}</p>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCatalogueStore } from '@/stores/catalogue'

const store = useCatalogueStore()
onMounted(() => store.fetchInstituts())
</script>
