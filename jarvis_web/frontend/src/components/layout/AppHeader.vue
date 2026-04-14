<template>
  <header class="sticky top-0 z-20 border-b border-slate-200 bg-white/90 px-4 py-3 backdrop-blur sm:px-6">
    <div class="flex items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <button class="rounded-lg border border-slate-200 p-2 text-slate-600 hover:bg-slate-100 lg:hidden" @click="$emit('toggle-sidebar')">
          ☰
        </button>
        <div>
          <h2 class="text-lg font-semibold text-slate-900">{{ title }}</h2>
          <p class="text-xs text-slate-500">Painel pessoal integrado</p>
        </div>
      </div>
      <span class="rounded-full bg-slate-900 px-3 py-1 text-xs font-semibold text-white">Online</span>
    </div>
  </header>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
})

defineEmits(['toggle-sidebar'])
</script>
