<template>
  <BaseLayout>
    <div class="min-h-screen bg-white pb-24 md:pb-12 text-[#170F49] overflow-x-hidden">
      <!-- Premium Hero Header -->
      <header class="relative overflow-hidden bg-slate-900 pt-10 pb-24 md:pt-16 md:pb-32 px-6 text-white text-center">
        <!-- Abstract Background Decor -->
        <div class="absolute top-0 right-0 -translate-y-1/2 translate-x-1/2 w-[600px] h-[600px] bg-primary-600/30 rounded-full blur-[120px]"></div>
        <div class="absolute bottom-0 left-0 translate-y-1/2 -translate-x-1/2 w-[400px] h-[400px] bg-purple-600/20 rounded-full blur-[80px]"></div>
        
        <div class="max-w-7xl mx-auto relative z-10 space-y-6 animate-reveal">
          <div class="relative inline-block group">
            <div class="w-32 h-32 md:w-40 md:h-40 bg-gradient-to-br from-primary-500 to-purple-600 rounded-[3rem] flex items-center justify-center text-4xl md:text-5xl font-black shadow-2xl border-4 border-white/10 group-hover:scale-105 transition-transform duration-500 animate-float">
              {{ authStore.user?.full_name?.charAt(0) || 'U' }}
            </div>
            <button 
              @click="showEditModal = true"
              class="absolute bottom-2 right-2 p-3 bg-white text-slate-900 rounded-2xl shadow-xl hover:bg-primary-500 hover:text-white transition-all active:scale-90"
            >
              <Edit3 class="w-5 h-5" />
            </button>
          </div>
          
          <div class="space-y-2">
            <h1 class="text-4xl md:text-6xl font-black tracking-tight">{{ authStore.user?.full_name || 'Guest User' }}</h1>
            <div class="flex items-center justify-center gap-3 text-slate-400 font-bold">
              <span class="flex items-center gap-1.5 px-3 py-1 bg-white/5 rounded-full border border-white/10">
                <Smartphone class="w-4 h-4" />
                {{ authStore.user?.phone }}
              </span>
              <span v-if="authStore.user?.is_phone_verified" class="px-2 py-0.5 bg-emerald-500/20 text-emerald-400 text-[10px] uppercase font-black tracking-widest rounded-full border border-emerald-500/30">Verified</span>
            </div>
          </div>
        </div>
      </header>

      <!-- Quick Stats (Floating Overlap) -->
      <div class="max-w-5xl mx-auto px-6 -mt-12 md:-mt-16 mb-20 relative z-20 animate-reveal-subtle">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-8">
          <div 
            v-for="stat in statCards" 
            :key="stat.label"
            class="bg-white border border-slate-100 p-6 rounded-[2.5rem] shadow-xl shadow-slate-900/5 text-center group hover:border-primary-500 transition-all duration-300"
          >
            <div class="w-10 h-10 bg-slate-50 rounded-xl flex items-center justify-center mx-auto mb-4 group-hover:bg-primary-50 group-hover:text-primary-600 transition-colors">
              <component :is="stat.icon" class="w-5 h-5" />
            </div>
            <p class="text-2xl font-black text-slate-900">{{ stat.value || '0' }}</p>
            <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mt-1">{{ stat.label }}</p>
          </div>
        </div>
      </div>

      <main class="max-w-4xl mx-auto px-6 space-y-20">
        <!-- Account Sections -->
        <section v-for="section in menuSections" :key="section.title" class="animate-reveal">
          <div class="flex items-center justify-between mb-8">
            <h3 class="text-xl font-black text-slate-900">{{ section.title }}</h3>
            <div class="h-px flex-grow bg-slate-100 mx-6"></div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button 
              v-for="item in section.items" 
              :key="item.label"
              @click="item.action()"
              class="group flex items-center gap-6 p-6 rounded-[2rem] border border-transparent hover:border-primary-200 hover:bg-white hover:shadow-xl transition-all duration-300 text-left"
              :class="section.bgColor || 'bg-slate-50'"
            >
              <div class="w-14 h-14 bg-white rounded-2xl flex items-center justify-center shadow-sm group-hover:scale-110 group-hover:rotate-3 transition-all duration-500">
                <component :is="item.icon" class="w-6 h-6 transition-colors" :class="item.iconClass" />
              </div>
              <div class="flex-1">
                <p class="font-black text-slate-900">{{ item.label }}</p>
                <p class="text-xs text-slate-400 font-medium">{{ item.desc }}</p>
              </div>
              <ChevronRight class="w-5 h-5 text-slate-300 group-hover:text-primary-500 transition-colors group-hover:translate-x-1" />
            </button>
          </div>
        </section>

        <!-- Logout CTA -->
        <div class="mt-16 mb-24 p-8 md:p-12 bg-slate-900 rounded-[3.5rem] flex flex-col items-center text-center relative overflow-hidden animate-reveal group">
          <!-- Ambient Light Effect -->
          <div class="absolute top-0 right-0 w-64 h-64 bg-red-500/10 rounded-full blur-[80px] -translate-y-1/2 translate-x-1/2"></div>
          
          <h3 class="text-xl font-black text-white mb-2 relative z-10">Done for today?</h3>
          <p class="text-slate-400 text-sm font-medium mb-10 max-w-xs mx-auto relative z-10">Securely sign out of your account to protect your data and privacy.</p>
          
          <button 
            @click="showLogoutModal = true"
            class="px-8 md:px-12 py-5 bg-white text-slate-900 rounded-3xl font-black text-sm uppercase tracking-widest hover:bg-red-500 hover:text-white transition-all active:scale-95 inline-flex items-center justify-center gap-3 shadow-2xl relative z-10 w-full sm:w-auto"
          >
            <LogOut class="w-5 h-5" />
            Sign Out Permanently
          </button>
          
          <div class="mt-12 flex items-center justify-center gap-4 relative z-10">
            <div class="h-px w-8 bg-slate-800"></div>
            <p class="text-[10px] text-slate-500 font-black uppercase tracking-[0.3em]">Version 2.0.4 Premium</p>
            <div class="h-px w-8 bg-slate-800"></div>
          </div>
        </div>
      </main>

      <!-- Edit Profile Modal -->
      <div v-if="showEditModal" class="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-slate-900/60 backdrop-blur-xl animate-fade">
        <div class="bg-white rounded-[3rem] p-10 max-w-md w-full shadow-2xl animate-revealScale">
          <div class="flex items-center justify-between mb-8">
            <h2 class="text-2xl font-black">Edit Profile</h2>
            <button @click="showEditModal = false" class="p-2 hover:bg-slate-50 rounded-xl transition-colors">
              <X class="w-6 h-6 text-slate-400" />
            </button>
          </div>
          
          <form @submit.prevent="handleUpdateProfile" class="space-y-6">
            <div class="space-y-2">
              <label class="text-xs font-black uppercase tracking-widest text-slate-400">Full Name</label>
              <input 
                v-model="editForm.full_name"
                class="w-full px-6 py-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-4 focus:ring-primary-500/10 focus:border-primary-500 outline-none font-bold transition-all"
                placeholder="Enter your name"
              >
            </div>
            <div class="space-y-2">
              <label class="text-xs font-black uppercase tracking-widest text-slate-400">Email Address</label>
              <input 
                v-model="editForm.email"
                type="email"
                class="w-full px-6 py-4 bg-slate-50 border border-slate-100 rounded-2xl focus:ring-4 focus:ring-primary-500/10 focus:border-primary-500 outline-none font-bold transition-all"
                placeholder="email@example.com"
              >
            </div>
            <button 
              type="submit"
              :disabled="authStore.loading"
              class="w-full py-5 bg-primary-600 text-white rounded-2xl font-black text-sm uppercase tracking-widest shadow-xl shadow-primary-600/20 hover:bg-primary-700 transition-all active:scale-95 disabled:opacity-50"
            >
              {{ authStore.loading ? 'Updating...' : 'Save Changes' }}
            </button>
          </form>
        </div>
      </div>

      <!-- Address Management Modal -->
      <div v-if="showAddressModal" class="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-slate-900/60 backdrop-blur-xl animate-fade">
        <div class="bg-white rounded-[3.5rem] p-8 md:p-12 max-w-2xl w-full max-h-[85vh] overflow-y-auto shadow-2xl animate-revealScale">
          <div class="flex items-center justify-between mb-10 sticky top-0 bg-white pb-4 z-10">
            <div>
              <h2 class="text-3xl font-black">My Addresses</h2>
              <p class="text-sm text-slate-400 font-bold mt-1 uppercase tracking-widest">Saved Service Locations</p>
            </div>
            <button @click="showAddressModal = false" class="p-3 hover:bg-slate-50 rounded-2xl transition-colors">
              <X class="w-6 h-6 text-slate-400" />
            </button>
          </div>

          <div class="space-y-6">
            <!-- Add New Address Form (Simple Inline) -->
            <button 
              v-if="!showNewAddressForm"
              @click="showNewAddressForm = true"
              class="w-full py-6 border-2 border-dashed border-slate-200 rounded-3xl flex items-center justify-center gap-3 text-slate-400 font-black hover:border-primary-500 hover:text-primary-500 transition-all group"
            >
              <Plus class="w-6 h-6 group-hover:rotate-90 transition-transform duration-300" />
              Add New Address
            </button>

            <form v-else @submit.prevent="handleAddAddress" class="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-50 p-6 rounded-[2.5rem] border border-slate-100 animate-fadeSlide">
              <div class="col-span-1 md:col-span-2 space-y-2">
                <input v-model="addressForm.label" placeholder="Label (Home, Office...)" class="w-full px-5 py-3 border border-slate-200 rounded-xl outline-none focus:border-primary-500 font-bold">
              </div>
              <div class="col-span-1 md:col-span-2">
                <input v-model="addressForm.address_line1" placeholder="Address Line 1" class="w-full px-5 py-3 border border-slate-200 rounded-xl outline-none focus:border-primary-500 font-bold">
              </div>
              <div>
                <input v-model="addressForm.city" placeholder="City" class="w-full px-5 py-3 border border-slate-200 rounded-xl outline-none focus:border-primary-500 font-bold">
              </div>
              <div>
                <input v-model="addressForm.pincode" placeholder="Pincode" class="w-full px-5 py-3 border border-slate-200 rounded-xl outline-none focus:border-primary-500 font-bold">
              </div>
              <div class="col-span-1 md:col-span-2 flex gap-3 pt-2">
                <button type="submit" class="flex-1 py-3 bg-primary-600 text-white rounded-xl font-black text-xs uppercase tracking-widest hover:bg-primary-700 shadow-lg shadow-primary-600/10">Add Location</button>
                <button type="button" @click="showNewAddressForm = false" class="px-6 py-3 bg-white border border-slate-200 text-slate-400 rounded-xl font-black text-xs uppercase tracking-widest">Cancel</button>
              </div>
            </form>

            <div v-if="addresses.length === 0 && !loading" class="text-center py-10">
              <MapPin class="w-12 h-12 text-slate-200 mx-auto mb-4" />
              <p class="text-slate-400 font-bold">No saved addresses yet.</p>
            </div>

            <div class="space-y-4">
              <div 
                v-for="addr in addresses" 
                :key="addr.id" 
                class="flex items-center justify-between p-6 bg-white border border-slate-100 rounded-3xl hover:border-primary-200 hover:shadow-lg transition-all"
              >
                <div class="flex items-start gap-5">
                  <div class="w-12 h-12 bg-primary-50 rounded-2xl flex items-center justify-center flex-shrink-0 text-primary-600">
                    <MapPin class="w-6 h-6" />
                  </div>
                  <div>
                    <h4 class="font-black text-slate-900 flex items-center gap-2">
                      {{ addr.label }}
                      <span v-if="addr.is_default" class="px-2 py-0.5 bg-primary-100 text-primary-600 text-[8px] uppercase font-black rounded-md">Default</span>
                    </h4>
                    <p class="text-xs text-slate-500 font-medium leading-relaxed mt-1">{{ addr.address_line1 }}, {{ addr.city }} - {{ addr.pincode }}</p>
                  </div>
                </div>
                <button @click="removeAddress(addr.id)" class="p-3 text-slate-300 hover:text-red-500 transition-colors">
                  <Trash2 class="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Logout Confirmation Modal -->
      <div v-if="showLogoutModal" class="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-slate-900/60 backdrop-blur-xl animate-fade">
        <div class="bg-white rounded-[3rem] p-10 max-w-sm w-full shadow-2xl animate-revealScale text-center">
          <div class="w-20 h-20 bg-red-50 rounded-[2rem] flex items-center justify-center mx-auto mb-6 text-red-500 animate-float">
            <LogOut class="w-10 h-10" />
          </div>
          <h2 class="text-2xl font-black text-slate-900 mb-2">Wait! Signing Out?</h2>
          <p class="text-slate-500 font-medium mb-10">Are you sure you want to end your current session? You will need to log in again to access your dashboard.</p>
          
          <div class="space-y-3">
            <button 
              @click="confirmLogout"
              class="w-full py-5 bg-red-500 text-white rounded-2xl font-black text-sm uppercase tracking-widest shadow-xl shadow-red-500/20 hover:bg-red-600 transition-all active:scale-95"
            >
              Yes, Sign Me Out
            </button>
            <button 
              @click="showLogoutModal = false"
              class="w-full py-5 bg-slate-100 text-slate-500 rounded-2xl font-black text-sm uppercase tracking-widest hover:bg-slate-200 transition-all active:scale-95"
            >
              Nevermind, Stay
            </button>
          </div>
        </div>
      </div>

    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, onMounted, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { useProfile } from '../../composables/useProfile'
