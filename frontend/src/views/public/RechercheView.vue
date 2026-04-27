<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">
      Résultats pour <span class="text-blue-700">"{{ query }}"</span>
      <span class="text-base font-normal text-gray-400 ml-2">({{ store.total }} résultat(s))</span>
    </h1>
    <RessourceList :ressources="store.ressources" :loading="store.loading" />
  </div>
</template>

<script setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'
import { useRessourcesStore } from '@/stores/ressources'
import RessourceList from '@/components/ressources/RessourceList.vue'

const route = useRoute()
const store = useRessourcesStore()

const query = route.query.q || ''

watch(
  () => route.query.q,
  (q) => { if (q) store.fetchRessources({ search: q }) },
  { immediate: true }
)
</script>
