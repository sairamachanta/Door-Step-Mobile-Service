<script setup>
import { reactive, onMounted, nextTick } from 'vue';

const props = defineProps({
  length: {
    type: Number,
    default: 6,
  },
});

const emit = defineEmits(['update:otp', 'complete']);

const otp = reactive(new Array(props.length).fill(''));
const inputRefs = reactive([]);

const handleInput = (event, index) => {
  const value = event.target.value;
  if (!/^\d*$/.test(value)) {
    otp[index] = '';
    return;
  }

  otp[index] = value.slice(-1);

  if (value && index < props.length - 1) {
    inputRefs[index + 1]?.focus();
  }

  emitOTP();
};

const handleKeyDown = (event, index) => {
  if (event.key === 'Backspace' && !otp[index] && index > 0) {
    inputRefs[index - 1]?.focus();
  }
};

const handlePaste = (event) => {
  event.preventDefault();
  const pasteData = event.clipboardData.getData('text').slice(0, props.length);
  if (/^\d+$/.test(pasteData)) {
    pasteData.split('').forEach((char, i) => {
      otp[i] = char;
    });
    inputRefs[Math.min(pasteData.length, props.length - 1)]?.focus();
    emitOTP();
  }
};

const emitOTP = () => {
  const otpString = otp.join('');
  emit('update:otp', otpString);
  if (otpString.length === props.length) {
    emit('complete', otpString);
  }
};

// Expose focus method to parent if needed, or auto focus on mount
onMounted(() => {
    nextTick(() => {
        // Optional: inputRefs[0]?.focus();
    });
});
</script>

<template>
  <div class="flex gap-2 sm:gap-3">
    <input
      v-for="(digit, index) in length"
      :key="index"
      :ref="(el) => (inputRefs[index] = el)"
      type="text"
      inputmode="numeric"
      maxlength="1"
      v-model="otp[index]"
      @input="handleInput($event, index)"
      @keydown="handleKeyDown($event, index)"
      @paste="handlePaste"
      class="w-10 h-12 sm:w-12 sm:h-14 border-2 rounded-xl text-center text-xl font-bold transition-all duration-200 focus:outline-none focus:ring-0"
      :class="[
        otp[index] 
          ? 'border-primary-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-white' 
          : 'border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 text-gray-500 dark:text-gray-400 focus:border-primary-500 focus:bg-white dark:focus:bg-gray-800'
      ]"
    />
  </div>
</template>
