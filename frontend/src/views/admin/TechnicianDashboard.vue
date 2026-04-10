<template>
  <BaseLayout>
    <div class="min-h-screen bg-slate-50 pb-24 md:pb-8">
      <!-- Header -->
      <header class="bg-white border-b border-slate-200 px-6 py-6 sticky top-0 z-30">
        <div class="max-w-5xl mx-auto flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-black text-slate-900">Admin <span class="text-primary-600">Portal</span></h1>
            <p class="text-slate-500 text-sm font-medium">Hello, {{ authStore.user?.full_name }}</p>
          </div>
          <div class="flex items-center gap-2">
            <div class="px-4 py-2 bg-emerald-50 text-emerald-700 rounded-xl border border-emerald-100 flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span class="text-xs font-black uppercase tracking-widest">{{ authStore.userRole === 'admin' ? 'Superadmin' : 'On Duty' }}</span>
            </div>
            <button @click="refreshAll" class="p-2 bg-slate-100 text-slate-600 rounded-xl hover:bg-slate-200 transition-colors">
              <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': loading.stats }" />
            </button>
          </div>
        </div>
      </header>

      <main class="max-w-5xl mx-auto p-4 md:p-8 space-y-6">
        <!-- Stats Row -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
          <div v-for="s in statCards" :key="s.label" class="bg-white rounded-2xl border border-slate-100 p-4 space-y-2 shadow-sm">
            <div :class="['w-9 h-9 rounded-xl flex items-center justify-center', s.color]">
              <component :is="s.icon" class="w-4 h-4" />
            </div>
            <p class="text-[10px] font-black uppercase tracking-widest text-slate-400">{{ s.label }}</p>
            <p class="text-2xl font-black text-slate-900">{{ loading.stats ? '…' : s.value }}</p>
          </div>
        </div>

        <!-- Dashboard Tabs -->
        <div class="flex gap-2 border-b border-slate-200">
          <button
            v-for="tab in tabs"
            :key="tab.code || tab.key"
            @click="activeTab = tab.code || tab.key"
            :class="[
              'px-4 py-2.5 text-sm font-bold transition-all border-b-2 -mb-px',
              activeTab === (tab.code || tab.key)
                ? 'border-primary-600 text-primary-600'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            ]"
          >{{ tab.label }}</button>
        </div>

        <!-- Tab: My Jobs -->
        <div v-if="activeTab === 'jobs'" class="space-y-4">
          <!-- Status Filter -->
          <div class="flex gap-2 flex-wrap">
            <button
              v-for="f in jobFilters"
              :key="f.value"
              @click="activeJobFilter = f.value; fetchBookings()"
              :class="[
                'px-4 py-2 rounded-xl text-xs font-bold border transition-all',
                activeJobFilter === f.value
                  ? 'bg-primary-600 text-white border-primary-600'
                  : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
              ]"
            >{{ f.label }}</button>
          </div>

          <div v-if="loading.bookings" class="flex justify-center py-12">
            <Loader2 class="w-8 h-8 animate-spin text-primary-500" />
          </div>

          <div v-else-if="bookings.length === 0" class="text-center py-12 space-y-2">
            <Inbox class="w-10 h-10 text-slate-300 mx-auto" />
            <p class="text-slate-400 font-bold">No jobs assigned</p>
          </div>

          <div v-else class="space-y-4">
            <div v-for="b in bookings" :key="b.id" class="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
              <div class="p-5 flex flex-col sm:flex-row sm:items-start justify-between gap-3">
                <div class="space-y-1">
                  <div class="flex items-center gap-2">
                    <p class="font-black text-slate-900">{{ b.booking_number }}</p>
                    <span :class="['px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-widest', statusClass(b.status)]">
                      {{ metadataStore.getLabel('BOOKING_STATUS', b.status) }}
                    </span>
                  </div>
                  <p class="text-sm font-bold text-slate-700">{{ b.service_name }}</p>
                  <p class="text-xs text-slate-500">{{ b.brand_name }} {{ b.model_name }}</p>
                </div>
                <div class="text-right">
                  <p class="font-black text-slate-900">₹{{ b.final_price }}</p>
                  <p class="text-xs text-slate-400 font-medium">{{ b.preferred_date }} · {{ b.preferred_time_slot }}</p>
                </div>
              </div>

              <!-- Customer Details -->
              <div class="px-5 pb-4 space-y-2 border-t border-slate-50 pt-3">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center text-xs font-bold text-blue-600">{{ b.customer_name?.[0] }}</div>
                  <div>
                    <p class="text-xs font-black text-slate-800">{{ b.customer_name }}</p>
                    <p class="text-[10px] text-slate-500 font-medium">{{ b.customer_phone }}</p>
                  </div>
                </div>
                <div v-if="b.full_address_snapshot" class="text-[10px] text-slate-500 flex gap-1">
                  <MapPin class="w-3 h-3 shrink-0" />
                  <span>{{ b.full_address_snapshot.address_line1 }}, {{ b.full_address_snapshot.city }}</span>
                </div>
              </div>

              <!-- Actions -->
              <div v-if="['assigned', 'in_progress'].includes(b.status)" class="px-5 pb-5 pt-2 border-t border-slate-50 flex gap-2">
                <input v-model="notesMap[b.id]" placeholder="Add notes…" class="flex-1 text-xs border border-slate-200 rounded-lg px-3 py-2" />
                <button
                  v-if="b.status === 'assigned'"
                  @click="updateJobStatus(b, 'in_progress')"
                  class="px-4 py-2 bg-amber-500 text-white rounded-lg text-xs font-bold hover:bg-amber-600"
                >Start</button>
                <button
                  v-if="b.status === 'in_progress'"
                  @click="updateJobStatus(b, 'completed')"
                  class="px-4 py-2 bg-emerald-600 text-white rounded-lg text-xs font-bold hover:bg-emerald-700"
                >Done</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Tab: Customers (Technician Role "controls user") -->
        <div v-if="activeTab === 'customers'" class="space-y-4">
          <div class="flex flex-col sm:flex-row justify-between gap-3">
            <input
              v-model="customerSearch"
              @input="debouncedFetchCustomers"
              placeholder="Search customers…"
              class="w-full sm:w-64 text-sm border border-slate-200 rounded-xl px-4 py-2 shadow-sm"
            />
          </div>

          <div v-if="loading.customers" class="flex justify-center py-12">
            <Loader2 class="w-8 h-8 animate-spin text-primary-500" />
          </div>

          <div v-else-if="customers.length === 0" class="text-center py-12 text-slate-400 font-medium">No customers found</div>

          <div v-else class="grid gap-3">
            <div v-for="c in customers" :key="c.id" class="bg-white rounded-2xl border border-slate-100 p-5 flex items-center justify-between shadow-sm">
              <div class="flex items-center gap-4">
                <div class="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center font-bold text-slate-600">{{ c.full_name?.[0] }}</div>
                <div>
                  <p class="font-bold text-slate-900">{{ c.full_name }}</p>
                  <p class="text-xs text-slate-500 font-medium">{{ c.phone }}</p>
                  <p class="text-[10px] text-slate-400 font-bold uppercase tracking-wider mt-1">{{ c.total_bookings }} Bookings</p>
                </div>
              </div>
              <div class="flex items-center gap-3">
                <span :class="['px-2.5 py-1 rounded-lg text-[9px] font-black uppercase tracking-widest', c.status === 'active' ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-600']">
                  {{ metadataStore.getLabel('USER_STATUS', c.status) }}
                </span>
                <button
                  @click="toggleCustomerStatus(c)"
                  class="p-2 bg-slate-50 text-slate-400 rounded-lg hover:text-red-500 hover:bg-red-50 transition-all"
                >
                  <UserX v-if="c.status === 'active'" class="w-4 h-4" />
                  <UserPlus v-else class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import BaseLayout from '../../components/BaseLayout.vue'
