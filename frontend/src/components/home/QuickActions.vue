<template>
  <section class="px-4">
    <h2 class="text-xl font-bold text-gray-900 mb-4">Quick Services</h2>
    
    <div class="grid grid-cols-3 gap-3">
      <!-- Service Cards -->
      <button
        v-for="action in actions"
        :key="action.id"
        @click="handleAction(action)"
        class="aspect-square bg-white rounded-lg border border-gray-200 p-4 flex flex-col items-center justify-center gap-2 shadow-subtle hover:shadow-card active:scale-95 transition-all duration-200"
      >
        <div 
          class="w-12 h-12 rounded-full flex items-center justify-center"
          :class="getIconBgClass(action.color)"
        >
          <component 
            :is="getIcon(action.icon)" 
            class="w-6 h-6"
            :class="getIconClass(action.color)"
          />
        </div>
        <span class="text-xs font-semibold text-gray-900 text-center leading-tight">{{ action.name }}</span>
        <span class="text-xs text-gray-500">from ₹999</span>
      </button>

      <!-- View All Card -->
      <button
        @click="$router.push('/services')"
        class="aspect-square rounded-lg p-4 flex flex-col items-center justify-center gap-2 border-2 border-primary-500 bg-gradient-to-br from-primary-50 to-purple-50 active:scale-95 transition-all duration-200"
      >
        <div class="w-12 h-12 rounded-full bg-primary-500 flex items-center justify-center">
          <Grid class="w-6 h-6 text-white" />
        </div>
        <span class="text-xs font-semibold text-primary-600">View All</span>
      </button>
    </div>
  </section>
</template>

<script setup>
import { Smartphone, Battery, Droplets, Code, Grid } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()

defineProps({
  actions: {
    type: Array,
    default: () => []
  }
})

const getIcon = (iconName) => {
  const icons = {
    'Smartphone': Smartphone,
    'Battery': Battery,
    'Droplets': Droplets,
    'Code': Code
  }
  return icons[iconName] || Smartphone
}

const getIconBgClass = (color) => {
  const classes = {
    'blue': 'bg-blue-100',
    'green': 'bg-green-100',
    'red': 'bg-orange-100',
    'purple': 'bg-purple-100'
  }
  return classes[color] || 'bg-gray-100'
}

const getIconClass = (color) => {
  const classes = {
    'blue': 'text-blue-500',
    'green': 'text-green-500',
    'red': 'text-orange-500',
    'purple': 'text-purple-500'
  }
  return classes[color] || 'text-gray-500'
}

const handleAction = (action) => {
  router.push('/booking/select-brand')
}
</script>