import BaseLayout from '../../components/BaseLayout.vue'
import { 
  Check, Smartphone, MapPin, CreditCard, HelpCircle, MessageCircle, 
  Bell, Lock, LogOut, ChevronRight, Edit3, X, Plus, Trash2,
  Calendar, Award, Wallet, Briefcase, Heart, Settings
} from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const { stats, addresses, loading, fetchStats, fetchAddresses, addAddress, removeAddress } = useProfile()

const showEditModal = ref(false)
const showAddressModal = ref(false)
const showNewAddressForm = ref(false)
const showLogoutModal = ref(false)

const editForm = reactive({
  full_name: authStore.user?.full_name || '',
  email: authStore.user?.email || ''
})

const addressForm = reactive({
  label: '',
  address_line1: '',
  city: '',
  state: 'Delhi',
  pincode: '',
  is_default: false
})

onMounted(async () => {
  await Promise.all([
    authStore.fetchUserProfile(),
    fetchStats(),
    fetchAddresses()
  ])
})

const statCards = computed(() => [
  { label: 'Total Bookings', value: stats.value?.total_bookings, icon: Briefcase },
  { label: 'Loyalty Points', value: stats.value?.loyalty_points, icon: Award },
  { label: 'Wallet Balance', value: `₹${stats.value?.wallet_balance || '0.00'}`, icon: Wallet },
  { label: 'Member Since', value: stats.value?.member_since, icon: Calendar }
])

