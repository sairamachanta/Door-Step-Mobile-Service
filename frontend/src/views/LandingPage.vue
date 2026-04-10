<template>
  <div class="min-h-screen bg-white pb-12 selection:bg-blue-100">
    <!-- 1. Premium Sticky Header -->
    <header class="glass-header px-4 py-4 md:px-8 flex items-center justify-between relative">
      <a href="#" @click.prevent="scrollToTop" class="flex items-center gap-2 cursor-pointer group">
        <div class="w-10 h-10 bg-[#0a0f1c] rounded-xl flex items-center justify-center shadow-[0_0_12px_rgba(0,230,255,0.4)] group-hover:scale-105 transition-all duration-300 border border-slate-800">
          <svg viewBox="0 0 100 100" class="w-7 h-7">
            <defs>
              <linearGradient id="neonGlow" x1="0%" y1="100%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#00f0ff" />
                <stop offset="100%" stop-color="#b026ff" />
              </linearGradient>
              <filter id="glow">
                <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                <feMerge>
                  <feMergeNode in="coloredBlur"/>
                  <feMergeNode in="SourceGraphic"/>
                </feMerge>
              </filter>
            </defs>
            <path d="M50 15 L90 82 Q92 86 88 86 L12 86 Q8 86 10 82 Z" fill="none" stroke="url(#neonGlow)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)"/>
            <text x="50" y="68" font-family="'Rajdhani', sans-serif" font-weight="900" font-style="italic" font-size="28" fill="white" text-anchor="middle" letter-spacing="1" filter="url(#glow)">DSM</text>
          </svg>
        </div>
        <span class="text-xl font-extrabold tracking-tight text-slate-900 font-outfit">Doorstep</span>
      </a>
      
      <!-- Centered Navigation -->
      <nav class="hidden md:flex items-center gap-8 absolute left-1/2 -translate-x-1/2">
        <a href="#about" class="text-sm font-bold text-slate-600 hover:text-primary-700 transition-colors">About</a>
        <a href="#services" class="text-sm font-bold text-slate-600 hover:text-primary-700 transition-colors">Services</a>
        <a href="#pricing" class="text-sm font-bold text-slate-600 hover:text-primary-700 transition-colors">Pricing</a>
        <a href="#faqs" class="text-sm font-bold text-slate-600 hover:text-primary-700 transition-colors">FAQs</a>
      </nav>

      <div class="flex items-center gap-4">
        <template v-if="authStore.isAuthenticated">
          <router-link to="/dashboard" class="hidden md:flex btn btn-secondary px-8 py-2.5 rounded-xl text-sm gap-2">
             <LayoutGrid class="w-4 h-4" />
             Go to Dashboard
          </router-link>
        </template>
        <template v-else>
          <router-link to="/login" class="hidden md:flex btn btn-primary px-8 py-2.5 rounded-xl text-sm">Sign In</router-link>
        </template>
        
        <button @click="mobileMenuOpen = true" class="md:hidden w-10 h-10 flex items-center justify-center text-slate-900 hover:bg-slate-100 rounded-lg transition-colors">
          <Menu class="w-6 h-6" />
        </button>
      </div>
    </header>

    <!-- Mobile Menu Overlay -->
    <Transition name="fade">
      <div v-if="mobileMenuOpen" @click="mobileMenuOpen = false" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 md:hidden"></div>
    </Transition>

    <!-- Mobile Menu Panel -->
    <Transition name="slide">
      <div v-if="mobileMenuOpen" class="fixed top-0 right-0 bottom-0 w-[280px] bg-white shadow-2xl z-50 md:hidden">
        <div class="flex flex-col h-full">
          <!-- Mobile Menu Header -->
          <div class="flex items-center justify-between p-4 border-b border-slate-200">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 bg-primary-700 rounded-lg flex items-center justify-center">
                <Zap class="w-5 h-5 text-white" />
              </div>
              <span class="font-bold text-lg text-slate-900">Menu</span>
            </div>
            <button @click="mobileMenuOpen = false" class="w-10 h-10 flex items-center justify-center text-slate-500 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors">
              <X class="w-6 h-6" />
            </button>
          </div>

          <!-- Mobile Menu Links -->
          <nav class="flex-1 overflow-y-auto p-4">
            <div class="space-y-2">
              <a @click="mobileMenuOpen = false" href="#about" class="flex items-center gap-3 px-4 py-3 text-slate-700 hover:bg-primary-50 hover:text-primary-700 rounded-xl transition-colors font-medium">
                <User class="w-5 h-5" />
                <span>About</span>
              </a>
              <a @click="mobileMenuOpen = false" href="#services" class="flex items-center gap-3 px-4 py-3 text-slate-700 hover:bg-primary-50 hover:text-primary-700 rounded-xl transition-colors font-medium">
                <Settings class="w-5 h-5" />
                <span>Services</span>
              </a>
              <a @click="mobileMenuOpen = false" href="#pricing" class="flex items-center gap-3 px-4 py-3 text-slate-700 hover:bg-primary-50 hover:text-primary-700 rounded-xl transition-colors font-medium">
                <Star class="w-5 h-5" />
                <span>Pricing</span>
              </a>
              <a @click="mobileMenuOpen = false" href="#faqs" class="flex items-center gap-3 px-4 py-3 text-slate-700 hover:bg-primary-50 hover:text-primary-700 rounded-xl transition-colors font-medium">
                <Headphones class="w-5 h-5" />
                <span>FAQs</span>
              </a>
            </div>
          </nav>

          <!-- Mobile Menu Footer -->
          <div class="p-4 border-t border-slate-200 space-y-3">
            <template v-if="authStore.isAuthenticated">
              <router-link @click="mobileMenuOpen = false" to="/dashboard" class="btn btn-secondary w-full rounded-xl text-center block py-3">
                Go to Dashboard
              </router-link>
              <button @click="authStore.logout()" class="btn btn-ghost w-full rounded-xl text-center block py-3 text-red-600">
                Logout
              </button>
            </template>
            <template v-else>
              <router-link @click="mobileMenuOpen = false" to="/login" class="btn btn-primary w-full rounded-xl text-center block py-3">
                Sign In
              </router-link>
              <router-link @click="mobileMenuOpen = false" to="/signup" class="btn btn-secondary w-full rounded-xl text-center block py-3">
                Sign Up
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </Transition>

    <main>
      <!-- 2. Hero Section -->
      <section class="section-container pt-12 md:pt-20 grid lg:grid-cols-2 gap-12 items-center">
        <div class="space-y-8 animate-reveal">
          <div class="space-y-4">
            <div class="inline-flex items-center gap-2 px-3 py-1 bg-blue-50 text-primary-700 rounded-full text-xs font-bold uppercase tracking-wider">
              <span class="w-2 h-2 bg-primary-700 rounded-full animate-pulse"></span>
              Available in 50+ Cities
            </div>
            <h1 class="text-4xl md:text-7xl font-black text-slate-900 tracking-tight leading-[1.1]">
              Expert <span class="text-grad-primary">Mobile Repairs</span> at Your Doorstep
            </h1>
            <p class="text-lg md:text-xl text-slate-500 font-medium max-w-xl">
              From cracked screens to motherboard micro-soldering, we bring certified technicians directly to your home or office.
            </p>
          </div>

          <!-- Search Bar -->
          <div class="flex flex-col md:flex-row items-center gap-4 p-2 bg-white rounded-3xl shadow-premium border border-slate-100 max-w-2xl">
            <div class="flex items-center gap-3 px-4 py-2 w-full md:w-auto md:border-r border-slate-100">
              <MapPin class="w-5 h-5 text-slate-400" />
              <input type="text" placeholder="Location" class="bg-transparent text-sm font-bold focus:outline-none w-full" />
            </div>
            <div class="flex items-center gap-3 px-4 py-2 flex-grow">
              <Smartphone class="w-5 h-5 text-slate-400" />
              <input type="text" placeholder="Device Brand & Model (e.g. iPhone 15)" class="bg-transparent text-sm font-bold focus:outline-none w-full" />
            </div>
            <button @click="router.push('/signup')" class="btn btn-secondary !px-10 rounded-2xl w-full md:w-auto">
              Book Now
            </button>
          </div>

          <div class="flex items-center gap-6 pt-4">
            <div class="flex -space-x-3">
              <img v-for="i in 4" :key="i" :src="`https://i.pravatar.cc/100?img=${i+10}`" 
                class="w-10 h-10 rounded-full border-4 border-white shadow-sm" />
            </div>
            <p class="text-sm font-bold text-slate-900">
              <span class="text-primary-700">500K+</span> Happy Customers
            </p>
          </div>
        </div>

        <div class="relative w-full h-[400px] lg:h-[600px] flex items-center justify-center animate-scale [animation-delay:200ms] reveal-visible">
          <HeroAnimation />
        </div>
      </section>

      <!-- 3. Service Categories Marquee -->
      <section id="services" class="bg-slate-50 py-24 md:py-32 overflow-hidden">
        <div class="mb-20 px-4 md:px-8 text-center space-y-4">
          <h2 class="text-3xl md:text-[60px] font-bold leading-tight text-slate-900 tracking-tight">Our <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-cyan-500">Services</span></h2>
          <p class="text-slate-500 font-medium max-w-3xl mx-auto text-lg md:text-2xl">No matter your device, Doorstep helps you get fixed, stay connected, and get back to life faster.</p>
        </div>

        <!-- Marquee Row 1 -->
        <!-- Marquee Row 1 -->
        <div class="marquee mb-12 py-12">
          <div class="marquee-content flex">
            <div v-for="cat in [...categoriesRow1, ...categoriesRow1, ...categoriesRow1]" :key="cat.name + '1'" 
              class="w-[300px] sm:w-[350px] pt-[70px] pb-8 px-8 mr-8 bg-white shadow-md hover:shadow-xl rounded-[2rem] border border-slate-100 flex-shrink-0 relative transition-transform duration-300">
              <div :class="['absolute -top-10 -left-6 w-28 h-28 rounded-full flex items-center justify-center border-[6px] border-slate-50 shadow-sm', cat.bgColor]">
                <component :is="cat.icon" :class="`w-10 h-10 ${cat.iconColor}`" />
              </div>
              <h3 :class="['text-2xl font-bold mb-3', cat.iconColor]">{{ cat.name }}</h3>
              <p class="text-slate-500 font-medium leading-relaxed">{{ cat.desc }}</p>
            </div>
          </div>
        </div>

        <!-- Marquee Row 2 (Reverse) -->
        <div class="marquee reverse py-12 -mt-12">
           <div class="marquee-content flex">
            <div v-for="cat in [...categoriesRow2, ...categoriesRow2, ...categoriesRow2]" :key="cat.name + '2'" 
              class="w-[300px] sm:w-[350px] pt-[70px] pb-8 px-8 mr-8 bg-white shadow-md hover:shadow-xl rounded-[2rem] border border-slate-100 flex-shrink-0 relative transition-transform duration-300">
              <div :class="['absolute -top-10 -left-6 w-28 h-28 rounded-full flex items-center justify-center border-[6px] border-slate-50 shadow-sm', cat.bgColor]">
                <component :is="cat.icon" :class="`w-10 h-10 ${cat.iconColor}`" />
              </div>
              <h3 :class="['text-2xl font-bold mb-3', cat.iconColor]">{{ cat.name }}</h3>
              <p class="text-slate-500 font-medium leading-relaxed">{{ cat.desc }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 4. How It Works -->
      <section class="section-container py-24">
        <div class="text-center max-w-3xl mx-auto mb-20 space-y-4">
          <h2 class="text-3xl md:text-[60px] font-bold leading-tight text-slate-900 tracking-tight">How It <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Works</span></h2>
          <p class="text-slate-500 font-medium text-lg">Simple 4-step process to get your service done.</p>
        </div>
        
        <div class="grid md:grid-cols-4 gap-12 relative">
          <!-- Connector Line -->
          <div class="hidden md:block absolute top-[48px] left-[10%] right-[10%] h-[2px] bg-gradient-to-r from-blue-100 via-indigo-100 to-blue-100 border-t-2 border-dashed border-slate-200 z-0"></div>
          
          <div v-for="(step, index) in workflow" :key="step.title" class="relative z-10 group text-center space-y-6">
            <div class="relative w-24 h-24 mx-auto perspective-1000">
               <!-- Decorative back blob -->
               <div :class="`absolute inset-0 ${step.blobColor} rounded-[2rem] rotate-6 group-hover:rotate-12 transition-transform duration-500 ease-out`"></div>
               <!-- Main Icon Box -->
               <div :class="`relative w-full h-full bg-white border border-slate-100 rounded-[2rem] flex items-center justify-center shadow-lg shadow-slate-200/50 group-hover:shadow-2xl group-hover:-translate-y-2 transition-all duration-500`">
                  <component :is="step.icon" :class="`w-10 h-10 ${step.iconColor} group-hover:scale-110 transition-transform duration-500`" />
               </div>
               <!-- Number Badge -->
               <div :class="`absolute -top-3 -right-3 w-10 h-10 ${step.badgeColor} text-white rounded-2xl flex items-center justify-center font-black text-sm shadow-lg border-4 border-white transition-colors duration-300`">
                  {{ index + 1 }}
               </div>
            </div>
            <div class="space-y-3 px-4">
              <h4 :class="`text-xl font-bold ${step.iconColor}`">{{ step.title }}</h4>
              <p class="text-sm text-slate-500 font-medium leading-relaxed">{{ step.desc }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 4.1 Why Choose Us -->
      <section class="bg-slate-50 py-24 md:py-32">
        <div class="section-container grid md:grid-cols-2 gap-16 items-center">
          <div class="space-y-12 animate-reveal">
            <div class="space-y-4">
              <h2 class="text-3xl md:text-[60px] font-bold leading-tight text-slate-900 tracking-tight">Why <span class="text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-amber-500">Trust Us?</span></h2>
              <p class="text-slate-500 font-medium text-lg">We prioritize quality, trust, and your satisfaction above all else.</p>
            </div>
            
            <div class="grid gap-8">
              <div v-for="benefit in benefits" :key="benefit.title" class="flex items-start gap-4 p-6 bg-white rounded-3xl shadow-sm border border-slate-100 group">
                <div class="w-14 h-14 rounded-2xl bg-blue-50 flex items-center justify-center group-hover:bg-primary-700 transition-colors">
                  <component :is="benefit.icon" class="w-7 h-7 text-primary-700 group-hover:text-white transition-colors" />
                </div>
                <div>
                  <h4 class="text-lg font-bold text-slate-900">{{ benefit.title }}</h4>
                  <p class="text-sm text-slate-500 font-medium leading-relaxed mt-1">{{ benefit.desc }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="relative flex justify-center animate-scale">
            <div class="grid grid-cols-2 gap-6 relative z-10 w-full">
              <div class="bg-white p-6 rounded-[2.5rem] shadow-premium space-y-4 translate-y-8">
                <div class="w-12 h-12 bg-emerald-100 rounded-2xl flex items-center justify-center">
                  <Star class="w-6 h-6 text-emerald-600 fill-emerald-600" />
                </div>
                <p class="text-2xl font-black text-slate-900 leading-none">4.9/5</p>
                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest leading-none">Customer Rating</p>
              </div>
              <div class="bg-white p-6 rounded-[2.5rem] shadow-premium space-y-4">
                <div class="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center">
                  <ShieldCheck class="w-6 h-6 text-primary-700" />
                </div>
                <p class="text-2xl font-black text-slate-900 leading-none">100%</p>
                <p class="text-xs font-bold text-slate-400 uppercase tracking-widest leading-none">Verified Pros</p>
              </div>
            </div>
            <!-- Background Image Blur -->
            <div class="absolute inset-0 bg-blue-400/10 blur-[100px] rounded-full"></div>
          </div>
        </div>
      </section>

      <!-- 5. Featured Services -->
      <section id="pricing" class="bg-white py-24 md:py-32 overflow-hidden animate-reveal">
        <div class="section-container">
          <div class="flex items-center justify-between mb-16">
            <h2 class="text-3xl md:text-[60px] font-bold leading-tight text-slate-900 tracking-tight">Popular <span class="text-transparent bg-clip-text bg-gradient-to-r from-emerald-500 to-teal-500">Repairs</span></h2>
            <div class="flex gap-4">
              <button @click="scrollServices('left')" class="w-12 h-12 rounded-full border border-slate-200 flex items-center justify-center text-slate-900 hover:bg-slate-50 transition-colors active:scale-95">
                <ChevronLeft class="w-6 h-6" />
              </button>
              <button @click="scrollServices('right')" class="w-12 h-12 rounded-full border border-slate-200 flex items-center justify-center text-slate-900 hover:bg-slate-50 transition-colors active:scale-95">
                <ChevronRight class="w-6 h-6" />
              </button>
            </div>
          </div>

          <div ref="servicesContainer" class="flex gap-8 overflow-x-auto hide-scrollbar snap-x pb-8 scroll-smooth">
            <div v-for="service in featuredServices" :key="service.name" 
              class="min-w-[320px] bg-white rounded-[3rem] p-6 border border-slate-100 shadow-xl shadow-slate-200/50 snap-center group">
              <div class="h-48 rounded-[2rem] overflow-hidden mb-6 relative">
                <img :src="service.img" @error="handleImageError" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
                <div class="absolute top-4 right-4 px-3 py-1 bg-white/90 backdrop-blur-md rounded-full text-xs font-bold text-slate-900 flex items-center gap-1">
                  <Star class="w-3 h-3 text-orange-500 fill-orange-500" />
                  {{ service.rating }}
                </div>
              </div>
              <div class="space-y-6">
                <div>
                  <h4 class="text-xl font-bold text-slate-900 mb-1">{{ service.name }}</h4>
                  <p class="text-sm text-slate-500 font-medium">Starts from <span class="text-emerald-600 font-bold">₹{{ service.price }}</span></p>
                </div>
                <button @click="router.push('/signup')" class="btn btn-secondary w-full rounded-2xl bg-white hover:bg-slate-50 hover:shadow-lg shadow-md shadow-slate-200/50 text-slate-900 border-0 transition-all">Book Now</button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 5.1 Testimonials Section -->
      <section class="bg-slate-50 section-container">
        <div class="text-center max-w-4xl mx-auto mb-20 space-y-4">
          <h2 class="text-3xl md:text-[60px] font-bold leading-tight text-slate-900 tracking-tight">What our <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-pink-600">customers</span> are saying</h2>
          <p class="text-slate-500 font-medium text-lg leading-relaxed">Hear from thousands of happy customers who experience our service daily.</p>
        </div>
        
        <div class="grid md:grid-cols-3 gap-8 pb-24">
          <div v-for="review in testimonials" :key="review.name" 
            class="bg-white p-8 rounded-[2.5rem] border border-slate-100 shadow-sm hover:shadow-premium transition-all">
            <div class="flex items-center gap-1 mb-6">
              <Star v-for="i in 5" :key="i" class="w-4 h-4 text-orange-500 fill-orange-500" />
            </div>
            <p class="text-slate-600 font-medium font-serif leading-relaxed mb-8">"{{ review.text }}"</p>
            <div class="flex items-center gap-4">
              <img :src="review.avatar" class="w-12 h-12 rounded-full border-2 border-primary-700/20" />
              <div>
                <h4 class="font-bold text-slate-900">{{ review.name }}</h4>
                <p class="text-[10px] font-black uppercase tracking-widest text-slate-400 mt-1">{{ review.service }} • {{ review.location }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 5.2 About Us Section -->
      <section id="about" class="bg-white py-24 md:py-32">
        <div class="section-container grid md:grid-cols-2 gap-12 items-center">
          <div class="relative h-[400px] rounded-[3rem] overflow-hidden shadow-2xl skew-y-2 border-[8px] border-slate-50">
             <img src="https://media.istockphoto.com/id/520113235/photo/multiethnic-people-in-circle-with-about-us-concept.jpg?s=612x612&w=0&k=20&c=xSoIZ1N07zrNyXPHdRievJT0I3oi0lKXva8-mQkU4ko=" 
               class="w-full h-full object-cover" alt="About Us" />
             <div class="absolute inset-0 bg-gradient-to-t from-slate-900/60 to-transparent"></div>
             <div class="absolute bottom-8 left-8 text-white">
                <p class="font-bold text-sm tracking-widest uppercase mb-1 opacity-80">Established 2024</p>
                <p class="text-2xl font-black">Hyderabad's #1 Repair Hub</p>
             </div>
          </div>
          <div class="space-y-8 animate-reveal">
            <div class="space-y-4">
              <div class="inline-flex items-center gap-2 px-3 py-1 bg-blue-100 text-primary-700 rounded-full text-xs font-bold uppercase tracking-wider">
                <MapPin class="w-3 h-3" /> Visit Our Store
              </div>
              <h2 class="text-3xl md:text-[60px] font-bold leading-tight text-slate-900 tracking-tight">About <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-700 to-indigo-800">Doorstep</span></h2>
              <p class="text-slate-500 font-medium leading-relaxed">
                We are a dedicated team of certified technicians committed to bringing premium mobile repair services directly to your location. Located in the heart of Hyderabad, we serve customers with speed, transparency, and original parts.
              </p>
            </div>
            
            <div class="space-y-4">
              <div class="flex items-start gap-4 p-4 bg-white rounded-2xl border border-slate-100 shadow-sm">
                <div class="w-10 h-10 bg-blue-50 rounded-xl flex items-center justify-center shrink-0">
                  <MapPin class="w-5 h-5 text-primary-700" />
                </div>
                <div>
                   <h4 class="font-bold text-slate-900">Our Location</h4>
                   <p class="text-sm text-slate-500 font-medium">KPHB Colony, Near Lulu Mall,<br>Hyderabad, Telangana</p>
                </div>
              </div>
              
              <div class="flex items-start gap-4 p-4 bg-white rounded-2xl border border-slate-100 shadow-sm">
                 <div class="w-10 h-10 bg-emerald-50 rounded-xl flex items-center justify-center shrink-0">
                   <Smartphone class="w-5 h-5 text-emerald-600" />
                 </div>
                 <div>
                    <h4 class="font-bold text-slate-900">Contact Us</h4>
                    <p class="text-sm text-slate-500 font-medium">Call/WhatsApp: <a href="tel:9390999539" class="text-primary-700 hover:underline">9390999539</a></p>
                 </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 5.3 FAQs Section -->
      <section id="faqs" class="bg-slate-50 section-container py-24">
        <div class="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <h2 class="text-3xl md:text-[60px] font-bold leading-tight text-slate-900 tracking-tight"><span class="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">FAQ</span></h2>
          <p class="text-slate-500 font-medium text-lg">Everything you need to know about our service.</p>
        </div>

        <div class="max-w-6xl mx-auto grid md:grid-cols-2 gap-6 items-start">
          <!-- Column 1 -->
          <div class="space-y-6">
            <div v-for="(faq, index) in faqs.slice(0, Math.ceil(faqs.length / 2))" :key="index" 
              class="bg-white shadow-md rounded-lg p-4 md:p-5 h-fit border border-slate-100">
              <button @click="faq.open = !faq.open" class="flex justify-between items-center w-full text-left font-bold text-base md:text-lg border-b border-gray-100 pb-4">
                 <span>{{ faq.question }}</span>
                 <span class="ml-3 flex-shrink-0">
                   <ChevronRight :class="['w-5 h-5 text-slate-400 transition-transform duration-300', faq.open ? 'rotate-90' : '']" />
                 </span>
              </button>
              <div v-show="faq.open" class="pt-4 text-sm md:text-base text-gray-700 text-left animate-fade-in">
                 {{ faq.answer }}
              </div>
            </div>
          </div>

          <!-- Column 2 -->
          <div class="space-y-6">
             <div v-for="(faq, index) in faqs.slice(Math.ceil(faqs.length / 2))" :key="index" 
              class="bg-white shadow-md rounded-lg p-4 md:p-5 h-fit border border-slate-100">
              <button @click="faq.open = !faq.open" class="flex justify-between items-center w-full text-left font-bold text-base md:text-lg border-b border-gray-100 pb-4">
                 <span>{{ faq.question }}</span>
                 <span class="ml-3 flex-shrink-0">
                   <ChevronRight :class="['w-5 h-5 text-slate-400 transition-transform duration-300', faq.open ? 'rotate-90' : '']" />
                 </span>
              </button>
              <div v-show="faq.open" class="pt-4 text-sm md:text-base text-gray-700 text-left animate-fade-in">
                 {{ faq.answer }}
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 6. Download App Section -->
      <section class="section-container">
        <div class="bg-grad-primary rounded-[4rem] p-12 md:p-20 grid lg:grid-cols-2 gap-12 items-center relative overflow-hidden">
          <!-- Background Decoration -->
          <div class="absolute top-0 right-0 w-96 h-96 bg-white/5 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2"></div>
          
          <div class="relative z-10 space-y-8">
            <div class="space-y-4">
              <h2 class="text-4xl md:text-5xl font-black text-white leading-tight">Services at Your Fingertips</h2>
              <p class="text-blue-100 text-lg font-medium opacity-80 max-w-md">Download our mobile app for real-time tracking, exclusive offers, and easier booking.</p>
            </div>
            
            <div class="flex flex-wrap gap-4">
              <button class="bg-white px-6 py-3 rounded-2xl flex items-center gap-3 hover:bg-blue-50 transition-colors">
                <img src="https://upload.wikimedia.org/wikipedia/commons/7/78/Google_Play_Store_badge_EN.svg" class="h-8" />
              </button>
              <button class="bg-white px-6 py-3 rounded-2xl flex items-center gap-3 hover:bg-blue-50 transition-colors">
                <img src="https://upload.wikimedia.org/wikipedia/commons/3/3c/Download_on_the_App_Store_Badge.svg" class="h-8" />
              </button>
            </div>

            <div class="flex items-center gap-4 p-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-3xl w-fit">
              <div class="w-20 h-20 bg-white p-2 rounded-2xl">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=https://doorstep.com" class="w-full h-full" />
              </div>
              <div class="text-white">
                <p class="text-sm font-black uppercase tracking-widest">Scan to Download</p>
                <p class="text-xs font-medium opacity-60 mt-1">Available for iOS & Android</p>
              </div>
            </div>
          </div>

          <div class="relative hidden lg:block">
            <div class="absolute inset-0 bg-blue-400/20 blur-[100px] rounded-full"></div>
            <img src="https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?auto=format&fit=crop&w=800&q=80" 
              class="w-80 mx-auto rounded-[3rem] shadow-2xl skew-x-[-4deg] relative z-10 border-[8px] border-white/20" />
          </div>
        </div>
      </section>
      <!-- 7. Call To Action (New) -->
      <section class="relative py-20 overflow-hidden">
        <div class="absolute inset-0">
          <img src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1600&q=80" class="w-full h-full object-cover" />
          <div class="absolute inset-0 bg-primary-900/80"></div>
        </div>
        <div class="section-container relative z-10 text-center flex flex-col items-center justify-center space-y-6">
          <h3 class="text-3xl md:text-4xl font-black text-white tracking-tight">Call To Action</h3>
          <p class="text-white/90 text-lg md:text-xl font-medium max-w-3xl leading-relaxed">
            Whether you're looking to grow your business, strengthen your online presence, or kickstart your career — we're here to help you succeed.
            <br class="hidden md:block">
            Partner with us, for expert digital marketing, smart business strategies, and industry-focused training that drives real results.
          </p>
          <a href="https://wa.me/919390999539" target="_blank" class="inline-flex items-center gap-3 bg-transparent border-2 border-white text-white px-8 py-3 rounded-full font-bold text-lg hover:bg-white hover:text-primary-900 transition-all duration-300 transform hover:scale-105">
            Call To Action
          </a>
        </div>
      </section>
    </main>

    <!-- 8. Compact Footer -->
    <footer class="bg-black border-t border-white/10 py-12">
      <div class="section-container grid md:grid-cols-4 gap-8 md:gap-12 text-sm">
        <div class="space-y-4">
          <div class="flex items-center gap-2">
            <div class="w-8 h-8 bg-primary-700/20 border border-primary-700/30 rounded-lg flex items-center justify-center">
              <Zap class="w-4 h-4 text-primary-400" />
            </div>
            <span class="text-xl font-black text-white font-outfit">Doorstep</span>
          </div>
          <p class="text-slate-400 leading-relaxed">
            Revolutionizing on-demand doorstep services with trusted professionals.
          </p>
          <div class="flex items-center gap-4 pt-2">
            <a href="#" class="w-8 h-8 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-slate-400 hover:text-white hover:bg-white/10 transition-all">
              <Instagram class="w-4 h-4" />
            </a>
            <a href="#" class="w-8 h-8 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-slate-400 hover:text-white hover:bg-white/10 transition-all">
              <Facebook class="w-4 h-4" />
            </a>
            <a href="#" class="w-8 h-8 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-slate-400 hover:text-white hover:bg-white/10 transition-all">
              <Twitter class="w-4 h-4" />
            </a>
            <a href="https://wa.me/919390999539" class="w-8 h-8 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-slate-400 hover:text-[#25D366] hover:bg-white/10 transition-all">
              <MessageCircle class="w-4 h-4" />
            </a>
          </div>
        </div>

        <div>
          <h4 class="text-white font-black mb-4 uppercase tracking-widest text-[10px] opacity-80">Helpful Links</h4>
          <ul class="space-y-2">
            <li v-for="l in ['About Us', 'Our Services', 'Pricing Plan', 'FAQs']" :key="l">
              <a href="#" class="text-slate-400 hover:text-white transition-colors">{{ l }}</a>
            </li>
          </ul>
        </div>

        <div>
          <h4 class="text-white font-black mb-4 uppercase tracking-widest text-[10px] opacity-80">Services</h4>
          <ul class="space-y-2">
            <li v-for="l in ['Display Fix', 'Battery Fix', 'Software Recovery', 'Motherboard Repair']" :key="l">
              <a href="#" class="text-slate-400 hover:text-white transition-colors">{{ l }}</a>
            </li>
          </ul>
        </div>

        <div>
          <h4 class="text-white font-black mb-4 uppercase tracking-widest text-[10px] opacity-80">Newsletter</h4>
          <div class="relative">
            <input type="email" placeholder="Email" class="w-full px-3 py-2 rounded-lg bg-white/5 border border-white/10 focus:outline-none focus:border-primary-500 text-white pr-10 text-xs placeholder:text-slate-600" />
            <button class="absolute right-1 top-1 w-7 h-7 bg-primary-700 text-white rounded flex items-center justify-center hover:bg-primary-600 transition-colors">
              <ArrowRight class="w-3 h-3" />
            </button>
          </div>
        </div>
      </div>
      
      <div class="section-container border-t border-white/10 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-xs">
        <p class="text-slate-500 font-bold">© 2026 Doorstep Technologies Inc.</p>
        <div class="flex gap-6">
          <router-link to="/privacy" class="text-slate-500 hover:text-white transition-colors">Privacy Policy</router-link>
          <router-link to="/terms" class="text-slate-500 hover:text-white transition-colors">Terms</router-link>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import HeroAnimation from '../components/HeroAnimation.vue'
import { 
  Zap, MapPin, Smartphone, ArrowRight, Menu, X,
  Settings, User, Star, ChevronLeft, ChevronRight,
  LayoutGrid, Battery, Cpu, Code, Headphones, Hammer, ShieldCheck, Camera,
  Search, Calendar, Truck, CreditCard,
  Droplets, ScanFace, Mic, Wifi, Tablet, Watch, Layers, Gauge,
  Instagram, Facebook, Twitter, MessageCircle
} from 'lucide-vue-next'

const scrolled = ref(false)
const mobileMenuOpen = ref(false)
const router = useRouter()
const authStore = useAuthStore()
const handleScroll = () => { scrolled.value = window.scrollY > 20 }

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  
  // Intersection Observer for scroll animations
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal-visible')
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.animate-reveal, .animate-scale').forEach((el) => {
    observer.observe(el);
  });
})

