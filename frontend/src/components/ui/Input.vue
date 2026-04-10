<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  modelValue: [String, Number],
  label: String,
  type: {
    type: String,
    default: 'text',
  },
  placeholder: String,
  error: String,
  id: String,
  required: Boolean,
});

defineEmits(['update:modelValue']);

const showPassword = ref(false);

const inputType = computed(() => {
    if (props.type === 'password') {
        return showPassword.value ? 'text' : 'password';
    }
    return props.type;
});
</script>

<template>
  <div class="w-full">
    <label v-if="label" :for="id" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1.5">
      {{ label }} <span v-if="required" class="text-error">*</span>
    </label>
    <div class="relative">
        <slot name="prefix"></slot>
        <input
        v-bind="$attrs"
        :id="id"
        :type="inputType"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        :placeholder="placeholder"
        class="block w-full rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm py-2.5 transition-colors duration-200"
        :class="[
            error ? 'border-error focus:border-error focus:ring-error' : '',
            $slots.prefix ? 'pl-10' : 'pl-3',
            type === 'password' || $slots.suffix ? 'pr-10' : 'pr-3'
        ]"
        />
        
        <!-- Built-in Password Toggle with custom Eye Icon -->
        <button v-if="type === 'password'" type="button" @click="showPassword = !showPassword" 
                class="absolute inset-y-0 right-0 pr-3 flex items-center bg-transparent border-0 focus:outline-none"
                tabindex="-1">
            <i v-if="showPassword" class="bi bi-eye-slash eye-icon"></i>
            <i v-else class="bi bi-eye eye-icon"></i>
        </button>

        <slot v-else name="suffix"></slot>
    </div>
    <p v-if="error" class="mt-1 text-sm text-error animate-slide-up">{{ error }}</p>
  </div>
</template>

<style scoped>
.eye-icon {
  color: #B5B7BA; 
  font-size: 1.2rem;
  cursor: pointer;
}
</style>
