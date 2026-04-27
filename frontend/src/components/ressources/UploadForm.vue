<template>
  <form @submit.prevent="submit" class="space-y-4">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Titre *</label>
      <input v-model="form.titre" type="text" class="input" required placeholder="Ex: Cours de thermodynamique — Chapitre 1" />
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Type *</label>
        <select v-model="form.type_ressource" class="input" required>
          <option value="cours">Cours</option>
          <option value="sujet">Sujet d'examen</option>
          <option value="td">Travaux dirigés</option>
          <option value="tp">Travaux pratiques</option>
          <option value="autre">Autre</option>
        </select>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Année académique</label>
        <input v-model.number="form.annee" type="number" class="input" :min="2000" :max="new Date().getFullYear() + 1" placeholder="2024" />
      </div>
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Matière *</label>
      <select v-model="form.matiere" class="input" required>
        <option disabled value="">Choisir une matière</option>
        <option v-for="m in matieres" :key="m.id" :value="m.id">{{ m.nom }}</option>
      </select>
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
      <textarea v-model="form.description" class="input resize-none" rows="2" placeholder="Description facultative…" />
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Fichier PDF *</label>
      <div
        class="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-blue-400 transition-colors"
        :class="{ 'border-blue-500 bg-blue-50': dragOver }"
        @dragover.prevent="dragOver = true"
        @dragleave="dragOver = false"
        @drop.prevent="handleDrop"
        @click="$refs.fileInput.click()"
      >
        <input ref="fileInput" type="file" accept=".pdf" class="hidden" @change="handleFile" />
        <template v-if="form.fichier">
          <svg class="w-8 h-8 mx-auto text-blue-600 mb-2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p class="text-sm font-medium text-gray-800">{{ form.fichier.name }}</p>
          <p class="text-xs text-gray-400 mt-1">{{ (form.fichier.size / 1024 / 1024).toFixed(2) }} Mo</p>
        </template>
        <template v-else>
          <svg class="w-8 h-8 mx-auto text-gray-300 mb-2" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5a4.5 4.5 0 01-1.41-8.775 5.25 5.25 0 0110.338-2.32 5.75 5.75 0 011.283 11.096H6.75z" />
          </svg>
          <p class="text-sm text-gray-500">Glisser-déposer ou <span class="text-blue-600 font-medium">parcourir</span></p>
          <p class="text-xs text-gray-400 mt-1">PDF uniquement — 20 Mo max</p>
        </template>
      </div>
      <p v-if="fileError" class="text-xs text-red-600 mt-1">{{ fileError }}</p>
    </div>

    <div v-if="error" class="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-2">{{ error }}</div>

    <div class="flex gap-3 justify-end">
      <button type="button" @click="$emit('cancel')" class="btn-secondary">Annuler</button>
      <button type="submit" class="btn-primary" :disabled="loading">
        <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
        </svg>
        {{ loading ? 'Envoi en cours…' : 'Publier la ressource' }}
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ressourcesApi } from '@/api/ressources'

const props = defineProps({ matieres: { type: Array, default: () => [] } })
const emit = defineEmits(['success', 'cancel'])

const form = reactive({ titre: '', type_ressource: 'cours', matiere: '', annee: '', description: '', fichier: null })
const loading = ref(false)
const error = ref(null)
const fileError = ref(null)
const dragOver = ref(false)

function handleFile(e) {
  const f = e.target.files[0]
  validateAndSet(f)
}
function handleDrop(e) {
  dragOver.value = false
  const f = e.dataTransfer.files[0]
  validateAndSet(f)
}
function validateAndSet(f) {
  fileError.value = null
  if (!f) return
  if (!f.name.toLowerCase().endsWith('.pdf')) { fileError.value = 'Seuls les fichiers PDF sont acceptés.'; return }
  if (f.size > 20 * 1024 * 1024) { fileError.value = 'Le fichier dépasse 20 Mo.'; return }
  form.fichier = f
}

async function submit() {
  if (!form.fichier) { fileError.value = 'Veuillez sélectionner un fichier PDF.'; return }
  loading.value = true
  error.value = null
  try {
    const fd = new FormData()
    fd.append('titre', form.titre)
    fd.append('type_ressource', form.type_ressource)
    fd.append('matiere', form.matiere)
    fd.append('fichier', form.fichier)
    if (form.annee) fd.append('annee', form.annee)
    if (form.description) fd.append('description', form.description)
    await ressourcesApi.createRessource(fd)
    emit('success')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Une erreur est survenue lors de l\'upload.'
  } finally {
    loading.value = false
  }
}
</script>
