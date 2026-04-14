import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AssistantView from '../views/AssistantView.vue'
import TasksView from '../views/TasksView.vue'
import AppointmentsView from '../views/AppointmentsView.vue'
import NotesView from '../views/NotesView.vue'
import ExpensesView from '../views/ExpensesView.vue'
import RemindersView from '../views/RemindersView.vue'
import SettingsView from '../views/SettingsView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/assistente', name: 'assistant', component: AssistantView },
  { path: '/tarefas', name: 'tasks', component: TasksView },
  { path: '/compromissos', name: 'appointments', component: AppointmentsView },
  { path: '/notas', name: 'notes', component: NotesView },
  { path: '/gastos', name: 'expenses', component: ExpensesView },
  { path: '/lembretes', name: 'reminders', component: RemindersView },
  { path: '/configuracoes', name: 'settings', component: SettingsView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
