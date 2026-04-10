<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ChevronLeft, Camera, X, ShieldCheck, Shield, Smartphone, Palette, HardDrive } from 'lucide-vue-next'
import BaseLayout from '../../components/BaseLayout.vue'
import { useBookingStore } from '../../stores/booking'

const router = useRouter()
const bookingStore = useBookingStore()

const photoLabels = ['Front View', 'Back View', 'Damaged Area', 'Other']
// Initialize with nulls or existing photos from store
const devicePhotos = ref([{ url: bookingStore.devicePhotos[0] || null }, { url: bookingStore.devicePhotos[1] || null }, { url: bookingStore.devicePhotos[2] || null }, { url: bookingStore.devicePhotos[3] || null }])
const fileInputs = ref([])

const storageOptions = ['64GB', '128GB', '256GB', '512GB', '1TB']
const colorOptions = ['Space Gray', 'Silver', 'Gold', 'Graphite', 'Sierra Blue', 'Deep Purple']

const triggerUpload = (index) => {
   fileInputs.value[index].click()
}

const handleFileChange = (event, index) => {
   const file = event.target.files[0]
   if (file) {
      const url = URL.createObjectURL(file)
      devicePhotos.value[index].url = url
      bookingStore.devicePhotos[index] = url 
   }
}

const removePhoto = (index) => {
   devicePhotos.value[index].url = null
   bookingStore.devicePhotos[index] = null
}

const canProceed = computed(() => {
   const hasPhoto = devicePhotos.value.some(p => p.url !== null)
   const hasCondition = bookingStore.deviceConditionDescription && bookingStore.deviceConditionDescription.trim().length > 0
   return hasPhoto && hasCondition && bookingStore.privacyAgreementSigned
})

