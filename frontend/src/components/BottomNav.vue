<template>
  <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 safe-bottom z-50 shadow-lg md:hidden">
    <div class="flex items-center justify-around h-[60px] px-2">
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="flex flex-col items-center justify-center flex-1 relative touch-target transition-all duration-200 active:scale-95"
        :class="isActive(item.path) ? 'text-primary-500' : 'text-gray-500'"
      >
        <!-- Active Indicator -->
        <div 
          v-if="isActive(item.path)" 
          class="absolute top-0 left-1/2 -translate-x-1/2 w-8 h-0.5 bg-primary-500 rounded-full"
        ></div>
        
        <!-- Icon with Badge -->
        <div class="relative">
          <component 
            :is="item.icon" 
            :class="isActive(item.path) ? 'text-primary-500' : 'text-gray-500'"
            class="w-6 h-6 transition-colors duration-200"
          />
          
          <!-- Notification Dot (Profile) -->
          <span 
            v-if="item.badge === 'dot'" 
            class="absolute -top-0.5 -right-0.5 w-2 h-2 bg-error rounded-full"
          ></span>
          
          <!-- Number Badge (Bookings) -->
          <span 
            v-if="typeof item.badge === 'number'" 
            class="absolute -top-1 -right-2 min-w-[18px] h-[18px] bg-primary-500 text-white text-[10px] font-semibold rounded-full flex items-center justify-center px-1"
          >
            {{ item.badge }}
          </span>
        </div>
        
        <!-- Label -->
        <span 
          class="text-xs mt-1 transition-all duration-200"
          :class="isActive(item.path) ? 'font-semibold text-primary-500' : 'font-medium text-gray-500'"
        >
          {{ item.label }}
        </span>
      </router-link>
    </div>
  </nav>

  <!-- Desktop Sidebar (hidden on mobile) -->
  <aside class="hidden md:flex md:flex-col md:fixed md:left-0 md:top-0 md:bottom-0 md:w-64 bg-white border-r border-gray-200 z-50">
    <div class="p-6 border-b border-gray-200">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-lg bg-primary-500 flex items-center justify-center text-white font-bold text-lg shadow-md">
          D
        </div>
        <span class="font-bold text-xl text-gray-900">Doorstep</span>
      </div>
    </div>

    <nav class="flex-1 p-4 space-y-1">
      <router-link
        v-for="item in navItems"
        :key="item.path"
        :to="item.path"
        class="flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 relative group"
        :class="isActive(item.path) 
          ? 'bg-primary-50 text-primary-600' 
          : 'text-gray-600 hover:bg-gray-50'"
      >
        <component 
          :is="item.icon" 
          class="w-5 h-5 transition-colors"
        />
        <span class="font-medium text-sm">{{ item.label }}</span>
        
        <!-- Badge for desktop -->
        <span 
          v-if="typeof item.badge === 'number'" 
          class="ml-auto min-w-[20px] h-5 bg-primary-500 text-white text-xs font-semibold rounded-full flex items-center justify-center px-1.5"
        >
          {{ item.badge }}
        </span>
        
        <span 
          v-if="item.badge === 'dot'" 
          class="ml-auto w-2 h-2 bg-error rounded-full"
        ></span>
      </router-link>
    </nav>

    <!-- Redesigned Sidebar Footer (Profile & Logout) -->
    <div class="mt-auto border-t border-gray-100 p-4">
      <div 
        @click="handleLogout" 
        class="flex items-center justify-between p-2 rounded-2xl cursor-pointer hover:bg-slate-50 transition-all group border border-transparent hover:border-slate-100"
      >
        <div class="flex items-center gap-3">
          <!-- Avatar -->
          <div class="w-10 h-10 rounded-xl bg-indigo-50 border border-indigo-100 flex items-center justify-center text-indigo-600 font-bold text-lg shadow-sm group-hover:scale-105 transition-transform">
            {{ authStore.user?.full_name?.charAt(0).toUpperCase() || 'S' }}
          </div>
          
          <!-- Details -->
          <div class="flex flex-col min-w-0">
            <h4 class="text-sm font-bold text-slate-900 truncate w-32">
              {{ authStore.user?.full_name || 'My Account' }}
            </h4>
            <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest leading-none mt-1">
              {{ authStore.user?.subscription_tier || 'Member' }}
            </p>
          </div>
        </div>

        <!-- Logout Icon -->
        <div class="flex items-center justify-center p-2 rounded-lg text-slate-400 group-hover:text-red-600 group-hover:bg-red-50 transition-all">
          <LogOut class="w-4 h-4" />
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { Home, Grid, ClipboardList, Crown, User, LogOut, Wrench, Users, CalendarCheck, LayoutDashboard } from 'lucide-vue-next'
import { useAuthStore } from '../stores/auth'
import { useDashboard } from '../composables/useDashboard'

const route = useRoute()
const authStore = useAuthStore()
const { stats, fetchAll } = useDashboard()

// Update data every 30s to keep badge fresh
let pollingInterval
onMounted(async () => {
  await fetchAll()
  pollingInterval = setInterval(fetchAll, 30000)
})

onUnmounted(() => {
  if (pollingInterval) clearInterval(pollingInterval)
})

const navItems = computed(() => {
  const role = authStore.userRole

  // --- Admin (superadmin tier) ---
  if (role === 'admin') {
    return [
      { path: '/admin/dashboard', label: 'Dashboard', icon: LayoutDashboard, badge: null },
      { path: '/admin/dashboard#technicians', label: 'Technicians', icon: Wrench, badge: null },
      { path: '/admin/dashboard#bookings', label: 'Bookings', icon: CalendarCheck, badge: null },
      { path: '/admin/dashboard#customers', label: 'Customers', icon: Users, badge: null },
      { path: '/profile', label: 'Profile', icon: User, badge: null },
    ]
  }

  // --- Technician ---
  if (role === 'technician') {
    return [
      { path: '/technician/dashboard', label: 'My Jobs', icon: ClipboardList, badge: null },
      { path: '/profile', label: 'Profile', icon: User, badge: null },
    ]
  }

  // --- Customer (default) ---
  return [
    { path: '/home', label: 'Home', icon: Home, badge: null },
    { path: '/services', label: 'Services', icon: Grid, badge: null },
    { path: '/bookings', label: 'Bookings', icon: ClipboardList, badge: stats.value?.scheduled_bookings || null },
    { path: '/subscriptions', label: 'Plans', icon: Crown, badge: null },
    { path: '/profile', label: 'Profile', icon: User, badge: null },
  ]
})

const isActive = (path) => {
  return route.path === path || route.path.startsWith(path + '/')
}

const handleLogout = () => {
  authStore.logout()
}
</script>

<style scoped>
/* Ensure smooth transitions */
a {
  -webkit-tap-highlight-color: transparent;
}
</style>
