<template>
  <BaseLayout>
    <div class="bg-gray-50 min-h-screen pb-24">
      <!-- Header -->
      <header class="bg-white sticky top-0 z-40 border-b border-gray-100 px-4 py-3 flex items-center space-x-3">
        <button @click="$router.back()" class="p-2 -ml-2 rounded-full hover:bg-gray-100">
          <ChevronLeft class="w-6 h-6 text-gray-600" />
        </button>
        <div class="flex-1">
          <h1 class="text-lg font-bold text-gray-900">Select Location</h1>
          <p class="text-xs text-gray-500">Step 6 of 7</p>
        </div>
        <div class="text-sm font-medium text-blue-600">6/7</div>
      </header>
      
      <!-- Progress Indicator -->
      <div class="bg-blue-600 h-1 w-5/6"></div>

      <main class="px-4 py-6 space-y-6">
         <!-- Loading State -->
         <div v-if="bookingStore.loading && !isSubmitting" class="py-20 flex flex-col items-center justify-center">
            <Loader2 class="w-10 h-10 text-blue-600 animate-spin mb-4" />
            <p class="text-gray-500 font-medium">Loading your addresses...</p>
         </div>

         <!-- Saved Addresses -->
         <section v-else-if="bookingStore.addresses.length > 0">
            <h3 class="font-black text-gray-900 mb-4 px-1 text-sm uppercase tracking-widest flex items-center gap-2">
               <MapPin class="w-4 h-4 text-blue-600" /> Saved Locations
            </h3>
            <div class="space-y-4">
               <div 
                 v-for="addr in bookingStore.addresses" 
                 :key="addr.id"
                 @click="selectAddress(addr)"
                 class="p-5 rounded-2xl border-2 cursor-pointer relative transition-all duration-300 bg-white"
                 :class="isSelected(addr) ? 'border-blue-600 bg-blue-50/30' : 'border-gray-100 hover:border-blue-200'"
               >
                  <div class="flex justify-between items-start mb-2">
                     <span 
                       class="px-2 py-0.5 rounded-lg text-[10px] font-black uppercase tracking-wider"
                       :class="getLabelClass(addr.label)"
                     >
                       {{ addr.label }}
                     </span>
                     <div v-if="isSelected(addr)" class="bg-blue-600 text-white p-1 rounded-full">
                        <CheckCircle class="w-4 h-4" />
                     </div>
                  </div>
                  
                  <p class="text-sm text-gray-900 font-bold leading-tight">{{ addr.address_line1 }}</p>
                  <p class="text-xs text-gray-500 mt-1">{{ addr.address_line2 }}</p>
                  <p class="text-xs text-gray-400 mt-2 flex items-center gap-1 font-medium">
                     <Navigation class="w-3 h-3" /> {{ addr.city }}, {{ addr.pincode }}
                  </p>
               </div>
            </div>
         </section>
         
         <!-- Empty State -->
         <div v-else-if="!showAddForm" class="py-12 px-6 text-center bg-white rounded-3xl border border-dashed border-gray-200">
            <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4">
               <MapPin class="w-8 h-8 text-gray-300" />
            </div>
            <h4 class="font-bold text-gray-900">No addresses yet</h4>
            <p class="text-xs text-gray-500 mt-1">Add your service location to continue</p>
         </div>
         
         <!-- Add New Button -->
         <button 
           v-if="!showAddForm"
           @click="showAddForm = true"
           class="w-full py-4 border-2 border-dashed border-blue-200 rounded-2xl text-blue-600 font-black text-sm bg-blue-50/50 hover:bg-blue-50 transition-all flex items-center justify-center gap-3 active:scale-95"
         >
            <Plus class="w-5 h-5" /> ADD NEW ADDRESS
         </button>

         <!-- Add Address Form -->
         <section v-if="showAddForm" class="bg-white p-6 rounded-3xl border border-gray-100 shadow-xl shadow-gray-200/50 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <div class="flex items-center justify-between mb-6">
               <h3 class="font-black text-gray-900 text-lg">New Location</h3>
               <button @click="showAddForm = false" class="p-2 bg-gray-50 rounded-full text-gray-400 hover:bg-gray-100">
                  <X class="w-5 h-5" />
               </button>
            </div>
            
            <form @submit.prevent="saveNewAddress" class="space-y-4">
               <div>
                  <label class="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2 px-1">Label</label>
                  <div class="flex gap-2">
                     <button 
                       v-for="type in ['Home', 'Office', 'Other']" 
                       :key="type" 
                       type="button"
                       @click="newAddress.label = type"
                       class="flex-1 py-2 px-3 rounded-xl text-xs font-bold transition-all border-2"
                       :class="newAddress.label === type ? 'bg-blue-600 border-blue-600 text-white' : 'bg-white border-gray-100 text-gray-500'"
                     >
                        {{ type }}
                     </button>
                  </div>
               </div>

               <div>
                  <label class="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2 px-1">Flat / Building / Plot <span class="text-red-500">*</span></label>
                  <input v-model="newAddress.address_line1" type="text" required class="w-full px-4 py-3 bg-gray-50 border-none rounded-2xl text-sm font-bold focus:ring-2 focus:ring-blue-600/20" placeholder="e.g. A-102, Silver Springs" />
               </div>
               
               <div>
                  <label class="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2 px-1">Street / Area</label>
                  <input v-model="newAddress.address_line2" type="text" class="w-full px-4 py-3 bg-gray-50 border-none rounded-2xl text-sm font-bold focus:ring-2 focus:ring-blue-600/20" placeholder="e.g. Model Town" />
               </div>
               
               <div class="grid grid-cols-2 gap-4">
                  <div>
                     <label class="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2 px-1">City <span class="text-red-500">*</span></label>
                     <input v-model="newAddress.city" type="text" required class="w-full px-4 py-3 bg-gray-50 border-none rounded-2xl text-sm font-bold focus:ring-2 focus:ring-blue-600/20" />
                  </div>
                  <div>
                     <label class="block text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2 px-1">Pincode <span class="text-red-500">*</span></label>
                     <input v-model="newAddress.pincode" type="text" required maxlength="6" pattern="\d{6}" class="w-full px-4 py-3 bg-gray-50 border-none rounded-2xl text-sm font-bold focus:ring-2 focus:ring-blue-600/20" placeholder="600001" />
                  </div>
               </div>

               <div class="flex items-center pt-2">
                  <input v-model="newAddress.is_default" id="default-addr" type="checkbox" class="h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-200 rounded-lg bg-gray-50" />
                  <label for="default-addr" class="ml-3 block text-sm font-bold text-gray-700">
                     Set as default address
                  </label>
               </div>
               
               <div class="pt-4">
                  <button 
                    type="submit" 
                    :disabled="isSubmitting"
                    class="w-full py-4 bg-blue-600 text-white rounded-2xl text-sm font-black hover:bg-blue-700 shadow-lg shadow-blue-200 flex items-center justify-center gap-2"
                  >
                     <Loader2 v-if="isSubmitting" class="w-4 h-4 animate-spin" />
                     {{ isSubmitting ? 'SAVING...' : 'SAVE ADDRESS' }}
                  </button>
               </div>
            </form>
         </section>
      </main>

      <!-- Footer Action -->
      <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 p-4 pb-8 z-50 md:pl-64">
         <div class="max-w-7xl mx-auto">
            <button 
              @click="confirmAddressSelection"
              :disabled="!bookingStore.selectedAddress || bookingStore.loading"
              class="w-full bg-blue-600 text-white px-8 py-4 rounded-2xl font-black text-lg shadow-xl shadow-blue-200 hover:bg-blue-700 transition-all disabled:opacity-50 active:scale-95"
            >
               PROCEED
            </button>
         </div>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ChevronLeft, Edit2, CheckCircle, Plus, X, Loader2, MapPin, Navigation } from 'lucide-vue-next'
