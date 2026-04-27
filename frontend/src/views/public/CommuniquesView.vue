<template>
  <div class="max-w-3xl mx-auto px-4 py-10">
    <h1 class="text-2xl font-bold text-gray-900 mb-8">Communiqués</h1>

    <!-- Chargement -->
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="card p-6 h-40 animate-pulse bg-gray-100" />
    </div>

    <!-- Liste -->
    <div v-else-if="communiques.length === 0" class="text-center py-16 text-gray-400">
      Aucun communiqué pour le moment.
    </div>

    <div v-else class="space-y-6">
      <div v-for="c in communiques" :key="c.id" class="card overflow-hidden">

        <!-- Image -->
        <div v-if="c.image" class="relative overflow-hidden bg-gray-100">
          <img
            :src="c.image"
            :alt="c.titre"
            class="w-full object-contain transition-all duration-300 cursor-zoom-in"
            :class="c._imageAgrandie ? 'max-h-none' : 'max-h-64'"
            @click="c._imageAgrandie = !c._imageAgrandie"
          />
          <button
            @click="c._imageAgrandie = !c._imageAgrandie"
            class="absolute bottom-2 right-2 bg-black/50 text-white text-xs px-2 py-1 rounded-full hover:bg-black/70 transition-colors"
          >
            {{ c._imageAgrandie ? 'Réduire ▲' : 'Agrandir ▼' }}
          </button>
        </div>       

        <div class="p-6">
          <!-- En-tête -->
          <div class="flex items-start justify-between gap-4 mb-3">
            <h2 class="text-lg font-semibold text-gray-900">{{ c.titre }}</h2>
            <span class="text-xs text-gray-400 shrink-0">{{ formatDate(c.created_at) }}</span>
          </div>

          <!-- Contenu -->
          <p class="text-gray-600 text-sm leading-relaxed whitespace-pre-line mb-5">{{ c.contenu }}</p>

          <!-- Actions -->
          <div class="flex items-center gap-4 border-t border-gray-100 pt-4">

            <!-- Like -->
            <button
              @click="toggleLike(c)"
              class="flex items-center gap-1.5 text-sm transition-colors"
              :class="c.utilisateur_a_like ? 'text-blue-700 font-medium' : 'text-gray-400 hover:text-blue-600'"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M7.493 18.75c-.425 0-.82-.236-.975-.632A7.48 7.48 0 016 15.375c0-1.75.599-3.358 1.602-4.634.151-.192.373-.309.6-.397.473-.183.89-.514 1.212-.924a9.042 9.042 0 012.861-2.4c.723-.384 1.35-.956 1.653-1.715a4.498 4.498 0 00.322-1.672V3a.75.75 0 01.75-.75 2.25 2.25 0 012.25 2.25c0 1.152-.26 2.243-.723 3.218-.266.558.107 1.282.725 1.282h3.126c1.026 0 1.945.694 2.054 1.715.045.422.068.85.068 1.285a11.95 11.95 0 01-2.649 7.521c-.388.482-.987.729-1.605.729H14.23c-.483 0-.964-.078-1.423-.23l-3.114-1.04a4.501 4.501 0 00-1.423-.23h-.777zM2.331 10.977a11.969 11.969 0 00-.831 4.398 12 12 0 00.52 3.507c.26.85 1.084 1.368 1.973 1.368H4.9c.445 0 .72-.498.523-.898a8.963 8.963 0 01-.924-3.977c0-1.708.476-3.305 1.302-4.666.245-.403-.028-.959-.5-.959H4.25c-.832 0-1.612.453-1.918 1.227z" />
              </svg>
              {{ c.nb_likes }}
            </button>

            <!-- Commentaires -->
            <button
              @click="toggleCommentaires(c)"
              class="flex items-center gap-1.5 text-sm text-gray-400 hover:text-blue-600 transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              {{ c.nb_commentaires }} commentaire(s)
            </button>

            <!-- Partage -->
            <div class="flex items-center gap-2 ml-auto">
              <span class="text-xs text-gray-400">Partager :</span>
              <a
                :href="`https://wa.me/?text=${encodeURIComponent(c.titre + ' — ' + urlCommunique(c.id))}`"
                target="_blank"
                class="text-green-500 hover:text-green-600 transition-colors"
                title="Partager sur WhatsApp"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
                  <path d="M11.998 0C5.372 0 0 5.373 0 12.004c0 2.118.554 4.104 1.523 5.832L0 24l6.335-1.508A11.956 11.956 0 0011.998 24C18.626 24 24 18.627 24 12.004 24 5.373 18.626 0 11.998 0zm.002 21.818a9.818 9.818 0 01-5.002-1.368l-.359-.213-3.721.976.993-3.63-.234-.374a9.847 9.847 0 01-1.507-5.209c0-5.44 4.427-9.864 9.83-9.864 5.404 0 9.832 4.424 9.832 9.864 0 5.441-4.428 9.818-9.832 9.818z"/>
                </svg>
              </a>
              <a
                :href="`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(urlCommunique(c.id))}`"
                target="_blank"
                class="text-blue-600 hover:text-blue-700 transition-colors"
                title="Partager sur Facebook"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
              </a>
            </div>
          </div>

          <!-- Section commentaires -->
          <div v-if="c._showCommentaires" class="mt-5 border-t border-gray-100 pt-5">

            <!-- Liste des commentaires -->
            <div class="space-y-3 mb-4">
              <div
                v-for="com in c._commentaires"
                :key="com.id"
                class="flex gap-3 group"
              >
                <div class="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-sm font-semibold shrink-0">
                  {{ com.auteur.username[0].toUpperCase() }}
                </div>
                <div class="flex-1 bg-gray-50 rounded-xl px-4 py-2">
                  <p class="text-xs font-semibold text-gray-700">{{ com.auteur.username }}</p>
                  <p class="text-sm text-gray-600 mt-0.5">{{ com.contenu }}</p>
                  <p class="text-xs text-gray-400 mt-1">{{ formatDate(com.created_at) }}</p>
                </div>
                <button
                  v-if="visiteur.user?.username === com.auteur.username"
                  @click="supprimerCommentaire(c, com.id)"
                  class="opacity-0 group-hover:opacity-100 text-red-400 hover:text-red-600 text-xs self-start mt-2"
                >
                  ✕
                </button>
              </div>
              <p v-if="c._commentaires?.length === 0" class="text-sm text-gray-400 text-center py-2">
                Aucun commentaire. Soyez le premier !
              </p>
            </div>

            <!-- Formulaire commentaire -->
            <div v-if="visiteur.isConnecte" class="flex gap-3">
              <div class="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-sm font-semibold shrink-0">
                {{ visiteur.user?.username[0].toUpperCase() }}
              </div>
              <div class="flex-1 flex gap-2">
                <input
                  v-model="c._nouveauCommentaire"
                  type="text"
                  class="input text-sm flex-1"
                  placeholder="Écrire un commentaire…"
                  @keyup.enter="soumettrCommentaire(c)"
                />
                <button @click="soumettrCommentaire(c)" class="btn-primary text-sm py-2 px-3">
                  Envoyer
                </button>
              </div>
            </div>

            <!-- Pas connecté -->
        <div v-else class="bg-gray-50 rounded-xl p-4 text-center">
          <p class="text-sm text-gray-500 mb-3">
            Connectez-vous pour commenter et liker
          </p>
          <div class="flex gap-2 justify-center">
            <button @click="$emit('ouvrirAuth', 'login')" class="btn-primary text-sm py-1.5">
              Se connecter
            </button>
            <button @click="$emit('ouvrirAuth', 'inscription')" class="btn-secondary text-sm py-1.5">
              S'inscrire
            </button>
          </div>
        </div>
          </div>

        </div>
      </div>
    </div>

    <!-- Modal Auth -->
    <div v-if="modalAuth" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-4" @click.self="modalAuth = null">
      <div class="bg-white rounded-2xl p-6 w-full max-w-sm shadow-xl">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-bold text-gray-900">
            {{ modalAuth === 'login' ? 'Se connecter' : 'Créer un compte' }}
          </h2>
          <button @click="modalAuth = null" class="text-gray-400 hover:text-gray-700">✕</button>
        </div>

        <form @submit.prevent="soumettrAuth" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nom d'utilisateur</label>
            <input v-model="authForm.username" type="text" class="input" required />
          </div>
          <div v-if="modalAuth === 'inscription'">
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input v-model="authForm.email" type="email" class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Mot de passe</label>
            <input v-model="authForm.password" type="password" class="input" required />
          </div>
          <div v-if="modalAuth === 'inscription'">
            <label class="block text-sm font-medium text-gray-700 mb-1">Confirmer le mot de passe</label>
            <input v-model="authForm.password2" type="password" class="input" required />
          </div>

          <div v-if="authErreur" class="text-sm text-red-600 bg-red-50 rounded-lg px-3 py-2">{{ authErreur }}</div>

          <button type="submit" class="btn-primary w-full justify-center" :disabled="authLoading">
            <svg v-if="authLoading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
            </svg>
            {{ modalAuth === 'login' ? 'Se connecter' : 'Créer mon compte' }}
          </button>

          <p class="text-center text-sm text-gray-500">
            <template v-if="modalAuth === 'login'">
              Pas encore de compte ?
              <button type="button" @click="modalAuth = 'inscription'" class="text-blue-700 hover:underline">S'inscrire</button>
            </template>
            <template v-else>
              Déjà un compte ?
              <button type="button" @click="modalAuth = 'login'" class="text-blue-700 hover:underline">Se connecter</button>
            </template>
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { communiquesApi } from '@/api/communiques'
import { useVisiteurStore } from '@/stores/visiteur'