import technicianService from '../../services/technicianService'
import { useAuthStore } from '../../stores/auth'
import { useMetadataStore } from '../../stores/metadataStore'
import { 
  Loader2, Inbox, CheckCircle2, ClipboardList, Zap, 
  CheckCheck, Clock, RefreshCw, MapPin, Users, UserX, UserPlus 
} from 'lucide-vue-next'

const authStore = useAuthStore()
const metadataStore = useMetadataStore()
const stats = ref(null)
const bookings = ref([])
const customers = ref([])
const pagination = ref({ total_pages: 1 })
const currentPage = ref(1)
const activeFilter = ref('all')
const activeJobFilter = ref('all')
const activeTab = ref('jobs')
const customerSearch = ref('')
const notesMap = reactive({})

const loading = reactive({ stats: false, bookings: false, customers: false })

const tabs = computed(() => metadataStore.getOptions('TECHNICIAN_TAB').length > 0 
  ? metadataStore.getOptions('TECHNICIAN_TAB') 
  : [
      { code: 'jobs', label: 'My Jobs' },
      { code: 'customers', label: 'Customers' }
    ]
)

// Computed tab key because my dynamic metadata uses 'code' while local used 'key'
const activeTabKey = computed(() => activeTab.value)

const jobFilters = computed(() => {
  const options = metadataStore.getOptions('BOOKING_STATUS')
  return [
    { value: 'all', label: 'All Jobs' },
    ...options.map(o => ({ value: o.code, label: o.label }))
  ]
})

