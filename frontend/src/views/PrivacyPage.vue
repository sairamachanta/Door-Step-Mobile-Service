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
          <h1 class="text-4xl md:text-5xl font-black text-slate-900 tracking-tight">Privacy Policy</h1>
          <p class="text-slate-500 font-medium">Last updated: February 14, 2026</p>
        </div>

        <!-- Content Sections -->
        <div class="prose prose-slate max-w-none space-y-8">
          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">1. Information We Collect</h2>
            <p class="text-slate-600 leading-relaxed mb-4">
              We collect information that you provide directly to us when using our services:
            </p>
            <ul class="list-disc list-inside text-slate-600 space-y-2 ml-4">
              <li><strong>Personal Information:</strong> Name, phone number, email address, and location</li>
              <li><strong>Device Information:</strong> Device model, IMEI number, and repair history</li>
              <li><strong>Payment Information:</strong> Payment method details (processed securely through third-party providers)</li>
              <li><strong>Service Data:</strong> Service requests, appointment details, and feedback</li>
            </ul>
          </section>

          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">2. How We Use Your Information</h2>
            <p class="text-slate-600 leading-relaxed mb-4">
              We use the information we collect to:
            </p>
            <ul class="list-disc list-inside text-slate-600 space-y-2 ml-4">
              <li>Provide, maintain, and improve our repair services</li>
              <li>Process your service requests and payments</li>
              <li>Send you service updates, confirmations, and reminders</li>
              <li>Respond to your comments, questions, and customer service requests</li>
              <li>Detect, prevent, and address technical issues and fraudulent activity</li>
              <li>Comply with legal obligations and enforce our terms</li>
            </ul>
          </section>

          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">3. Information Sharing</h2>
            <p class="text-slate-600 leading-relaxed">
              We do not sell, trade, or rent your personal information to third parties. We may share your information only in the following circumstances:
            </p>
            <ul class="list-disc list-inside text-slate-600 space-y-2 ml-4 mt-4">
              <li><strong>Service Providers:</strong> With technicians assigned to your repair request</li>
              <li><strong>Payment Processors:</strong> To process your payments securely</li>
              <li><strong>Legal Requirements:</strong> When required by law or to protect our rights</li>
              <li><strong>Business Transfers:</strong> In connection with a merger, acquisition, or sale of assets</li>
            </ul>
          </section>

          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">4. Data Security</h2>
            <p class="text-slate-600 leading-relaxed">
              We implement appropriate technical and organizational measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction. However, no method of transmission over the internet is 100% secure, and we cannot guarantee absolute security.
            </p>
          </section>

          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">5. Data Retention</h2>
            <p class="text-slate-600 leading-relaxed">
              We retain your personal information for as long as necessary to fulfill the purposes outlined in this Privacy Policy, unless a longer retention period is required by law. Service history and warranty information are retained for up to 2 years.
            </p>
          </section>

          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">6. Your Rights</h2>
            <p class="text-slate-600 leading-relaxed mb-4">
              You have the right to:
            </p>
            <ul class="list-disc list-inside text-slate-600 space-y-2 ml-4">
              <li>Access and receive a copy of your personal information</li>
              <li>Correct inaccurate or incomplete information</li>
              <li>Request deletion of your personal information</li>
              <li>Opt-out of marketing communications</li>
              <li>Withdraw consent where processing is based on consent</li>
            </ul>
          </section>

          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">7. Cookies and Tracking</h2>
            <p class="text-slate-600 leading-relaxed">
              We use cookies and similar tracking technologies to improve your experience on our website and mobile app. You can control cookies through your browser settings, but disabling cookies may affect functionality.
            </p>
          </section>

          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">8. Children's Privacy</h2>
            <p class="text-slate-600 leading-relaxed">
              Our services are not directed to individuals under the age of 18. We do not knowingly collect personal information from children. If you believe we have collected information from a child, please contact us immediately.
            </p>
          </section>

          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">9. Changes to This Policy</h2>
            <p class="text-slate-600 leading-relaxed">
              We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and updating the "Last updated" date.
            </p>
          </section>

          <section>
            <h2 class="text-2xl font-bold text-slate-900 mb-4">10. Contact Us</h2>
            <p class="text-slate-600 leading-relaxed">
              If you have any questions about this Privacy Policy, please contact us:
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
