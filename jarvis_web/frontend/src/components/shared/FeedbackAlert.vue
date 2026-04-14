<template>
  <p v-if="message" :class="classes" class="rounded-lg border px-3 py-2 text-sm">
    {{ message }}
  </p>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: { type: String, default: 'info' },
  message: { type: String, default: '' },
})

const classes = computed(() => {
  if (props.type === 'error') return 'border-red-200 bg-red-50 text-red-700'
  if (props.type === 'success') return 'border-emerald-200 bg-emerald-50 text-emerald-700'
  return 'border-blue-200 bg-blue-50 text-blue-700'
})
</script>
