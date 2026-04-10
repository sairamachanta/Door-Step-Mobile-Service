<template>
  <BaseLayout>
    <div class="min-h-screen bg-slate-50 pb-24 md:pb-8 transition-colors duration-300">
      <!-- Header -->
      <header class="bg-white border-b border-slate-200 px-6 py-6 sticky top-0 z-30">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 class="text-2xl font-black text-slate-900">Admin <span class="text-primary-600">Portal</span></h1>
            <p class="text-slate-500 text-sm font-medium">Manage Staff, Customers & Operations</p>
          </div>
          <div class="flex items-center gap-3">
            <div class="px-4 py-2 bg-emerald-50 text-emerald-700 rounded-xl border border-emerald-100 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span class="text-xs font-black uppercase tracking-widest">System Live</span>
            </div>
            <button @click="refreshData" :disabled="loading.stats" class="p-2 bg-slate-100 text-slate-600 rounded-xl hover:bg-slate-200 transition-colors">
              <RefreshCw class="w-5 h-5" :class="{ 'animate-spin': loading.stats }" />
            </button>
          </div>
        </div>
      </header>

      <main class="max-w-7xl mx-auto p-4 md:p-8 space-y-8">
        <!-- Dashboard Summary Overview (Total Stats) -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
          <div v-for="s in statCards" :key="s.label" class="bg-white p-6 rounded-[24px] border border-slate-100 shadow-sm hover:shadow-md transition-all duration-300 group">
            <div class="flex items-center justify-between mb-4">
              <div :class="['w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-300 group-hover:scale-110', s.color]">
                <component :is="s.icon" class="w-6 h-6" />
              </div>
              <div class="text-[10px] font-black uppercase tracking-widest text-slate-400 bg-slate-50 px-2 py-1 rounded-lg">Real-time</div>
            </div>
            <div>
              <p class="text-xs font-bold text-slate-500 mb-1">{{ s.label }}</p>
              <p class="text-3xl font-black text-slate-900 tracking-tight">{{ loading.stats ? '…' : s.value }}</p>
            </div>
          </div>
        </div>

        <!-- Section Navigation Tabs -->
        <div class="flex gap-4 border-b border-slate-200 overflow-x-auto pb-0.5 no-scrollbar">
          <button
            v-for="tab in tabs"
            :key="tab.key"
            @click="activeTab = tab.key"
            :class="[
              'px-6 py-4 text-sm font-black transition-all border-b-4 -mb-[2px] whitespace-nowrap uppercase tracking-widest flex items-center gap-2',
              activeTab === tab.key
                ? 'border-primary-600 text-primary-600'
                : 'border-transparent text-slate-400 hover:text-slate-600'
            ]"
          >
            <Users v-if="tab.key === 'users'" class="w-4 h-4" />
            <Wrench v-if="tab.key === 'technicians'" class="w-4 h-4" />
            <ShieldCheck v-if="tab.key === 'admins'" class="w-4 h-4" />
            <CalendarCheck v-if="tab.key === 'bookings'" class="w-4 h-4" />
            {{ tab.label }}
          </button>
        </div>

        <!-- Dynamic Content Area -->
        <transition name="fade" mode="out-in">
          <div :key="activeTab" class="space-y-6">
            
            <!-- Users / Techs / Admins Management (Shared Table Layout) -->
            <div v-if="['users', 'technicians', 'admins'].includes(activeTab)" class="space-y-6">
              
              <!-- Context Summary & Action Bar -->
              <div class="flex flex-col xl:flex-row justify-between gap-6">
                <!-- Inline Summary Cards -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 flex-1">
                  <div class="bg-white px-4 py-5 rounded-[20px] border border-slate-100 shadow-sm flex items-center gap-4">
                      <div class="w-10 h-10 rounded-2xl bg-primary-50 text-primary-600 flex items-center justify-center shrink-0">
                        <Users v-if="activeTab === 'users'" class="w-5 h-5" />
                        <Wrench v-else-if="activeTab === 'technicians'" class="w-5 h-5" />
                        <ShieldCheck v-else class="w-5 h-5" />
                      </div>
                      <div>
                        <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Active {{ activeTab.slice(0,-1) }}</p>
                        <p class="text-xl font-black text-slate-900 leading-none mt-1">{{ stats?.[`total_${activeTab === 'users' ? 'customers' : activeTab}`] || 0 }}</p>
                      </div>
                  </div>
                  <div class="bg-white px-4 py-5 rounded-[20px] border border-slate-100 shadow-sm flex items-center gap-4">
                      <div class="w-10 h-10 rounded-2xl bg-red-50 text-red-600 flex items-center justify-center shrink-0">
                        <UserX class="w-5 h-5" />
                      </div>
                      <div>
                        <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Suspended</p>
                        <p class="text-xl font-black text-slate-900 leading-none mt-1">{{ stats?.[`suspended_${activeTab === 'users' ? 'users' : activeTab}`] || 0 }}</p>
                      </div>
                  </div>
                </div>

                <!-- Search & Controls -->
                <div class="flex flex-wrap items-center gap-3 xl:justify-end flex-1">
                  <div class="relative w-full sm:w-80 group">
                    <Search class="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 group-focus-within:text-primary-500 transition-colors" />
                    <input 
                      v-model="searchModel" 
                      @input="debouncedFetch"
                      :placeholder="`Search ${activeTab}…`" 
                      class="w-full bg-white border border-slate-200 rounded-2xl pl-11 pr-4 py-3 text-sm font-bold focus:ring-4 focus:ring-primary-500/10 focus:border-primary-500 transition-all outline-none"
                    />
                  </div>
                  <button @click="showAddStaff = true" class="flex items-center gap-2 px-6 py-3 bg-primary-600 text-white rounded-2xl text-xs font-black uppercase tracking-widest hover:bg-primary-700 transition-all shadow-lg shadow-primary-600/20 active:scale-95">
                    <Plus class="w-4 h-4" /> Add {{ activeTab.slice(0,-1) }}
                  </button>
                </div>
              </div>

              <!-- Premium Table Container -->
              <div class="bg-white rounded-[32px] border border-slate-200 shadow-sm overflow-hidden min-h-[400px]">
                <div class="overflow-x-auto">
                  <table class="w-full text-left border-collapse">
                    <thead>
                      <tr class="bg-slate-50/50 border-b border-slate-100">
                        <th class="px-8 py-5 text-[10px] font-black text-slate-400 uppercase tracking-widest">User Details</th>
                        <th class="px-6 py-5 text-[10px] font-black text-slate-400 uppercase tracking-widest">Phone Number</th>
                        <th class="px-6 py-5 text-[10px] font-black text-slate-400 uppercase tracking-widest">Account Status</th>
                        <th class="px-6 py-5 text-[10px] font-black text-slate-400 uppercase tracking-widest">Registered Date</th>
                        <th class="px-8 py-5 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Action</th>
                      </tr>
                    </thead>
                    <tbody v-if="!loadingTab" class="divide-y divide-slate-100">
                      <tr v-for="user in currentList" :key="user.id" class="hover:bg-slate-50/50 transition-colors group">
                        <td class="px-8 py-6">
                          <div class="flex items-center gap-4">
                            <div class="w-12 h-12 rounded-2xl bg-slate-100 flex items-center justify-center font-black text-slate-400 text-lg group-hover:bg-primary-50 group-hover:text-primary-600 transition-colors">
                              {{ user.full_name?.[0]?.toUpperCase() }}
                            </div>
                            <div>
                              <p class="font-black text-slate-900 group-hover:text-primary-700 transition-colors leading-tight">{{ user.full_name }}</p>
                              <p class="text-xs text-slate-400 font-medium mt-0.5">{{ user.email || 'no-email@registered.com' }}</p>
                            </div>
                          </div>
                        </td>
                        <td class="px-6 py-6">
                          <span class="text-sm font-black text-slate-600 tabular-nums">{{ user.phone }}</span>
                        </td>
                        <td class="px-6 py-6">
                          <div class="flex items-center gap-2">
                              <span :class="[
                                'px-3 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-tighter flex items-center gap-1.5',
                                user.status === 'active' ? 'bg-emerald-50 text-emerald-600 border border-emerald-100' : 'bg-red-50 text-red-600 border border-red-100'
                              ]">
                                <span :class="['w-1.5 h-1.5 rounded-full', user.status === 'active' ? 'bg-emerald-500' : 'bg-red-500']"></span>
                                {{ user.status }}
                              </span>
                              <span v-if="user.is_phone_verified" class="px-3 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-tighter bg-blue-50 text-blue-600 border border-blue-100 flex items-center gap-1.5">
                                <ShieldCheck class="w-3 h-3" /> VERIFIED
                              </span>
                          </div>
                        </td>
                        <td class="px-6 py-6">
                          <p class="text-sm font-bold text-slate-500 tabular-nums">{{ formatDate(user.created_at) }}</p>
                        </td>
                        <td class="px-8 py-6">
                            <div class="flex items-center justify-end gap-2">
                              <select :value="user.role" @change="(e) => changeUserRole(user, e.target.value)" class="text-[10px] bg-slate-100 border-none rounded-xl px-3 py-2 font-black uppercase tracking-widest text-slate-600 focus:ring-0 cursor-pointer hover:bg-slate-200 transition-colors">
                                  <option v-for="r in metadataStore.getOptions('USER_ROLE')" :key="r.code" :value="r.code">{{ r.label }}</option>
                              </select>
                              <button @click="toggleStatus(user)" 
                                      :title="user.status === 'active' ? 'Suspend Account' : 'Reactivate Account'"
                                      :class="['p-2 rounded-xl transition-all', user.status === 'active' ? 'text-red-400 hover:bg-red-50 hover:text-red-600' : 'text-emerald-400 hover:bg-emerald-50 hover:text-emerald-600']">
                                  <UserX v-if="user.status === 'active'" class="w-5 h-5" />
                                  <ShieldCheck v-else class="w-5 h-5" />
                              </button>
                              <button @click="deleteUser(user)" class="p-2 rounded-xl text-slate-400 hover:bg-red-50 hover:text-red-600 transition-all">
                                  <Trash2 class="w-5 h-5" />
                              </button>
                            </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>

                  <!-- Table Loading / Empty State -->
                  <div v-if="loadingTab" class="flex flex-col items-center justify-center py-24 gap-4">
                      <Loader2 class="w-12 h-12 animate-spin text-primary-500" />
                      <p class="text-xs font-black uppercase tracking-[0.2em] text-slate-400">Synchronizing Data…</p>
                  </div>
                  <div v-if="!loadingTab && currentList.length === 0" class="flex flex-col items-center justify-center py-24 gap-4">
                      <div class="w-16 h-16 rounded-3xl bg-slate-50 flex items-center justify-center">
                        <Users class="w-8 h-8 text-slate-200" />
                      </div>
                      <p class="text-sm font-black text-slate-400 uppercase tracking-widest">No matching records found.</p>
                  </div>
                </div>

                <!-- Pagination Bar -->
                <div v-if="currentPagination.total_pages > 1" class="px-8 py-6 bg-slate-50/50 border-t border-slate-100 flex items-center justify-between">
                    <button 
                      @click="fetchCurrent(currentPage - 1)" 
                      :disabled="currentPage === 1"
                      class="flex items-center gap-2 px-4 py-2 rounded-xl border border-slate-200 bg-white text-xs font-black uppercase tracking-widest text-slate-600 hover:bg-slate-50 disabled:opacity-30 transition-all"
                    >
                      Previous
                    </button>
                    <div class="flex items-center gap-2">
                      <button 
                        v-for="p in currentPagination.total_pages" 
                        :key="p" 
                        @click="fetchCurrent(p)"
                        :class="['w-10 h-10 rounded-xl text-xs font-black transition-all', currentPage === p ? 'bg-primary-600 text-white shadow-lg' : 'text-slate-400 hover:bg-white hover:text-slate-900 border border-transparent hover:border-slate-200']"
                      >
                        {{ p }}
                      </button>
                    </div>
                    <button 
                      @click="fetchCurrent(currentPage + 1)" 
                      :disabled="currentPage === currentPagination.total_pages"
                      class="flex items-center gap-2 px-4 py-2 rounded-xl border border-slate-200 bg-white text-xs font-black uppercase tracking-widest text-slate-600 hover:bg-slate-50 disabled:opacity-30 transition-all"
                    >
                      Next
                    </button>
                </div>
              </div>
            </div>

            <!-- Tab: Bookings -->
            <div v-if="activeTab === 'bookings'" class="space-y-4">
              <div class="flex flex-col sm:flex-row justify-between gap-3 items-start sm:items-center">
                <h2 class="text-xl font-black text-slate-900">Operational Oversight</h2>
                <select v-model="bookingStatusFilter" @change="fetchBookings(1)" class="text-sm border border-slate-200 rounded-xl px-3 py-2 font-medium">
                  <option value="">All Statuses</option>
                  <option v-for="s in bookingStatuses" :key="s.value" :value="s.value">{{ s.label }}</option>
                </select>
              </div>

              <div v-if="loading.bookings" class="flex justify-center py-12">
                <Loader2 class="w-8 h-8 animate-spin text-primary-500" />
              </div>

              <div v-else-if="bookings.length === 0" class="text-center py-12 text-slate-400 font-medium">No records matched your criteria.</div>

              <div v-else class="space-y-3">
                <div v-for="b in bookings" :key="b.id" class="bg-white rounded-2xl border border-slate-100 p-5 shadow-sm space-y-3 hover:border-primary-100 transition-all">
                  <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div>
                      <div class="flex items-center gap-2">
                        <p class="font-black text-slate-900">{{ b.booking_number }}</p>
                        <span :class="['px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-widest', statusClass(b.status)]">
                            {{ b.status }}
                        </span>
                      </div>
                      <p class="text-sm text-slate-600 font-bold mt-1">{{ b.service_name }} · {{ b.brand_name }} {{ b.model_name }}</p>
                    </div>
                    <div class="text-right">
                      <p class="font-black text-primary-700 text-lg">₹{{ b.final_price }}</p>
                      <p class="text-[10px] text-slate-400 font-bold uppercase tracking-widest">{{ b.preferred_date }} · {{ b.preferred_time_slot }}</p>
                    </div>
                  </div>
                  
                  <!-- Assign Technician -->
                  <div v-if="['pending','confirmed'].includes(b.status)" class="flex flex-col sm:flex-row gap-2 items-start sm:items-center border-t border-slate-50 pt-3">
                    <label class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Assign Technician</label>
                    <select v-model="assignMap[b.id]" class="text-sm border border-slate-200 rounded-xl px-3 py-1.5 font-medium flex-1 focus:ring-primary-500">
                      <option value="">-- Select Personnel --</option>
                      <option v-for="t in technicians.filter(s => s.status === 'active')" :key="t.id" :value="t.id">{{ t.full_name }}</option>
                    </select>
                    <button
                      @click="assignBooking(b.id)"
                      :disabled="!assignMap[b.id]"
                      class="px-4 py-1.5 bg-primary-600 text-white text-xs font-bold rounded-xl hover:bg-primary-700 disabled:opacity-40 transition-all shadow-md"
                    >Assign Now</button>
                  </div>
                  <div v-else-if="b.technician_id" class="border-t border-slate-50 pt-3 flex items-center justify-between">
                    <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Assigned Personnel</p>
                    <div class="flex items-center gap-2">
                        <Wrench class="w-3 h-3 text-primary-500" />
                        <span class="text-xs font-bold text-slate-700">{{ technicians.find(s => s.id === b.technician_id)?.full_name || 'Assigned Tech' }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Pagination -->
              <div v-if="bookingPagination.total_pages > 1" class="flex justify-center gap-2 pt-2">
                <button
                  v-for="p in bookingPagination.total_pages"
                  :key="p"
                  @click="fetchBookings(p)"
                  :class="['w-9 h-9 rounded-xl text-sm font-bold border transition-all', bookingPage === p ? 'bg-primary-600 text-white border-primary-600 shadow-lg' : 'text-slate-600 border-slate-200 hover:bg-slate-50']"
                >{{ p }}</button>
              </div>
            </div>
          </div>
        </transition>
      </main>
    </div>

    <!-- Add Staff Modal -->
    <div v-if="showAddStaff" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
      <div class="bg-white rounded-3xl p-8 shadow-2xl w-full max-w-md space-y-5 animate-in slide-in-from-bottom-4">
        <div class="flex justify-between items-center">
            <h2 class="text-xl font-black text-slate-900">Add Staff Member</h2>
            <button @click="showAddStaff = false" class="p-1 hover:bg-slate-100 rounded-full transition-colors"><Plus class="w-6 h-6 rotate-45 text-slate-400" /></button>
        </div>
        <div class="space-y-4">
          <div class="space-y-1">
              <label class="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-1">Assigned Role</label>
              <div class="flex gap-2">
                  <button v-for="r in ['admin', 'technician']" :key="r" @click="newStaff.role = r" 
                    :class="['flex-1 py-2 px-3 rounded-xl border text-xs font-bold uppercase tracking-widest transition-all', 
                    newStaff.role === r ? 'bg-primary-600 text-white border-primary-600 shadow-md' : 'bg-slate-50 text-slate-500 border-slate-200 hover:bg-slate-100']">
                    {{ r }}
                  </button>
              </div>
          </div>
          <input v-model="newStaff.full_name" placeholder="Full Legal Name" class="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:ring-2 focus:ring-primary-300 outline-none" />
          <input v-model="newStaff.phone" placeholder="Phone (Digits only)" type="tel" class="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:ring-2 focus:ring-primary-300 outline-none" />
          <input v-model="newStaff.password" type="password" placeholder="Secure Password" class="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm font-bold focus:ring-2 focus:ring-primary-300 outline-none" />
        </div>
        <p v-if="addStaffError" class="text-sm text-red-500 font-bold bg-red-50 p-3 rounded-xl border border-red-100">{{ addStaffError }}</p>
        <div class="pt-2">
          <button @click="createStaff" :disabled="loading.addStaff" class="w-full py-4 bg-primary-600 text-white rounded-2xl text-sm font-black uppercase tracking-widest hover:bg-primary-700 disabled:opacity-50 transition-all shadow-xl">
            {{ loading.addStaff ? 'Authorizing…' : 'Finalize Addition' }}
          </button>
        </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, computed, onMounted, reactive, watch } from 'vue'
