<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { getRoleDashboard } from '../router';
import OTPInput from '../components/OTPInput.vue';
import Button from '../components/ui/Button.vue';
import Card from '../components/ui/Card.vue';
import ThemeToggle from '../components/ui/ThemeToggle.vue';
import { ArrowLeft } from 'lucide-vue-next';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const phone = route.query.phone || '';
const otpType = route.query.type || 'signup';

const otpValue = ref('');
const timeLeft = ref(30);
const timer = ref(null);

const startTimer = () => {
    timeLeft.value = 30;
    if (timer.value) clearInterval(timer.value);
    timer.value = setInterval(() => { if (timeLeft.value > 0) timeLeft.value--; else clearInterval(timer.value); }, 1000);
}

const handleVerify = async () => {
    if (otpValue.value.length !== 6) return;
    try {
        await authStore.verifyOTP(phone, otpValue.value, otpType);
        router.replace(getRoleDashboard(authStore.userRole));
    } catch (e) { 
        otpValue.value = ""; 
    }
};

const handleResend = async () => {
    if (timeLeft.value > 0) return;
    try {
        await authStore.resendOTP(phone, otpType);
        startTimer();
    } catch (e) {}
};

onMounted(() => { if (!phone) router.replace('/signup'); startTimer(); });
onUnmounted(() => { if (timer.value) clearInterval(timer.value); });
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden transition-colors duration-300">
    <div class="absolute top-4 right-4 left-4 flex justify-between items-center pointer-events-auto z-50">
        <router-link to="/" class="text-sm font-bold text-slate-500 hover:text-primary-600 transition-colors flex items-center gap-2 group/back bg-white/50 backdrop-blur-md px-4 py-2 rounded-full border border-gray-200 shadow-sm">
          <ArrowLeft class="w-4 h-4 group-hover/back:-translate-x-1 transition-transform" /> 
          Back to Website
        </router-link>
        <ThemeToggle />
    </div>

    <!-- Background Accents -->
    <div class="absolute inset-0 w-full h-full overflow-hidden pointer-events-none">
         <div class="absolute top-[20%] left-[20%] w-96 h-96 bg-primary-400/20 rounded-full blur-[100px] animate-pulse-slow"></div>
         <div class="absolute bottom-[20%] right-[20%] w-96 h-96 bg-purple-400/20 rounded-full blur-[100px] animate-pulse-slow" style="animation-delay: 1s;"></div>
    </div>

    <div class="sm:mx-auto sm:w-full sm:max-w-md relative z-10">
      <div class="text-center mb-10">
          <div class="mx-auto w-16 h-16 bg-white dark:bg-gray-800 rounded-2xl shadow-lg flex items-center justify-center text-primary-600 dark:text-primary-400 mb-6 transform rotate-3 hover:rotate-6 transition-transform">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
          </div>
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Verification Code</h2>
          <p class="mt-2 text-gray-500 dark:text-gray-400">
            We sent a secure code to you.
          </p>
          <div class="mt-2 inline-flex items-center px-3 py-1 rounded-full bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 text-sm font-medium">
             +91 {{ phone }}
          </div>
      </div>

      <Card class="py-8 px-4 sm:px-10 dark:bg-gray-900/50 backdrop-blur-sm border-gray-200/60 dark:border-gray-700/60">
        <div class="space-y-8">
            <div class="flex justify-center">
                <OTPInput :length="6" @update:otp="otpValue = $event" @complete="handleVerify" />
            </div>

            <div v-if="authStore.error" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3 text-center">
                 <p class="text-sm text-red-600 dark:text-red-400">{{ authStore.error }}</p>
            </div>

            <Button 
                @click="handleVerify" 
                :disabled="otpValue.length !== 6" 
                :loading="authStore.loading"
                class="w-full shadow-lg shadow-primary-500/25"
            >
                Verify Account
            </Button>

            <div class="text-center">
                <p class="text-sm text-gray-500 dark:text-gray-400">
                    Didn't receive the code? 
                    <button 
                        @click="handleResend" 
                        :disabled="timeLeft > 0"
                        class="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 disabled:text-gray-400 dark:disabled:text-gray-600 transition ml-1"
                    >
                        {{ timeLeft > 0 ? `Resend in ${timeLeft}s` : 'Resend Code' }}
                    </button>
                </p>
            </div>
        </div>
      </Card>
      
      <p class="mt-8 text-center text-sm text-gray-500 dark:text-gray-400">
          <router-link to="/login" class="font-medium text-gray-900 dark:text-gray-200 hover:underline">
              &larr; Back to Login
          </router-link>
      </p>
    </div>
  </div>
</template>
