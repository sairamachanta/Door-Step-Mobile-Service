<template>
  <!-- Premium Subscription (if active) -->
  <section v-if="subscription && subscription.is_active" class="px-4 mt-6">
    <div class="relative rounded-xl bg-gradient-to-br from-yellow-400 to-orange-500 p-6 shadow-elevated overflow-hidden">
      <!-- Decorative Circles -->
      <div class="absolute -top-10 -right-10 w-32 h-32 bg-white/10 rounded-full"></div>
      <div class="absolute -bottom-8 -left-8 w-24 h-24 bg-white/10 rounded-full"></div>

      <div class="relative z-10">
        <div class="flex items-center gap-2 mb-2">
          <div class="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center">
            <Crown class="w-5 h-5 text-white" />
          </div>
          <span class="px-2 py-0.5 bg-white/20 text-white text-[10px] font-semibold rounded-full uppercase">Premium</span>
        </div>

        <h3 class="text-2xl font-bold text-white mb-1">Premium Plan</h3>
        <p class="text-sm text-white/90 mb-4">Unlimited repairs & priority service</p>

        <div class="bg-white/20 backdrop-blur-sm rounded-lg p-4 mb-4">
          <p class="text-xs text-white/90 mb-2">Repairs this month</p>
          <p class="text-lg font-bold text-white mb-2">1 of 3 used</p>
          <div class="h-2 bg-white/30 rounded-full overflow-hidden">
            <div class="h-full bg-white rounded-full" style="width: 33%"></div>
          </div>
        </div>

        <div class="flex flex-wrap gap-2 mb-4">
          <span class="px-3 py-1 bg-white/20 text-white text-xs font-medium rounded-full flex items-center gap-1">
            <Check class="w-3 h-3" />
            Free Delivery
          </span>
          <span class="px-3 py-1 bg-white/20 text-white text-xs font-medium rounded-full flex items-center gap-1">
            <Check class="w-3 h-3" />
            Priority Support
          </span>
        </div>

        <button class="w-full py-2.5 bg-white text-orange-600 text-sm font-semibold rounded-lg hover:bg-gray-50 active:scale-95 transition-all duration-200">
          View Details
        </button>
      </div>
    </div>
  </section>

  <!-- Promotional Card (if no subscription) -->
  <section v-else class="px-4 mt-6">
    <div class="relative rounded-xl bg-gradient-to-br from-blue-50 to-purple-50 p-6 border-2 border-primary-200">
      <div class="flex gap-4">
        <div class="w-12 h-12 bg-gradient-to-br from-primary-500 to-purple-500 rounded-full flex items-center justify-center flex-shrink-0">
          <Sparkles class="w-6 h-6 text-white" />
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-bold text-gray-900 mb-1">Save up to 30% with Premium</h3>
          <p class="text-sm text-gray-600 mb-4">Get unlimited repairs and priority service</p>
          <button class="px-6 py-2.5 bg-gradient-to-r from-primary-500 to-purple-500 text-white text-sm font-semibold rounded-lg hover:shadow-lg active:scale-95 transition-all duration-200">
            Subscribe Now
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { Crown, Check, Sparkles } from 'lucide-vue-next'

defineProps({
  subscription: {
    type: Object,
    default: null
  }
})
</script>
