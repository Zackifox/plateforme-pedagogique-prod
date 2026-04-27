<template>
  <div>
    <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="i in 6" :key="i" class="card p-4 h-40 animate-pulse bg-gray-100" />
    </div>
    <div v-else-if="ressources.length === 0" class="text-center py-16 text-gray-400">
      <svg class="w-12 h-12 mx-auto mb-3 opacity-30" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664" />
      </svg>
      <p>Aucune ressource disponible</p>
    </div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <RessourceCard v-for="r in ressources" :key="r.id" :ressource="r" />
    </div>
  </div>
</template>

<script setup>
import RessourceCard from './RessourceCard.vue'
defineProps({
  ressources: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
})
</script>
