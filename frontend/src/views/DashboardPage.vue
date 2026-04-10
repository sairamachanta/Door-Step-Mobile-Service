<template>
  <BaseLayout>
    <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50/30 pb-20 md:pb-8">
      <!-- Enhanced Header -->
      <header class="bg-white/80 backdrop-blur-xl px-4 py-4 md:px-6 md:py-6 border-b border-gray-100 sticky top-0 z-20 shadow-sm">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl md:text-3xl font-black text-slate-900 tracking-tight bg-gradient-to-r from-primary-700 to-blue-600 bg-clip-text text-transparent">
              Dashboard
            </h1>
            <p class="text-[11px] md:text-sm text-slate-600 font-medium mt-0.5 md:mt-1">
              Welcome back, <span class="font-bold text-primary-700">{{ authStore.user?.full_name?.split(' ')[0] || 'User' }}</span>! ✨
            </p>
          </div>
          <div class="flex items-center gap-2 md:gap-3">
            <button @click="handleRetry" class="p-2 md:p-2.5 bg-blue-50 rounded-xl text-blue-600 hover:bg-blue-100 transition-colors" title="Refresh Data">
              <RefreshCw :class="['w-4 h-4 md:w-5 md:h-5', loading.stats ? 'animate-spin' : '']" />
            </button>
            <!-- Mobile Only Logout -->
            <button @click="authStore.logout()" class="md:hidden p-2 bg-slate-100 rounded-xl text-slate-600 hover:bg-slate-200 transition-colors">
              <LogOut class="w-4 h-4" />
            </button>
          </div>
        </div>
      </header>

      <main class="p-4 md:p-6 space-y-6 md:space-y-8 animate-reveal max-w-7xl mx-auto">
        <!-- Quick Stats with Loading States -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
          <div v-for="stat in stats" :key="stat.label" 
            class="bg-white p-4 md:p-6 rounded-2xl md:rounded-3xl border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1 cursor-pointer group">
            <div class="flex items-start justify-between mb-2 md:mb-3">
              <div :class="['w-10 h-10 md:w-12 md:h-12 rounded-xl md:rounded-2xl flex items-center justify-center transition-transform group-hover:scale-110', stat.bgColor]">
                <component :is="stat.icon" :class="['w-5 h-5 md:w-6 md:h-6', stat.iconColor]" />
              </div>
              <ChevronRight class="w-3 h-3 md:w-4 md:h-4 text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
            <div>
              <p class="text-[9px] md:text-[10px] font-black uppercase tracking-widest text-slate-400 mb-0.5 md:mb-1">{{ stat.label }}</p>
              <p class="text-lg md:text-2xl font-black text-slate-900">{{ stat.value }}</p>
            </div>
          </div>
        </div>

        <!-- Active Booking or Empty State -->
        <div v-if="activeBooking" class="relative overflow-hidden bg-gradient-to-br from-primary-700 to-blue-600 rounded-3xl md:rounded-[2.5rem] p-6 md:p-8 text-white shadow-2xl">
          <div class="absolute top-0 right-0 w-64 h-64 md:w-96 md:h-96 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
          <div class="absolute bottom-0 left-0 w-48 h-48 md:w-64 md:h-64 bg-black/10 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2"></div>
          
          <div class="relative z-10 space-y-4 md:space-y-6">
            <div class="flex items-center justify-between">
              <span class="px-3 py-1 md:px-4 md:py-1.5 bg-white/20 backdrop-blur-md rounded-full text-[10px] md:text-xs font-bold uppercase tracking-widest flex items-center gap-1.5 md:gap-2">
                <span class="w-1.5 h-1.5 md:w-2 md:h-2 bg-green-400 rounded-full animate-pulse"></span>
                Active Request
              </span>
              <span class="text-blue-100 text-xs md:text-sm font-bold">{{ activeBooking.date }}</span>
            </div>
            
            <div>
              <h3 class="text-2xl md:text-3xl font-black mb-1 md:mb-2 leading-tight">{{ activeBooking.service }}</h3>
              <p class="text-blue-100 text-sm md:text-base font-medium flex items-center gap-2">
                <User class="w-3.5 h-3.5 md:w-4 md:h-4" />
                Technician: {{ activeBooking.technician }}
              </p>
            </div>
            
            <div class="space-y-1.5 md:space-y-2">
              <div class="flex items-center justify-between text-[11px] md:text-sm">
                <span class="font-medium text-blue-100">Progress</span>
                <span class="font-black">60%</span>
              </div>
              <div class="flex items-center gap-4">
                <div class="flex-grow h-2 md:h-3 bg-white/20 rounded-full overflow-hidden backdrop-blur-sm">
                  <div class="w-3/5 h-full bg-gradient-to-r from-white to-blue-100 rounded-full shadow-lg"></div>
                </div>
              </div>
            </div>
            
            <div class="flex flex-col sm:flex-row gap-3">
              <button class="flex-1 py-2.5 md:py-3.5 bg-white text-primary-700 rounded-xl md:rounded-2xl font-black text-[11px] md:text-sm hover:bg-blue-50 transition-all hover:scale-105 shadow-lg">
                Track Status
              </button>
              <button class="flex-1 py-2.5 md:py-3.5 bg-white/10 backdrop-blur-md text-white border-2 border-white/30 rounded-xl md:rounded-2xl font-black text-[11px] md:text-sm hover:bg-white/20 transition-all">
                Contact Tech
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State for No Active Booking -->
        <div v-else class="relative overflow-hidden bg-gradient-to-br from-slate-100 to-slate-50 rounded-[2.5rem] p-12 text-center border-2 border-dashed border-slate-300">
          <div class="max-w-md mx-auto space-y-4">
            <div class="w-20 h-20 bg-slate-200 rounded-full flex items-center justify-center mx-auto">
              <Calendar class="w-10 h-10 text-slate-400" />
            </div>
            <div>
              <h3 class="text-xl font-black text-slate-700 mb-2">No Active Bookings</h3>
              <p class="text-slate-500 font-medium">Book a service to get started with expert repairs at your doorstep!</p>
            </div>
            <button @click="router.push('/services')" class="inline-flex items-center gap-2 px-6 py-3 bg-primary-700 text-white rounded-2xl font-bold hover:bg-primary-800 transition-all hover:scale-105 shadow-lg">
              <Smartphone class="w-5 h-5" />
              Book a Service
            </button>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="space-y-5">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-black text-slate-900 tracking-tight">Quick Book</h3>
            <router-link to="/services" class="text-sm font-bold text-primary-700 hover:text-primary-800 flex items-center gap-1">
              View All
              <ChevronRight class="w-4 h-4" />
            </router-link>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 md:gap-4">
            <button v-for="cat in quickCategories" :key="cat.name" 
              @click="router.push('/services')"
              class="flex flex-col items-center gap-2 md:gap-3 p-3 md:p-4 bg-white rounded-2xl border border-gray-100 hover:border-primary-200 hover:shadow-lg transition-all group hover:-translate-y-1">
              <div :class="['w-12 h-12 md:w-16 md:h-16 rounded-xl md:rounded-2xl flex items-center justify-center transition-all group-hover:scale-110', cat.bgColor]">
                <component :is="cat.icon" :class="['w-6 md:w-8 h-6 md:h-8', cat.iconColor]" />
              </div>
              <span class="text-[10px] md:text-xs font-bold text-slate-700 group-hover:text-primary-700 transition-colors uppercase tracking-wider">{{ cat.name }}</span>
            </button>
          </div>
        </div>

        <!-- Recent Activity with Better UX -->
        <div class="space-y-5">
          <div class="flex items-center justify-between">
            <h3 class="text-xl font-black text-slate-900 tracking-tight">Recent Activity</h3>
            <button @click="router.push('/bookings')" class="text-sm font-bold text-primary-700 hover:text-primary-800 flex items-center gap-1">
              View All
              <ChevronRight class="w-4 h-4" />
            </button>
          </div>
          
          <!-- Empty State -->
          <div v-if="recentActivity.length === 0" class="bg-white rounded-2xl p-12 text-center border border-gray-100">
            <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Clock class="w-8 h-8 text-slate-400" />
            </div>
            <h4 class="text-lg font-bold text-slate-700 mb-2">No Activity Yet</h4>
            <p class="text-slate-500 text-sm">Your booking history will appear here</p>
          </div>

          <!-- Activity List -->
          <div v-else class="space-y-3">
            <div v-for="activity in recentActivity" :key="activity.id" 
              class="flex items-center gap-4 p-5 bg-white rounded-2xl border border-gray-100 hover:border-primary-200 hover:shadow-md transition-all cursor-pointer group">
              <div :class="['w-14 h-14 rounded-2xl flex items-center justify-center flex-shrink-0 transition-transform group-hover:scale-110',
                activity.status === 'Completed' ? 'bg-emerald-50' : 'bg-orange-50']">
                <CheckCircle2 v-if="activity.status === 'Completed'" class="w-7 h-7 text-emerald-500" />
                <Clock v-else class="w-7 h-7 text-orange-500" />
              </div>
              <div class="flex-grow min-w-0">
                <h4 class="text-base font-bold text-slate-900 truncate group-hover:text-primary-700 transition-colors">{{ activity.title }}</h4>
                <p class="text-sm text-slate-500 font-medium mt-0.5">{{ activity.time }}</p>
              </div>
              <div class="flex items-center gap-3">
                <span :class="['text-xs font-black px-3 py-1.5 rounded-xl uppercase tracking-wider', 
                  activity.status === 'Completed' ? 'bg-emerald-50 text-emerald-600' : 'bg-orange-50 text-orange-600']">
                  {{ activity.status }}
                </span>
                <ChevronRight class="w-5 h-5 text-slate-400 opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
            </div>
          </div>
        </div>

        <!-- Call to Action Banner -->
        <div class="bg-gradient-to-r from-primary-700 to-blue-600 rounded-3xl p-8 text-white relative overflow-hidden">
          <div class="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl"></div>
          <div class="relative z-10 flex items-center justify-between">
            <div class="space-y-2">
              <h3 class="text-2xl font-black">Need Help?</h3>
              <p class="text-blue-100 font-medium">Our support team is available 24/7</p>
            </div>
            <a href="https://wa.me/919390999539" target="_blank" 
              class="px-6 py-3 bg-white text-primary-700 rounded-2xl font-black hover:bg-blue-50 transition-all hover:scale-105 shadow-lg flex items-center gap-2">
              <MessageCircle class="w-5 h-5" />
              Contact Us
            </a>
          </div>
        </div>
      </main>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useDashboard } from '../composables/useDashboard'
