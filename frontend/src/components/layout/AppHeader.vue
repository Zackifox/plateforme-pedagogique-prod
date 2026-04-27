<template>
  <header class="bg-white border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between gap-4">

      <!-- Logo -->
      <router-link to="/" class="flex items-center gap-2 font-bold text-blue-700 text-lg shrink-0">
        <img src="C:\Users\DAVID\Downloads\plateforme-pedagogique\logo.jpeg" alt="Logo" class="w-7 h-7 object-contain" />
        <span class="hidden sm:inline">UET-UCO-UUT Plateforme Pédagogique</span>
      </router-link>

      <!-- Recherche -->
      <form @submit.prevent="rechercher" class="flex-1 max-w-md hidden sm:block">
        <input v-model="query" type="search" placeholder="Rechercher un cours, une matière…" class="input text-sm" />
      </form>

      <!-- Navigation -->
      <nav class="flex items-center gap-1">

        <!-- Liens publics (desktop) -->
        <router-link
          v-for="lien in liensPublics"
          :key="lien.to"
          :to="lien.to"
          class="px-3 py-2 text-sm text-gray-600 hover:text-blue-700 hover:bg-blue-50 rounded-lg transition-colors hidden md:block"
          active-class="text-blue-700 bg-blue-50"
        >
          {{ lien.label }}
        </router-link>

        <!-- Visiteur non connecté -->
        <template v-if="!visiteur.isConnecte && !auth.isAuthenticated">
          <button
            @click="ouvrirModal('inscription')"
            class="btn-secondary text-sm py-1.5 hidden sm:flex"
          >
            S'inscrire
          </button>
          <button
            @click="ouvrirModal('login')"
            class="btn-primary text-sm py-1.5 hidden sm:flex"
          >
            Se connecter
          </button>
        </template>

        <!-- Visiteur connecté -->
        <template v-else-if="visiteur.isConnecte && !auth.isAuthenticated">
          <div class="hidden sm:flex items-center gap-2">
            <div class="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-sm font-semibold">
              {{ visiteur.user?.username?.[0]?.toUpperCase() }}
            </div>
            <span class="text-sm text-gray-700 hidden md:block">{{ visiteur.user?.username }}</span>
            <button @click="visiteur.logout()" class="text-xs text-gray-400 hover:text-red-500 px-2 py-1 rounded hover:bg-red-50">
              Déconnexion
            </button>
          </div>
        </template>

        <!-- Admin connecté -->
        <template v-if="auth.isAuthenticated">
          <router-link to="/admin" class="btn-primary text-sm py-1.5 ml-1">
            Back-office
          </router-link>
          <button @click="deconnecter" class="p-2 text-gray-400 hover:text-red-500 transition-colors" title="Déconnexion">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>
        </template>

        <!-- Menu burger mobile -->
        <button @click="menuOuvert = !menuOuvert" class="md:hidden p-2 text-gray-500 hover:text-blue-700 ml-1">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </nav>
    </div>

    <!-- Recherche mobile -->
    <div class="sm:hidden px-4 pb-3">
      <form @submit.prevent="rechercher">
        <input v-model="query" type="search" placeholder="Rechercher un cours…" class="input text-sm w-full" />
      </form>
    </div>

    <!-- Menu mobile -->
    <div v-if="menuOuvert" class="md:hidden border-t border-gray-100 bg-white px-4 py-3 space-y-1">
      <router-link
        v-for="lien in liensPublics"
        :key="lien.to"
        :to="lien.to"
        @click="menuOuvert = false"
        class="flex items-center px-3 py-2 text-sm text-gray-700 hover:text-blue-700 hover:bg-blue-50 rounded-lg"
        active-class="text-blue-700 bg-blue-50"
      >
        {{ lien.label }}
      </router-link>

      <!-- Boutons auth mobile -->
      <div v-if="!visiteur.isConnecte && !auth.isAuthenticated" class="flex gap-2 pt-2 border-t border-gray-100 mt-2">
        <button @click="ouvrirModal('inscription'); menuOuvert = false" class="btn-secondary text-sm flex-1 justify-center">
          S'inscrire
        </button>
        <button @click="ouvrirModal('login'); menuOuvert = false" class="btn-primary text-sm flex-1 justify-center">
          Se connecter
        </button>
      </div>
      <div v-else-if="visiteur.isConnecte && !auth.isAuthenticated" class="flex items-center justify-between pt-2 border-t border-gray-100 mt-2">
        <span class="text-sm text-gray-700 font-medium">{{ visiteur.user?.username }}</span>
        <button @click="visiteur.logout(); menuOuvert = false" class="text-xs text-red-500 hover:underline">
          Déconnexion
        </button>
      </div>
    </div>

    <!-- Modal inscription / connexion -->
    <div v-if="modalAuth" class="fixed inset-0 bg-black/50 flex items-center justify-center z-[100] px-4" @click.self="modalAuth = null">
      <div class="bg-white rounded-2xl p-6 w-full max-w-sm shadow-xl">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-bold text-gray-900">
            {{ modalAuth === 'login' ? 'Se connecter' : 'Créer un compte' }}
          </h2>
          <button @click="modalAuth = null" class="text-gray-400 hover:text-gray-700 text-xl leading-none">✕</button>
        </div>

        <form @submit.prevent="soumettrAuth" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email ou nom d'utilisateur</label>
            <input v-model="authForm.username" type="text" class="input" required autocomplete="username"
              placeholder="Email ou nom d'utilisateur" />
          </div>
          <div v-if="modalAuth === 'inscription'">
            <label class="block text-sm font-medium text-gray-700 mb-1">Adresse email *</label>
            <input v-model="authForm.email" type="email" class="input" required autocomplete="email" placeholder="votre@email.com" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Mot de passe</label>
            <input v-model="authForm.password" type="password" class="input" required autocomplete="current-password" />
          </div>
          <div v-if="modalAuth === 'inscription'">
            <label class="block text-sm font-medium text-gray-700 mb-1">Confirmer le mot de passe</label>
            <input v-model="authForm.password2" type="password" class="input" required />
          </div>

          <div v-if="authErreur" class="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
            {{ authErreur }}
          </div>
                    <!-- Bouton Google -->
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-200"></div>
            </div>
            <div class="relative flex justify-center text-xs">
              <span class="bg-white px-3 text-gray-400">ou continuer avec</span>
            </div>
          </div>

          <button
            type="button"
            @click="loginAvecGoogle"
            class="w-full flex items-center justify-center gap-3 border border-gray-300 rounded-lg px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
          >
            <svg class="w-5 h-5" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Continuer avec Google
          </button>

          <button type="submit" class="btn-primary w-full justify-center" :disabled="authLoading">
            <svg v-if="authLoading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
            </svg>
            {{ authLoading ? 'En cours…' : (modalAuth === 'login' ? 'Se connecter' : 'Créer mon compte') }}
          </button>

          <p class="text-center text-sm text-gray-500">
            <template v-if="modalAuth === 'login'">
              Pas encore de compte ?
              <button type="button" @click="modalAuth = 'inscription'" class="text-blue-700 hover:underline font-medium">
                S'inscrire
              </button>
            </template>
            <template v-else>
              Déjà un compte ?
              <button type="button" @click="modalAuth = 'login'" class="text-blue-700 hover:underline font-medium">
                Se connecter
              </button>
            </template>
          </p>
        </form>
      </div>
    </div>

  </header>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useVisiteurStore } from '@/stores/visiteur'

