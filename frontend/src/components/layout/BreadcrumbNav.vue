<template>
  <nav class="flex items-center gap-1.5 text-sm text-gray-500 mb-6 flex-wrap">
    <router-link to="/" class="hover:text-blue-700">Accueil</router-link>
    <template v-for="(crumb, i) in crumbs" :key="i">
      <span>/</span>
      <router-link v-if="crumb.to" :to="crumb.to" class="hover:text-blue-700">{{ crumb.label }}</router-link>
      <span v-else class="text-gray-800 font-medium">{{ crumb.label }}</span>
    </template>
  </nav>
</template>

<script setup>
defineProps({
  crumbs: { type: Array, default: () => [] },
})
</script>