import BaseLayout from '../components/BaseLayout.vue'
import { 
  LogOut, LayoutGrid, Calendar, Wallet, Star,
  Smartphone, Battery, Cpu, Zap, Clock, CheckCircle2, ChevronRight,
  RefreshCw, AlertCircle, User, MessageCircle
} from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()

// Use dashboard composable for dynamic data
const {
  stats: apiStats,
  activeBooking: apiActiveBooking,
  recentBookings: apiRecentBookings,
  quickActions: apiQuickActions,
  loading,
  error,
  fetchAll,
  retry
} = useDashboard()

// Icon mapping for dynamic category icons
const iconMap = {
  Smartphone,
  Battery,
  Cpu,
  Zap,
  Calendar,
  Wallet,
  Star,
  LayoutGrid
}

const getIcon = (name) => iconMap[name] || Smartphone

// Computed properties to use API data
const stats = computed(() => {
  return [
    { label: 'Total Bookings', value: String(apiStats.value?.total_bookings || '0'), icon: LayoutGrid, bgColor: 'bg-blue-50', iconColor: 'text-blue-600' },
    { label: 'Scheduled', value: String(apiStats.value?.scheduled_bookings || '0'), icon: Calendar, bgColor: 'bg-emerald-50', iconColor: 'text-emerald-600' },
    { label: 'Credits', value: `₹${apiStats.value?.wallet_balance || '0'}`, icon: Wallet, bgColor: 'bg-amber-50', iconColor: 'text-amber-600' },
    { label: 'Reward Points', value: String(apiStats.value?.loyalty_points || '0'), icon: Star, bgColor: 'bg-rose-50', iconColor: 'text-rose-600' }
  ]
})

const activeBooking = computed(() => apiActiveBooking.value || null)
const recentActivity = computed(() => apiRecentBookings.value || [])
const quickCategories = computed(() => {
    return (apiQuickActions.value?.quick_actions || apiQuickActions.value || []).map(action => ({
        name: action.name,
        icon: getIcon(action.icon),
        bgColor: 'bg-blue-50', // Default style
        iconColor: 'text-blue-600',
        id: action.id
    }))
})

// Fetch data on mount
onMounted(async () => {
    // Redirect non-customers to their role-specific dashboard
    if (authStore.userRole && authStore.userRole !== 'customer') {
        const { getRoleDashboard } = await import('../router')
        router.replace(getRoleDashboard(authStore.userRole))
        return
    }
    await fetchAll()
})

const handleRetry = () => {
  fetchAll()
}
</script>

<style scoped>
.shadow-premium {
  box-shadow: 0 20px 40px -15px rgba(30, 64, 175, 0.3);
}

.animate-reveal {
  animation: reveal 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes reveal {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
