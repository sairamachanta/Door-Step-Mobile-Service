<template>
  <BaseLayout>
    <div class="bg-gray-50 min-h-screen pb-24">
      <!-- Header -->
      <header class="bg-white sticky top-0 z-40 border-b border-gray-100 px-4 py-3 flex items-center space-x-3">
        <button @click="$router.back()" class="p-2 -ml-2 rounded-full hover:bg-gray-100">
          <ChevronLeft class="w-6 h-6 text-gray-600" />
        </button>
        <div class="flex-1">
          <h1 class="text-lg font-bold text-gray-900">Schedule Repair</h1>
          <p class="text-xs text-gray-500">Step 5 of 7</p>
        </div>
        <div class="text-sm font-medium text-blue-600">5/7</div>
      </header>

      <main class="px-4 py-4 space-y-6">
         <!-- Date Selection -->
         <section>
            <h3 class="font-bold text-gray-800 mb-3 ml-1 text-sm uppercase tracking-wider">Select Date</h3>
            <div class="flex space-x-3 overflow-x-auto pb-4 scrollbar-hide">
               <div 
                 v-for="date in dates" 
                 :key="date.fullDate"
                 @click="selectDate(date)"
                 class="min-w-[75px] py-4 rounded-2xl border flex flex-col items-center justify-center cursor-pointer transition-all duration-300 relative"
                 :class="isSelectedDate(date) ? 'bg-blue-600 border-blue-600 text-white shadow-lg shadow-blue-200 scale-105' : 'bg-white border-gray-100 text-gray-600 hover:border-blue-300'"
               >
                  <span class="text-[10px] font-bold uppercase mb-1 opacity-80">{{ date.dayName }}</span>
                  <span class="text-xl font-black">{{ date.dayNumber }}</span>
                  <div v-if="date.available" class="w-1.5 h-1.5 rounded-full mt-2" :class="isSelectedDate(date) ? 'bg-white' : 'bg-green-500'"></div>
               </div>
            </div>
         </section>

         <!-- Time Slots -->
         <section>
            <h3 class="font-bold text-gray-800 mb-3 ml-1 text-sm uppercase tracking-wider">Available Slots</h3>
            
            <div v-if="loadingSlots" class="py-12 flex flex-col items-center justify-center bg-white rounded-2xl border border-gray-100">
               <Loader2 class="animate-spin h-8 w-8 text-blue-600 mb-3" />
               <p class="text-gray-500 text-xs font-medium">Checking availability...</p>
            </div>
            
            <div v-else-if="timeSlots.length > 0" class="grid grid-cols-2 gap-3">
               <div 
                 v-for="slot in timeSlots" 
                 :key="slot.id"
                 @click="selectTimeSlot(slot)"
                 class="p-4 rounded-2xl border flex flex-col items-center justify-center cursor-pointer transition-all duration-300 text-center relative overflow-hidden group"
                 :class="[
                    !slot.is_active ? 'bg-gray-50 border-gray-100 opacity-60 cursor-not-allowed' :
                    isSelectedTime(slot) ? 'bg-blue-50 border-blue-500 text-blue-700 shadow-inner' : 'bg-white border-gray-100 hover:border-blue-200'
                 ]"
               >
                  <div v-if="isSelectedTime(slot)" class="absolute top-0 right-0 p-1 bg-blue-500 text-white rounded-bl-xl">
                      <CheckCircle class="w-3 h-3" />
                  </div>

                  <Clock class="w-5 h-5 mb-2" :class="isSelectedTime(slot) ? 'text-blue-600' : 'text-gray-400 group-hover:text-blue-400'" />
                  <span class="text-xs font-bold leading-tight">{{ slot.slot_time }}</span>
                  <p class="text-[9px] mt-1 font-bold uppercase tracking-tighter" :class="slot.is_active ? 'text-green-500' : 'text-red-400'">
                     {{ slot.is_active ? 'Bookable' : 'Unavailable' }}
                  </p>
               </div>
            </div>

            <div v-else class="py-10 text-center bg-white rounded-2xl border border-dashed border-gray-200">
                <p class="text-gray-400 text-xs font-medium">No slots found for this date.</p>
            </div>
         </section>

         <!-- Service Location -->
         <section>
            <h3 class="font-bold text-gray-800 mb-3 ml-1 text-sm uppercase tracking-wider">Repair Mode</h3>
            <div class="grid grid-cols-1 gap-3">
               <div 
                 @click="setLocation('doorstep')"
                 class="p-4 rounded-2xl border cursor-pointer relative flex items-center gap-4 transition-all duration-300 group"
                 :class="bookingStore.serviceLocation === 'doorstep' ? 'bg-blue-50 border-blue-500 shadow-sm' : 'bg-white border-gray-100 hover:bg-gray-50'"
               >
                  <div class="w-12 h-12 rounded-xl bg-blue-100 flex items-center justify-center text-blue-600 group-hover:scale-110 transition">
                     <Home class="w-6 h-6" />
                  </div>
                  <div class="flex-1">
                     <h4 class="font-black text-gray-900 text-sm">Doorstep Service</h4>
                     <p class="text-[11px] text-gray-500">Professional visits your home/office</p>
                  </div>
                  <div v-if="bookingStore.serviceLocation === 'doorstep'" class="text-blue-600">
                     <CheckCircle class="w-6 h-6" />
                  </div>
               </div>

               <div 
                 @click="setLocation('service_center')"
                 class="p-4 rounded-2xl border cursor-pointer relative flex items-center gap-4 transition-all duration-300 group"
                 :class="bookingStore.serviceLocation === 'service_center' ? 'bg-blue-50 border-blue-500 shadow-sm' : 'bg-white border-gray-100 hover:bg-gray-50'"
               >
                  <div class="w-12 h-12 rounded-xl bg-gray-100 flex items-center justify-center text-gray-600 group-hover:scale-110 transition">
                     <MapPin class="w-6 h-6" />
                  </div>
                  <div class="flex-1">
                     <h4 class="font-black text-gray-900 text-sm">Service Center</h4>
                     <p class="text-[11px] text-gray-500">Drop off at our verified center</p>
                  </div>
                  <div v-if="bookingStore.serviceLocation === 'service_center'" class="text-blue-600">
                     <CheckCircle class="w-6 h-6" />
                  </div>
               </div>
            </div>
         </section>
      </main>

      <!-- Footer Action -->
      <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 p-4 pb-8 z-50 md:pl-64">
         <div class="max-w-7xl mx-auto">
            <button 
              @click="proceedNext"
              :disabled="!canProceed"
              class="w-full bg-blue-600 text-white px-8 py-4 rounded-2xl font-black text-lg shadow-lg shadow-blue-200 hover:bg-blue-700 transition active:scale-95 disabled:opacity-50 disabled:active:scale-100"
            >
               Confirm Selection
            </button>
         </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ChevronLeft, Clock, CheckCircle, Home, MapPin, Loader2 } from 'lucide-vue-next'