import BaseLayout from '../../components/BaseLayout.vue'
import adminService from '../../services/adminService'
import { useMetadataStore } from '../../stores/metadataStore'
import { Users, Wrench, CalendarCheck, DollarSign, Plus, Loader2, RefreshCw, Star, Info, ShieldCheck, UserX, Search, Trash2 } from 'lucide-vue-next'

const metadataStore = useMetadataStore()

const stats = ref(null)
const admins = ref([])
const adminsPagination = ref({ total_pages: 1 })
const adminsPage = ref(1)
const adminSearch = ref('')

const users = ref([])
const usersPagination = ref({ total_pages: 1 })
const usersPage = ref(1)
const userSearch = ref('')

const technicians = ref([])
const techniciansPagination = ref({ total_pages: 1 })
const techniciansPage = ref(1)
const technicianSearch = ref('')

const bookings = ref([])
const bookingPagination = ref({ total_pages: 1 })
const bookingPage = ref(1)
const bookingStatusFilter = ref('')

const assignMap = reactive({})
const activeTab = ref('users')
const showAddStaff = ref(false)
const addStaffError = ref('')
const newStaff = ref({ full_name: '', phone: '', password: '', role: 'admin' })

const loading = reactive({
  stats: false,
  admins: false,
  users: false,
  technicians: false,
  bookings: false,
  addStaff: false,
})

