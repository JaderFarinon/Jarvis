<template>
  <div class="space-y-4">
    <PageCard>
      <div class="mb-4 flex items-start justify-between gap-2">
        <div>
          <h3 class="text-lg font-semibold text-slate-900">{{ title }}</h3>
          <p class="text-sm text-slate-500">{{ subtitle }}</p>
        </div>
      </div>

      <FeedbackAlert :type="feedbackType" :message="feedbackMessage" />

      <form class="mt-3 grid gap-3 md:grid-cols-2" @submit.prevent="save">
        <label v-for="field in fields" :key="field.key" class="space-y-1 text-sm">
          <span class="font-medium text-slate-700">{{ field.label }}</span>
          <input
            v-if="field.type !== 'textarea' && field.type !== 'select'"
            v-model="form[field.key]"
            :required="field.required"
            :type="field.type || 'text'"
            class="w-full rounded-lg border border-slate-200 px-3 py-2 outline-none ring-slate-300 focus:ring"
          />
          <textarea
            v-else-if="field.type === 'textarea'"
            v-model="form[field.key]"
            :required="field.required"
            rows="3"
            class="w-full rounded-lg border border-slate-200 px-3 py-2 outline-none ring-slate-300 focus:ring"
          ></textarea>
          <select
            v-else
            v-model="form[field.key]"
            :required="field.required"
            class="w-full rounded-lg border border-slate-200 px-3 py-2 outline-none ring-slate-300 focus:ring"
          >
            <option v-for="option in field.options || []" :key="option" :value="option">{{ option }}</option>
          </select>
        </label>

        <div class="md:col-span-2 flex flex-wrap gap-2">
          <button class="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800" :disabled="loading">
            {{ editingId ? 'Salvar alterações' : 'Criar registro' }}
          </button>
          <button v-if="editingId" type="button" class="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100" @click="resetForm">
            Cancelar edição
          </button>
        </div>
      </form>
    </PageCard>

    <PageCard>
      <div v-if="loading" class="text-sm text-slate-500">Carregando...</div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-full text-sm">
          <thead class="border-b border-slate-200 bg-slate-50 text-left text-slate-600">
            <tr>
              <th class="px-3 py-2">ID</th>
              <th v-for="field in fields" :key="field.key" class="px-3 py-2">{{ field.label }}</th>
              <th class="px-3 py-2 text-right">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.id" class="border-b border-slate-100">
              <td class="px-3 py-2 text-slate-500">{{ item.id }}</td>
              <td v-for="field in fields" :key="field.key" class="px-3 py-2">{{ formatValue(item[field.key], field.type) }}</td>
              <td class="px-3 py-2 text-right">
                <div class="inline-flex gap-2">
                  <button class="rounded-md border border-slate-200 px-2 py-1 text-xs font-medium hover:bg-slate-100" @click="startEdit(item)">Editar</button>
                  <button class="rounded-md bg-red-600 px-2 py-1 text-xs font-medium text-white hover:bg-red-700" @click="remove(item.id)">Excluir</button>
                </div>
              </td>
            </tr>
            <tr v-if="!items.length">
              <td :colspan="fields.length + 2" class="px-3 py-6 text-center text-slate-500">Nenhum registro encontrado.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </PageCard>
  </div>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import PageCard from '../shared/PageCard.vue'
import FeedbackAlert from '../shared/FeedbackAlert.vue'
import { moduleApi } from '../../services/api'

const props = defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, required: true },
  moduleKey: { type: String, required: true },
  fields: { type: Array, required: true },
})

const items = ref([])
const loading = ref(false)
const editingId = ref(null)
const feedbackMessage = ref('')
const feedbackType = ref('info')
const form = reactive({})

function initialValue(field) {
  if (field.type === 'number') return 0
  if (field.type === 'date' || field.type === 'datetime-local') return ''
  if (field.options?.length) return field.options[0]
  return ''
}

function resetForm() {
  props.fields.forEach((field) => {
    form[field.key] = initialValue(field)
  })
  editingId.value = null
}

function normalizeDateTime(value) {
  if (!value) return ''
  return value.length === 16 ? `${value}:00` : value
}

function normalizePayload() {
  const payload = {}
  props.fields.forEach((field) => {
    if (field.type === 'number') {
      payload[field.key] = Number(form[field.key])
      return
    }

    if (field.type === 'datetime-local') {
      payload[field.key] = normalizeDateTime(form[field.key])
      return
    }

    payload[field.key] = form[field.key]
  })
  return payload
}

function formatValue(value, type) {
  if (value === null || value === undefined || value === '') return '-'
  if (type === 'date') return new Date(`${value}T00:00:00`).toLocaleDateString('pt-BR')
  if (type === 'datetime-local') return new Date(value).toLocaleString('pt-BR')
  return value
}

function normalizeInputValue(value, type) {
  if (value === null || value === undefined) return initialValue({ type })
  if (type === 'datetime-local') return String(value).slice(0, 16)
  return value
}

async function load() {
  loading.value = true
  feedbackMessage.value = ''
  try {
    const { data } = await moduleApi.list(props.moduleKey)
    items.value = data
  } catch (error) {
    feedbackType.value = 'error'
    feedbackMessage.value = error?.response?.data?.detail || 'Falha ao carregar registros.'
  } finally {
    loading.value = false
  }
}

function startEdit(item) {
  editingId.value = item.id
  props.fields.forEach((field) => {
    form[field.key] = normalizeInputValue(item[field.key], field.type)
  })
}

async function save() {
  loading.value = true
  feedbackMessage.value = ''
  try {
    const payload = normalizePayload()
    if (editingId.value) await moduleApi.update(props.moduleKey, editingId.value, payload)
    else await moduleApi.create(props.moduleKey, payload)

    feedbackType.value = 'success'
    feedbackMessage.value = editingId.value ? 'Registro atualizado com sucesso.' : 'Registro criado com sucesso.'
    await load()
    resetForm()
  } catch (error) {
    feedbackType.value = 'error'
    feedbackMessage.value = error?.response?.data?.detail || 'Erro ao salvar registro.'
  } finally {
    loading.value = false
  }
}

async function remove(id) {
  loading.value = true
  feedbackMessage.value = ''
  try {
    await moduleApi.remove(props.moduleKey, id)
    feedbackType.value = 'success'
    feedbackMessage.value = 'Registro excluído com sucesso.'
    await load()
  } catch (error) {
    feedbackType.value = 'error'
    feedbackMessage.value = error?.response?.data?.detail || 'Erro ao excluir registro.'
  } finally {
    loading.value = false
  }
}

watch(
  () => props.moduleKey,
  async () => {
    resetForm()
    await load()
  },
  { immediate: true },
)
</script>
