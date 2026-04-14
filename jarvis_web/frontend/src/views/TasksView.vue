<template>
  <CrudManager title="Tarefas" subtitle="Gerencie tarefas e acompanhe status." module-key="tasks" :fields="fields" />
</template>

<script setup>
import CrudManager from '../components/crud/CrudManager.vue'

const fields = [
  { key: 'title', label: 'Título', required: true },
  { key: 'description', label: 'Descrição', type: 'textarea' },
  { key: 'priority', label: 'Prioridade', type: 'select', options: ['low', 'medium', 'high'], required: true },
  { key: 'status', label: 'Status', type: 'select', options: ['pending', 'in_progress', 'done'], required: true },
  { key: 'due_date', label: 'Data limite', type: 'date' },
]
</script>
