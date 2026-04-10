<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { getRoleDashboard } from '../router';
import { ArrowLeft } from 'lucide-vue-next';
import Button from '../components/ui/Button.vue';
import Input from '../components/ui/Input.vue';
import ThemeToggle from '../components/ui/ThemeToggle.vue';

const router = useRouter();
const authStore = useAuthStore();

const phone = ref('');
const password = ref('');
const useOtp = ref(false);
const errors = ref({});

const validate = () => {
    errors.value = {};
    if (!phone.value) errors.value.phone = "Phone number is required";
    else if (!/^\d{10}$/.test(phone.value) && !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(phone.value)) {
        errors.value.phone = "Enter a valid 10-digit phone or system UUID";
    }
    
    if (!useOtp.value && !password.value) {
        errors.value.password = "Password is required";
    }
    return Object.keys(errors.value).length === 0;
};

const handleLogin = async () => {
    if (!validate()) return; 

    try {
        if (useOtp.value) {
            await authStore.loginWithOTP(phone.value);
            router.push({ path: '/verify-otp', query: { phone: phone.value, type: 'login' } });
        } else {
            await authStore.login(phone.value, password.value);
            router.replace(getRoleDashboard(authStore.userRole));
        }
    } catch (e) {
        // Error handled in store
    }
};
</script>

