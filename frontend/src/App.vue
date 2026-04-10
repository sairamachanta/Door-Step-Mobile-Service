<script setup>
import { onMounted } from 'vue'
import { useMetadataStore } from './stores/metadataStore'

const metadataStore = useMetadataStore()

onMounted(() => {
  metadataStore.initialize()
})
</script>

<template>
  <router-view></router-view>
</template>

<style scoped>
</style>
