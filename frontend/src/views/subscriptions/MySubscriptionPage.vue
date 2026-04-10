<template>
  <BaseLayout>
    <div class="min-h-screen bg-white pb-24 md:pb-12 text-[#170F49] overflow-x-hidden">
      <!-- Premium Hero Header -->
      <header class="relative overflow-hidden bg-slate-50 pt-16 pb-24 md:pt-24 md:pb-32 px-6">
        <!-- Abstract Background Decor -->
        <div class="absolute top-0 right-0 -translate-y-1/2 translate-x-1/2 w-[600px] h-[600px] bg-primary-200/40 rounded-full blur-[120px]"></div>
        <div class="absolute bottom-0 left-0 translate-y-1/2 -translate-x-1/2 w-[400px] h-[400px] bg-purple-200/30 rounded-full blur-[80px]"></div>
        
        <div class="max-w-7xl mx-auto relative z-10 text-center space-y-6 animate-reveal">
          <div class="inline-flex items-center gap-2 px-4 py-2 bg-primary-100 rounded-full border border-primary-200 mb-2">
            <Crown class="w-4 h-4 text-primary-600" />
            <span class="text-xs font-black uppercase tracking-widest text-primary-700">Premium Protection</span>
          </div>
          <h1 class="text-4xl md:text-7xl font-black tracking-tight leading-tight max-w-4xl mx-auto">
            Pick a Plan, <span class="bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">Stay Protected</span> 24/7
          </h1>
          <p class="text-lg md:text-xl text-slate-500 font-medium max-w-2xl mx-auto leading-relaxed">
            Ultimate peace of mind for your precious devices. Choose a plan that fits your lifestyle and save up to 40% on every repair.
          </p>
        </div>
      </header>

      <!-- Active Subscription Indicator (Glassmorphism) -->
      <div v-if="mySubscription" class="max-w-5xl mx-auto px-6 -mt-16 mb-20 relative z-20 animate-reveal">
        <div class="bg-white/80 backdrop-blur-2xl border-2 border-primary-500 shadow-2xl shadow-primary-500/10 rounded-[3rem] p-8 md:p-10 flex flex-col md:flex-row items-center justify-between gap-8">
          <div class="flex items-center gap-6">
            <div class="w-20 h-20 bg-gradient-to-br from-primary-600 to-purple-600 rounded-[2rem] flex items-center justify-center shadow-xl shadow-primary-500/20 animate-float">
              <Crown class="w-10 h-10 text-white" />
            </div>
            <div class="text-center md:text-left">
              <p class="text-[10px] font-black text-primary-600 uppercase tracking-widest mb-1">Your Active Subscription</p>
              <h3 class="text-3xl font-black text-slate-900">{{ mySubscription.plan?.name }} Access</h3>
            </div>
          </div>
          <div class="h-16 w-px bg-slate-200 hidden md:block"></div>
          <div class="flex items-center gap-10">
            <div class="text-center md:text-right">
              <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Renews On</p>
              <p class="text-xl font-black text-slate-900">{{ formatDate(mySubscription.end_date) }}</p>
            </div>
            <button class="px-8 py-4 bg-slate-900 text-white rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-primary-600 transition-all shadow-xl shadow-slate-900/10 active:scale-95">
              Manage
            </button>
          </div>
        </div>
      </div>

      <main class="max-w-7xl mx-auto px-6 py-12">
        <!-- Pricing Cards Grid -->
        <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div v-for="i in 4" :key="i" class="bg-slate-50 rounded-[3rem] p-8 h-[550px] animate-pulse"></div>
        </div>
        
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-32 animate-reveal">
          <div
            v-for="plan in plans"
            :key="plan.id"
            class="group relative flex flex-col bg-white rounded-[3rem] border-2 p-10 transition-all duration-500 hover:shadow-2xl h-full"
            :class="[
              plan.is_popular 
                ? 'border-primary-500 shadow-xl shadow-primary-500/5 ring-8 ring-primary-500/5 z-10 scale-100 md:scale-105' 
                : 'border-slate-100 hover:border-primary-200'
            ]"
          >
            <!-- Badge -->
            <div v-if="plan.is_popular" class="absolute top-0 right-0 bg-primary-600 text-white px-6 py-2 rounded-bl-[1.5rem] rounded-tr-[2.8rem] text-[10px] font-black uppercase tracking-widest">
              Most Popular
            </div>

            <div class="mb-10">
              <span class="text-xs font-black tracking-widest uppercase transition-colors"
                :class="plan.is_popular ? 'text-primary-600' : 'text-slate-400 group-hover:text-primary-600'"
              >
                {{ plan.name }}
              </span>
              
              <div class="flex items-baseline gap-1 mt-6 mb-3">
                <span class="text-5xl font-black tracking-tighter">₹{{ plan.discounted_price || plan.price }}</span>
                <span class="text-slate-400 font-bold text-sm tracking-wide">/mo</span>
              </div>
              
              <p class="text-sm text-slate-500 font-medium leading-relaxed min-h-[48px]">
                {{ plan.description }}
              </p>
            </div>

            <!-- Action Button -->
            <button 
              @click="handlePurchase(plan)"
              :disabled="purchaseLoading || mySubscription?.plan?.id === plan.id"
              class="w-full py-5 rounded-2xl font-black text-xs uppercase tracking-widest flex items-center justify-center gap-2 mb-10 transition-all active:scale-95 shadow-lg group"
              :class="[
                mySubscription?.plan?.id === plan.id
                  ? 'bg-emerald-50 text-emerald-600 border border-emerald-100 cursor-default'
                  : plan.is_popular
                    ? 'bg-primary-600 text-white hover:bg-primary-700 shadow-primary-600/20'
                    : 'bg-slate-900 text-white hover:bg-primary-600 shadow-slate-900/10'
              ]"
            >
              <CheckCircle v-if="mySubscription?.plan?.id === plan.id" class="w-4 h-4" />
              <span>{{ (mySubscription?.plan?.id === plan.id) ? 'Active Plan' : (plan.price === 0 ? 'Get Started' : 'Upgrade to ' + plan.name) }}</span>
              <ArrowRight v-if="mySubscription?.plan?.id !== plan.id" class="w-4 h-4 transition-transform group-hover:translate-x-1" />
            </button>

            <!-- Features -->
            <div class="space-y-5 flex-grow">
              <p class="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Core Benefits</p>
              <div v-for="(feature, idx) in plan.features" :key="idx" class="flex items-start gap-4 group/item">
                <div class="w-6 h-6 rounded-full bg-emerald-50 flex items-center justify-center flex-shrink-0 border border-emerald-100 transition-colors group-hover/item:bg-emerald-500">
                  <Check class="w-3 h-3 text-emerald-600 transition-colors group-hover/item:text-white" />
                </div>
                <span class="text-sm font-bold text-slate-600 group-hover/item:text-slate-900 transition-colors">{{ feature }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Comparison Table Section -->
        <section class="py-24 animate-reveal">
          <div class="text-center mb-16 space-y-4">
            <h2 class="text-4xl font-black tracking-tight">Compare Everything</h2>
            <p class="text-slate-500 font-medium max-w-xl mx-auto">See why thousands of users choose our Pro and Enterprise plans for total protection.</p>
          </div>

          <div class="overflow-x-auto rounded-[3rem] border border-slate-100 shadow-xl shadow-slate-200/20">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-slate-50">
                  <th class="p-4 md:p-8 text-[10px] md:text-sm font-black uppercase tracking-widest text-slate-400">Feature</th>
                  <th v-for="plan in plans" :key="plan.id" class="p-4 md:p-8 text-center min-w-[120px] md:min-w-[150px]">
                    <span class="text-[10px] md:text-xs font-black uppercase tracking-widest" :class="plan.is_popular ? 'text-primary-600' : 'text-slate-900'">{{ plan.name }}</span>
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-50">
                <tr v-for="row in comparisonRows" :key="row.label" class="hover:bg-slate-50/50 transition-colors">
                  <td class="p-4 md:p-8 font-bold text-slate-700 text-xs md:text-base">{{ row.label }}</td>
                  <td v-for="(val, idx) in row.values" :key="idx" class="p-4 md:p-8 text-center text-[11px] md:text-sm">
                    <div v-if="typeof val === 'boolean'" class="flex justify-center">
                      <Check v-if="val" class="w-5 h-5 text-emerald-500" />
                      <X v-else class="w-5 h-5 text-slate-300" />
                    </div>
                    <span v-else class="font-black" :class="val === 'Unlimited' ? 'text-primary-600' : 'text-slate-500'">{{ val }}</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Testimonials -->
        <section class="py-24 animate-reveal">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
            <div class="space-y-8">
              <h2 class="text-4xl md:text-5xl font-black tracking-tight leading-tight">Trusted by <span class="text-primary-600">thousands</span> of device owners</h2>
              <div class="space-y-12">
                <div v-for="t in testimonials" :key="t.name" class="relative group">
                  <div class="absolute -left-4 top-0 bottom-0 w-1 bg-slate-100 group-hover:bg-primary-500 transition-colors rounded-full"></div>
                  <p class="text-xl italic text-slate-600 font-medium mb-4 leading-relaxed line-clamp-3">"{{ t.quote }}"</p>
                  <div class="flex items-center gap-4">
                    <img :src="t.avatar" class="w-12 h-12 rounded-2xl object-cover grayscale group-hover:grayscale-0 transition-all" alt="User">
                    <div>
                      <h4 class="font-black text-slate-900">{{ t.name }}</h4>
                      <p class="text-xs font-bold text-slate-400 uppercase tracking-widest">{{ t.plan }} Subscriber</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="bg-primary-600 rounded-[4rem] p-12 text-white relative h-full flex flex-col justify-center overflow-hidden shadow-2xl shadow-primary-500/20">
              <div class="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
              <Crown class="w-20 h-20 text-white/20 mb-8" />
              <h3 class="text-3xl font-black mb-6 leading-tight">"The Pro plan saved me ₹8,000 on a single screen repair. Best decision ever!"</h3>
              <p class="text-primary-100 font-bold text-sm uppercase tracking-widest">— Rohit Sharma, Delhi</p>
            </div>
          </div>
        </section>

        <!-- FAQ Section -->
        <section class="py-24 max-w-3xl mx-auto animate-reveal">
          <div class="text-center mb-16">
            <h2 class="text-4xl font-black tracking-tight mb-4">Got Questions?</h2>
            <p class="text-slate-500 font-medium">Everything you need to know about our protection plans.</p>
          </div>
          <div class="space-y-4">
            <div 
              v-for="(faq, idx) in faqs" 
              :key="idx" 
              class="group border border-slate-100 rounded-3xl overflow-hidden transition-all duration-300"
              :class="activeFaq === idx ? 'bg-slate-50 border-primary-100' : 'bg-white hover:border-slate-200'"
            >
              <button 
                @click="activeFaq = activeFaq === idx ? null : idx"
                class="w-full p-8 flex items-center justify-between text-left"
              >
                <span class="font-black text-lg transition-colors" :class="activeFaq === idx ? 'text-primary-600' : 'text-slate-900'">{{ faq.q }}</span>
                <Plus class="w-6 h-6 transition-transform duration-300" :class="{ 'rotate-45 text-primary-600': activeFaq === idx }" />
              </button>
              <div 
                v-show="activeFaq === idx" 
                class="px-8 pb-8 text-slate-500 font-medium leading-relaxed animate-fadeSlide"
              >
                {{ faq.a }}
              </div>
            </div>
          </div>
        </section>
      </main>
      
      <!-- Sticky CTA (Footer Style) -->
      <footer class="bg-slate-900 py-20 px-6 text-white text-center mt-20 relative overflow-hidden">
        <div class="max-w-4xl mx-auto space-y-8 relative z-10">
          <h2 class="text-4xl md:text-5xl font-black tracking-tight">Your device deserves the best protection</h2>
          <p class="text-slate-400 text-lg font-medium max-w-2xl mx-auto">Join over 100,000+ protected users across India and stop worrying about accidents today.</p>
          <div class="flex flex-col md:flex-row items-center justify-center gap-6 pt-4">
            <button class="px-10 py-5 bg-primary-600 text-white rounded-2xl font-black text-sm uppercase tracking-widest hover:bg-primary-500 transition-all shadow-xl shadow-primary-600/20">
              Get Protected Now
            </button>
            <a href="tel:1800-DEVICE-CARE" class="px-10 py-5 bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl font-black text-sm uppercase tracking-widest hover:bg-white/10 transition-all">
              Call Support
            </a>
          </div>
        </div>
        <!-- Background decor -->
        <div class="absolute -bottom-24 -left-24 w-64 h-64 bg-primary-500/20 rounded-full blur-[100px]"></div>
      </footer>
    </div>

    <!-- Success Modal -->
    <div v-if="showSuccess" class="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-slate-900/60 backdrop-blur-xl animate-fade">
      <div class="bg-white rounded-[4rem] p-12 max-w-sm w-full text-center shadow-[0_32px_120px_rgba(0,0,0,0.15)] animate-revealScale">
        <div class="w-24 h-24 bg-gradient-to-br from-emerald-400 to-emerald-600 rounded-[2.5rem] flex items-center justify-center mx-auto mb-8 shadow-xl shadow-emerald-500/20">
          <CheckCheck class="w-12 h-12 text-white" />
        </div>
        <h2 class="text-3xl font-black mb-4">You're Protected!</h2>
        <p class="text-slate-500 font-medium leading-relaxed mb-10">Your plan has been activated successfully. Welcome to the elite tier of mobile care!</p>
        <button @click="showSuccess = false" class="w-full py-5 bg-slate-900 text-white rounded-2xl font-black uppercase tracking-widest text-xs shadow-xl active:scale-95 transition-all">
          Awesome, Thanks!
        </button>
      </div>
    </div>
  </BaseLayout>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import BaseLayout from '../../components/BaseLayout.vue'
import { useSubscriptions } from '../../composables/useSubscriptions'
import { Crown, Check, X, ArrowRight, CheckCircle, CheckCheck, Plus } from 'lucide-vue-next'

const {
  plans,
  mySubscription,
  loading,
  purchaseLoading,
  fetchPlans,
  fetchMySubscription,
  purchasePlan
} = useSubscriptions()

const showSuccess = ref(false)
const activeFaq = ref(null)

const comparisonRows = [
  { label: 'Free Doorstep Service', values: [true, true, true, true] },
  { label: 'Visiting Charges', values: ['₹299', 'Free', 'Free', 'Free'] },
  { label: 'Monthly Service Requests', values: ['1', '5', 'Unlimited', 'Unlimited'] },
  { label: 'Warranty Protection', values: ['Standard', '15 Days', '30 Days', '60 Days'] },
  { label: 'Part Price Discount', values: ['0%', '10%', '20%', '30%'] },
  { label: 'Priority Support', values: [false, false, true, true] },
  { label: 'Free Screen Shield', values: [false, false, false, '1 / Year'] },
  { label: 'Dedicated Account Manager', values: [false, false, false, true] }
]

const testimonials = [
  {
    name: "Sneha Kapoor",
    plan: "Pro",
    quote: "I was skeptical at first, but the doorstep service is incredibly fast. They saved my phone twice in 3 months with 0 visiting charges!",
    avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?q=80&w=150&auto=format&fit=crop"
  },
  {
    name: "Arjun Mehta",
    plan: "Enterprise",
    quote: "The 60-day warranty on repairs is a game changer. I never worry about my screen again. Platinum quality support!",
    avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=150&auto=format&fit=crop"
  }
]

const faqs = [
  { q: "Can I upgrade my plan anytime?", a: "Yes, you can upgrade to a higher tier plan at any time. The remaining balance of your current plan will be pro-rated towards the new plan." },
  { q: "Is the doorstep service really free?", a: "For Starter, Pro, and Enterprise users, visiting charges are absolutely zero. Free users pay a nominal visiting fee of ₹299 per visit." },
  { q: "What does the warranty cover?", a: "Our warranty covers the specific parts replaced and our labor. It ensures that if the part fails or the issue recurs due to our work, we fix it for free." },
  { q: "Are there any hidden charges?", a: "No. The plan price covers all the benefits listed. You only pay for the price of spare parts used, which are also discounted based on your plan!" }
]

onMounted(async () => {
  await Promise.all([
    fetchPlans(),
    fetchMySubscription()
  ])
})

const handlePurchase = async (plan) => {
  try {
    await purchasePlan(plan.id)
    showSuccess.value = true
  } catch (err) {
    alert('Purchase unsuccessful. Please check your network or try again later.')
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return 'TBD'
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { 
    month: 'long', 
    day: 'numeric', 
    year: 'numeric' 
  })
}
</script>

<style scoped>
.animate-reveal {
  animation: reveal 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-revealScale {
  animation: revealScale 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-fade {
  animation: fade 0.4s ease-out forwards;
}

.animate-fadeSlide {
  animation: fadeSlide 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.animate-float {
  animation: float 4s ease-in-out infinite;
}

@keyframes reveal {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes revealScale {
  from { opacity: 0; transform: scale(0.9) translateY(20px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes fade {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeSlide {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f8fafc;
}

::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #cbd5e1;
}
</style>
