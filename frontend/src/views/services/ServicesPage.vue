<template>
  <BaseLayout>
    <div class="min-h-screen bg-slate-50 pb-24 md:pb-8">
      <!-- Premium Header -->
      <header class="bg-white/80 backdrop-blur-xl border-b border-slate-100 px-6 py-6 sticky top-0 z-30 shadow-sm">
        <div class="max-w-7xl mx-auto space-y-6">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-3xl font-black text-slate-900 tracking-tight bg-gradient-to-r from-primary-700 to-blue-600 bg-clip-text text-transparent">
                Expert Services
              </h1>
              <p class="text-sm text-slate-500 font-medium mt-1">Professional repairs at your doorstep</p>
            </div>
          </div>
          
          <!-- Search & Filter Container -->
          <div class="flex flex-col md:flex-row gap-4">
            <!-- Search Bar -->
            <div class="relative flex-grow group">
              <Search class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 group-focus-within:text-primary-600 transition-colors" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search for screen, battery, or any repair..."
                class="w-full h-14 pl-12 pr-4 bg-slate-100/50 rounded-2xl text-sm font-medium border-2 border-transparent focus:border-primary-500 focus:bg-white focus:ring-4 focus:ring-primary-500/10 transition-all duration-300"
              />
            </div>
            
            <!-- Category Chips -->
            <div class="flex gap-2 overflow-x-auto hide-scrollbar pb-1 md:pb-0 items-center">
              <button
                v-for="cat in formattedCategories"
                :key="cat.id"
                @click="selectedCategory = cat.id"
                class="px-5 py-3 rounded-xl text-xs font-black uppercase tracking-widest whitespace-nowrap transition-all duration-300 active:scale-95 border-2"
                :class="selectedCategory === cat.id 
                  ? 'bg-primary-700 text-white border-primary-700 shadow-lg shadow-primary-700/20' 
                  : 'bg-white text-slate-600 border-slate-100 hover:border-primary-200 hover:text-primary-600'"
              >
                {{ cat.name }}
              </button>
            </div>
          </div>
        </div>
      </header>

      <main class="max-w-7xl mx-auto p-6">
        <!-- Loading State -->
        <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="i in 6" :key="i" class="bg-white rounded-[2rem] p-6 space-y-4 border border-slate-100">
            <div class="w-16 h-16 bg-slate-100 rounded-2xl animate-pulse"></div>
            <div class="space-y-2">
              <div class="h-6 bg-slate-100 rounded-lg w-3/4 animate-pulse"></div>
              <div class="h-4 bg-slate-100 rounded-lg w-full animate-pulse"></div>
              <div class="h-4 bg-slate-100 rounded-lg w-5/6 animate-pulse"></div>
            </div>
            <div class="pt-4 flex justify-between items-center">
              <div class="h-8 bg-slate-100 rounded-lg w-24 animate-pulse"></div>
              <div class="h-10 bg-slate-100 rounded-xl w-28 animate-pulse"></div>
            </div>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="bg-red-50 rounded-[2rem] p-12 text-center border-2 border-dashed border-red-200">
          <AlertCircle class="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h3 class="text-xl font-black text-red-900 mb-2">Oops! Something went wrong</h3>
          <p class="text-red-600 font-medium mb-6">{{ error }}</p>
          <button @click="handleRetry" class="px-8 py-3 bg-red-600 text-white rounded-2xl font-bold hover:bg-red-700 transition-all active:scale-95 shadow-lg shadow-red-600/20">
            Retry Connection
          </button>
        </div>

        <!-- No Results -->
        <div v-else-if="services.length === 0" class="bg-white rounded-[2rem] p-16 text-center border border-slate-100">
          <div class="w-24 h-24 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-6">
            <Search class="w-12 h-12 text-slate-300" />
          </div>
          <h3 class="text-2xl font-black text-slate-800 mb-2">No repair services found</h3>
          <p class="text-slate-500 font-medium mb-8">Try adjusting your search or category filters</p>
          <button @click="resetFilters" class="px-8 py-3 bg-primary-700 text-white rounded-2xl font-bold hover:bg-primary-800 transition-all">
            Clear All Filters
          </button>
        </div>

        <!-- Services Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-reveal">
          <div
            v-for="service in services"
            :key="service.id"
            class="group bg-white rounded-[2rem] p-6 border border-slate-100 hover:border-primary-200 hover:shadow-2xl hover:shadow-primary-700/5 transition-all duration-500 flex flex-col"
          >
            <div class="flex items-start justify-between mb-6">
              <!-- Animated Icon -->
              <div 
                class="w-16 h-16 rounded-2xl flex items-center justify-center transition-all duration-500 group-hover:scale-110 group-hover:rotate-3 shadow-sm"
                :style="{ backgroundColor: `${service.icon_color}15`, color: service.icon_color }"
              >
                <component 
                  :is="getLucideIcon(service.icon)" 
                  class="w-8 h-8"
                />
              </div>
              
              <!-- Popular Tag -->
              <span v-if="service.is_popular" class="px-3 py-1 bg-amber-50 text-amber-600 text-[10px] font-black uppercase tracking-widest rounded-full border border-amber-100">
                Popular
              </span>
            </div>

            <div class="flex-grow space-y-3">
              <h3 class="text-xl font-black text-slate-900 group-hover:text-primary-700 transition-colors">{{ service.name }}</h3>
              <p class="text-sm text-slate-500 font-medium leading-relaxed line-clamp-3">
                {{ service.description }}
              </p>
              
              <!-- Features -->
              <div class="flex flex-wrap gap-3 pt-2">
                <div class="flex items-center gap-1.5 text-xs font-bold text-slate-400">
                  <Clock class="w-4 h-4 text-primary-500/50" />
                  {{ service.duration || '30-45m' }}
                </div>
                <div class="flex items-center gap-1.5 text-xs font-bold text-slate-400">
                  <Shield class="w-4 h-4 text-emerald-500/50" />
                  {{ service.warranty || '6m Warranty' }}
                </div>
              </div>
            </div>

            <!-- Price & Action -->
            <div class="mt-8 pt-6 border-t border-slate-50 flex items-center justify-between">
              <div>
                <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Starts from</p>
                <p class="text-2xl font-black text-slate-900">₹{{ service.starting_price || '999' }}</p>
              </div>
              <button 
                @click="handleBooking(service)"
                class="px-6 py-3.5 bg-slate-900 text-white rounded-2xl font-black text-sm hover:bg-primary-700 hover:scale-105 active:scale-95 transition-all duration-300 shadow-lg shadow-slate-900/10 hover:shadow-primary-700/20"
              >
                Book Now
              </button>
            </div>
          </div>
        </div>
      </main>

      <!-- Floating Support Button -->
      <a 
        href="https://wa.me/919390999539" 
        target="_blank"
        class="fixed bottom-24 right-6 md:bottom-8 md:right-8 w-14 h-14 bg-emerald-500 text-white rounded-full flex items-center justify-center shadow-2xl shadow-emerald-500/30 hover:scale-110 active:scale-95 transition-all z-40 group"
      >
        <MessageSquare class="w-6 h-6" />
        <span class="absolute right-full mr-4 px-4 py-2 bg-slate-900 text-white text-xs font-bold rounded-xl opacity-0 group-hover:opacity-100 pointer-events-none transition-all whitespace-nowrap">
          Need help? Chat with us
        </span>
      </a>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import BaseLayout from '../../components/BaseLayout.vue'
