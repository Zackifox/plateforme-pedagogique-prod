<template>
  <div class="max-w-2xl mx-auto px-4 py-8">
    <div class="flex items-center gap-3 mb-8">
      <router-link to="/admin" class="text-gray-400 hover:text-gray-700">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
      </router-link>
      <h1 class="text-2xl font-bold text-gray-900">Publier une ressource</h1>
    </div>

    <div v-if="success" class="card p-8 text-center">
      <svg class="w-12 h-12 text-green-500 mx-auto mb-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <h2 class="text-lg font-semibold text-gray-900 mb-2">Ressource publiée avec succès</h2>
      <div class="flex gap-3 justify-center mt-4">
        <button @click="reset" class="btn-primary">Publier une autre</button>
        <router-link to="/admin/ressources" class="btn-secondary">Voir les ressources</router-link>
      </div>
    </div>

    <div v-else class="space-y-6">

      <!-- Étape 1 : Sélection hiérarchique -->
      <div class="card p-5">
        <h2 class="font-semibold text-gray-700 mb-4">1. Choisir la destination</h2>
        <div class="space-y-3">

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Institut *</label>
            <select v-model="selectedInstitut" class="input" @change="onInstitutChange">
              <option value="">-- Choisir un institut --</option>
              <option v-for="i in instituts" :key="i.id" :value="i.id">
                {{ i.nom }} {{ i.sigle ? '(' + i.sigle + ')' : '' }}
              </option>
            </select>
            <p v-if="instituts.length === 0" class="text-xs text-red-500 mt-1">
              Aucun institut trouvé. Créez-en un dans
              <router-link to="/admin/catalogue" class="underline">Gestion du catalogue</router-link>.
            </p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Filière *</label>
            <select v-model="selectedFiliere" class="input" @change="onFiliereChange" :disabled="!selectedInstitut || loadingFilieres">
              <option value="">-- {{ loadingFilieres ? 'Chargement...' : 'Choisir une filière' }} --</option>
              <option v-for="f in filieres" :key="f.id" :value="f.id">{{ f.nom }}</option>
            </select>
            <p v-if="selectedInstitut && !loadingFilieres && filieres.length === 0" class="text-xs text-orange-500 mt-1">
              Aucune filière pour cet institut.
            </p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Niveau *</label>
            <select v-model="selectedNiveau" class="input" @change="onNiveauChange" :disabled="!selectedFiliere || loadingNiveaux">
              <option value="">-- {{ loadingNiveaux ? 'Chargement...' : 'Choisir un niveau' }} --</option>
              <option v-for="n in niveaux" :key="n.id" :value="n.id">{{ n.nom }}</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Matière *</label>
            <select v-model="selectedMatiere" class="input" :disabled="!selectedNiveau || loadingMatieres">
              <option value="">-- {{ loadingMatieres ? 'Chargement...' : 'Choisir une matière' }} --</option>
              <option v-for="m in matieres" :key="m.id" :value="m.id">{{ m.nom }}</option>
            </select>
          </div>

        </div>
      </div>

      <!-- Étape 2 : Détails de la ressource -->
      <div class="card p-5" :class="{ 'opacity-40 pointer-events-none': !selectedMatiere }">
        <h2 class="font-semibold text-gray-700 mb-4">2. Détails de la ressource</h2>

        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Titre *</label>
            <input v-model="form.titre" type="text" class="input" placeholder="Ex: Cours de thermodynamique — Chapitre 1" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Type *</label>
              <select v-model="form.type_ressource" class="input">
                <option value="cours">Cours</option>
                <option value="sujet">Sujet d'examen</option>
                <option value="td">Travaux dirigés</option>
                <option value="tp">Travaux pratiques</option>
                <option value="autre">Autre</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Année</label>
              <input v-model.number="form.annee" type="number" class="input" placeholder="2024" :min="2000" :max="2030" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea v-model="form.description" class="input resize-none" rows="2" placeholder="Description facultative…" />
          </div>

          <!-- Zone PDF -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Fichier PDF *</label>
            <div
              class="border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors"
              :class="fichier ? 'border-green-400 bg-green-50' : 'border-gray-300 hover:border-blue-400'"
              @click="$refs.fileInput.click()"
              @dragover.prevent
              @drop.prevent="onDrop"
            >
              <input ref="fileInput" type="file" accept=".pdf" class="hidden" @change="onFileChange" />
              <template v-if="fichier">
                <p class="font-medium text-green-700">{{ fichier.name }}</p>
                <p class="text-xs text-gray-400 mt-1">{{ (fichier.size / 1024 / 1024).toFixed(2) }} Mo</p>
                <button @click.stop="fichier = null" class="text-xs text-red-500 mt-2 hover:underline">Supprimer</button>
              </template>
              <template v-else>
                <p class="text-gray-500">Cliquez ici ou glissez votre PDF</p>
                <p class="text-xs text-gray-400 mt-1">PDF uniquement · 20 Mo max</p>
              </template>
            </div>
            <p v-if="fileError" class="text-xs text-red-600 mt-1">{{ fileError }}</p>
          </div>

          <div v-if="uploadError" class="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-2">
            {{ uploadError }}
          </div>

          <div class="flex gap-3 justify-end pt-2">
            <router-link to="/admin" class="btn-secondary">Annuler</router-link>
            <button @click="soumettre" class="btn-primary" :disabled="uploading || !peutSoumettre">
              <svg v-if="uploading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
              </svg>
              {{ uploading ? 'Envoi en cours…' : 'Publier la ressource' }}
            </button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'

