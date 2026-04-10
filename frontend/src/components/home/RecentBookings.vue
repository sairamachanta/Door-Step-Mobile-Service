<template>
  <section class="px-4 mt-6">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-bold text-gray-900">Recent Bookings</h2>
      <button class="text-sm font-semibold text-primary-500">View All</button>
    </div>

    <!-- Bookings List -->
    <div v-if="bookings && bookings.length > 0" class="space-y-3">
      <div
        v-for="booking in bookings.slice(0, 3)"
        :key="booking.id"
        class="bg-white rounded-lg border border-gray-200 p-4 shadow-subtle hover:shadow-card transition-shadow duration-200"
      >
        <div class="flex gap-3">
          <!-- Icon -->
          <div class="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center flex-shrink-0">
            <Smartphone class="w-6 h-6 text-blue-500" />
          </div>

          <!-- Content -->
          <div class="flex-1 min-w-0">
            <div class="flex items-start justify-between mb-2">
              <div>
                <h4 class="text-sm font-semibold text-gray-900">Screen Replacement</h4>
                <p class="text-xs text-gray-500">iPhone 14 Pro</p>
              </div>
              <span class="px-2 py-0.5 bg-orange-100 text-orange-700 text-xs font-medium rounded-full whitespace-nowrap">
                In Progress
              </span>
            </div>

            <div class="flex items-center gap-3 text-xs text-gray-500 mb-3">
              <span class="flex items-center gap-1">
                <Calendar class="w-3.5 h-3.5" />
                Today, 3:00 PM
              </span>
              <span class="flex items-center gap-1">
                <MapPin class="w-3.5 h-3.5" />
                Doorstep
              </span>
            </div>

            <div class="flex gap-2">
              <button class="flex-1 py-2 bg-primary-500 text-white text-xs font-semibold rounded-lg hover:bg-primary-700 active:scale-95 transition-all duration-200">
                Track Order
              </button>
              <button class="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 active:scale-95 transition-all duration-200">
                <Phone class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="bg-gray-50 rounded-lg p-8 text-center">
      <div class="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-3">
        <ClipboardList class="w-8 h-8 text-gray-400" />
      </div>
      <h3 class="text-sm font-semibold text-gray-900 mb-1">No bookings yet</h3>
      <p class="text-xs text-gray-500 mb-4">You don't have any ongoing services.</p>
      <button class="px-6 py-2 bg-primary-500 text-white text-sm font-semibold rounded-lg hover:bg-primary-700">
        Book Now
      </button>
    </div>
  </section>
</template>

<script setup>
import { Smartphone, Calendar, MapPin, Phone, ClipboardList } from 'lucide-vue-next'

defineProps({
  bookings: {
    type: Array,
    default: () => []
  }
})
</script>