const tabs = computed(() => metadataStore.getOptions('ADMIN_TAB').map(opt => ({
    key: opt.code,
    label: opt.label
})))

const bookingStatuses = computed(() => metadataStore.getOptions('BOOKING_STATUS'))

const statCards = computed(() => [
  { label: 'Active Users', value: stats.value?.total_customers ?? 0, icon: Users, color: 'bg-indigo-50 text-indigo-600' },
  { label: 'Staff Force', value: stats.value?.total_technicians ?? 0, icon: Wrench, color: 'bg-primary-50 text-primary-600' },
  { label: 'Suspended', value: stats.value?.total_suspended ?? 0, icon: UserX, color: 'bg-red-50 text-red-600' },
  { label: 'Requests', value: stats.value?.total_bookings ?? 0, icon: CalendarCheck, color: 'bg-amber-50 text-amber-600' },
  { label: 'Net Revenue', value: `₹${(stats.value?.total_revenue ?? 0).toLocaleString('en-IN')}`, icon: DollarSign, color: 'bg-emerald-50 text-emerald-700' },
])

const statusClass = (status) => {
  const config = metadataStore.getUIConfig('BOOKING_STATUS', status)
  const color = config.color || 'slate'
  
  const colors = {
    amber: 'bg-amber-50 text-amber-600 border border-amber-100',
    blue: 'bg-blue-50 text-blue-600 border border-blue-100',
    violet: 'bg-violet-50 text-violet-600 border border-violet-100',
    orange: 'bg-orange-50 text-orange-600 border border-orange-100',
    emerald: 'bg-emerald-50 text-emerald-700 border border-emerald-100',
    red: 'bg-red-50 text-red-600 border border-red-100',
    slate: 'bg-slate-100 text-slate-500 border border-slate-200'
  }
  
  return colors[color] || colors.slate
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A'
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })
}

