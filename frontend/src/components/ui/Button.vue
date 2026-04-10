<script setup>
import LoadingSpinner from '../../components/LoadingSpinner.vue';

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'ghost', 'outline', 'danger'].includes(value),
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value),
  },
  loading: Boolean,
  disabled: Boolean,
  type: {
      type: String,
      default: 'button'
  }
});
</script>

<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    class="inline-flex items-center justify-center font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed active:scale-95"
    :class="[
      // Base styles based on size
      size === 'sm' ? 'px-3 py-1.5 text-xs rounded-md' : '',
      size === 'md' ? 'px-4 py-2 text-sm rounded-lg' : '',
      size === 'lg' ? 'px-6 py-3 text-base rounded-xl' : '',

      // Variants
      variant === 'primary' ? 'bg-primary-600 hover:bg-primary-700 text-white shadow-sm hover:shadow focus:ring-primary-500' : '',
      variant === 'secondary' ? 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-200 border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 focus:ring-gray-200' : '',
      variant === 'ghost' ? 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800' : '',
      variant === 'outline' ? 'border-2 border-primary-600 text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-900/20' : '',
      variant === 'danger' ? 'bg-error text-white hover:bg-red-600 focus:ring-red-500' : '',
    ]"
  >
    <LoadingSpinner v-if="loading" class="w-4 h-4 mr-2" :class="variant === 'primary' ? 'text-white' : 'text-primary-600'" />
    <slot></slot>
  </button>
</template>
