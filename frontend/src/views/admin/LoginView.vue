<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4">
    <div class="w-full max-w-sm bg-white rounded-2xl border border-gray-200 shadow-sm p-8">
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-blue-100 mb-4">
          <svg class="w-6 h-6 text-blue-700" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
        </div>
        <h1 class="text-xl font-bold text-gray-900">Espace administrateur</h1>
        <p class="text-sm text-gray-500 mt-1">Connexion réservée aux gestionnaires</p>
      </div>

      <form @submit.prevent="submit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Identifiant</label>
          <input v-model="username" type="text" class="input" required autocomplete="username" placeholder="nom_utilisateur" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Mot de passe</label>
          <input v-model="password" type="password" class="input" required autocomplete="current-password" placeholder="••••••••" />
        </div>

        <div v-if="error" class="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-2">
          {{ error }}
        </div>

        <button type="submit" class="btn-primary w-full justify-center" :disabled="loading">
          <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
          </svg>
          {{ loading ? 'Connexion…' : 'Se connecter' }}
        </button>
      </form>

      <div class="mt-6 text-center">
        <router-link to="/" class="text-sm text-gray-400 hover:text-blue-700">
          Retour à l'accueil
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)

async function submit() {
  loading.value = true
  error.value = null
  try {
    await auth.login(username.value, password.value)
    router.push({ name: 'Dashboard' })
  } catch (e) {
    error.value = e.response?.data?.detail || 'Identifiants incorrects.'
  } finally {
    loading.value = false
  }
}
</script>
