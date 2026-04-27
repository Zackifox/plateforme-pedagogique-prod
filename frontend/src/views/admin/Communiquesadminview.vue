<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Communiqués</h1>
      <button @click="ouvrirFormulaire()" class="btn-primary">+ Nouveau communiqué</button>
    </div>

    <!-- Liste -->
    <div class="space-y-4">
      <div v-for="c in communiques" :key="c.id" class="card p-5">
        <div class="flex items-start justify-between gap-4">
          <div class="flex-1 min-w-0">
            <h2 class="font-semibold text-gray-900 truncate">{{ c.titre }}</h2>
            <p class="text-sm text-gray-500 mt-1 line-clamp-2">{{ c.contenu }}</p>
            <div class="flex items-center gap-4 mt-2 text-xs text-gray-400">
              <span>{{ formatDate(c.created_at) }}</span>
              <span>{{ c.nb_likes }} like(s)</span>
              <span>{{ c.nb_commentaires }} commentaire(s)</span>
            </div>
          </div>
          <div class="flex gap-2 shrink-0">
            <button @click="ouvrirFormulaire(c)" class="btn-secondary text-xs py-1.5">Modifier</button>
            <button @click="confirmerSuppression(c)" class="btn-danger text-xs py-1.5">Supprimer</button>
          </div>
        </div>
      </div>
      <div v-if="communiques.length === 0 && !loading" class="text-center py-12 text-gray-400">
        Aucun communiqué publié.
      </div>
    </div>

    <!-- Modal formulaire -->
    <div v-if="formulaireOuvert" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4" @click.self="formulaireOuvert = false">
      <div class="bg-white rounded-2xl p-6 w-full max-w-xl shadow-xl max-h-screen overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-bold">{{ enEdition ? 'Modifier' : 'Nouveau communiqué' }}</h2>
          <button @click="formulaireOuvert = false" class="text-gray-400 hover:text-gray-700">✕</button>
        </div>

        <form @submit.prevent="sauvegarder" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Titre *</label>
            <input v-model="form.titre" type="text" class="input" required />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Contenu *</label>
            <textarea v-model="form.contenu" class="input resize-none" rows="6" required />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Image (facultatif)</label>
            <input type="file" accept="image/*" @change="onImage" class="text-sm text-gray-600" />
          </div>
          <div v-if="erreur" class="text-sm text-red-600 bg-red-50 rounded-lg px-3 py-2">{{ erreur }}</div>
          <div class="flex gap-3 justify-end pt-2">
            <button type="button" @click="formulaireOuvert = false" class="btn-secondary">Annuler</button>
            <button type="submit" class="btn-primary" :disabled="saving">
              {{ saving ? 'Enregistrement…' : (enEdition ? 'Mettre à jour' : 'Publier') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal suppression -->
    <div v-if="aSupprimer" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4">
      <div class="bg-white rounded-xl p-6 max-w-sm w-full shadow-xl">
        <h2 class="font-semibold text-gray-900 mb-2">Confirmer la suppression</h2>
        <p class="text-sm text-gray-500 mb-6">Supprimer <strong>{{ aSupprimer.titre }}</strong> ? Cette action est irréversible.</p>
        <div class="flex gap-3 justify-end">
          <button @click="aSupprimer = null" class="btn-secondary text-sm">Annuler</button>
          <button @click="supprimer" class="btn-danger text-sm">Supprimer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { communiquesApi } from '@/api/communiques'

const communiques = ref([])
const loading = ref(true)
const formulaireOuvert = ref(false)
const enEdition = ref(null)
const saving = ref(false)
const erreur = ref('')
const aSupprimer = ref(null)
const imageFile = ref(null)

const form = reactive({ titre: '', contenu: '' })

onMounted(charger)

async function charger() {
  loading.value = true
  try {
    const { data } = await communiquesApi.getCommuniques()
    communiques.value = data.results || data
  } finally {
    loading.value = false
  }
}

function ouvrirFormulaire(c = null) {
  enEdition.value = c
  form.titre = c?.titre || ''
  form.contenu = c?.contenu || ''
  imageFile.value = null
  erreur.value = ''
  formulaireOuvert.value = true
}

function onImage(e) {
  imageFile.value = e.target.files[0] || null
}

async function sauvegarder() {
  saving.value = true
  erreur.value = ''
  try {
    const fd = new FormData()
    fd.append('titre', form.titre)
    fd.append('contenu', form.contenu)
    if (imageFile.value) fd.append('image', imageFile.value)

    if (enEdition.value) {
      const { data } = await communiquesApi.updateCommunique(enEdition.value.id, fd)
      const idx = communiques.value.findIndex(c => c.id === enEdition.value.id)
      if (idx !== -1) communiques.value[idx] = { ...communiques.value[idx], ...data }
    } else {
      const { data } = await communiquesApi.createCommunique(fd)
      communiques.value.unshift(data)
    }
    formulaireOuvert.value = false
  } catch (e) {
    erreur.value = e.response?.data ? JSON.stringify(e.response.data) : 'Erreur lors de l\'enregistrement.'
  } finally {
    saving.value = false
  }
}

function confirmerSuppression(c) { aSupprimer.value = c }

async function supprimer() {
  try {
    await communiquesApi.deleteCommunique(aSupprimer.value.id)
    communiques.value = communiques.value.filter(c => c.id !== aSupprimer.value.id)
    aSupprimer.value = null
  } catch {}
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' })
}
</script>