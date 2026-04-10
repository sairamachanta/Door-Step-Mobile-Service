<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const showContent = ref(false);

onMounted(() => {
  setTimeout(() => {
    showContent.value = true;
  }, 300);

  if (authStore.isAuthenticated) {
    setTimeout(() => router.replace('/home'), 1500); 
  }
});
</script>

<template>
  <div class="min-h-screen relative overflow-hidden flex flex-col items-center justify-center bg-gray-900">
     <!-- Abstract Background -->
    <div class="absolute inset-0 w-full h-full bg-[radial-gradient(#1f2937_1px,transparent_1px)] [background-size:16px_16px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)]"></div>

    <!-- Animated Shapes -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
        <div class="absolute top-[20%] left-[20%] w-[40%] h-[40%] bg-primary-600/20 rounded-full blur-[100px] animate-pulse-slow"></div>
        <div class="absolute bottom-[20%] right-[20%] w-[40%] h-[40%] bg-purple-600/20 rounded-full blur-[100px] animate-pulse-slow" style="animation-delay: 2s;"></div>
    </div>

    <!-- Content -->
    <div 
      class="z-10 text-center px-6 transition-all duration-1000 ease-out transform"
      :class="showContent ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'"
    >
      <!-- Logo -->
      <div class="mb-10 relative inline-block group">
        <div class="absolute inset-0 bg-gradient-to-tr from-primary-500 to-purple-600 rounded-3xl blur-lg opacity-75 group-hover:opacity-100 transition duration-500"></div>
        <div class="relative bg-black border border-white/10 rounded-3xl w-28 h-28 flex items-center justify-center text-5xl font-bold text-white shadow-2xl skew-y-3 group-hover:skew-y-0 transition-transform duration-500">
          <span class="bg-clip-text text-transparent bg-gradient-to-tr from-primary-400 to-purple-400">D</span>
        </div>
      </div>

      <!-- Text -->
      <h1 class="text-5xl font-extrabold text-white mb-4 tracking-tight">
        Doorstep
      </h1>
      <p class="text-gray-400 text-lg mb-12 max-w-sm mx-auto leading-relaxed">
        Expert technicians. Premium service.<br>Directly to you.
      </p>

      <!-- Buttons -->
      <div class="space-y-4 w-full max-w-xs mx-auto">
        <button 
          @click="router.push('/signup')"
          class="w-full relative group overflow-hidden bg-white text-gray-900 font-bold py-3.5 px-6 rounded-xl shadow-lg transition-transform transform hover:-translate-y-1 active:scale-95"
        >
          <span class="absolute inset-0 w-full h-full bg-gradient-to-r from-primary-500 via-purple-500 to-pink-500 opacity-0 group-hover:opacity-10 transition-opacity"></span>
          Get Started
        </button>
        
        <button 
          @click="router.push('/login')"
          class="w-full bg-white/5 backdrop-blur-md border border-white/10 text-white font-semibold py-3.5 px-6 rounded-xl hover:bg-white/10 transition duration-300"
        >
          Login
        </button>
      </div>
    </div>
  </div>
</template>