import { useServices } from '../../composables/useServices'
import { 
  Search, Clock, Shield, Smartphone, Battery, Droplets, Code, 
  Camera, Wrench, AlertCircle, MessageSquare, Laptop, 
  Zap, Heart, ChevronRight, Tablet, Monitor
} from 'lucide-vue-next'

const router = useRouter()
const searchQuery = ref('')
const selectedCategory = ref('All')

const {
  categories,
  services,
  loading,
  error,
  fetchCategories,
  fetchServices
} = useServices()

// Format categories for UI
const formattedCategories = computed(() => {
  const cats = [{ id: 'All', name: 'All Repairs' }]
  if (categories.value && categories.value.categories) {
    categories.value.categories.forEach(c => {
      cats.push({ id: c.id, name: c.name })
    })
  }
  return cats
})

// Debounced fetch
let fetchTimeout
watch([searchQuery, selectedCategory], () => {
  clearTimeout(fetchTimeout)
  fetchTimeout = setTimeout(() => {
    fetchServices({ 
      categoryId: selectedCategory.value, 
      search: searchQuery.value 
    })
  }, 300)
})

onMounted(async () => {
  await Promise.all([
    fetchCategories(),
    fetchServices({ categoryId: 'All' })
  ])
})

const handleRetry = () => {
  fetchCategories()
  fetchServices({ categoryId: selectedCategory.value, search: searchQuery.value })
}

const resetFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = 'All'
}

const handleBooking = (service) => {
  // In a real app, we'd go to brand selection with the service pre-selected
  router.push('/booking/select-brand')
}

// Icon mapping helper
const getLucideIcon = (iconName) => {
  const icons = {
    Smartphone, Battery, Droplets, Code, Camera, 
    Wrench, Laptop, Zap, Tablet, Monitor
  }
  return icons[iconName] || Smartphone
}
</script>

<style scoped>
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.animate-reveal {
  animation: reveal 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes reveal {
  from { opacity: 0; transform: translateY(30px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}

.shadow-card {
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
}
</style>
