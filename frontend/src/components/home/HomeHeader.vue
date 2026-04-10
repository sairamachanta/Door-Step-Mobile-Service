<template>
  <header class="sticky top-0 z-40 bg-white border-b border-gray-200 transition-shadow duration-200" :class="{ 'shadow-md': scrolled }">
    <!-- Location Row -->
    <div class="flex items-center justify-between px-4 pt-3 pb-2">
      <button class="flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-gray-50 active:scale-95 transition-all duration-200">
        <MapPin class="w-4 h-4 text-primary-500" />
        <div class="text-left">
          <p class="text-[10px] text-gray-500 uppercase tracking-wide">Location</p>
          <p class="text-sm font-semibold text-gray-900">Tiruppur, Tamil Nadu</p>
        </div>
        <ChevronDown class="w-4 h-4 text-gray-400" />
      </button>

      <button class="relative p-2 rounded-lg hover:bg-gray-50 active:scale-95 transition-all duration-200">
        <Bell class="w-5 h-5 text-gray-600" />
        <span class="absolute top-1.5 right-1.5 w-2 h-2 bg-error rounded-full"></span>
      </button>
    </div>

    <!-- Search Bar -->
    <div class="px-4 pb-3">
      <div class="relative">
        <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          placeholder="Search for repairs..."
          class="w-full h-11 pl-10 pr-4 bg-gray-100 rounded-lg text-sm placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:bg-white transition-all duration-200"
        />
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { MapPin, Bell, ChevronDown, Search } from 'lucide-vue-next'

const scrolled = ref(false)

const handleScroll = () => {
  scrolled.value = window.scrollY > 10
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
