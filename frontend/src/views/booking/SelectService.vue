<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  ChevronLeft, Smartphone, Clock, ShieldCheck, Check, 
  HelpCircle, Battery, Zap, Loader2, Camera, Volume2, 
  Mic, Monitor, Lock, Cpu, Droplets, Fingerprint, Search, Power
} from 'lucide-vue-next'
import BaseLayout from '../../components/BaseLayout.vue'
import { useBookingStore } from '../../stores/booking'

const router = useRouter()
const bookingStore = useBookingStore()

const expandedServiceId = ref(null)

onMounted(() => {
  if (!bookingStore.selectedModelId) {
    router.replace('/booking/select-model')
    return
  }
  bookingStore.fetchServices(bookingStore.selectedModelId)
})

const iconMap = {
  'Smartphone': Smartphone,
  'Battery': Battery,
  'Zap': Zap,
  'Camera': Camera,
  'Volume2': Volume2,
  'Mic': Mic,
  'Monitor': Monitor,
  'Lock': Lock,
  'Cpu': Cpu,
  'Droplets': Droplets,
  'Fingerprint': Fingerprint,
  'Search': Search,
  'Power': Power
}

const getIcon = (iconName) => {
   return iconMap[iconName] || Smartphone
}

const toggleDetails = (id) => {
   expandedServiceId.value = expandedServiceId.value === id ? null : id
}

const selectService = async (pricing) => {
   await bookingStore.fetchPricingDetails(pricing.id)
   router.push('/booking/service-details')
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
          <h1 class="text-lg font-bold text-gray-900">Select Service</h1>
          <p class="text-xs text-gray-500">{{ bookingStore.selectedModel?.model_name || 'Device' }} Repairs</p>
        </div>
        <div class="text-sm font-medium text-blue-600">3/7</div>
      </header>
      
      <!-- Device Summary -->
      <div class="bg-blue-50 px-4 py-3 flex items-center justify-between border-b border-blue-100">
         <div class="flex items-center space-x-3">
            <img 
              v-if="bookingStore.selectedModel?.image_url" 
              :src="bookingStore.selectedModel.image_url" 
              class="w-10 h-10 object-contain mix-blend-multiply"
            />
            <Smartphone v-else class="w-8 h-8 text-blue-400" />
            <div>
               <p class="text-xs text-blue-600 font-medium">Repairing</p>
               <h3 class="font-bold text-gray-800 text-sm">{{ bookingStore.selectedModel?.model_name || 'Selected Device' }}</h3>
            </div>
         </div>
         <button @click="router.push('/booking/select-model')" class="text-xs text-blue-600 font-medium underline">
            Change
         </button>
      </div>

      <main class="px-4 py-4 space-y-4">
        <div v-if="bookingStore.loading" class="flex flex-col items-center justify-center py-20">
          <Loader2 class="w-10 h-10 text-blue-500 animate-spin mb-4" />
          <p class="text-gray-500 font-medium">Loading services...</p>
        </div>

        <template v-else>
          <!-- Service Cards -->
          <div 
            v-for="pricing in bookingStore.services" 
            :key="pricing.id"
            class="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden"
          >
             <div class="p-4 flex gap-4">
                <!-- Icon -->
                <div class="w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0" :style="{ backgroundColor: pricing.service.icon_color + '20' }">
                   <component :is="getIcon(pricing.service.icon_name)" class="w-6 h-6" :style="{ color: pricing.service.icon_color }" />
                </div>
                
                <div class="flex-1">
                   <div class="flex justify-between items-start mb-1">
                      <h3 class="font-bold text-gray-900 text-sm leading-tight pr-2">{{ pricing.service.service_name }}</h3>
                      <span class="font-bold text-blue-600 text-sm">₹{{ Math.round(pricing.final_price).toLocaleString() }}</span>
                   </div>
                   
                   <div class="flex items-center text-[10px] text-gray-500 space-x-3 mb-2">
                      <span class="flex items-center"><Clock class="w-3 h-3 mr-1" /> {{ pricing.estimated_time_min }}-{{ pricing.estimated_time_max }} mins</span>
                      <span class="flex items-center text-green-600"><ShieldCheck class="w-3 h-3 mr-1" /> {{ pricing.warranty_months }}M Warranty</span>
                   </div>
                   
                   <p class="text-xs text-gray-600 line-clamp-2 mb-3">{{ pricing.service.description }}</p>
                   
                   <div class="flex gap-2">
                      <button 
                        @click="toggleDetails(pricing.id)"
                        class="flex-1 py-1.5 text-[11px] font-medium text-gray-600 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
                      >
                        {{ expandedServiceId === pricing.id ? 'Hide Details' : 'View Details' }}
                      </button>
                      <button 
                        @click="selectService(pricing)"
                        class="flex-1 py-1.5 text-[11px] font-bold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition shadow-sm"
                      >
                        Select
                      </button>
                   </div>
                </div>
             </div>
             
             <!-- Expanded Details -->
             <div v-if="expandedServiceId === pricing.id" class="bg-gray-50 px-4 py-3 border-t border-gray-100">
                 <h4 class="text-xs font-bold text-gray-700 mb-2 uppercase">Typical Symptoms:</h4>
                 <ul class="space-y-1 mb-3">
                    <li v-for="(item, idx) in pricing.service.typical_symptoms" :key="idx" class="flex items-start text-[11px] text-gray-600">
                       <Check class="w-3 h-3 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                       {{ item }}
                    </li>
                 </ul>
                 <div class="flex items-center text-[10px] text-gray-400">
                   <span class="mr-2">Part Grade: {{ pricing.part_grade.toUpperCase() }}</span>
                   <span v-if="pricing.is_doorstep_available" class="text-green-500">• Doorstep Available</span>
                 </div>
             </div>
          </div>
          
          <!-- Empty State -->
          <div v-if="bookingStore.services.length === 0" class="text-center py-10 bg-white rounded-2xl border border-dashed border-gray-200">
             <Smartphone class="w-12 h-12 text-gray-300 mx-auto mb-2" />
             <p class="text-gray-500 font-medium">No services found for this model</p>
             <button class="mt-4 text-blue-600 font-medium text-sm hover:underline">Request a custom repair</button>
          </div>

          <!-- Diagnostic Option -->
          <div class="bg-white rounded-xl border-2 border-dashed border-gray-200 p-4 flex items-center gap-4">
             <div class="w-10 h-10 rounded-full bg-yellow-50 flex items-center justify-center flex-shrink-0">
                 <HelpCircle class="w-5 h-5 text-yellow-600" />
             </div>
             <div class="flex-1">
                <h3 class="font-bold text-gray-900 text-sm leading-tight">Not sure what's wrong?</h3>
                <p class="text-[11px] text-gray-500">Book our complete diagnostic service. Refundable if you proceed with repair.</p>
             </div>
             <button class="px-3 py-1.5 bg-yellow-100 text-yellow-700 text-xs font-bold rounded-lg hover:bg-yellow-200">
                Check
             </button>
          </div>
        </template>
      </main>
    </div>
  </BaseLayout>
</template>