onUnmounted(() => window.removeEventListener('scroll', handleScroll))

const categoriesRow1 = [
  { name: 'Display Fix', desc: 'Screen replacement & glass repair', icon: Smartphone, bgColor: 'bg-blue-100', iconColor: 'text-blue-600' },
  { name: 'Power & Battery', desc: 'Original battery & charging fix', icon: Battery, bgColor: 'bg-emerald-100', iconColor: 'text-emerald-600' },
  { name: 'Camera Systems', desc: 'Lens & focus module repair', icon: Camera, bgColor: 'bg-rose-100', iconColor: 'text-rose-600' },
  { name: 'Logic Board', desc: 'Advanced micro-soldering fixes', icon: Cpu, bgColor: 'bg-orange-100', iconColor: 'text-orange-600' },
  { name: 'Software Fix', desc: 'OS repair & data recovery', icon: Code, bgColor: 'bg-indigo-100', iconColor: 'text-indigo-600' },
  { name: 'Audio Systems', desc: 'Speaker & mic port cleaning', icon: Headphones, bgColor: 'bg-amber-100', iconColor: 'text-amber-600' },
  { name: 'Hardware Buttons', desc: 'Power & volume switch fix', icon: Hammer, bgColor: 'bg-slate-100', iconColor: 'text-slate-600' },
  { name: 'Signal & Wifi', desc: 'Antenna & connectivity repair', icon: Wifi, bgColor: 'bg-cyan-100', iconColor: 'text-cyan-600' }
]

