<template>
  <div class="min-h-screen bg-white">
    <!-- Header -->
    <header class="glass-header px-4 py-4 md:px-8 flex items-center justify-between border-b border-slate-100">
      <router-link to="/" class="flex items-center gap-2 group">
        <div class="w-10 h-10 bg-primary-700 rounded-xl flex items-center justify-center shadow-premium">
          <Zap class="w-6 h-6 text-white" />
        </div>
        <span class="text-xl font-extrabold tracking-tight text-slate-900 font-outfit">Doorstep</span>
      </router-link>
      
      <a href="#" @click.prevent="router.back()" class="text-sm font-bold text-slate-500 hover:text-primary-700 transition-colors flex items-center gap-2 group">
        <ArrowLeft class="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
        <span>Go Back</span>
      </a>
    </header>

    <!-- Content -->
    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="space-y-8">
        <!-- Title -->
        <div class="text-center space-y-4 pb-8 border-b border-slate-200">
          <h1 class="text-4xl md:text-5xl font-black text-slate-900 tracking-tight">Terms of Service</h1>
          <p class="text-slate-500 font-medium">Last updated: February 14, 2026</p>
        </div>

        <!-- Content Sections -->
        <div class="prose prose-slate max-w-none space-y-8">
          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">1. Acceptance of Terms</h2>
            <p class="text-slate-600 leading-relaxed">
              By accessing and using Doorstep's mobile repair services, you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by the above, please do not use this service.
            </p>
          </section>

          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">2. Service Description</h2>
            <p class="text-slate-600 leading-relaxed mb-4">
              Doorstep provides on-demand mobile device repair services at your location. Our services include but are not limited to:
            </p>
            <ul class="list-disc list-inside text-slate-600 space-y-2 ml-4">
              <li>Screen replacement and repair</li>
              <li>Battery replacement</li>
              <li>Camera and audio system repairs</li>
              <li>Software troubleshooting and updates</li>
              <li>Water damage treatment</li>
              <li>Logic board and component-level repairs</li>
            </ul>
          </section>

          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">3. Service Warranty</h2>
            <p class="text-slate-600 leading-relaxed">
              We provide a 6-month warranty on screen replacements and a 3-month warranty on other parts and repairs. The warranty covers defects in parts and workmanship but does not cover damage caused by misuse, accidents, or unauthorized modifications.
            </p>
          </section>

          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">4. Payment Terms</h2>
            <p class="text-slate-600 leading-relaxed">
              Payment is due upon completion of service. We accept cash, UPI, credit cards, and debit cards. A nominal visiting charge of ₹99 applies, which is waived if you proceed with any repair service.
            </p>
          </section>

          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">5. Cancellation Policy</h2>
            <p class="text-slate-600 leading-relaxed">
              You may cancel your service request up to 2 hours before the scheduled appointment without any charges. Cancellations made within 2 hours of the appointment may incur a cancellation fee.
            </p>
          </section>

          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">6. Data Protection</h2>
            <p class="text-slate-600 leading-relaxed">
              While we take every precaution to protect your data during repairs, we strongly recommend backing up your device before service. Doorstep is not responsible for any data loss that may occur during the repair process.
            </p>
          </section>

          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">7. Limitation of Liability</h2>
            <p class="text-slate-600 leading-relaxed">
              Doorstep's liability is limited to the cost of the repair service provided. We are not liable for any indirect, incidental, or consequential damages arising from the use of our services.
            </p>
          </section>

          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">8. Contact Information</h2>
            <p class="text-slate-600 leading-relaxed">
              For questions about these Terms of Service, please contact us at:
            </p>
            <div class="bg-slate-50 rounded-xl p-6 mt-4 border border-slate-200">
              <p class="text-slate-900 font-bold mb-2">Doorstep Mobile Services</p>
              <p class="text-slate-600">KPHB Colony, Near Lulu Mall, Hyderabad, Telangana</p>
              <p class="text-slate-600">Phone/WhatsApp: <a href="tel:9390999539" class="text-primary-700 hover:underline font-bold">9390999539</a></p>
            </div>
          </section>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="bg-slate-50 border-t border-slate-200 py-8 mt-16">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <p class="text-sm text-slate-500">© 2026 Doorstep Technologies Inc. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { Zap, ArrowLeft } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<style scoped>
.glass-header {
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(12px);
  background: rgba(255, 255, 255, 0.8);
}
</style>
