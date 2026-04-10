<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import Button from '../components/ui/Button.vue';
import Input from '../components/ui/Input.vue';
import ThemeToggle from '../components/ui/ThemeToggle.vue';
import { ArrowLeft } from 'lucide-vue-next';

const router = useRouter();
const authStore = useAuthStore();

const form = ref({
  full_name: '',
  phone: '',
  email: '',
  password: '',
  confirm_password: '',
  referral_code: '',
  agree_terms: false
});

const errors = ref({});

const validate = () => {
  errors.value = {};
  if (form.value.full_name.length < 3) errors.value.full_name = "Name must be at least 3 characters";
  if (!/^\d{10}$/.test(form.value.phone)) errors.value.phone = "Phone must be 10 digits";
  if (form.value.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) errors.value.email = "Invalid email";
  if (form.value.password.length < 8) errors.value.password = "Password min 8 chars";
  if (form.value.password !== form.value.confirm_password) errors.value.confirm_password = "Passwords do not match";
  if (!form.value.agree_terms) errors.value.agree_terms = "Required";
  return Object.keys(errors.value).length === 0;
};

const handleSubmit = async () => {
  if (!validate()) return;
  try {
    const signupData = {
        full_name: form.value.full_name,
        phone: String(form.value.phone),
        password: form.value.password,
        ...(form.value.email && { email: form.value.email }),
        ...(form.value.referral_code && { referral_code: form.value.referral_code }),
    };
    
    // Call standard backend signup
    await authStore.signup(signupData);
    
    router.push({ path: '/verify-otp', query: { phone: form.value.phone, type: 'signup' } });
  } catch (e) {
    // Error is already set in authStore.error, just log for debugging
    console.error('Signup error:', e);
  }
};
</script>

<template>
  <div class="min-h-screen grid lg:grid-cols-2">
    
    <!-- Left: Form Section -->
    <div class="flex flex-col justify-center px-4 sm:px-6 lg:px-20 xl:px-24 bg-white dark:bg-gray-900 transition-colors duration-300">
      <!-- Header with Logo and Back Button -->
      <div class="absolute top-6 left-0 right-0 px-4 sm:px-6 lg:px-20 xl:px-24 z-50">
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

      <div class="mx-auto w-full max-w-sm lg:w-96">
        <div class="text-center mb-8">
          <h2 class="text-3xl font-bold tracking-tight text-gray-900 dark:text-white mb-2">
            {{ authStore.isAuthenticated ? 'Welcome back' : 'Create an account' }}
          </h2>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            {{ authStore.isAuthenticated ? 'You are already signed in to your account.' : 'Start your journey with us today.' }}
          </p>
        </div>

        <div v-if="authStore.isAuthenticated" class="space-y-6">
          <div class="bg-primary-50 dark:bg-primary-900/20 border border-primary-100 dark:border-primary-800 rounded-2xl p-6 text-center space-y-4">
             <div class="w-16 h-16 bg-white dark:bg-gray-800 rounded-2xl shadow-sm mx-auto flex items-center justify-center text-primary-600 font-bold text-2xl">
                {{ authStore.user?.full_name?.[0] || 'U' }}
             </div>
             <Button @click="router.replace('/dashboard')" class="w-full">
                Enter Dashboard
             </Button>
          </div>
        </div>

        <form v-else class="space-y-5" @submit.prevent="handleSubmit">
          
          <Input id="full_name" label="Full Name" v-model.trim="form.full_name" placeholder="John Doe" :error="errors.full_name" required />
          
          <Input id="phone" label="Phone Number" v-model.trim="form.phone" type="tel" :error="errors.phone" required>
            <template #prefix>
                 <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span class="text-gray-500 dark:text-gray-400 sm:text-sm font-medium">+91</span>
                </div>
            </template>
          </Input>

          <Input id="email" label="Email" v-model.trim="form.email" type="email" placeholder="john@example.com" :error="errors.email" />

          <div class="grid grid-cols-2 gap-4">
              <Input id="password" label="Password" v-model.trim="form.password" type="password" autocomplete="new-password" :error="errors.password" required />
              <Input id="confirm" label="Confirm" v-model.trim="form.confirm_password" type="password" autocomplete="new-password" :error="errors.confirm_password" required />
          </div>

          <Input id="referral" label="Referral Code" v-model="form.referral_code" placeholder="OPTIONAL" />

          <div class="flex items-start">
             <div class="flex items-center h-5">
               <input v-model="form.agree_terms" id="agree_terms" type="checkbox" class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded bg-gray-50 dark:bg-gray-800 dark:border-gray-600" />
             </div>
             <div class="ml-3 text-sm">
               <label for="agree_terms" class="font-medium text-gray-700 dark:text-gray-300">I agree to the <router-link to="/terms" class="text-primary-600 hover:text-primary-500 dark:text-primary-400">Terms</router-link> and <router-link to="/privacy" class="text-primary-600 hover:text-primary-500 dark:text-primary-400">Privacy Policy</router-link></label>
               <p v-if="errors.agree_terms" class="text-error text-xs mt-1">{{ errors.agree_terms }}</p>
             </div>
           </div>

           <div v-if="authStore.error" class="text-sm text-error bg-red-50 dark:bg-red-900/10 p-2 rounded">{{ authStore.error }}</div>

          <Button type="submit" :loading="authStore.loading" class="w-full shadow-lg shadow-primary-500/20">
            Create Account
          </Button>

          <p class="text-center text-sm text-gray-600 dark:text-gray-400">
            Already have an account?
            <router-link to="/login" class="font-medium text-primary-600 hover:text-primary-500 dark:text-primary-400 transition-colors">
              Sign in
            </router-link>
          </p>
        </form>
      </div>
    </div>

    <!-- Right: Visual Section -->
    <div class="hidden lg:relative lg:flex bg-gray-50 dark:bg-gray-950 items-center justify-center overflow-hidden">
        <div class="absolute inset-0 w-full h-full bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] dark:bg-[radial-gradient(#1f2937_1px,transparent_1px)] [background-size:16px_16px] [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)]"></div>
        <div class="relative z-10 w-full max-w-lg px-8 text-center animate-slide-up" style="animation-delay: 0.1s">
            <h2 class="text-4xl font-extrabold text-gray-900 dark:text-white mb-6 tracking-tight">Join the community</h2>
            <div class="grid grid-cols-2 gap-4 text-left">
                <div class="p-4 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
                    <div class="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center text-blue-600 dark:text-blue-400 mb-3">
                         <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    </div>
                    <h3 class="font-semibold text-gray-900 dark:text-white">Fast Service</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Book repair in minutes.</p>
                </div>
                <div class="p-4 bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
                    <div class="w-10 h-10 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center text-green-600 dark:text-green-400 mb-3">
                         <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    </div>
                    <h3 class="font-semibold text-gray-900 dark:text-white">Secure</h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Trusted professionals.</p>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>
