<template>
  <section class="px-4 mt-6">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-bold text-gray-900">Your Devices</h2>
      <button class="text-sm font-semibold text-primary-500">Add Device</button>
    </div>

    <div v-if="devices && devices.length > 0" class="flex gap-4 overflow-x-auto hide-scrollbar snap-x pb-2">
      <div
        v-for="device in devices"
        :key="device.id"
        class="min-w-[288px] bg-white rounded-lg border border-gray-200 p-5 shadow-subtle snap-start flex-shrink-0"
      >
        <div class="flex gap-3 mb-4">
          <div class="w-16 h-16 bg-gray-100 rounded-lg flex items-center justify-center flex-shrink-0">
            <Smartphone class="w-8 h-8 text-gray-400" />
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-xs text-gray-500">Apple</p>
            <h4 class="text-sm font-semibold text-gray-900">iPhone 14 Pro</h4>
            <p class="text-xs text-gray-500 mt-1">Serviced 15 days ago</p>
          </div>
        </div>

        <div class="mb-4">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs text-gray-500">Warranty</span>
            <span class="text-xs font-semibold text-success">45 days left</span>
          </div>
          <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
            <div class="h-full bg-success rounded-full" style="width: 75%"></div>
          </div>
          <p class="text-[10px] text-gray-400 mt-1">Valid till Jan 15, 2024</p>
        </div>

        <button class="w-full py-2.5 bg-primary-500 text-white text-sm font-semibold rounded-lg hover:bg-primary-700 active:scale-95 transition-all duration-200">
          Book Repair
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="bg-white rounded-lg border-2 border-dashed border-gray-300 p-8 text-center">
      <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
        <Smartphone class="w-8 h-8 text-gray-400" />
      </div>
      <h3 class="text-sm font-semibold text-gray-900 mb-1">No devices yet</h3>
      <button class="text-sm font-semibold text-primary-500 mt-2">Add Your First Device</button>
    </div>
  </section>
</template>

<script setup>
import { Smartphone } from 'lucide-vue-next'

defineProps({
  devices: {
    type: Array,
    default: () => []
  }
})
</script>