<template>
  <div class="min-h-screen grid lg:grid-cols-2">
    <!-- Left: Form Section -->
    <div class="flex flex-col justify-center px-4 sm:px-6 lg:px-20 xl:px-24 bg-white dark:bg-gray-900 transition-colors duration-300 min-h-screen py-20 lg:py-0">
      <!-- Header with Logo and Back Button -->
      <div class="absolute top-6 left-0 right-0 px-4 sm:px-6 lg:px-20 xl:px-24 z-50 lg:block hidden">
        <div class="flex justify-between items-center">
          <router-link to="/" class="flex items-center gap-2 group">
            <div class="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center text-white font-bold text-lg shadow-lg shadow-primary-500/30 transition-transform group-hover:scale-110">D</div>
            <span class="font-bold text-xl text-gray-900 dark:text-white">Doorstep</span>
          </router-link>
          <div class="flex items-center gap-4">
            <router-link to="/" class="text-sm font-bold text-slate-500 hover:text-primary-600 transition-colors flex items-center gap-2 group/back">
              <ArrowLeft class="w-4 h-4 group-hover/back:-translate-x-1 transition-transform" /> 
              <span class="hidden md:inline">Back to Website</span>
            </router-link>
            <ThemeToggle />
          </div>
        </div>
      </div>

      <!-- Mobile Header (Relative) -->
      <div class="lg:hidden mb-8">
        <div class="flex justify-between items-center">
          <router-link to="/" class="flex items-center gap-2 group">
            <div class="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center text-white font-bold text-lg shadow-lg shadow-primary-500/30 transition-transform group-hover:scale-110">D</div>
            <span class="font-bold text-xl text-gray-900 dark:text-white">Doorstep</span>
          </router-link>
          <ThemeToggle />
        </div>
      </div>

      <div class="mx-auto w-full max-w-sm lg:w-96">
        <div class="text-center mb-10">
          <h2 class="text-3xl font-bold tracking-tight text-gray-900 dark:text-white mb-2">
            {{ authStore.isAuthenticated ? 'Welcome back' : 'Sign in' }}
          </h2>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            {{ authStore.isAuthenticated ? 'You are already signed in to your account.' : 'Please enter your details to sign in.' }}
          </p>
        </div>

        <div v-if="authStore.isAuthenticated" class="space-y-6">
          <div class="bg-primary-50 dark:bg-primary-900/20 border border-primary-100 dark:border-primary-800 rounded-2xl p-6 text-center space-y-4">
             <div class="w-16 h-16 bg-white dark:bg-gray-800 rounded-2xl shadow-sm mx-auto flex items-center justify-center text-primary-600 font-bold text-2xl">
                {{ authStore.user?.full_name?.[0] || 'U' }}
             </div>
             <div>
                <p class="font-bold text-gray-900 dark:text-white">{{ authStore.user?.full_name }}</p>
                <p class="text-sm text-gray-500">{{ authStore.user?.phone }}</p>
             </div>
             <Button @click="router.replace(getRoleDashboard(authStore.userRole))" class="w-full">
                Enter Dashboard
             </Button>
             <button @click="authStore.logout()" class="text-sm font-bold text-gray-500 hover:text-red-500 transition-colors">
                Sign out of this account
             </button>
          </div>
        </div>

        <form v-else class="space-y-6" @submit.prevent="handleLogin">
          
          <Input 
            id="phone" 
            label="Phone Number" 
            v-model.trim="phone" 
            type="tel" 
            placeholder="9876543210" 
            :error="errors.phone"
            required
          >
            <template #prefix>
                 <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span v-if="!phone.includes('-')" class="text-gray-500 dark:text-gray-400 sm:text-sm font-medium">+91</span>
                </div>
            </template>
          </Input>
          
          <div v-if="!useOtp">
             <div class="relative">
                <Input 
                    id="password" 
                    label="Password" 
                    v-model.trim="password" 
                    type="password"
                    placeholder="••••••••" 
                    auto-complete="current-password"
                    :error="errors.password"
                    required
                />
             </div>
             <div class="flex items-center justify-end mt-2">
                <router-link to="/forgot-password" class="text-sm font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400">
                  Forgot password?
                </router-link>
             </div>
          </div>

          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input id="remember-me" name="remember-me" type="checkbox" class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded bg-gray-50 dark:bg-gray-800 dark:border-gray-600" />
              <label for="remember-me" class="ml-2 block text-sm text-gray-900 dark:text-gray-300">
                Remember me
              </label>
            </div>
            
             <div class="flex items-center cursor-pointer" @click="useOtp = !useOtp">
                <span class="mr-2 text-sm text-gray-600 dark:text-gray-400">Login with OTP</span>
                <div class="relative inline-block w-10 align-middle select-none transition duration-200 ease-in">
                    <input tabindex="-1" type="checkbox" :checked="useOtp" class="toggle-checkbox absolute block w-5 h-5 rounded-full bg-white border-4 appearance-none cursor-pointer border-gray-300 pointer-events-none"/>
                    <div class="toggle-label block overflow-hidden h-5 rounded-full cursor-pointer transition-colors duration-200" :class="useOtp ? 'bg-primary-500' : 'bg-gray-300'"></div>
                </div>
             </div>
          </div>

          <div v-if="authStore.error" class="rounded-lg bg-red-50 dark:bg-red-900/20 p-4 border border-red-200 dark:border-red-800">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800 dark:text-red-200">{{ authStore.error }}</h3>
              </div>
            </div>
          </div>

          <Button type="submit" :loading="authStore.loading" class="w-full shadow-lg shadow-primary-500/20">
            {{ useOtp ? 'Send OTP' : 'Sign in' }}
          </Button>

          <p class="text-center text-sm text-gray-600 dark:text-gray-400">
            Don't have an account?
            <router-link to="/signup" class="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 transition-colors">
              Sign up
            </router-link>
          </p>
        </form>
      </div>
    </div>

    <!-- Right: Visual Section -->
    <div class="hidden lg:relative lg:flex bg-gray-50 dark:bg-gray-950 items-center justify-center overflow-hidden">
        <!-- Abstract Background -->
        <div class="absolute inset-0 w-full h-full bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] dark:bg-[radial-gradient(#1f2937_1px,transparent_1px)] [background-size:16px_16px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)]"></div>
        
        <div class="relative z-10 w-full max-w-md px-8 text-center animate-slide-up">
            <div class="w-24 h-24 bg-gradient-to-tr from-primary-500 to-purple-600 rounded-3xl mx-auto mb-8 shadow-2xl flex items-center justify-center rotate-3 hover:rotate-6 transition-transform duration-500">
                 <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                 </svg>
            </div>
            <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Manage repairs with ease</h2>
            <p class="text-lg text-gray-600 dark:text-gray-400 leading-relaxed">
                Connect with expert technicians, track your service requests, and get your device fixed without leaving your home.
            </p>
        </div>
        
        <!-- Decoration Circles -->
        <div class="absolute -top-24 -right-24 w-96 h-96 bg-primary-500/10 rounded-full blur-3xl dark:bg-primary-500/20"></div>
        <div class="absolute -bottom-24 -left-24 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl dark:bg-purple-500/20"></div>
    </div>
  </div>
</template>

<style scoped>
/* Custom Toggle Style */
.toggle-checkbox:checked {
  right: 0;
  border-color: #6366f1;
}
.toggle-checkbox:checked + .toggle-label {
  @apply bg-primary-500;
}
</style>
