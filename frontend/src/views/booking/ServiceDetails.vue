<script setup>
import { ref } from 'vue'
import { ChevronLeft, Ticket, Check, CheckCircle, Clock, ShieldCheck } from 'lucide-vue-next'
import BaseLayout from '../../components/BaseLayout.vue'
import { useBookingStore } from '../../stores/booking'

const bookingStore = useBookingStore()

const couponCode = ref('')
const loadingCoupon = ref(false)
const couponError = ref('')

const availableAddons = [
   { id: '1', name: 'Premium Tempered Glass', description: '9H Hardness Protection', price: 499 },
   { id: '2', name: 'Carbon Fiber Back Skin', description: 'Scratch & Fingerprint protection', price: 299 }
]

const isAddonSelected = (addon) => {
   return bookingStore.selectedAddons.some(a => a.id === addon.id)
}

const applyCoupon = async () => {
   if (!couponCode.value) return
   // This would be bookingStore.applyCoupon(couponCode.value)
}

const applyCouponCode = async (code) => {
    couponCode.value = code
}
</script>

<template>
  <BaseLayout>
    <div class="bg-gray-50 min-h-screen pb-24">
      <!-- Header -->
      <header class="bg-white sticky top-0 z-40 border-b border-gray-100 px-4 py-3 flex items-center space-x-3">
        <button @click="$router.back()" class="p-2 -ml-2 rounded-full hover:bg-gray-100">
          <ChevronLeft class="w-6 h-6 text-gray-600" />
        </button>
        <div class="flex-1">
          <h1 class="text-lg font-bold text-gray-900">Service Details</h1>
          <p class="text-xs text-gray-500">Step 4 of 7</p>
        </div>
        <div class="text-sm font-medium text-blue-600">4/7</div>
      </header>

      <main class="px-4 py-4 space-y-6">
        <!-- Summary Card -->
        <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100 flex items-center space-x-4">
            <img 
              v-if="bookingStore.selectedModel?.image_url" 
              :src="bookingStore.selectedModel.image_url" 
              class="w-12 h-12 object-contain"
            />
            <div class="flex-1">
               <h3 class="font-bold text-gray-900 text-sm">{{ bookingStore.selectedModel?.model_name }}</h3>
               <p class="text-xs text-blue-600 font-medium">{{ bookingStore.selectedService?.service_name }}</p>
            </div>
            <button @click="$router.push('/booking/select-service')" class="text-xs text-gray-500 underline">Change</button>
        </div>

        <!-- Service Info -->
        <div class="grid grid-cols-2 gap-3">
          <div class="bg-white p-3 rounded-xl border border-gray-100 flex items-center space-x-3">
            <div class="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center">
              <Clock class="w-4 h-4 text-blue-600" />
            </div>
            <div>
              <p class="text-[10px] text-gray-500 uppercase font-bold">Time</p>
              <p class="text-xs font-bold text-gray-900">{{ bookingStore.pricingDetails?.estimated_time_min }}-{{ bookingStore.pricingDetails?.estimated_time_max }} min</p>
            </div>
          </div>
          <div class="bg-white p-3 rounded-xl border border-gray-100 flex items-center space-x-3">
            <div class="w-8 h-8 rounded-lg bg-green-50 flex items-center justify-center">
              <ShieldCheck class="w-4 h-4 text-green-600" />
            </div>
            <div>
              <p class="text-[10px] text-gray-500 uppercase font-bold">Warranty</p>
              <p class="text-xs font-bold text-gray-900">{{ bookingStore.pricingDetails?.warranty_months }} Months</p>
            </div>
          </div>
        </div>

        <!-- Pricing Card -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
           <div class="p-5">
              <h3 class="text-xs font-bold text-gray-400 mb-4 uppercase tracking-widest">Pricing Breakdown</h3>
              
              <div class="space-y-3 text-sm">
                 <div class="flex justify-between text-gray-600">
                    <span>{{ bookingStore.selectedService?.service_name }} Part</span>
                    <span>₹{{ Math.round(bookingStore.pricingDetails?.part_cost || 0).toLocaleString() }}</span>
                 </div>
                 <div class="flex justify-between text-gray-600">
                    <span>Professional Labor</span>
                    <span>₹{{ Math.round(bookingStore.pricingDetails?.labor_cost || 0).toLocaleString() }}</span>
                 </div>
                 <div v-if="bookingStore.pricingDetails?.extra_charges > 0" class="flex justify-between text-gray-600">
                    <span>Other Charges</span>
                    <span>₹{{ Math.round(bookingStore.pricingDetails?.extra_charges).toLocaleString() }}</span>
                 </div>
                 
                 <div class="my-2 border-t border-dashed border-gray-200"></div>
                 
                 <div v-if="bookingStore.appliedCoupon" class="flex justify-between text-green-600 font-medium">
                    <span class="flex items-center"><Ticket class="w-4 h-4 mr-2" /> Coupon Discount</span>
                    <span>-₹{{ bookingStore.appliedCoupon.discount_value }}</span>
                 </div>

                 <div v-for="addon in bookingStore.selectedAddons" :key="addon.id" class="flex justify-between text-blue-600">
                    <span>Add-on: {{ addon.name }}</span>
                    <span>+₹{{ addon.price }}</span>
                 </div>
              </div>
           </div>
           
           <div class="bg-gray-900 px-5 py-4 flex justify-between items-center">
              <span class="text-sm font-medium text-gray-400">Total payable</span>
              <span class="text-xl font-bold text-white">₹{{ Math.round(bookingStore.finalPrice).toLocaleString() }}</span>
           </div>
        </div>

        <!-- Addons -->
        <section>
           <h3 class="font-bold text-gray-800 mb-3 ml-1 text-sm">Recommended Add-ons</h3>
           <div class="grid grid-cols-1 gap-3">
              <div 
                v-for="addon in availableAddons" 
                :key="addon.id"
                class="bg-white p-4 rounded-xl border flex items-center justify-between cursor-pointer transition-all active:scale-95"
                :class="isAddonSelected(addon) ? 'border-blue-500 bg-blue-50' : 'border-gray-200'"
                @click="bookingStore.toggleAddon(addon)"
              >
                 <div class="flex items-center space-x-3">
                    <div 
                      class="w-6 h-6 rounded-lg border-2 flex items-center justify-center"
                      :class="isAddonSelected(addon) ? 'bg-blue-600 border-blue-600' : 'border-gray-300 bg-white'"
                    >
                       <Check v-if="isAddonSelected(addon)" class="w-4 h-4 text-white" />
                    </div>
                    <div>
                       <h4 class="text-sm font-bold text-gray-900">{{ addon.name }}</h4>
                       <p class="text-[10px] text-gray-500">{{ addon.description }}</p>
                    </div>
                 </div>
                 <span class="text-sm font-bold text-gray-700">₹{{ addon.price }}</span>
              </div>
           </div>
        </section>

        <!-- Coupon -->
        <section>
           <h3 class="font-bold text-gray-800 mb-3 ml-1 text-sm">Have a Coupon?</h3>
           <div class="flex gap-2">
              <input 
                v-model="couponCode"
                type="text" 
                placeholder="Enter code (e.g. WELCOME500)" 
                class="flex-1 px-4 py-3 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 bg-white"
              />
              <button 
                class="bg-blue-600 text-white px-6 py-3 rounded-xl text-sm font-bold shadow-md shadow-blue-100"
              >
                Apply
              </button>
           </div>
        </section>

      </main>

      <!-- Footer Action -->
      <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 p-4 pb-8 z-50 md:pl-64">
         <div class="max-w-7xl mx-auto flex items-center justify-between">
            <div class="flex flex-col">
               <p class="text-[10px] text-gray-400 font-bold uppercase tracking-wider">Estimated Total</p>
               <p class="text-xl font-black text-gray-900">₹{{ Math.round(bookingStore.finalPrice).toLocaleString() }}</p>
            </div>
            <button 
              @click="$router.push('/booking/schedule')"
              class="bg-blue-600 text-white px-10 py-3.5 rounded-xl font-bold shadow-lg shadow-blue-200 hover:bg-blue-700 transition active:scale-95"
            >
               Choose Slot
            </button>
         </div>
      </div>
    </div>
  </BaseLayout>
</template>