const menuSections = [
  {
    title: 'Account Settings',
    bgColor: 'bg-slate-50',
    items: [
      { label: 'Saved Addresses', desc: 'Manage your primary locations', icon: MapPin, iconClass: 'text-emerald-500', action: () => showAddressModal.value = true },
      { label: 'Payment Methods', desc: 'UPI, Credit Cards, Wallets', icon: CreditCard, iconClass: 'text-purple-500', action: () => {} },
      { label: 'My Devices', desc: 'Saved phone models & history', icon: Smartphone, iconClass: 'text-primary-500', action: () => {} },
    ]
  },
  {
    title: 'Preference & Security',
    bgColor: 'bg-slate-50',
    items: [
      { label: 'Notifications', desc: 'Alerts, updates & OTPs', icon: Bell, iconClass: 'text-amber-500', action: () => {} },
      { label: 'Privacy & Security', desc: 'Passcode & data settings', icon: Lock, iconClass: 'text-slate-400', action: () => {} },
    ]
  },
  {
    title: 'Support & Help',
    bgColor: 'bg-indigo-50/50',
    items: [
      { label: 'Chat With Experts', desc: '24/7 technical assistance', icon: MessageCircle, iconClass: 'text-primary-600', action: () => {} },
      { label: 'Help Center', desc: 'FAQs and platform guides', icon: HelpCircle, iconClass: 'text-slate-500', action: () => {} },
    ]
  }
]

const handleUpdateProfile = async () => {
  try {
    await authStore.updateProfile(editForm)
    showEditModal.value = false
  } catch (err) {
    alert(err.message || 'Update failed')
  }
}

const handleAddAddress = async () => {
  try {
    await addAddress({ ...addressForm })
    Object.keys(addressForm).forEach(k => addressForm[k] = k === 'state' ? 'Delhi' : k === 'is_default' ? false : '')
    showNewAddressForm.value = false
  } catch (err) {
    alert('Failed to add address')
  }
}

const confirmLogout = async () => {
  showLogoutModal.value = false
  await authStore.logout()
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'TBD'
  return new Date(dateStr).toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    year: 'numeric' 
  })
}
</script>

<style scoped>
.animate-reveal {
  animation: reveal 1s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-revealScale {
  animation: revealScale 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-fade {
  animation: fade 0.4s ease-out forwards;
}

.animate-fadeSlide {
  animation: fadeSlide 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-float {
  animation: float 5s ease-in-out infinite;
}

@keyframes reveal {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes reveal-subtle {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-reveal-subtle {
  animation: reveal-subtle 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes revealScale {
  from { opacity: 0; transform: scale(0.9) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes fade {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeSlide {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #f1f5f9;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #e2e8f0;
}
</style>
