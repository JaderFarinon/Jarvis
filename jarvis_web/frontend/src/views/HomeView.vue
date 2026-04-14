<template>
  <div class="space-y-4">
    <section class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <PageCard v-for="card in cards" :key="card.label">
        <p class="text-sm text-slate-500">{{ card.label }}</p>
        <p class="mt-2 text-3xl font-bold text-slate-900">{{ card.value }}</p>
      </PageCard>
    </section>

    <PageCard>
      <div class="mb-3 flex items-center justify-between">
        <h3 class="text-lg font-semibold">Ações rápidas</h3>
        <button class="rounded-lg border border-slate-200 px-3 py-1.5 text-sm hover:bg-slate-50" :disabled="loading" @click="loadSummary">Atualizar</button>
      </div>

      <FeedbackAlert :type="error ? 'error' : 'info'" :message="error" />

      <div class="grid gap-2 sm:grid-cols-2 lg:grid-cols-4">
        <RouterLink v-for="item in quickActions" :key="item.path" :to="item.path" class="rounded-lg border border-slate-200 p-3 text-sm font-medium text-slate-700 transition hover:bg-slate-100">
          {{ item.label }}
        </RouterLink>
      </div>
    </PageCard>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import PageCard from '../components/shared/PageCard.vue'
import FeedbackAlert from '../components/shared/FeedbackAlert.vue'
import { dashboardApi } from '../services/api'

const quickActions = [
  { label: 'Nova tarefa', path: '/tarefas' },
  { label: 'Novo compromisso', path: '/compromissos' },
  { label: 'Nova nota', path: '/notas' },
  { label: 'Novo lembrete', path: '/lembretes' },
]

const counts = ref({ tasks: 0, appointments: 0, expenses: 0, reminders: 0 })
const loading = ref(false)
const error = ref('')

const cards = computed(() => [
  { label: 'Tarefas pendentes', value: counts.value.tasks },
  { label: 'Próximos compromissos', value: counts.value.appointments },
  { label: 'Gastos recentes', value: counts.value.expenses },
  { label: 'Lembretes', value: counts.value.reminders },
])

async function loadSummary() {
  loading.value = true
  error.value = ''
  try {
    const [tasks, appointments, expenses, reminders] = await Promise.all([
      dashboardApi.tasks(),
      dashboardApi.appointments(),
      dashboardApi.expenses(),
      dashboardApi.reminders(),
    ])

    counts.value = {
      tasks: tasks.data.filter((item) => ['pending', 'in_progress'].includes(item.status)).length,
      appointments: appointments.data.slice(0, 5).length,
      expenses: expenses.data.slice(0, 10).length,
      reminders: reminders.data.filter((item) => item.status === 'pending').length,
    }
  } catch (err) {
    error.value = err?.response?.data?.detail || 'Não foi possível carregar os dados da home.'
  } finally {
    loading.value = false
  }
}

onMounted(loadSummary)
</script>