const auth = useAuthStore()
const visiteur = useVisiteurStore()
const router = useRouter()
const query = ref('')
const menuOuvert = ref(false)
const modalAuth = ref(null)
const authLoading = ref(false)
const authErreur = ref('')
const authForm = reactive({ username: '', email: '', password: '', password2: '' })

const liensPublics = [
  { label: 'Accueil', to: '/' },
  { label: 'Communiqués', to: '/communiques' },
  { label: 'À propos', to: '/a-propos' },
]


async function loginAvecGoogle() {
  try {
    await new Promise((resolve, reject) => {
      const client = window.google.accounts.oauth2.initTokenClient({
        client_id: '727006221568-rkhqg3n96j78gla1oreqggqge3eodo3p.apps.googleusercontent.com',
        scope: 'email profile openid',
        callback: async (response) => {
          if (response.error) { reject(response); return }
          try {
            // Obtenir le id_token via le access_token Google
            const res = await fetch(
              `https://www.googleapis.com/oauth2/v3/userinfo`,
              { headers: { Authorization: `Bearer ${response.access_token}` } }
            )
            const userInfo = await res.json()
            // Envoyer au backend pour créer/connecter l'utilisateur
            await visiteur.loginGoogle(response.access_token)
            modalAuth.value = null
            resolve()
          } catch (e) { reject(e) }
        },
      })
      client.requestAccessToken()
    })
  } catch (e) {
    authErreur.value = 'Connexion Google échouée. Réessayez.'
  }
}




function ouvrirModal(type) {
  modalAuth.value = type
  authErreur.value = ''
  authForm.username = ''
  authForm.email = ''
  authForm.password = ''
  authForm.password2 = ''
  menuOuvert.value = false
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
      authErreur.value = 'Une erreur est survenue. Vérifiez vos informations.'
    }
  } finally {
    authLoading.value = false
  }
}

function rechercher() {
  if (query.value.trim()) {
    router.push({ name: 'Recherche', query: { q: query.value.trim() } })
    query.value = ''
    menuOuvert.value = false
  }
}

function deconnecter() {
  auth.logout()
  router.push('/')
}
</script>