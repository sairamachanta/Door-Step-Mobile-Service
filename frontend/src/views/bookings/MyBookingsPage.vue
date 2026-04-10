<template>
  <BaseLayout>
    <div class="min-h-screen bg-slate-50 pb-24 md:pb-8">
      <!-- Premium Header -->
      <header class="bg-white/80 backdrop-blur-xl border-b border-slate-100 px-6 py-6 sticky top-0 z-30 shadow-sm">
        <div class="max-w-7xl mx-auto space-y-6">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-3xl font-black text-slate-900 tracking-tight bg-gradient-to-r from-primary-700 to-blue-600 bg-clip-text text-transparent">
                My Bookings
              </h1>
              <p class="text-sm text-slate-500 font-medium mt-1">Track and manage your repair requests</p>
            </div>
          </div>
          
          <!-- Search & Tabs Container -->
          <div class="space-y-4">
            <!-- Segmented Control (Tabs) -->
            <div class="flex p-1.5 bg-slate-100 rounded-[1.25rem] w-full max-w-lg gap-1.5">
              <button
                v-for="tab in tabs"
                :key="tab.value"
                @click="selectedStatus = tab.value"
                class="flex-1 flex flex-col sm:flex-row items-center justify-center gap-1 sm:gap-2 py-3 rounded-xl text-[11px] md:text-xs font-black uppercase tracking-wide transition-all duration-500 active:scale-95 group relative overflow-hidden"
                :class="selectedStatus === tab.value 
                   ? 'bg-white text-primary-700 shadow-xl shadow-black/5' 
                  : 'text-slate-500 hover:text-slate-900 hover:bg-white/50'"
              >
                <component 
                  :is="tab.icon" 
                  class="w-3.5 h-3.5 sm:w-4 sm:h-4 transition-transform duration-500 group-hover:scale-110" 
                  :class="selectedStatus === tab.value ? 'text-primary-600' : ''"
                />
                <span class="relative z-10 scale-[0.9] sm:scale-100">{{ tab.label }}</span>
                <!-- Active Indicator Bar -->
                <div v-if="selectedStatus === tab.value" class="absolute bottom-0 left-0 right-0 h-1 bg-primary-600 rounded-full mx-2"></div>
              </button>
            </div>

            <!-- Search Bar -->
            <div class="relative group max-w-2xl">
              <Search class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 group-focus-within:text-primary-600 transition-colors" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search by booking ID or service name..."
                class="w-full h-12 pl-12 pr-4 bg-white rounded-2xl text-sm font-medium border border-slate-200 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 transition-all duration-300"
              />
            </div>
          </div>
        </div>
      </header>

      <main class="max-w-7xl mx-auto p-6">
        <!-- Loading State -->
        <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div v-for="i in 4" :key="i" class="bg-white rounded-[2rem] p-6 space-y-4 border border-slate-100">
            <div class="flex justify-between">
              <div class="h-4 bg-slate-100 rounded w-1/3 animate-pulse"></div>
              <div class="h-6 bg-slate-100 rounded-full w-20 animate-pulse"></div>
            </div>
            <div class="flex gap-4">
              <div class="w-16 h-16 bg-slate-100 rounded-2xl animate-pulse"></div>
              <div class="flex-1 space-y-2">
                <div class="h-6 bg-slate-100 rounded w-3/4 animate-pulse"></div>
                <div class="h-4 bg-slate-100 rounded w-1/2 animate-pulse"></div>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-4 pt-4 border-t border-slate-50">
              <div class="h-10 bg-slate-100 rounded-xl animate-pulse"></div>
              <div class="h-10 bg-slate-100 rounded-xl animate-pulse"></div>
            </div>
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="bg-red-50 rounded-[2rem] p-12 text-center border-2 border-dashed border-red-200">
          <AlertCircle class="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h3 class="text-xl font-black text-red-900 mb-2">Failed to load bookings</h3>
          <p class="text-red-600 font-medium mb-6">{{ error }}</p>
          <button @click="handleRetry" class="px-8 py-3 bg-red-600 text-white rounded-2xl font-bold hover:bg-red-700 transition-all active:scale-95 shadow-lg shadow-red-600/20">
            Retry Connection
          </button>
        </div>

        <!-- Empty State -->
        <div v-else-if="bookings.length === 0" class="bg-white rounded-[2rem] p-16 text-center border border-slate-100">
          <div class="w-24 h-24 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-6">
            <ClipboardList class="w-12 h-12 text-slate-300" />
          </div>
          <h3 class="text-2xl font-black text-slate-800 mb-2">No bookings found</h3>
          <p class="text-slate-500 font-medium mb-8">You haven't made any bookings in this category yet</p>
          <button @click="router.push('/services')" class="px-8 py-3 bg-primary-700 text-white rounded-2xl font-bold hover:bg-primary-800 transition-all">
            Book a Service
          </button>
        </div>

        <!-- Bookings Grid -->
        <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-reveal">
          <div
            v-for="booking in bookings"
            :key="booking.id"
            class="group bg-white rounded-[2rem] p-6 border border-slate-100 hover:border-primary-200 hover:shadow-2xl hover:shadow-primary-700/5 transition-all duration-500"
          >
            <!-- Card Header: ID & Status -->
            <div class="flex items-center justify-between mb-6">
              <div class="flex items-center gap-2">
                <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-100">
                  #{{ booking.booking_number }}
                </span>
                <span class="text-[10px] text-slate-300">•</span>
                <span class="text-[10px] font-bold text-slate-400">{{ formatDate(booking.created_at) }}</span>
              </div>
              <span 
                class="px-3.5 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest border"
                :class="getStatusClasses(booking.status)"
              >
                {{ formatStatus(booking.status) }}
              </span>
            </div>

            <!-- Card Body: Service & Device -->
            <div class="flex gap-5 mb-8">
              <div 
                class="w-16 h-16 rounded-2xl flex items-center justify-center flex-shrink-0 transition-transform group-hover:scale-110"
                :class="getServiceBg(booking.service_type)"
              >
                <component 
                  :is="getServiceIcon(booking.service_icon)" 
                  class="w-8 h-8 text-white"
                />
              </div>
              <div class="flex-1 min-w-0">
                <h3 class="text-xl font-black text-slate-900 group-hover:text-primary-700 transition-colors truncate">
                  {{ booking.service_name }}
                </h3>
                <p class="text-sm font-bold text-slate-500 flex items-center gap-1.5 mt-0.5">
                  <Smartphone class="w-4 h-4 text-slate-400" />
                  {{ booking.brand_name }} {{ booking.model_name }}
                </p>
              </div>
            </div>

            <!-- Card Info: Date & Price -->
            <div class="grid grid-cols-2 gap-4 py-4 border-y border-slate-50 mb-8">
              <div class="space-y-1">
                <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Scheduled For</p>
                <div class="flex items-center gap-2 text-sm font-bold text-slate-700">
                  <Calendar class="w-4 h-4 text-primary-500" />
                  {{ formatDateSmall(booking.preferred_date) }}
                </div>
              </div>
              <div class="space-y-1">
                <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Total Amount</p>
                <p class="text-lg font-black text-slate-900">₹{{ booking.final_price }}</p>
              </div>
            </div>

            <!-- Card Actions -->
            <div class="grid grid-cols-2 gap-3">
              <button 
                @click="handleTrack(booking.id)"
                class="py-3.5 bg-slate-900 text-white rounded-2xl font-black text-xs hover:bg-primary-700 transition-all active:scale-95 shadow-lg shadow-slate-900/10 hover:shadow-primary-700/20"
              >
                Track Status
              </button>
              <button 
                @click="handleDetails(booking.id)"
                class="py-3.5 bg-white text-slate-600 border border-slate-100 rounded-2xl font-black text-xs hover:bg-slate-50 transition-all"
              >
                View Details
              </button>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="pagination.totalPages > 1" class="mt-12 flex justify-center items-center gap-4">
          <button 
            @click="handlePageChange(pagination.page - 1)"
            :disabled="pagination.page === 1"
            class="p-3 bg-white border border-slate-100 rounded-xl disabled:opacity-30 disabled:cursor-not-allowed hover:bg-slate-50 transition-all"
          >
            <ChevronLeft class="w-5 h-5" />
          </button>
          <span class="text-sm font-black text-slate-700 uppercase tracking-widest">
            Page {{ pagination.page }} of {{ pagination.totalPages }}
          </span>
          <button 
            @click="handlePageChange(pagination.page + 1)"
            :disabled="pagination.page === pagination.totalPages"
            class="p-3 bg-white border border-slate-100 rounded-xl disabled:opacity-30 disabled:cursor-not-allowed hover:bg-slate-50 transition-all"
          >
            <ChevronRight class="w-5 h-5" />
          </button>
        </div>
      </main>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BaseLayout from '../../components/BaseLayout.vue'