import dayjs from 'dayjs'
import axios from 'axios'
import BaseLayout from '../../components/BaseLayout.vue'
import { useBookingStore } from '../../stores/booking'

const router = useRouter()
const bookingStore = useBookingStore()
const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const dates = ref([])
const timeSlots = ref([])
const loadingSlots = ref(false)

onMounted(() => {
   generateDates()
   
   if (bookingStore.selectedDate) {
       fetchTimeSlots(bookingStore.selectedDate)
   } else {
       // Auto select today
       const today = dayjs().format('YYYY-MM-DD')
       bookingStore.selectedDate = today
       fetchTimeSlots(today)
   }
})

const generateDates = () => {
   const today = dayjs()
   const tempDates = []
   
   for (let i = 0; i < 7; i++) {
      const date = today.add(i, 'day')
      tempDates.push({
         fullDate: date.format('YYYY-MM-DD'),
         dayName: i === 0 ? 'Today' : i === 1 ? 'Tmrrw' : date.format('ddd'),
         dayNumber: date.format('D'),
         available: true 
      })
   }
   dates.value = tempDates
}

const isSelectedDate = (date) => {
   return bookingStore.selectedDate === date.fullDate
}

const selectDate = (date) => {
   bookingStore.selectedDate = date.fullDate
   bookingStore.selectedTimeSlot = null 
   fetchTimeSlots(date.fullDate)
}

const fetchTimeSlots = async (date) => {
   loadingSlots.value = true
   try {
     const response = await axios.get(`${API_BASE}/availability`, {
       params: { date }
     })
     timeSlots.value = response.data
   } catch (err) {
     console.error('Failed to fetch slots:', err)
   } finally {
     loadingSlots.value = false
   }
}

const isSelectedTime = (slot) => {
   return bookingStore.selectedTimeSlot === slot.id
}

const selectTimeSlot = (slot) => {
   if (!slot.is_active) return
   bookingStore.selectedTimeSlot = slot.id
}

const setLocation = (loc) => {
   bookingStore.serviceLocation = loc
}

const canProceed = computed(() => {
   return bookingStore.selectedDate && bookingStore.selectedTimeSlot
})

const proceedNext = () => {
   if (bookingStore.serviceLocation === 'doorstep') {
      router.push('/booking/address')
   } else {
      router.push('/booking/device-info')
   }
}
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>
