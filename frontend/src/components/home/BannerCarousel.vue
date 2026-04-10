<template>
  <div class="mx-4 my-6">
    <div class="relative h-48 rounded-xl overflow-hidden shadow-card">
      <!-- Slides -->
      <div 
        class="flex transition-transform duration-500 ease-in-out h-full"
        :style="{ transform: `translateX(-${currentSlide * 100}%)` }"
      >
        <div
          v-for="(banner, index) in banners"
          :key="banner.id"
          class="min-w-full h-full relative flex-shrink-0"
        >
          <img
            :src="banner.image_url"
            :alt="banner.title"
            class="w-full h-full object-cover"
          />
          
          <!-- Gradient Overlay -->
          <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent"></div>
          
          <!-- Content -->
          <div class="absolute bottom-0 left-0 right-0 p-6">
            <h3 class="text-2xl font-bold text-white mb-1">{{ banner.title }}</h3>
            <p class="text-sm text-white/90 mb-4">{{ banner.description }}</p>
            <button class="px-4 py-2 bg-white text-primary-500 text-sm font-semibold rounded-lg shadow-md hover:shadow-lg active:scale-95 transition-all duration-200">
              {{ banner.cta_text }}
            </button>
          </div>
        </div>
      </div>

      <!-- Indicators -->
      <div class="absolute bottom-3 left-1/2 -translate-x-1/2 flex gap-2">
        <button
          v-for="(banner, index) in banners"
          :key="'indicator-' + banner.id"
          @click="goToSlide(index)"
          class="w-2 h-2 rounded-full transition-all duration-200"
          :class="currentSlide === index ? 'bg-white w-6' : 'bg-white/50'"
        ></button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  banners: {
    type: Array,
    default: () => []
  }
})

const currentSlide = ref(0)
let autoSlideInterval = null

const goToSlide = (index) => {
  currentSlide.value = index
  resetAutoSlide()
}

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % props.banners.length
}

const startAutoSlide = () => {
  autoSlideInterval = setInterval(nextSlide, 4000)
}

const resetAutoSlide = () => {
  if (autoSlideInterval) {
    clearInterval(autoSlideInterval)
  }
  startAutoSlide()
}

onMounted(() => {
  if (props.banners.length > 1) {
    startAutoSlide()
  }
})

onUnmounted(() => {
  if (autoSlideInterval) {
    clearInterval(autoSlideInterval)
  }
})
</script>