import { useBookings } from '../../composables/useBookings'
import { 
  Search, Calendar, Clock, MapPin, User, Smartphone, 
  ClipboardList, AlertCircle, RefreshCw, ChevronLeft, 
  ChevronRight, CheckCircle2, XCircle, Timer, Grid
} from 'lucide-vue-next'

const router = useRouter()
const searchQuery = ref('')
const selectedStatus = ref('active')

const {
  bookings,
  loading,
  error,
  pagination,
  fetchBookings
} = useBookings()

const tabs = [
  { label: 'Active', value: 'active', icon: Timer },
  { label: 'Completed', value: 'completed', icon: CheckCircle2 },
  { label: 'Cancelled', value: 'cancelled', icon: XCircle },
  { label: 'All', value: 'all', icon: Grid }
]

// Debounced fetch
let fetchTimeout
watch([searchQuery, selectedStatus], () => {
  clearTimeout(fetchTimeout)
  fetchTimeout = setTimeout(() => {
    fetchBookings({ 
      status: selectedStatus.value, 
      search: searchQuery.value,
      page: 1
    })
  }, 300)
})

onMounted(() => {
  fetchBookings({ status: 'active', page: 1 })
})

const handleRetry = () => {
  fetchBookings({ status: selectedStatus.value, search: searchQuery.value, page: pagination.value.page })
}

