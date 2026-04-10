<template>
  <section class="px-4 mt-6">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-bold text-gray-900">What Customers Say</h2>
    </div>

    <div class="flex gap-4 overflow-x-auto hide-scrollbar snap-x pb-2">
      <div
        v-for="review in reviews"
        :key="review.id"
        class="min-w-[320px] bg-white rounded-lg border border-gray-200 p-5 shadow-subtle snap-start flex-shrink-0"
      >
        <!-- Header -->
        <div class="flex items-start gap-3 mb-3">
          <div class="w-12 h-12 rounded-full bg-gradient-to-br from-primary-400 to-purple-500 flex items-center justify-center text-white font-bold text-lg flex-shrink-0">
            {{ review.customer_name.charAt(0) }}
          </div>
          <div class="flex-1 min-w-0">
            <h4 class="text-sm font-semibold text-gray-900">{{ review.customer_name }}</h4>
            <div class="flex items-center gap-1 mt-0.5">
              <Star v-for="i in 5" :key="i" class="w-4 h-4 fill-yellow-400 text-yellow-400" />
            </div>
            <p class="text-xs text-gray-500 mt-0.5">2 days ago</p>
          </div>
          <span v-if="review.is_verified" class="px-2 py-0.5 bg-green-100 text-green-700 text-[10px] font-semibold rounded-full">
            Verified
          </span>
        </div>

        <!-- Review Text -->
        <p class="text-sm text-gray-600 line-clamp-3 mb-3">{{ review.review_text }}</p>

        <!-- Service Tag -->
        <div class="pt-3 border-t border-gray-100 flex items-center gap-2">
          <div class="w-6 h-6 rounded bg-blue-100 flex items-center justify-center">
            <Smartphone class="w-4 h-4 text-blue-500" />
          </div>
          <span class="text-xs text-gray-500">{{ review.service_name }}</span>
        </div>
      </div>
    </div>

    <div class="text-center mt-4">
      <button class="text-sm font-semibold text-primary-500 hover:text-primary-700 flex items-center gap-1 mx-auto">
        Read More Reviews
        <ChevronRight class="w-4 h-4" />
      </button>
    </div>
  </section>
</template>

<script setup>
import { Star, Smartphone, ChevronRight } from 'lucide-vue-next'

defineProps({
  reviews: {
    type: Array,
    default: () => []
  }
})
</script>
