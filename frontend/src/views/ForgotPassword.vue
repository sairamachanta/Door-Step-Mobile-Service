<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import OTPInput from '../components/OTPInput.vue';
import Button from '../components/ui/Button.vue';
import Input from '../components/ui/Input.vue';
import Card from '../components/ui/Card.vue';
import ThemeToggle from '../components/ui/ThemeToggle.vue';

const router = useRouter();
const authStore = useAuthStore();
const step = ref(1);
const phone = ref('');
const otpCode = ref('');
const newPassword = ref('');
const confirmPassword = ref('');

const handleStep1 = async () => { 
    if (phone.value.length !== 10) return; 
    try { 
        await authStore.forgotPassword(phone.value); 
        step.value = 2; 
    } catch (e) {} 
};

const handleStep2 = () => { 
    if (otpCode.value.length === 6) step.value = 3; 
};

const handleStep3 = async () => { 
    if (!newPassword.value || newPassword.value !== confirmPassword.value) return; 
    try { 
        await authStore.resetPassword(phone.value, otpCode.value, newPassword.value, confirmPassword.value); 
        router.push('/login'); 
    } catch (e) {} 
};
</script>

<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-950 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden transition-colors duration-300">
    <div class="absolute top-4 right-4">
         <ThemeToggle />
    </div>
     <!-- Background Accents -->
    <div class="absolute inset-0 w-full h-full pointer-events-none">
         <div class="absolute top-[-20%] right-[20%] w-[600px] h-[600px] bg-primary-100 dark:bg-primary-900/10 rounded-full blur-[100px]"></div>
    </div>

    <div class="sm:mx-auto sm:w-full sm:max-w-md relative z-10">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Reset Password</h2>
        <p class="mt-2 text-gray-500 dark:text-gray-400">Restore access to your account</p>
      </div>

      <!-- Steps Indicator -->
      <div class="flex justify-center mb-8 space-x-2">
           <div v-for="i in 3" :key="i" class="h-1.5 w-16 rounded-full transition-all duration-300" :class="step >= i ? 'bg-primary-600' : 'bg-gray-200 dark:bg-gray-700'"></div>
      </div>

      <Card class="py-10 px-6 sm:px-10 dark:bg-gray-900/50 backdrop-blur-sm border-gray-200/60 dark:border-gray-700/60">
         
         <!-- Step 1 -->
         <div v-if="step === 1" class="space-y-6 animate-fade-in">
              <div class="text-center mb-4">
                  <p class="text-sm text-gray-600 dark:text-gray-300">Enter your phone number to receive a verification code.</p>
              </div>
              
              <Input 
                id="phone" 
                label="Phone Number" 
                v-model="phone" 
                type="tel" 
                placeholder="9876543210"
              >
                 <template #prefix>
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <span class="text-gray-500 dark:text-gray-400 sm:text-sm font-medium">+91</span>
                    </div>
                </template>
              </Input>

              <Button @click="handleStep1" :loading="authStore.loading" :disabled="phone.length !== 10" class="w-full">
                Send Code
              </Button>
         </div>

         <!-- Step 2 -->
         <div v-if="step === 2" class="space-y-8 animate-fade-in">
             <div class="text-center mb-4">
                 <p class="text-sm text-gray-600 dark:text-gray-300">Enter the code sent to <span class="font-semibold text-gray-900 dark:text-white">+91 {{ phone }}</span></p>
             </div>
             <div class="flex justify-center">
                 <OTPInput :length="6" @update:otp="otpCode = $event" @complete="handleStep2" />
             </div>
             <Button @click="handleStep2" :disabled="otpCode.length !== 6" class="w-full">
                 Next
             </Button>
         </div>

         <!-- Step 3 -->
         <div v-if="step === 3" class="space-y-6 animate-fade-in">
              <div class="text-center mb-4">
                  <p class="text-sm text-gray-600 dark:text-gray-300">Create a new strong password.</p>
              </div>
              
              <Input id="newPassword" label="New Password" v-model="newPassword" type="password" />
              <Input id="confirmPassword" label="Confirm Password" v-model="confirmPassword" type="password" />
              
              <Button @click="handleStep3" :loading="authStore.loading" class="w-full">
                 Reset Password
               </Button>
         </div>

         <!-- Error -->
         <div v-if="authStore.error" class="mt-6 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-3 text-center">
            <p class="text-sm text-red-600 dark:text-red-400">{{ authStore.error }}</p>
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