const handlePageChange = (newPage) => {
  fetchBookings({ status: selectedStatus.value, search: searchQuery.value, page: newPage })
}

const handleTrack = (id) => {
  // Navigation to tracking page
  console.log('Track', id)
}

const handleDetails = (id) => {
  // Navigation to details page
  console.log('Details', id)
}

// Helpers
const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric' 
  })
}

const formatDateSmall = (dateStr) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { day: 'numeric', month: 'short' })
}

const formatStatus = (status) => {
  return status.replace('_', ' ')
}

const getStatusClasses = (status) => {
  switch (status.toLowerCase()) {
    case 'pending': return 'bg-amber-50 text-amber-600 border-amber-100'
    case 'confirmed': return 'bg-blue-50 text-blue-600 border-blue-100'
    case 'assigned': return 'bg-indigo-50 text-indigo-600 border-indigo-100'
    case 'in_progress': return 'bg-primary-50 text-primary-600 border-primary-100'
    case 'completed': return 'bg-emerald-50 text-emerald-600 border-emerald-100'
    case 'cancelled': return 'bg-red-50 text-red-600 border-red-100'
    default: return 'bg-slate-50 text-slate-600 border-slate-100'
  }
}

const getServiceBg = (type) => {
  switch (type?.toLowerCase()) {
    case 'screen': return 'bg-gradient-to-br from-blue-400 to-blue-600'
    case 'battery': return 'bg-gradient-to-br from-emerald-400 to-emerald-600'
    case 'charging': return 'bg-gradient-to-br from-amber-400 to-amber-600'
    case 'software': return 'bg-gradient-to-br from-purple-400 to-purple-600'
    default: return 'bg-gradient-to-br from-slate-400 to-slate-600'
  }
}

const getServiceIcon = (iconName) => {
  const icons = { Smartphone, Battery, Timer, Grid }
  return icons[iconName] || Smartphone
}
</script>

<style scoped>
.animate-reveal {
  animation: reveal 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes reveal {
  from { opacity: 0; transform: translateY(30px) scale(0.98); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
</style>
