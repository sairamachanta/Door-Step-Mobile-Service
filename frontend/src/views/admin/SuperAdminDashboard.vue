<template>
  <BaseLayout>
    <div class="min-h-screen bg-slate-950 text-white p-6 md:p-12">
      <header class="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-12">
        <div class="space-y-2">
          <div class="inline-flex items-center gap-2 px-3 py-1 bg-primary-500/10 border border-primary-500/20 rounded-full">
            <ShieldCheck class="w-4 h-4 text-primary-400" />
            <span class="text-[10px] font-black uppercase tracking-widest text-primary-400">System Administrator</span>
          </div>
          <h1 class="text-4xl md:text-5xl font-black tracking-tight leading-tight">
            SuperAdmin <span class="text-grad-primary">Control Center</span>
          </h1>
          <p class="text-slate-400 font-medium">Global oversight and system-level configurations.</p>
        </div>
        
        <div class="flex items-center gap-4">
          <button @click="fetchUsers" class="btn btn-secondary !bg-slate-900 border-slate-800 flex items-center gap-2">
            <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': loading }" />
            Sync Data
          </button>
        </div>
      </header>

      <!-- Global Stats -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div v-for="stat in globalStats" :key="stat.label" class="bg-slate-900/50 backdrop-blur-xl border border-white/5 p-8 rounded-[2.5rem] space-y-4">
          <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center', stat.bgColor]">
            <component :is="stat.icon" class="w-6 h-6 text-white" />
          </div>
          <div>
            <p class="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-1">{{ stat.label }}</p>
            <p class="text-3xl font-black">{{ stat.value }}</p>
          </div>
        </div>
      </div>

      <!-- User Management Table (Placeholder) -->
      <section class="bg-slate-900/30 border border-white/5 rounded-[3rem] overflow-hidden">
        <div class="p-8 border-b border-white/5 flex items-center justify-between">
          <h3 class="text-xl font-bold">User Management</h3>
          <div class="flex items-center gap-4">
             <div class="relative">
                <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <input type="text" placeholder="Search users..." class="bg-slate-800/50 border border-white/10 rounded-xl pl-10 pr-4 py-2 text-sm focus:outline-none focus:border-primary-500 w-64" />
             </div>
          </div>
        </div>
        
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="text-[10px] font-black uppercase tracking-widest text-slate-500 border-b border-white/5">
                <th class="p-8">User Info</th>
                <th class="p-8">Account Role</th>
                <th class="p-8">Status</th>
                <th class="p-8">Joined Date</th>
                <th class="p-8 text-right">Actions</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-white/5">
              <tr v-for="user in users" :key="user.id" class="hover:bg-white/5 transition-colors group">
                <td class="p-8">
                  <div class="flex items-center gap-4">
                    <div class="w-10 h-10 rounded-xl bg-slate-800 flex items-center justify-center font-bold text-primary-400">
                      {{ user.full_name[0] }}
                    </div>
                    <div>
                      <p class="font-bold">{{ user.full_name }}</p>
                      <p class="text-xs text-slate-500">{{ user.phone }}</p>
                    </div>
                  </div>
                </td>
                <td class="p-8">
                  <span :class="['px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-widest border', getRoleClasses(user.role)]">
                    {{ user.role === 'admin' ? 'Technician' : user.role }}
                  </span>
                </td>
                <td class="p-8">
                  <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                    <span class="text-sm font-medium text-slate-300">Active</span>
                  </div>
                </td>
                <td class="p-8 text-sm text-slate-400">
                  {{ new Date(user.created_at).toLocaleDateString() }}
                </td>
                <td class="p-8 text-right">
                  <button class="p-2 hover:bg-white/10 rounded-lg transition-colors">
                    <MoreVertical class="w-5 h-5 text-slate-500" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BaseLayout from '../../components/BaseLayout.vue'
import api from '../../services/api'
import { 
  ShieldCheck, Users, Smartphone, BarChart3, RefreshCw, 
  Search, MoreVertical, ShieldAlert, Cpu
} from 'lucide-vue-next'

const users = ref([])
const loading = ref(false)
const globalStats = ref([
  { label: 'Total Users', value: '450+', icon: Users, bgColor: 'bg-blue-600 shadow-lg shadow-blue-600/20' },
  { label: 'Active Repairs', value: '82', icon: Cpu, bgColor: 'bg-primary-600 shadow-lg shadow-primary-600/20' },
  { label: 'Revenue (MTD)', value: '₹4.2L', icon: BarChart3, bgColor: 'bg-emerald-600 shadow-lg shadow-emerald-600/20' }
])

const fetchUsers = async () => {
    loading.value = true
    try {
        const response = await api.get('/admin/users')
        users.value = response.data
    } catch (e) {
        console.error("Failed to fetch users", e)
    } finally {
        loading.value = false
    }
}

const getRoleClasses = (role) => {
    switch (role) {
        case 'superadmin': return 'text-rose-400 border-rose-400/20 bg-rose-400/5'
        case 'admin': return 'text-amber-400 border-amber-400/20 bg-amber-400/5'
        default: return 'text-blue-400 border-blue-400/20 bg-blue-400/5'
    }
}

onMounted(fetchUsers)
</script>

<style scoped>
.text-grad-primary {
  background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
</style>