const router = useRouter()

// État hiérarchie
const instituts = ref([])
const filieres = ref([])
const niveaux = ref([])
const matieres = ref([])
const selectedInstitut = ref('')
const selectedFiliere = ref('')
const selectedNiveau = ref('')
const selectedMatiere = ref('')
const loadingFilieres = ref(false)
const loadingNiveaux = ref(false)
const loadingMatieres = ref(false)

// État formulaire
const form = reactive({ titre: '', type_ressource: 'cours', annee: '', description: '' })
const fichier = ref(null)
const fileError = ref('')
const uploadError = ref('')
const uploading = ref(false)
const success = ref(false)

const peutSoumettre = computed(() =>
  selectedMatiere.value && form.titre && fichier.value
)

onMounted(async () => {
  try {
    const { data } = await api.get('/api/catalogue/instituts/')
    instituts.value = data.results || data
  } catch (e) {
    console.error('Erreur chargement instituts', e)
  }
})

async function onInstitutChange() {
  selectedFiliere.value = ''
  selectedNiveau.value = ''
  selectedMatiere.value = ''
  filieres.value = []
  niveaux.value = []
  matieres.value = []
  if (!selectedInstitut.value) return
  loadingFilieres.value = true
  try {
    const { data } = await api.get(`/api/catalogue/instituts/${selectedInstitut.value}/filieres/`)
    filieres.value = data.results || data
  } catch (e) {
    console.error('Erreur chargement filières', e)
  } finally {
    loadingFilieres.value = false
  }
}

async function onFiliereChange() {
  selectedNiveau.value = ''
  selectedMatiere.value = ''
  niveaux.value = []
  matieres.value = []
  if (!selectedFiliere.value) return
  loadingNiveaux.value = true
  try {
    const { data } = await api.get(`/api/catalogue/filieres/${selectedFiliere.value}/niveaux/`)
    niveaux.value = data.results || data
  } catch (e) {
    console.error('Erreur chargement niveaux', e)
  } finally {
    loadingNiveaux.value = false
  }
}

async function onNiveauChange() {
  selectedMatiere.value = ''
  matieres.value = []
  if (!selectedNiveau.value) return
  loadingMatieres.value = true
  try {
    const { data } = await api.get(`/api/catalogue/niveaux/${selectedNiveau.value}/matieres/`)
    matieres.value = data.results || data
  } catch (e) {
    console.error('Erreur chargement matières', e)
  } finally {
    loadingMatieres.value = false
  }
}

function onFileChange(e) {
  validerFichier(e.target.files[0])
}

function onDrop(e) {
  validerFichier(e.dataTransfer.files[0])
}

function validerFichier(f) {
  fileError.value = ''
  if (!f) return
  if (!f.name.toLowerCase().endsWith('.pdf')) {
    fileError.value = 'Seuls les fichiers PDF sont acceptés.'
    return
  }
  if (f.size > 20 * 1024 * 1024) {
    fileError.value = 'Le fichier dépasse 20 Mo.'
    return
  }
  fichier.value = f
}

async function soumettre() {
  if (!peutSoumettre.value) return
  uploading.value = true
  uploadError.value = ''
  try {
    const fd = new FormData()
    fd.append('titre', form.titre)
    fd.append('type_ressource', form.type_ressource)
    fd.append('matiere', selectedMatiere.value)
    fd.append('fichier', fichier.value)
    if (form.annee) fd.append('annee', form.annee)
    if (form.description) fd.append('description', form.description)
    await api.post('/api/ressources/', fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    success.value = true
  } catch (e) {
    uploadError.value = e.response?.data
      ? JSON.stringify(e.response.data)
      : 'Erreur lors de l\'upload. Vérifiez les champs.'
  } finally {
    uploading.value = false
  }
}

function reset() {
  success.value = false
  selectedInstitut.value = ''
  selectedFiliere.value = ''
  selectedNiveau.value = ''
  selectedMatiere.value = ''
  filieres.value = []
  niveaux.value = []
  matieres.value = []
  form.titre = ''
  form.type_ressource = 'cours'
  form.annee = ''
  form.description = ''
  fichier.value = null
}
</script>