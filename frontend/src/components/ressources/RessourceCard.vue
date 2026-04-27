<template>
  <div class="card p-4 flex flex-col gap-3">
    <div class="flex items-start justify-between gap-2">
      <div class="flex-1 min-w-0">
        <h3 class="font-semibold text-gray-900 truncate">{{ ressource.titre }}</h3>
        <p v-if="ressource.description" class="text-sm text-gray-500 mt-0.5 line-clamp-2">{{ ressource.description }}</p>
      </div>
      <span :class="badgeClass">{{ ressource.type_label }}</span>
    </div>

    <div class="flex items-center gap-3 text-xs text-gray-400">
      <span v-if="ressource.annee">{{ ressource.annee }}</span>
      <span>{{ ressource.nb_telechargements }} téléchargement(s)</span>
    </div>

    <div class="flex gap-2 mt-auto">
      <a
        :href="previewUrl"
        target="_blank"
        class="btn-secondary text-xs py-1.5 flex-1 justify-center"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
        </svg>
        Aperçu
      </a>
      <a
        :href="downloadUrl"
        class="btn-primary text-xs py-1.5 flex-1 justify-center"
        download
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
        Télécharger
      </a>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ressourcesApi } from '@/api/ressources'

const props = defineProps({
  ressource: { type: Object, required: true },
})

const badgeMap = {
  cours: 'badge-cours',
  sujet: 'badge-sujet',
  td: 'badge-td',
  tp: 'badge-tp',
  autre: 'badge-autre',
}
const badgeClass = computed(() => badgeMap[props.ressource.type_ressource] || 'badge-autre')
const downloadUrl = computed(() => ressourcesApi.getDownloadUrl(props.ressource.id))
const previewUrl = computed(() => ressourcesApi.getPreviewUrl(props.ressource.id))
</script>