const currentList = computed(() => {
  if (activeTab.value === 'users') return users.value
  if (activeTab.value === 'technicians') return technicians.value
  if (activeTab.value === 'admins') return admins.value
  return []
})

const currentPagination = computed(() => {
  if (activeTab.value === 'users') return usersPagination.value
  if (activeTab.value === 'technicians') return techniciansPagination.value
  if (activeTab.value === 'admins') return adminsPagination.value
  return { total_pages: 1 }
})

const currentPage = computed(() => {
  if (activeTab.value === 'users') return usersPage.value
  if (activeTab.value === 'technicians') return techniciansPage.value
  if (activeTab.value === 'admins') return adminsPage.value
  return 1
})

const loadingTab = computed(() => {
  if (activeTab.value === 'users') return loading.users
  if (activeTab.value === 'technicians') return loading.technicians
  if (activeTab.value === 'admins') return loading.admins
  return false
})

const searchModel = computed({
  get: () => {
    if (activeTab.value === 'users') return userSearch.value
    if (activeTab.value === 'technicians') return technicianSearch.value
    if (activeTab.value === 'admins') return adminSearch.value
    return ''
  },
  set: (val) => {
    if (activeTab.value === 'users') userSearch.value = val
    if (activeTab.value === 'technicians') technicianSearch.value = val
    if (activeTab.value === 'admins') adminSearch.value = val
  }
})

