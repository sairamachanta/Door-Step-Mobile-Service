<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ChevronLeft, Search, Smartphone, Loader2 } from 'lucide-vue-next'
import BaseLayout from '../../components/BaseLayout.vue'
import { useBookingStore } from '../../stores/booking'

const route = useRoute()
const router = useRouter()
const bookingStore = useBookingStore()

const searchQuery = ref('')
const selectedYear = ref('')
const sortBy = ref('popular')

onMounted(() => {
  if (!bookingStore.selectedBrandId) {
    router.replace('/booking/select-brand')
    return
  }
  bookingStore.fetchModels(bookingStore.selectedBrandId)
})

const filteredModels = computed(() => {
  let result = bookingStore.models
  
  // Search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(m => m.model_name.toLowerCase().includes(query))
  }
  
  // Filter Year
  if (selectedYear.value) {
    result = result.filter(m => m.release_year.toString() === selectedYear.value)
  }
  
  // Sort
  result = [...result].sort((a, b) => { 
      switch (sortBy.value) {
          case 'popular':
              return (b.is_popular === a.is_popular) ? 0 : b.is_popular ? 1 : -1
          case 'newest':
              return b.release_year - a.release_year
          case 'name':
              return a.model_name.localeCompare(b.model_name)
          default:
              return 0
      }
  })
  
  return result
})

const selectModel = (model) => {
  bookingStore.setModel(model.id)
  router.push('/booking/select-service')
}
</script>

<template>
  <BaseLayout>
    <div class="bg-gray-50 min-h-screen pb-24">
      <!-- Header -->
      <header class="bg-white sticky top-0 z-40 border-b border-gray-100 px-4 py-3 flex items-center space-x-3">
        <button @click="$router.back()" class="p-2 -ml-2 rounded-full hover:bg-gray-100">
          <ChevronLeft class="w-6 h-6 text-gray-600" />
        </button>
        <div class="flex-1">
          <h1 class="text-lg font-bold text-gray-900">Select Model</h1>
          <p class="text-xs text-gray-500">{{ bookingStore.selectedBrand?.name || 'Device' }} Models</p>
        </div>
        <div class="text-sm font-medium text-blue-600">2/7</div>
      </header>

      <main class="px-4 py-4">
        <!-- Search -->
        <div class="relative mb-4">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Search models..." 
            class="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition shadow-sm"
          />
        </div>
        
        <!-- Filters -->
        <div class="flex space-x-2 mb-6 overflow-x-auto pb-2 scrollbar-hide">
          <select v-model="selectedYear" class="px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm text-gray-700 min-w-[100px] outline-none focus:ring-2 focus:ring-blue-500/20">
            <option value="">All Years</option>
            <option value="2024">2024</option>
            <option value="2023">2023</option>
            <option value="2022">2022</option>
            <option value="2021">2021</option>
          </select>
          
          <select v-model="sortBy" class="px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm text-gray-700 min-w-[120px] outline-none focus:ring-2 focus:ring-blue-500/20">
             <option value="popular">Popular First</option>
             <option value="newest">Newest First</option>
             <option value="name">Name A-Z</option>
          </select>
        </div>

        <div v-if="bookingStore.loading" class="flex flex-col items-center justify-center py-20">
          <Loader2 class="w-10 h-10 text-blue-500 animate-spin mb-4" />
          <p class="text-gray-500 font-medium">Loading models...</p>
        </div>

        <template v-else>
          <!-- Models Grid -->
          <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
             <div 
               v-for="model in filteredModels" 
               :key="model.id"
               @click="selectModel(model)"
               class="bg-white p-4 rounded-xl border border-gray-100 shadow-sm cursor-pointer hover:border-blue-500 hover:shadow-md transition relative group"
             >
                <!-- Popular Badge -->
                <span v-if="model.is_popular" class="absolute top-2 right-2 bg-yellow-100 text-yellow-800 text-[10px] font-bold px-2 py-0.5 rounded-full">POPULAR</span>
                
                <div class="h-32 mb-3 flex items-center justify-center bg-gray-50 rounded-lg">
                  <img v-if="model.image_url" :src="model.image_url" :alt="model.model_name" class="h-28 object-contain transition group-hover:scale-105" />
                  <Smartphone v-else class="w-12 h-12 text-gray-400 group-hover:scale-105 transition" />
                </div>
                
                <h3 class="font-bold text-gray-900 text-sm mb-1 group-hover:text-blue-600 transition">{{ model.model_name }}</h3>
                <div class="flex justify-between items-center">
                   <span class="text-xs text-gray-500">{{ model.release_year }}</span>
                   <span v-if="model.original_price" class="text-[10px] text-gray-400 line-through">₹{{ model.original_price }}</span>
                </div>
             </div>
          </div>
          
          <!-- Empty State -->
          <div v-if="filteredModels.length === 0" class="text-center py-10 bg-white rounded-2xl border border-dashed border-gray-200">
             <Smartphone class="w-12 h-12 text-gray-300 mx-auto mb-2" />
             <p class="text-gray-500 font-medium">No models found</p>
             <button class="mt-4 text-blue-600 font-medium text-sm hover:underline">Model not listed?</button>
          </div>
        </template>
      </main>
    </div>
  </BaseLayout>
</template>