const goToPayment = () => {
    router.push('/booking/payment')
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
          <h1 class="text-lg font-bold text-gray-900">Device Details</h1>
          <p class="text-xs text-gray-500">Step 7 of 7</p>
        </div>
        <div class="text-sm font-medium text-blue-600">7/7</div>
      </header>

      <main class="px-4 py-6 space-y-8">
         <!-- Device Config -->
         <section class="grid grid-cols-1 gap-6">
            <div>
               <h3 class="font-black text-gray-900 mb-4 px-1 text-xs uppercase tracking-widest flex items-center gap-2">
                  <HardDrive class="w-4 h-4 text-blue-600" /> Storage Capacity
               </h3>
               <div class="flex flex-wrap gap-2">
                  <button 
                    v-for="opt in storageOptions" 
                    :key="opt"
                    @click="bookingStore.deviceStorage = opt"
                    class="px-4 py-2.5 rounded-xl text-xs font-bold transition-all border-2"
                    :class="bookingStore.deviceStorage === opt ? 'bg-blue-600 border-blue-600 text-white' : 'bg-white border-gray-100 text-gray-500 hover:border-blue-200'"
                  >
                     {{ opt }}
                  </button>
               </div>
            </div>

            <div>
               <h3 class="font-black text-gray-900 mb-4 px-1 text-xs uppercase tracking-widest flex items-center gap-2">
                  <Palette class="w-4 h-4 text-blue-600" /> Device Color
               </h3>
               <div class="flex flex-wrap gap-2">
                  <button 
                    v-for="opt in colorOptions" 
                    :key="opt"
                    @click="bookingStore.deviceColor = opt"
                    class="px-4 py-2.5 rounded-xl text-xs font-bold transition-all border-2"
                    :class="bookingStore.deviceColor === opt ? 'bg-blue-600 border-blue-600 text-white' : 'bg-white border-gray-100 text-gray-500 hover:border-blue-200'"
                  >
                     {{ opt }}
                  </button>
               </div>
            </div>
         </section>

         <!-- Photo Upload -->
         <section>
            <h3 class="font-black text-gray-900 mb-1 px-1 text-xs uppercase tracking-widest flex items-center gap-2">
               <Camera class="w-4 h-4 text-blue-600" /> Device Photos
            </h3>
            <p class="text-[10px] text-gray-400 font-medium px-1 mb-4">Upload at least one photo of the damaged area</p>
            
            <div class="grid grid-cols-2 gap-4">
               <div 
                  v-for="(photo, index) in devicePhotos" 
                  :key="index"
                  class="aspect-square rounded-2xl border-2 border-dashed flex flex-col items-center justify-center transition-all bg-white cursor-pointer relative overflow-hidden group"
                  :class="photo.url ? 'border-blue-600' : 'border-gray-200 hover:border-blue-300 hover:bg-gray-50'"
                  @click="triggerUpload(index)"
               >
                  <template v-if="photo.url">
                     <img :src="photo.url" class="w-full h-full object-cover" />
                     <div class="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition"></div>
                     <button @click.stop="removePhoto(index)" class="absolute top-2 right-2 bg-white text-red-500 rounded-full p-1.5 shadow-lg active:scale-95">
                        <X class="w-4 h-4" />
                     </button>
                  </template>
                  <template v-else>
                     <div class="p-3 bg-gray-50 rounded-2xl mb-2 group-hover:scale-110 transition">
                        <Camera class="w-6 h-6 text-gray-400" />
                     </div>
                     <span class="text-[10px] text-gray-400 font-black uppercase tracking-tighter">{{ photoLabels[index] }}</span>
                  </template>
                  
                  <input 
                     type="file" 
                     :ref="el => fileInputs[index] = el" 
                     class="hidden" 
                     accept="image/*"
                     @change="handleFileChange($event, index)"
                  />
               </div>
            </div>
         </section>

         <!-- IMEI -->
         <section>
            <h3 class="font-black text-gray-900 mb-3 px-1 text-xs uppercase tracking-widest flex items-center gap-2">
               <Smartphone class="w-4 h-4 text-blue-600" /> Device IMEI
            </h3>
            <div class="relative">
               <input 
                  v-model="bookingStore.deviceIMEI"
                  type="text" 
                  placeholder="15-digit IMEI (Optional)" 
                  maxlength="15"
                  class="w-full px-5 py-4 rounded-2xl bg-white border border-gray-100 font-bold text-sm focus:outline-none focus:ring-4 focus:ring-blue-600/5 focus:border-blue-600 transition"
               />
               <button class="absolute right-4 top-1/2 -translate-y-1/2 text-[10px] font-black text-blue-600 uppercase">How to find?</button>
            </div>
         </section>
         
         <!-- Condition Description -->
         <section>
            <h3 class="font-black text-gray-900 mb-3 px-1 text-xs uppercase tracking-widest">Problem Description</h3>
            <textarea 
               v-model="bookingStore.deviceConditionDescription"
               rows="3" 
               placeholder="Tell us exactly what's wrong (e.g. Screen flickering, lines on display...)" 
               class="w-full px-5 py-4 rounded-2xl bg-white border border-gray-100 font-bold text-sm focus:outline-none focus:ring-4 focus:ring-blue-600/5 focus:border-blue-600 transition placeholder:text-gray-300"
            ></textarea>
         </section>

         <!-- Data Safety -->
         <section class="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm space-y-5">
            <h3 class="font-black text-gray-900 text-sm flex items-center uppercase tracking-widest">
               <ShieldCheck class="w-5 h-5 text-green-500 mr-2" />
               Safety & Privacy
            </h3>
            
            <label class="flex items-start space-x-4 cursor-pointer group">
               <div class="relative flex items-center">
                  <input v-model="bookingStore.dataBackupRequested" type="checkbox" class="h-6 w-6 text-blue-600 rounded-lg border-2 border-gray-200 focus:ring-blue-600/20 bg-gray-50 cursor-pointer" />
               </div>
               <div>
                  <span class="text-sm font-black text-gray-800 group-hover:text-blue-600 transition">Assisted Backup</span>
                  <p class="text-[10px] text-gray-400 font-medium">Technician will help save your data before proceeding</p>
               </div>
            </label>
            
            <div class="border-t border-gray-100"></div>
            
            <label class="flex items-start space-x-4 cursor-pointer group">
               <div class="relative flex items-center">
                  <input v-model="bookingStore.privacyAgreementSigned" type="checkbox" class="h-6 w-6 text-blue-600 rounded-lg border-2 border-gray-200 focus:ring-blue-600/20 bg-gray-50 cursor-pointer" />
               </div>
               <span class="text-xs font-bold text-gray-500 leading-normal">
                  I agree to the <a href="#" class="text-blue-600 hover:underline">Privacy Policy</a> and authorize verified technicians to handle my device.
               </span>
            </label>
         </section>
         
         <!-- Protection Plan -->
         <section class="bg-gray-900 rounded-3xl p-6 text-white shadow-xl shadow-gray-200 overflow-hidden relative">
            <div class="absolute -right-4 -top-4 w-24 h-24 bg-blue-500/10 rounded-full blur-2xl"></div>
            <div class="flex justify-between items-center mb-4 relative z-10">
               <h3 class="font-black flex items-center gap-2"><Shield class="w-5 h-5 text-yellow-500" /> Device Care+</h3>
               <label class="relative inline-flex items-center cursor-pointer">
                 <input type="checkbox" v-model="bookingStore.deviceInsuranceOpted" class="sr-only peer">
                 <div class="w-12 h-6.5 bg-gray-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[4px] after:left-[4px] after:bg-white after:rounded-full after:h-4.5 after:w-4.5 after:transition-all peer-checked:bg-blue-600 border-2 border-gray-700"></div>
               </label>
            </div>
            <p class="text-[11px] text-gray-400 mb-4 leading-relaxed">Protect your device from accidental damage or liquid spills during service. Includes 1-year coverage.</p>
            <div class="flex items-center justify-between">
               <span class="text-xs font-black text-yellow-500 tracking-widest uppercase">Only ₹199 extra</span>
               <span class="bg-white/10 px-3 py-1 rounded-full text-[10px] font-black uppercase">Most Popular</span>
            </div>
         </section>

      </main>

      <!-- Footer Action -->
      <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 p-4 pb-8 z-50 md:pl-64">
         <div class="max-w-7xl mx-auto">
            <button 
              @click="goToPayment"
              :disabled="!canProceed"
              class="w-full bg-blue-600 text-white px-8 py-4 rounded-2xl font-black text-lg shadow-xl shadow-blue-200 hover:bg-blue-700 transition-all disabled:opacity-50 active:scale-95"
            >
               PROCEED TO PAYMENT
            </button>
         </div>
      </div>
    </div>
  </BaseLayout>
</template>