const categoriesRow2 = [
  { name: 'Water Damage', desc: 'Liquid exposure cleaning', icon: Droplets, bgColor: 'bg-sky-100', iconColor: 'text-sky-600' },
  { name: 'Back Glass', desc: 'Housing & frame replacement', icon: Layers, bgColor: 'bg-fuchsia-100', iconColor: 'text-fuchsia-600' },
  { name: 'Face ID & Sensors', desc: 'Biometric sensor calibration', icon: ScanFace, bgColor: 'bg-violet-100', iconColor: 'text-violet-600' },
  { name: 'Charging Port', desc: 'Dock connector replacement', icon: Zap, bgColor: 'bg-yellow-100', iconColor: 'text-yellow-600' },
  { name: 'Microphone Fix', desc: 'Audio input clarity repair', icon: Mic, bgColor: 'bg-red-100', iconColor: 'text-red-600' },
  { name: 'Tablet Repair', desc: 'iPad & Android tablet service', icon: Tablet, bgColor: 'bg-teal-100', iconColor: 'text-teal-600' },
  { name: 'Smart Watch', desc: 'Battery & screen for wearables', icon: Watch, bgColor: 'bg-lime-100', iconColor: 'text-lime-600' },
  { name: 'Diagnostics', desc: 'Full device health checkup', icon: Gauge, bgColor: 'bg-gray-100', iconColor: 'text-gray-600' }
]

