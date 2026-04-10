<template>
  <BaseLayout>
    <div class="bg-gray-50 min-h-screen pb-24">
      <!-- Header -->
      <header class="bg-white sticky top-0 z-40 border-b border-gray-100 px-4 py-3 flex items-center space-x-3">
        <button @click="$router.back()" class="p-2 -ml-2 rounded-full hover:bg-gray-100">
          <ChevronLeft class="w-6 h-6 text-gray-600" />
        </button>
        <div class="flex-1">
          <h1 class="text-lg font-bold text-gray-900">Select Brand</h1>
          <p class="text-xs text-gray-500">Step 1 of 7</p>
        </div>
        <div class="text-sm font-medium text-blue-600">1/7</div>
      </header>

      <main class="px-4 py-4">
        <!-- Search -->
        <div class="relative mb-6">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Search brands..." 
            class="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition shadow-sm"
          />
        </div>

        <div v-if="bookingStore.loading && bookingStore.brands.length === 0" class="flex flex-col items-center justify-center py-20">
          <Loader2 class="w-10 h-10 text-blue-500 animate-spin mb-4" />
          <p class="text-gray-500 font-medium">Loading brands...</p>
        </div>

        <template v-else>
          <!-- Popular Brands -->
          <div v-if="!searchQuery && popularBrands.length > 0" class="mb-6">
            <h2 class="text-sm font-bold text-gray-700 mb-3 uppercase tracking-wide">Popular Brands</h2>
            <div class="grid grid-cols-3 gap-3">
               <div 
                v-for="brand in popularBrands" 
                :key="brand.id"
                @click="selectBrand(brand)"
                class="bg-white p-4 rounded-xl border border-gray-100 shadow-sm flex flex-col items-center justify-center gap-2 cursor-pointer hover:border-blue-500 hover:shadow-md transition group h-32"
              >
                <!-- Logo with fallback -->
                <div class="w-12 h-12 bg-gradient-to-br from-blue-100 to-purple-100 rounded-full flex items-center justify-center text-2xl group-hover:scale-110 transition duration-300">
                  {{ getEmoji(brand.name) }}
                </div>
                <span class="text-xs font-medium text-gray-700 group-hover:text-blue-600">{{ brand.name }}</span>
              </div>
            </div>
          </div>

          <!-- All Brands -->
          <h2 class="text-sm font-bold text-gray-700 mb-3 uppercase tracking-wide">All Brands</h2>
          <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-3">
              <div 
                v-for="brand in filteredBrands" 
                :key="brand.id"
                @click="selectBrand(brand)"
                class="bg-white p-4 rounded-xl border border-gray-100 shadow-sm flex flex-col items-center justify-center gap-2 cursor-pointer hover:border-blue-500 hover:shadow-md transition group h-28"
              >
                 <!-- Logo with emoji/text fallback -->
                <div class="w-10 h-10 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center text-lg font-semibold text-gray-600 group-hover:scale-110 transition duration-300">
                  {{ getEmoji(brand.name) }}
                </div>
                <span class="text-xs font-medium text-gray-700 text-center">{{ brand.name }}</span>
              </div>
              
              <!-- Other Brand Option -->
              <div 
                @click="openOtherBrandModal"
                class="bg-gray-50 p-4 rounded-xl border border-dashed border-gray-300 flex flex-col items-center justify-center gap-2 cursor-pointer hover:bg-gray-100 transition h-28"
              >
                <HelpCircle class="w-6 h-6 text-gray-400" />
                <span class="text-xs font-medium text-gray-500">Other</span>
              </div>
          </div>

          <!-- Empty State -->
          <div v-if="filteredBrands.length === 0" class="text-center py-10">
             <Smartphone class="w-12 h-12 text-gray-300 mx-auto mb-2" />
             <p class="text-gray-500 font-medium">No brands found</p>
             <p class="text-gray-400 text-sm">Try searching for something else</p>
          </div>
        </template>
      </main>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ChevronLeft, Search, Smartphone, HelpCircle, Loader2 } from 'lucide-vue-next'
import BaseLayout from '../../components/BaseLayout.vue'
import { useBookingStore } from '../../stores/booking'

const router = useRouter()
const bookingStore = useBookingStore()

const searchQuery = ref('')

onMounted(() => {
  bookingStore.fetchBrands()
})

const popularBrands = computed(() => {
  return bookingStore.brands.filter(b => b.is_popular).slice(0, 6)
})

const filteredBrands = computed(() => {
  if (!searchQuery.value) return bookingStore.brands
  const query = searchQuery.value.toLowerCase()
  return bookingStore.brands.filter(brand => brand.name.toLowerCase().includes(query))
})

const selectBrand = (brand) => {
  bookingStore.setBrand(brand.id)
  router.push('/booking/select-model')
}

// Logic to handle emoji fallbacks for brands
const getEmoji = (name) => {
  const map = {
    'Apple': '🍎',
    'Samsung': '📱',
    'Google': '🤖',
    'OnePlus': '➕',
    'Xiaomi': '🧧',
    'Sony': '📷',
    'Nothing': '⚫',
    'Realme': '🟡',
    'Vivo': '💎',
    'Oppo': '🟢'
  }
  return map[name] || name.charAt(0)
}

const openOtherBrandModal = () => {
  alert('Custom brand selection coming soon!')
}
</script>