import BaseLayout from '../../components/BaseLayout.vue'
import { useBookingStore } from '../../stores/booking'

const router = useRouter()
const bookingStore = useBookingStore()

const showAddForm = ref(false)
const isSubmitting = ref(false)

const newAddress = ref({
   label: 'Home',
   address_line1: '',
   address_line2: '',
   city: 'Tiruppur',
   state: 'Tamil Nadu',
   pincode: '',
   is_default: false
})

onMounted(() => {
   bookingStore.fetchAddresses()
})

const getLabelClass = (label) => {
   switch(label) {
      case 'Home': return 'bg-blue-100 text-blue-700'
      case 'Office': return 'bg-gray-100 text-gray-700'
      default: return 'bg-yellow-100 text-yellow-700'
   }
}

const isSelected = (addr) => {
   return bookingStore.selectedAddress?.id === addr.id
}

const selectAddress = (addr) => {
   bookingStore.selectedAddress = addr
}

const saveNewAddress = async () => {
   if (newAddress.value.pincode.length !== 6) {
      return
   }
   
   isSubmitting.value = true
   const result = await bookingStore.addAddress(newAddress.value)
   isSubmitting.value = false

   if (result.success) {
      showAddForm.value = false
      newAddress.value = {
         label: 'Home',
         address_line1: '',
         address_line2: '',
         city: 'Tiruppur',
         state: 'Tamil Nadu',
         pincode: '',
         is_default: false
      }
   } else {
      alert(result.message)
   }
}

const confirmAddressSelection = () => {
   router.push('/booking/device-info')
}
</script>
