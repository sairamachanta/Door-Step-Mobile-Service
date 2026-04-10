<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-6 pb-20">
    <!-- Success Card -->
    <div class="bg-white w-full max-w-md rounded-[40px] shadow-2xl shadow-gray-200/50 border border-gray-100 overflow-hidden text-center p-8 space-y-8 animate-in fade-in zoom-in duration-700">
       
       <!-- Success Visual -->
       <div class="relative mx-auto w-24 h-24">
          <div class="absolute inset-0 bg-green-500/10 rounded-full animate-pulse"></div>
          <div class="absolute inset-2 bg-green-500/20 rounded-full animate-ping duration-1000"></div>
          <div class="relative w-full h-full bg-green-500 rounded-full flex items-center justify-center shadow-lg shadow-green-200">
             <CheckCircle2 class="w-12 h-12 text-white" />
          </div>
       </div>
       
       <div class="space-y-2">
          <h1 class="text-3xl font-black text-gray-900 tracking-tight">Success!</h1>
          <p class="text-sm text-gray-400 font-medium">Your repair request has been locked in.</p>
       </div>

       <!-- Booking ID Badge -->
       <div class="bg-gray-50 rounded-2xl py-3 px-6 inline-flex flex-col items-center gap-1 border border-gray-100">
          <span class="text-[10px] font-black text-gray-400 uppercase tracking-widest">Booking Reference</span>
          <span class="text-lg font-black text-blue-600">#{{ bookingId }}</span>
       </div>
       
       <!-- Status Timeline Card -->
       <div class="bg-blue-600 rounded-3xl p-6 text-left relative overflow-hidden shadow-xl shadow-blue-200">
          <div class="absolute -right-4 -top-4 w-24 h-24 bg-white/10 rounded-full blur-2xl"></div>
          <div class="flex items-start gap-4">
             <div class="w-10 h-10 rounded-2xl bg-white/20 flex items-center justify-center flex-shrink-0">
                <Search class="w-5 h-5 text-white animate-pulse" />
             </div>
             <div class="space-y-1">
                <h3 class="font-black text-white text-sm uppercase tracking-wider">Assigning Expert</h3>
                <p class="text-[11px] text-blue-100 leading-relaxed">We are matching your request with the best technician in <strong>{{ bookingStore.selectedAddress?.city || 'your area' }}</strong>. You'll get an SMS shortly.</p>
             </div>
          </div>
       </div>

       <!-- Summary Info -->
       <div class="grid grid-cols-2 gap-4">
          <div class="bg-gray-50 p-4 rounded-2xl text-left border border-gray-100">
             <p class="text-[9px] font-black text-gray-400 uppercase tracking-tighter mb-1">Date</p>
             <p class="text-xs font-bold text-gray-900">{{ formattedDate }}</p>
          </div>
          <div class="bg-gray-50 p-4 rounded-2xl text-left border border-gray-100">
             <p class="text-[9px] font-black text-gray-400 uppercase tracking-tighter mb-1">Time Slot</p>
             <p class="text-xs font-bold text-gray-900">{{ bookingStore.selectedTimeSlot || 'ASAP' }}</p>
          </div>
       </div>

       <!-- Action Buttons -->
       <div class="space-y-4 pt-4">
          <button 
             @click="trackBooking"
             class="w-full bg-gray-900 text-white px-8 py-5 rounded-3xl font-black text-sm uppercase tracking-widest hover:bg-black transition-all shadow-xl shadow-gray-200 active:scale-95 flex items-center justify-center gap-3"
          >
             Track Status <ArrowRight class="w-4 h-4" />
          </button>
          
          <button 
             @click="goHome"
             class="w-full bg-white text-gray-500 px-8 py-4 rounded-3xl font-black text-xs uppercase tracking-widest hover:bg-gray-50 transition-all border border-gray-100 active:scale-95"
          >
             Return Home
          </button>
       </div>
    </div>
    
    <p class="mt-8 text-[11px] text-gray-400 font-bold uppercase tracking-widest flex items-center gap-2">
       <ShieldCheck class="w-4 h-4" /> Secure Doorstep Repair Service
    </p>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { CheckCircle2, Search, ArrowRight, ShieldCheck } from 'lucide-vue-next'
import dayjs from 'dayjs'
import { useBookingStore } from '../../stores/booking'

const route = useRoute()
const router = useRouter()
const bookingStore = useBookingStore()

const bookingId = route.params.bookingId

const formattedDate = computed(() => {
   if (!bookingStore.selectedDate) return 'Today'
   return dayjs(bookingStore.selectedDate).format('MMM DD, YYYY')
})

// Clear booking flow after some time or on navigation
onMounted(() => {
   // Confetti placeholder
   console.log('Booking Successful:', bookingId)
})

const trackBooking = () => {
   bookingStore.clearBookingFlow()
   router.push('/bookings')
}

const goHome = () => {
   bookingStore.clearBookingFlow()
   router.push('/home')
}
</script>
