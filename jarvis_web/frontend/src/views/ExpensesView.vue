<template>
  <CrudManager title="Gastos" subtitle="Controle despesas recentes." module-key="expenses" :fields="fields" />
</template>

<script setup>
import CrudManager from '../components/crud/CrudManager.vue'

const fields = [
  { key: 'description', label: 'Descrição', required: true },
  { key: 'amount', label: 'Valor', type: 'number', required: true },
  { key: 'category', label: 'Categoria' },
  { key: 'expense_date', label: 'Data do gasto', type: 'date', required: true },
  { key: 'payment_method', label: 'Método de pagamento' },
  { key: 'notes', label: 'Observações', type: 'textarea' },
]
</script>
