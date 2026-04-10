<template>
  <div class="min-h-screen flex flex-col md:flex-row bg-gray-50">
    <!-- Desktop Sidebar Space -->
    <div class="hidden md:block md:w-64"></div>
    
    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col pb-[60px] md:pb-0">
      <slot />
    </div>
    
    <!-- Bottom Navigation -->
    <BottomNav />
  </div>
</template>

<script setup>
import BottomNav from './BottomNav.vue'
</script>