// Consolidated fetcher that understands activeTab
async function fetchCurrent(page = 1) {
    if (activeTab.value === 'users') await fetchUsers(page)
    else if (activeTab.value === 'technicians') await fetchTechnicians(page)
    else if (activeTab.value === 'admins') await fetchAdmins(page)
    else if (activeTab.value === 'bookings') await fetchBookings(page)
}

// Watch activeTab to fetch data if list is empty
watch(activeTab, (newTab) => {
    if (['users', 'technicians', 'admins', 'bookings'].includes(newTab)) {
        fetchCurrent(1)
    }
})

async function fetchStats() {
  loading.stats = true
  try {
    const res = await adminService.getStats()
    stats.value = res.data
  } catch (e) { console.error('Stats fetch failed:', e) } 
  finally { loading.stats = false }
}

async function fetchAdmins(page = 1) {
  loading.admins = true
  adminsPage.value = page
  try {
    const res = await adminService.getUsers({ role: 'admin', page, search: adminSearch.value || null })
    admins.value = res.data.users
    adminsPagination.value = res.data.pagination
  } catch (e) { console.error('Admins fetch failed:', e) } 
  finally { loading.admins = false }
}

async function fetchUsers(page = 1) {
  loading.users = true
  usersPage.value = page
  try {
    const res = await adminService.getUsers({ role: 'customer', page, search: userSearch.value || null })
    users.value = res.data.users
    usersPagination.value = res.data.pagination
  } catch (e) { console.error('Users fetch failed:', e) } 
  finally { loading.users = false }
}

