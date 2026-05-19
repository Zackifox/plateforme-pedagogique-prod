<template>
  <div class="card p-4 flex flex-col gap-3">
    <div class="flex items-start justify-between gap-2">
      <div class="flex-1 min-w-0">
        <h3 class="font-semibold text-gray-900 truncate">
          {{ ressource.titre }}
        </h3>

        <p
          v-if="ressource.description"
          class="text-sm text-gray-500 mt-0.5 line-clamp-2"
        >
          {{ ressource.description }}
        </p>
      </div>

      <span :class="badgeClass">
        {{ ressource.type_label }}
      <a
        :href="apercuUrl"
        target="_blank"
        rel="noopener noreferrer"
        class="btn-secondary text-xs py-1.5 flex-1 justify-center"
      >
        Aperçu
      </a>
      <a
        :href="downloadUrl"
        target="_blank"
        rel="noopener noreferrer"
        class="btn-primary text-xs py-1.5 flex-1 justify-center"
      >
        Télécharger
      </a>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  ressource: {
    type: Object,
    required: true,
  },
})

const API_URL = import.meta.env.VITE_API_URL || ''

const badgeMap = {
  cours: 'badge-cours',
  sujet: 'badge-sujet',
  td: 'badge-td',
  tp: 'badge-tp',
  autre: 'badge-autre',
}

const badgeClass = computed(() => {
  return badgeMap[props.ressource.type_ressource] || 'badge-autre'
})

const downloadUrl = computed(() => {
  return `${API_URL}/api/ressources/${props.ressource.id}/telecharger/`
})

const apercuUrl = computed(() => {
  return `${API_URL}/api/ressources/${props.ressource.id}/apercu/`
})
    </div>

    <div class="flex gap-2 mt-auto">

      <!-- Bouton Aperçu -->
      <a
        :href="apercuUrl"
        target="_blank"
        rel="noopener noreferrer"
        class="btn-secondary text-xs py-1.5 flex-1 justify-center"
      >
        Aperçu
      </a>

      <!-- Bouton Télécharger -->
      <a
        :href="downloadUrl"
        target="_blank"
        rel="noopener noreferrer"
        class="btn-primary text-xs py-1.5 flex-1 justify-center"
      >
        Télécharger
      </a>

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  ressource: {
    type: Object,
    required: true,
  },
})

const API_URL = import.meta.env.VITE_API_URL || ''

const badgeMap = {
  cours: 'badge-cours',
  sujet: 'badge-sujet',
  td: 'badge-td',
  tp: 'badge-tp',
  autre: 'badge-autre',
}

const badgeClass = computed(() => {
  return badgeMap[props.ressource.type_ressource] || 'badge-autre'
})

const downloadUrl = computed(() => {
  return `${API_URL}/api/ressources/${props.ressource.id}/telecharger/`
})

const apercuUrl = computed(() => {
  return `${API_URL}/api/ressources/${props.ressource.id}/apercu/`
})
</script>