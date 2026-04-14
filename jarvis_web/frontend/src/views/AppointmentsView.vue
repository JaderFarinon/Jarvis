<template>
  <CrudManager title="Compromissos" subtitle="Organize sua agenda." module-key="appointments" :fields="fields" />
</template>

<script setup>
import CrudManager from '../components/crud/CrudManager.vue'

const fields = [
  { key: 'title', label: 'Título', required: true },
  { key: 'description', label: 'Descrição', type: 'textarea' },
  { key: 'date', label: 'Data', type: 'date', required: true },
  { key: 'time', label: 'Hora', type: 'time', required: true },
  { key: 'location', label: 'Local' },
  { key: 'status', label: 'Status', type: 'select', options: ['scheduled', 'done', 'canceled'], required: true },
]
</script>
