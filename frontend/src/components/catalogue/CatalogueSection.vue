<template>
  <div>
    <!-- Formulaire d'ajout -->
    <form @submit.prevent="submitCreer" class="card p-4 mb-5 flex flex-wrap gap-3 items-end">
      <div v-for="champ in champs" :key="champ.key" class="flex-1 min-w-32">
        <label class="block text-xs font-medium text-gray-600 mb-1">
          {{ champ.label }} <span v-if="champ.required" class="text-red-500">*</span>
        </label>
        <input
          v-model="formCreer[champ.key]"
          :type="champ.type || 'text'"
          :required="champ.required"
          class="input text-sm"
          :placeholder="champ.label"
        />
      </div>
      <div v-if="extra" class="flex-1 min-w-32">
        <label class="block text-xs font-medium text-gray-600 mb-1">{{ extra.label }} *</label>
        <select v-model="formCreer[extra.key]" class="input text-sm" required>
          <option disabled value="">Choisir</option>
          <option v-for="o in extra.options" :key="o.id" :value="o.id">{{ o.nom }}</option>
        </select>
      </div>
      <button type="submit" class="btn-primary text-sm py-2 shrink-0">+ Ajouter</button>
    </form>

    <!-- Liste -->
    <div v-if="loading" class="text-center text-gray-400 py-6">Chargement…</div>
    <div v-else-if="items.length === 0" class="text-center text-gray-400 py-6">Aucun élément.</div>
    <div v-else class="card overflow-hidden">
      <table class="w-full text-sm">
        <thead class="bg-gray-50 border-b border-gray-200">
          <tr>
            <th v-for="champ in champs" :key="champ.key" class="text-left px-4 py-3 font-medium text-gray-600">
              {{ champ.label }}
            </th>
            <th v-if="extra" class="text-left px-4 py-3 font-medium text-gray-600">{{ extra.label }}</th>
            <th class="px-4 py-3 text-right font-medium text-gray-600">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="item in items" :key="item.id" class="hover:bg-gray-50">
            <td v-for="champ in champs" :key="champ.key" class="px-4 py-3 text-gray-700">
              {{ item[champ.key] || '—' }}
            </td>
            <td v-if="extra" class="px-4 py-3 text-gray-500">
              {{ extra.options.find(o => o.id === item[extra.key])?.nom || '—' }}
            </td>
            <td class="px-4 py-3 text-right">
              <div class="flex justify-end gap-2">
                <button
                  @click="ouvrirEdition(item)"
                  class="text-blue-600 hover:text-blue-800 text-xs px-2 py-1 rounded hover:bg-blue-50 transition-colors"
                >
                  Modifier
                </button>
                <button
                  @click="$emit('delete', item.id)"
                  class="text-red-500 hover:text-red-700 text-xs px-2 py-1 rounded hover:bg-red-50 transition-colors"
                >
                  Supprimer
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal modification -->
    <div v-if="itemEnEdition" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 px-4" @click.self="itemEnEdition = null">
      <div class="bg-white rounded-2xl p-6 w-full max-w-md shadow-xl">
        <div class="flex items-center justify-between mb-5">
          <h2 class="text-lg font-bold text-gray-900">Modifier</h2>
          <button @click="itemEnEdition = null" class="text-gray-400 hover:text-gray-700 text-xl leading-none">✕</button>
        </div>

        <form @submit.prevent="submitModifier" class="space-y-4">
          <div v-for="champ in champs" :key="champ.key">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              {{ champ.label }} <span v-if="champ.required" class="text-red-500">*</span>
            </label>
            <input
              v-model="formEdition[champ.key]"
              :type="champ.type || 'text'"
              :required="champ.required"
              class="input"
            />
          </div>
          <div v-if="extra">
            <label class="block text-sm font-medium text-gray-700 mb-1">{{ extra.label }} *</label>
            <select v-model="formEdition[extra.key]" class="input" required>
              <option disabled value="">Choisir</option>
              <option v-for="o in extra.options" :key="o.id" :value="o.id">{{ o.nom }}</option>
            </select>
          </div>

          <div v-if="erreur" class="text-sm text-red-600 bg-red-50 rounded-lg px-3 py-2">{{ erreur }}</div>

          <div class="flex gap-3 justify-end pt-2">
            <button type="button" @click="itemEnEdition = null" class="btn-secondary">Annuler</button>
            <button type="submit" class="btn-primary" :disabled="saving">
              {{ saving ? 'Enregistrement…' : 'Enregistrer' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

const props = defineProps({
  titre: String,
  items: { type: Array, default: () => [] },
  champs: { type: Array, default: () => [{ key: 'nom', label: 'Nom', required: true }] },
  extra: { type: Object, default: null },
  loading: Boolean,
})
const emit = defineEmits(['create', 'update', 'delete'])

// Formulaire création
const formCreer = reactive({})
props.champs.forEach(c => { formCreer[c.key] = '' })
if (props.extra) formCreer[props.extra.key] = ''

function submitCreer() {
  emit('create', { ...formCreer })
  props.champs.forEach(c => { formCreer[c.key] = '' })
  if (props.extra) formCreer[props.extra.key] = ''
}

// Formulaire édition
const itemEnEdition = ref(null)
const formEdition = reactive({})
const saving = ref(false)
const erreur = ref('')

function ouvrirEdition(item) {
  itemEnEdition.value = item
  props.champs.forEach(c => { formEdition[c.key] = item[c.key] || '' })
  if (props.extra) formEdition[props.extra.key] = item[props.extra.key] || ''
  erreur.value = ''
}

async function submitModifier() {
  saving.value = true
  erreur.value = ''
  try {
    emit('update', { id: itemEnEdition.value.id, data: { ...formEdition } })
    itemEnEdition.value = null
  } catch (e) {
    erreur.value = 'Erreur lors de la modification.'
  } finally {
    saving.value = false
  }
}
</script>