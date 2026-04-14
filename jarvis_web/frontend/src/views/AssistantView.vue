<template>
  <div class="grid gap-4 xl:grid-cols-[300px,1fr]">
    <PageCard>
      <div class="mb-3 flex items-center justify-between">
        <h3 class="text-lg font-semibold">Conversas</h3>
        <button class="rounded-lg border border-slate-200 px-2 py-1 text-xs hover:bg-slate-100" @click="createConversation">+ Nova</button>
      </div>

      <div v-if="conversationsLoading" class="text-sm text-slate-500">Carregando...</div>
      <ul v-else class="space-y-2">
        <li v-for="conversation in conversations" :key="conversation.id">
          <button
            class="w-full rounded-lg border px-3 py-2 text-left text-sm hover:bg-slate-50"
            :class="activeConversationId === conversation.id ? 'border-slate-900 bg-slate-900 text-white hover:bg-slate-900' : 'border-slate-200 text-slate-700'"
            @click="openConversation(conversation.id)"
          >
            {{ conversation.title }}
          </button>
        </li>
      </ul>
    </PageCard>

    <PageCard>
      <FeedbackAlert :type="feedbackType" :message="feedbackMessage" />

      <div class="mb-4 mt-3 h-[55vh] space-y-3 overflow-y-auto rounded-xl border border-slate-200 bg-slate-50 p-3">
        <article
          v-for="message in messages"
          :key="message.id"
          :class="message.role === 'assistant' ? 'mr-8 bg-white' : 'ml-8 bg-slate-900 text-white'"
          class="rounded-xl p-3 text-sm shadow-sm"
        >
          <p class="mb-1 text-xs uppercase tracking-wide opacity-70">{{ message.role }}</p>
          <p class="whitespace-pre-wrap">{{ message.content }}</p>
        </article>
        <p v-if="!messages.length" class="text-sm text-slate-500">Inicie uma conversa com o assistente.</p>
      </div>

      <form class="flex gap-2" @submit.prevent="sendMessage">
        <input
          v-model="messageText"
          placeholder="Digite sua mensagem..."
          class="flex-1 rounded-lg border border-slate-200 px-3 py-2 outline-none ring-slate-300 focus:ring"
          :disabled="chatLoading"
          required
        />
        <button class="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800" :disabled="chatLoading">
          {{ chatLoading ? 'Enviando...' : 'Enviar' }}
        </button>
      </form>
    </PageCard>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import PageCard from '../components/shared/PageCard.vue'
import FeedbackAlert from '../components/shared/FeedbackAlert.vue'
import { chatApi } from '../services/api'

const conversations = ref([])
const messages = ref([])
const activeConversationId = ref(null)
const messageText = ref('')
const conversationsLoading = ref(false)
const chatLoading = ref(false)
const feedbackType = ref('info')
const feedbackMessage = ref('')

async function loadConversations() {
  conversationsLoading.value = true
  try {
    const { data } = await chatApi.listConversations()
    conversations.value = data
    if (data.length && !activeConversationId.value) {
      await openConversation(data[0].id)
    }
  } catch (error) {
    feedbackType.value = 'error'
    feedbackMessage.value = error?.response?.data?.detail || 'Falha ao carregar conversas.'
  } finally {
    conversationsLoading.value = false
  }
}

async function openConversation(id) {
  activeConversationId.value = id
  try {
    const { data } = await chatApi.listMessages(id)
    messages.value = data
  } catch (error) {
    feedbackType.value = 'error'
    feedbackMessage.value = error?.response?.data?.detail || 'Falha ao carregar mensagens.'
  }
}

async function createConversation() {
  try {
    const { data } = await chatApi.createConversation(`Conversa ${new Date().toLocaleString('pt-BR')}`)
    conversations.value.unshift(data)
    await openConversation(data.id)
  } catch (error) {
    feedbackType.value = 'error'
    feedbackMessage.value = error?.response?.data?.detail || 'Falha ao criar conversa.'
  }
}

async function sendMessage() {
  if (!messageText.value.trim()) return

  chatLoading.value = true
  feedbackMessage.value = ''
  try {
    const { data } = await chatApi.sendAssistantMessage(messageText.value, activeConversationId.value)
    activeConversationId.value = data.conversation_id

    await loadConversations()
    await openConversation(data.conversation_id)
    messageText.value = ''
  } catch (error) {
    feedbackType.value = 'error'
    feedbackMessage.value = error?.response?.data?.detail || 'Erro ao enviar mensagem.'
  } finally {
    chatLoading.value = false
  }
}

onMounted(loadConversations)
</script>