const statCards = computed(() => [
  { label: 'Total Assigned', value: stats.value?.total_assigned ?? 0, icon: ClipboardList, color: 'bg-primary-50 text-primary-600' },
  { label: 'In Progress', value: stats.value?.in_progress ?? 0, icon: Zap, color: 'bg-amber-50 text-amber-600' },
  { label: 'Completed', value: stats.value?.completed ?? 0, icon: CheckCheck, color: 'bg-emerald-50 text-emerald-700' },
  { label: 'Pending', value: stats.value?.pending ?? 0, icon: Clock, color: 'bg-slate-100 text-slate-600' },
])

const statusClass = (status) => {
  const config = metadataStore.getUIConfig('BOOKING_STATUS', status)
  const color = config.color || 'slate'
  
  const colors = {
    amber: 'bg-amber-50 text-amber-600',
    blue: 'bg-blue-50 text-blue-600',
    violet: 'bg-violet-50 text-violet-600',
    orange: 'bg-orange-50 text-orange-600',
    emerald: 'bg-emerald-50 text-emerald-700',
    red: 'bg-red-50 text-red-600',
    slate: 'bg-slate-100 text-slate-500'
  }
  
  return colors[color] || colors.slate
}

async function fetchStats() {
  loading.stats = true
  try { stats.value = (await technicianService.getStats()).data } catch (e) {} finally { loading.stats = false }
}

async function fetchBookings(page = 1) {
  loading.bookings = true
  currentPage.value = page
  try {
    const res = (await technicianService.getMyBookings({
      status: activeJobFilter.value === 'all' ? null : activeJobFilter.value,
      page,
      limit: 10,
    })).data
    bookings.value = res.bookings
    pagination.value = res.pagination
  } catch (e) {} finally { loading.bookings = false }
}

async function fetchCustomers() {
  loading.customers = true
  try {
    const res = (await technicianService.getCustomers({ search: customerSearch.value || null })).data
    customers.value = res.customers
  } catch (e) {} finally { loading.customers = false }
}

let searchTimer = null
function debouncedFetchCustomers() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(fetchCustomers, 400)
}

async function refreshAll() {
  await Promise.all([fetchStats(), fetchBookings(), fetchCustomers()])
}

async function updateJobStatus(booking, newStatus) {
  try {
    await technicianService.updateBookingStatus(booking.id, newStatus, notesMap[booking.id] || null)
    booking.status = newStatus
    delete notesMap[booking.id]
    fetchStats()
  } catch (e) {
    alert('Update failed')
  }
}

async function toggleCustomerStatus(customer) {
  const newStatus = customer.status === 'active' ? 'suspended' : 'active'
  try {
    await technicianService.updateCustomerStatus(customer.id, newStatus)
    customer.status = newStatus
  } catch (e) {
    alert('Status update failed')
  }
}

onMounted(() => {
  fetchStats()
  fetchBookings()
  fetchCustomers()
})
</script>