const workflow = [
  { title: 'Choose Service', desc: 'Quickly find what you need from our categories.', icon: Search, blobColor: 'bg-blue-100', iconColor: 'text-blue-600', badgeColor: 'bg-blue-600' },
  { title: 'Select Schedule', desc: 'Pick a date and time that fits your day.', icon: Calendar, blobColor: 'bg-purple-100', iconColor: 'text-purple-600', badgeColor: 'bg-purple-600' },
  { title: 'Expert Arrives', desc: 'A verified professional comes to your location.', icon: Truck, blobColor: 'bg-orange-100', iconColor: 'text-orange-600', badgeColor: 'bg-orange-600' },
  { title: 'Pay & Relax', desc: 'Service completed with a quality guarantee.', icon: CreditCard, blobColor: 'bg-emerald-100', iconColor: 'text-emerald-600', badgeColor: 'bg-emerald-600' }
]

const benefits = [
  { title: 'Verified Professionals', desc: 'Background-checked and certified experts for every job.', icon: User },
  { title: 'Transparent Pricing', desc: 'No hidden fees. Pay what you see on the screen.', icon: ShieldCheck },
  { title: 'Flexible Scheduling', desc: 'Book instantly or schedule for later at your convenience.', icon: Zap }
]

const featuredServices = [
  { name: 'iPhone Screen Fix', price: '1,999', rating: '4.9', img: 'https://images.unsplash.com/photo-1556656793-062ff9878233?auto=format&fit=crop&w=600&q=80' },
  { name: 'Battery Replacement', price: '899', rating: '4.8', img: 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?auto=format&fit=crop&w=600&q=80' },
  { name: 'Water Damage Cure', price: '1,499', rating: '5.0', img: 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=600&q=80' },
  { name: 'Back Glass Repair', price: '1,299', rating: '4.7', img: 'https://images.unsplash.com/photo-1605236453806-6ff36851218e?auto=format&fit=crop&w=600&q=80' },
  { name: 'Charging Port Fix', price: '699', rating: '4.8', img: 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=600&q=80' },
  { name: 'Camera Replacement', price: '1,199', rating: '4.9', img: 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=600&q=80' },
  { name: 'Motherboard Repair', price: '2,999', rating: '5.0', img: 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=600&q=80' },
  { name: 'Software Update', price: '499', rating: '4.6', img: 'https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=600&q=80' }
]

const handleImageError = (e) => {
  e.target.src = 'https://images.unsplash.com/photo-1597740985671-2a8a3b80502e?auto=format&fit=crop&w=600&q=80'
}

const servicesContainer = ref(null)
const scrollServices = (direction) => {
  if (!servicesContainer.value) return
  const scrollAmount = 400
  servicesContainer.value.scrollLeft += direction === 'left' ? -scrollAmount : scrollAmount
}

const testimonials = [
  { name: 'Aditi Sharma', location: 'Bengaluru', service: 'Screen Replacement', text: 'The professional arrived on time and did an amazing job with my iPhone screen. It looks brand new now!', avatar: 'https://i.pravatar.cc/100?img=45' },
  { name: 'Rahul Verma', location: 'Mumbai', service: 'Battery Fix', text: 'Excellent service! My battery life is finally back to normal. The best part is I didn\'t have to leave my home.', avatar: 'https://i.pravatar.cc/100?img=52' },
  { name: 'Sneha Rao', location: 'Pune', service: 'Motherboard Repair', text: 'Highly technical and professional. They fixed a logic board issue that others said was impossible.', avatar: 'https://i.pravatar.cc/100?img=36' }
]

const faqs = ref([
  { question: 'Do you use original parts?', answer: 'Yes, we use 100% original OEM parts for all repairs to ensure maximum performance and longevity for your device.', open: true },
  { question: 'Is there a warranty on repairs?', answer: 'Absolutely! We offer a 6-month warranty on screen replacements and a 3-month warranty on other parts.', open: false },
  { question: 'How long does a repair take?', answer: 'Most repairs like screen or battery replacements are completed within 30-45 minutes at your doorstep.', open: false },
  { question: 'Do I need to backup my data?', answer: 'While our repairs are safe, we always recommend backing up your data as a precautionary measure before any service.', open: false },
  { question: 'Is there a visiting charge?', answer: 'We have a nominal visiting charge of ₹99, which is waived off if you proceed with any repair service.', open: false }
])
</script>

<style scoped>
.text-grad-primary {
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hide-scrollbar::-webkit-scrollbar {
  display: none;
}

/* Scroll Animation Observer Classes */
.reveal-visible {
  opacity: 1 !important;
  transform: translateY(0) !important;
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

.animate-reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

.perspective-1000 {
  perspective: 1000px;
}

.scene {
  width: 280px;
  height: 560px;
  perspective: 1000px;
  @media (max-width: 768px) {
    height: 400px;
  }
}

.phone-container {
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
}

.animate-spin-3d {
  animation: spin360 20s linear infinite;
}

@keyframes spin360 {
  0% { transform: rotateY(0deg) rotateX(10deg); }
  100% { transform: rotateY(360deg) rotateX(10deg); }
}

.face {
  position: absolute;
  background-color: #e2e8f0; /* Default chassis color - Titanium Silver */
  border: 1px solid #cbd5e1;
}

/* Dimensions Config */
/* Width: 280px, Height: 560px, Depth: 40px */

.front {
  width: 280px;
  height: 560px;
  transform: translateZ(20px); /* Depth/2 */
  border-radius: 40px;
  background: black;
  border: 4px solid #94a3b8; /* Bezel */
  overflow: hidden;
  backface-visibility: hidden;
}

.back {
  width: 280px;
  height: 560px;
  transform: rotateY(180deg) translateZ(20px);
  border-radius: 40px;
  background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%); /* Titanium finish */
  backface-visibility: hidden;
}

.right {
  width: 40px; /* Depth */
  height: 560px;
  left: 120px; /* (Width - Depth) / 2 = (280 - 40) / 2 = 120 */
  transform: rotateY(90deg) translateZ(140px); /* Width/2 */
  background: #94a3b8;
}

.left {
  width: 40px;
  height: 560px;
  left: 120px;
  transform: rotateY(-90deg) translateZ(140px);
  background: #cbd5e1;
}

.top {
  width: 280px;
  height: 40px;
  top: 260px; /* (Height - Depth) / 2 = (560 - 40) / 2 = 260 */
  transform: rotateX(90deg) translateZ(280px); /* Height/2 */
  background: #e2e8f0;
}

.bottom {
  width: 280px;
  height: 40px;
  top: 260px;
  transform: rotateX(-90deg) translateZ(280px);
  background: #94a3b8;
}

.screen-content {
  width: 100%;
  height: 100%;
  background: #0f172a;
  border-radius: 36px;
}

/* Marquee Animation */
.marquee {
  position: relative;
  width: 100%;
  overflow: hidden;
  mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);
}

.marquee-content {
  display: flex;
  width: max-content;
  animation: scroll 40s linear infinite;
}

.marquee-content:hover {
  animation-play-state: paused;
}

.marquee.reverse .marquee-content {
  animation: scroll-reverse 40s linear infinite;
}

@keyframes scroll {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}

@keyframes scroll-reverse {
  from { transform: translateX(-50%); }
  to { transform: translateX(0); }
}

/* Mobile Menu Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(100%);
}
</style>
