<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ChevronLeft, ChevronDown, Smartphone, CreditCard, Banknote, Wallet, Info, CheckCircle2, Shield, Loader2, Receipt } from 'lucide-vue-next'
import dayjs from 'dayjs'
import BaseLayout from '../../components/BaseLayout.vue'
import { useBookingStore } from '../../stores/booking'

const router = useRouter()
const bookingStore = useBookingStore()

const showSummary = ref(true)

// Redirect if flow is broken
if (!bookingStore.selectedPricingId) {
   router.replace('/booking/select-brand')
}

const formattedDate = computed(() => {
   if (!bookingStore.selectedDate) return ''
   return dayjs(bookingStore.selectedDate).format('MMM DD, YYYY')
})

const getButtonText = computed(() => {
   if (bookingStore.loading) return 'PROCESSING...'
   if (bookingStore.paymentMethod === 'cash') {
      return `CONFIRM BOOKING`
   } else {
      return `PAY ₹${bookingStore.finalPrice.toLocaleString()}`
   }
})

const confirmBooking = async () => {
   const result = await bookingStore.createBooking()
   if (result.success) {
      router.push(`/booking/success/${result.booking_id}`)
   } else {
      alert('Booking failed: ' + result.message)
   }
}
</script>

<template>
  <BaseLayout>
    <div class="bg-gray-50 min-h-screen pb-32">
      <!-- Header -->
      <header class="bg-white sticky top-0 z-40 border-b border-gray-100 px-4 py-3 flex items-center space-x-3">
        <button @click="$router.back()" class="p-2 -ml-2 rounded-full hover:bg-gray-100">
          <ChevronLeft class="w-6 h-6 text-gray-600" />
        </button>
        <div class="flex-1">
          <h1 class="text-lg font-bold text-gray-900">Final Step</h1>
          <p class="text-xs text-gray-500">Secure Payment</p>
        </div>
        <div class="bg-green-100 text-green-700 px-2 py-1 rounded text-[10px] font-black uppercase">SECURE</div>
      </header>

      <main class="px-4 py-6 space-y-8">
         <!-- Order Summary Card -->
         <section class="bg-white rounded-3xl shadow-xl shadow-gray-200/50 border border-gray-100 overflow-hidden">
            <div 
              class="p-6 flex justify-between items-center cursor-pointer hover:bg-gray-50/50 transition"
              @click="showSummary = !showSummary"
            >
               <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-blue-50 rounded-2xl flex items-center justify-center">
                     <Receipt class="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                     <h3 class="font-black text-gray-900 text-sm uppercase tracking-widest">Order Summary</h3>
                     <p class="text-[10px] text-gray-400 font-bold">{{ bookingStore.selectedModel?.model_name }}</p>
                  </div>
               </div>
               <ChevronDown class="w-5 h-5 text-gray-300 transition-transform duration-300" :class="showSummary ? 'rotate-180' : ''" />
            </div>
            
            <div v-show="showSummary" class="px-6 pb-6 space-y-4 animate-in fade-in slide-in-from-top-2 duration-300">
               <!-- Details Grid -->
               <div class="grid grid-cols-2 gap-4 pt-2">
                  <div class="space-y-1">
                     <p class="text-[9px] font-black text-gray-400 uppercase tracking-tighter">Device & Service</p>
                     <p class="text-xs font-bold text-gray-900 leading-tight">
                        {{ bookingStore.selectedBrand?.name }} {{ bookingStore.selectedModel?.model_name }} • {{ bookingStore.selectedService?.service_name }}
                     </p>
                  </div>
                  <div class="space-y-1 text-right">
                     <p class="text-[9px] font-black text-gray-400 uppercase tracking-tighter">Schedule</p>
                     <p class="text-xs font-bold text-gray-900">{{ formattedDate }} • {{ bookingStore.selectedTimeSlot }}</p>
                  </div>
               </div>

               <div class="border-t border-gray-50 pt-4">
                  <div class="space-y-2.5">
                     <div class="flex justify-between text-xs items-center">
                        <span class="text-gray-500 font-medium">Service Fee</span>
                        <span class="font-bold text-gray-900">₹{{ bookingStore.pricingDetails?.final_price }}</span>
                     </div>
                     <div v-for="addon in bookingStore.selectedAddons" :key="addon.id" class="flex justify-between text-xs items-center">
                        <span class="text-gray-500 font-medium">{{ addon.addon_name }}</span>
                        <span class="font-bold text-gray-900">₹{{ addon.price }}</span>
                     </div>
                     <div v-if="bookingStore.deviceInsuranceOpted" class="flex justify-between text-xs items-center">
                        <span class="text-green-600 font-bold flex items-center gap-1"><Shield class="w-3 h-3" /> Device Care+</span>
                        <span class="font-bold text-gray-900">₹199</span>
                     </div>
                  </div>
               </div>
               
               <div class="bg-blue-600 rounded-2xl p-4 flex justify-between items-center mt-4">
                  <span class="text-white/70 text-[10px] font-black uppercase tracking-widest">Grand Total</span>
                  <span class="text-white text-xl font-black">₹{{ bookingStore.finalPrice.toLocaleString() }}</span>
               </div>
            </div>
         </section>

         <!-- Payment Methods -->
         <section class="space-y-4">
            <h3 class="font-black text-gray-900 px-1 text-xs uppercase tracking-widest flex items-center gap-2">
               Select Payment Mode
            </h3>
            <div class="space-y-3">
               <!-- UPI -->
               <label 
                 class="flex items-center p-5 bg-white border-2 rounded-2xl cursor-pointer transition-all duration-300 relative group overflow-hidden"
                 :class="bookingStore.paymentMethod === 'upi' ? 'border-blue-600 bg-blue-50/20' : 'border-gray-100 hover:border-blue-200'"
               >
                  <input type="radio" v-model="bookingStore.paymentMethod" value="upi" class="hidden" />
                  <div class="w-12 h-12 bg-gray-50 rounded-2xl flex items-center justify-center mr-4 group-hover:scale-110 transition">
                     <Smartphone class="w-6 h-6 text-blue-600" />
                  </div>
                  <div class="flex-1">
                     <span class="block font-black text-gray-900 text-sm uppercase">Quick UPI</span>
                     <span class="block text-[10px] text-gray-400 font-bold uppercase tracking-tighter">GPay, PhonePe, Paytm, Any UPI app</span>
                  </div>
                  <div v-if="bookingStore.paymentMethod === 'upi'" class="text-blue-600">
                     <CheckCircle2 class="w-6 h-6" />
                  </div>
               </label>
               
               <!-- Card -->
               <label 
                 class="flex items-center p-5 bg-white border-2 rounded-2xl cursor-pointer transition-all duration-300 relative group overflow-hidden"
                 :class="bookingStore.paymentMethod === 'card' ? 'border-blue-600 bg-blue-50/20' : 'border-gray-100 hover:border-blue-200'"
               >
                  <input type="radio" v-model="bookingStore.paymentMethod" value="card" class="hidden" />
                  <div class="w-12 h-12 bg-gray-50 rounded-2xl flex items-center justify-center mr-4 group-hover:scale-110 transition">
                     <CreditCard class="w-6 h-6 text-purple-600" />
                  </div>
                  <div class="flex-1">
                     <span class="block font-black text-gray-900 text-sm uppercase">Card Payment</span>
                     <span class="block text-[10px] text-gray-400 font-bold uppercase tracking-tighter">Debit / Credit • Visa, Master, RuPay</span>
                  </div>
                  <div v-if="bookingStore.paymentMethod === 'card'" class="text-blue-600">
                     <CheckCircle2 class="w-6 h-6" />
                  </div>
               </label>
               
               <!-- Cash -->
               <label 
                 class="flex items-center p-5 bg-white border-2 rounded-2xl cursor-pointer transition-all duration-300 relative group overflow-hidden"
                 :class="bookingStore.paymentMethod === 'cash' ? 'border-blue-600 bg-blue-50/20' : 'border-gray-100 hover:border-blue-200'"
               >
                  <input type="radio" v-model="bookingStore.paymentMethod" value="cash" class="hidden" />
                  <div class="w-12 h-12 bg-gray-50 rounded-2xl flex items-center justify-center mr-4 group-hover:scale-110 transition">
                     <Banknote class="w-6 h-6 text-green-600" />
                  </div>
                  <div class="flex-1">
                     <span class="block font-black text-gray-900 text-sm uppercase">Cash on Delivery</span>
                     <span class="block text-[10px] text-gray-400 font-bold uppercase tracking-tighter">Pay our technician after service</span>
                  </div>
                  <div v-if="bookingStore.paymentMethod === 'cash'" class="text-blue-600">
                     <CheckCircle2 class="w-6 h-6" />
                  </div>
               </label>
            </div>
         </section>
         
         <div class="flex items-start gap-3 bg-gray-900 p-5 rounded-3xl text-xs text-white shadow-lg">
             <Info class="w-5 h-5 text-blue-400 flex-shrink-0" />
             <p class="leading-relaxed font-medium opacity-80">
               Your booking is backed by <strong>Doorstep Warranty</strong>. Secure transactions and verified technicians only.
               <span class="block mt-1 text-[10px] text-gray-400">By proceeding, you agree to our Terms of Service.</span>
             </p>
         </div>
      </main>

      <!-- Footer Action -->
      <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 p-4 pb-8 z-50 md:pl-64">
         <div class="max-w-7xl mx-auto flex flex-col gap-4">
            <button 
              @click="confirmBooking"
              :disabled="bookingStore.loading"
              class="w-full bg-blue-600 text-white px-8 py-5 rounded-3xl font-black text-lg shadow-xl shadow-blue-200 hover:bg-blue-700 transition-all disabled:opacity-70 flex items-center justify-center gap-3 active:scale-95"
            >
               <Loader2 v-if="bookingStore.loading" class="animate-spin w-6 h-6" />
               {{ getButtonText }}
            </button>
         </div>
      </div>
    </div>
  </BaseLayout>
</template>