async function fetchTechnicians(page = 1) {
  loading.technicians = true
  techniciansPage.value = page
  try {
    const res = await adminService.getUsers({ role: 'technician', page, search: technicianSearch.value || null })
    technicians.value = res.data.users
    techniciansPagination.value = res.data.pagination
  } catch (e) { console.error('Technicians fetch failed:', e) } 
  finally { loading.technicians = false }
}

async function fetchBookings(page = 1) {
  loading.bookings = true
  bookingPage.value = page
  try {
    const res = await adminService.getAllBookings({ status: bookingStatusFilter.value || null, page, limit: 15 })
    bookings.value = res.data.bookings
    bookingPagination.value = res.data.pagination
  } catch (e) { console.error('Bookings fetch failed:', e) } 
  finally { loading.bookings = false }
}

let searchTimer = null
function debouncedFetch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => fetchCurrent(1), 400)
}

async function refreshData() {
  await Promise.all([fetchStats(), fetchCurrent(1)])
}

async function toggleStatus(user) {
  const newStatus = user.status === 'active' ? 'suspended' : 'active'
  if (!confirm(`Are you sure you want to change ${user.full_name}'s status to ${newStatus}?`)) return
  
  try {
    if (user.role === 'customer') {
      await adminService.updateCustomerStatus(user.id, newStatus)
    } else {
      await adminService.updateStaffStatus(user.id, newStatus)
    }
    user.status = newStatus
    fetchStats()
  } catch (e) {
    alert('Failed to update status.')
  }
}

