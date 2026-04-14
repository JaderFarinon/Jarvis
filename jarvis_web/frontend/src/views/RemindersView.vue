<template>
  <CrudManager title="Lembretes" subtitle="Não perca prazos importantes." module-key="reminders" :fields="fields" />
</template>

<script setup>
import CrudManager from '../components/crud/CrudManager.vue'

const fields = [
  { key: 'title', label: 'Título', required: true },
  { key: 'description', label: 'Descrição', type: 'textarea' },
  { key: 'remind_at', label: 'Lembrar em', type: 'datetime-local', required: true },
  { key: 'status', label: 'Status', type: 'select', options: ['pending', 'done', 'canceled'], required: true },
]
</script>