const visiteur = useVisiteurStore()
const communiques = ref([])
const loading = ref(true)
const modalAuth = ref(null)
const authLoading = ref(false)
const authErreur = ref('')
const authForm = reactive({ username: '', email: '', password: '', password2: '' })

onMounted(charger)

async function charger() {
  loading.value = true
  try {
    const { data } = await communiquesApi.getCommuniques()
    communiques.value = (data.results || data).map(c => ({
      ...c,
      _showCommentaires: false,
      _commentaires: [],
      _nouveauCommentaire: '',
      _imageAgrandie: false,
    }))
  } finally {
    loading.value = false
  }
}

async function toggleLike(c) {
  if (!visiteur.isConnecte) { ouvrirModal('login'); return }
  try {
    const { data } = await communiquesApi.liker(c.id)
    c.utilisateur_a_like = data.liked
    c.nb_likes = data.nb_likes
  } catch { ouvrirModal('login') }
}

async function toggleCommentaires(c) {
  c._showCommentaires = !c._showCommentaires
  if (c._showCommentaires && c._commentaires.length === 0) {
    try {
      const { data } = await communiquesApi.getCommentaires(c.id)
      c._commentaires = data
    } catch {}
  }
}

async function soumettrCommentaire(c) {
  if (!c._nouveauCommentaire.trim()) return
  try {
    const { data } = await communiquesApi.commenter(c.id, c._nouveauCommentaire.trim())
    c._commentaires.push(data)
    c.nb_commentaires++
    c._nouveauCommentaire = ''
  } catch {}
}

async function supprimerCommentaire(c, commentaireId) {
  try {
    await communiquesApi.supprimerCommentaire(c.id, commentaireId)
    c._commentaires = c._commentaires.filter(com => com.id !== commentaireId)
    c.nb_commentaires--
  } catch {}
}

function ouvrirModal(type) {
  modalAuth.value = type
  authErreur.value = ''
  authForm.username = ''
  authForm.email = ''
  authForm.password = ''
  authForm.password2 = ''
}

async function soumettrAuth() {
  authLoading.value = true
  authErreur.value = ''
  try {
    if (modalAuth.value === 'inscription') {
      await visiteur.inscrire(authForm.username, authForm.email, authForm.password, authForm.password2)
    } else {
      await visiteur.login(authForm.username, authForm.password)
    }
    modalAuth.value = null
  } catch (e) {
    const err = e.response?.data
    if (typeof err === 'object') {
      authErreur.value = Object.values(err).flat().join(' ')
    } else {
      authErreur.value = 'Une erreur est survenue.'
    }
  } finally {
    authLoading.value = false
  }
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('fr-FR', {
    day: 'numeric', month: 'long', year: 'numeric',
  })
}

function urlCommunique(id) {
  return `${window.location.origin}/communiques#${id}`
}
</script>