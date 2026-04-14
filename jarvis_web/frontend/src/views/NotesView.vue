<template>
  <CrudManager title="Notas" subtitle="Capture ideias e informações." module-key="notes" :fields="fields" />
</template>

<script setup>
import CrudManager from '../components/crud/CrudManager.vue'

const fields = [
  { key: 'title', label: 'Título', required: true },
  { key: 'content', label: 'Conteúdo', type: 'textarea', required: true },
  { key: 'tag', label: 'Tag' },
]
</script>