async function changeUserRole(user, newRole) {
    if (user.role === newRole) return
    if (!confirm(`Are you sure you want to change role for ${user.full_name} to ${newRole}?`)) return
    try {
        await adminService.updateUserRole(user.id, newRole)
        alert('Role updated successfully. Refreshing...')
        fetchCurrent(1)
        fetchStats()
    } catch (e) {
        alert('Failed to update role. Policy violation or server error.')
    }
}

async function deleteUser(user) {
    if (user.is_protected) {
        alert('Cannot delete protected system accounts (Root Admin)')
        return
    }
    if (!confirm(`WARING: Permanent Deletion!\nAre you sure you want to delete ${user.full_name}? This action cannot be undone.`)) return
    
    try {
        await adminService.deleteUser(user.id)
        alert('User deleted successfully.')
        fetchCurrent(1)
        fetchStats()
    } catch (e) {
        alert(e.response?.data?.detail || 'Deletion failed. User might have active dependencies.')
    }
}

async function createStaff() {
  addStaffError.value = ''
  if (!newStaff.value.full_name || !newStaff.value.phone || !newStaff.value.password) {
    addStaffError.value = 'Security: All fields are mandatory'
    return
  }
  loading.addStaff = true
  try {
    await adminService.createStaff(newStaff.value)
    showAddStaff.value = false
    newStaff.value = { full_name: '', phone: '', password: '', role: 'admin' }
    fetchCurrent(1)
    fetchStats()
  } catch (e) {
    addStaffError.value = e.response?.data?.detail || 'Handshake failed'
  } finally { loading.addStaff = false }
}

async function assignBooking(bookingId) {
  const techId = assignMap[bookingId]
  if (!techId) return
  try {
    await adminService.assignBooking(bookingId, techId)
    fetchBookings(bookingPage.value)
    delete assignMap[bookingId]
  } catch (e) { alert('Deployment failed') }
}

onMounted(() => {
  fetchStats()
  fetchCurrent(1)
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.animate-in {
    animation-duration: 0.3s;
    animation-fill-mode: both;
}
.slide-in-from-bottom-4 { animation-name: slideInFromBottom; }

@keyframes slideInFromBottom {
    from { transform: translateY(1rem); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
