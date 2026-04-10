<template>
  <div class="animation-container w-full h-full flex justify-center items-center overflow-hidden">
    <div class="stage">
      <div class="circle-bg"></div>
      <div class="ring"></div>
      <div class="orbit"></div>
      <div class="orbit2"></div>

      <div class="scene">
        <div class="phone-wrap" ref="phoneWrap">

          <!-- FRONT -->
          <div class="phone-front">
            <div class="phone-screen">
              <div class="wallpaper"></div>

              <!-- Dynamic Island -->
              <div class="dynamic-island"></div>

              <!-- Status Bar -->
              <div class="status-bar">
                <div class="status-time">9:41</div>
                <div class="status-icons">
                  <div style="display:flex;gap:1.5px;align-items:flex-end">
                    <div class="signal-bar" style="height:3px"></div>
                    <div class="signal-bar" style="height:5px"></div>
                    <div class="signal-bar" style="height:7px"></div>
                    <div class="signal-bar" style="height:9px;background:rgba(255,255,255,0.35)"></div>
                  </div>
                  <div class="wifi-icon"></div>
                  <div class="battery"></div>
                </div>
              </div>

              <!-- Lock time -->
              <div class="lock-time">9:41</div>
              <div class="lock-date">Doorstep Service</div>

              <!-- Notifications -->
              <div class="notif-area">
                <div class="notif">
                  <div class="notif-icon" style="background:#1a8cff">💬</div>
                  <div class="notif-text">
                    <div class="notif-app">Messages · now</div>
                    <div class="notif-msg">Technician: I've arrived!</div>
                    <div class="notif-sub">Tap to reply</div>
                  </div>
                </div>
                <div class="notif">
                  <div class="notif-icon" style="background:linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888)">📱</div>
                  <div class="notif-text">
                    <div class="notif-app">Update · 2m ago</div>
                    <div class="notif-msg">Service Completed!</div>
                    <div class="notif-sub">Thank you for choosing us</div>
                  </div>
                </div>
              </div>

              <!-- Dock -->
              <div class="dock">
                <div class="dock-icon" style="background:#1cd14f">📞</div>
                <div class="dock-icon" style="background:#1a8cff">💬</div>
                <div class="dock-icon" style="background:#ff6820">🌐</div>
                <div class="dock-icon" style="background:#8b5cf6">🛡️</div>
              </div>

              <!-- Home bar -->
              <div class="home-bar"></div>

              <!-- Video overlay replacement -->
              <!-- By default we replace the video with pure CSS styling to avoid missing video files breaking the UI. -->

              <!-- Glare -->
              <div class="glare"></div>
            </div>
          </div>

          <!-- BACK -->
          <div class="phone-back">
            <!-- Camera module -->
            <div class="cam-module">
              <div class="cam-lens"></div>
              <div class="cam-lens"></div>
              <div class="cam-lens"></div>
              <div class="cam-flash"></div>
            </div>
            <!-- Laser bolt -->
            <div class="bolt">
              <svg viewBox="0 0 40 70"><polygon points="28,0 10,38 22,38 12,70 34,26 20,26" fill="rgba(60,130,255,0.7)"/></svg>
            </div>
          </div>

          <!-- FRAME EDGES -->
          <div class="phone-top"></div>
          <div class="phone-bottom"></div>
          
          <!-- SIDES -->
          <div class="phone-side phone-side-right"></div>
          <div class="phone-side phone-side-left"></div>

        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;600&family=Rajdhani:wght@300;500;700&display=swap');

.animation-container {
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Rajdhani', sans-serif;
  overflow: hidden;
  width: 100%;
  height: 100%;
}

@media (prefers-reduced-motion: reduce) {
  * {
    animation-play-state: paused !important;
  }
}

/* ── CIRCLE STAGE ── */
.stage {
  position: relative;
  width: 360px; 
  height: 360px;
  transform: scale(0.9);
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (min-width: 768px) {
  .stage { transform: scale(1.1); }
}
@media (min-width: 1024px) {
  .stage { transform: scale(1.2); }
}

.circle-bg {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 30%, #111838 0%, #06060f 65%);
  box-shadow:
    0 0 0 1px rgba(60,100,255,0.18),
    0 0 60px rgba(40,80,255,0.3),
    0 0 120px rgba(60,30,200,0.15),
    inset 0 0 80px rgba(5,5,30,0.9);
}

/* Spinning conic ring */
.ring {
  position: absolute;
  inset: -2px;
  border-radius: 50%;
  background: conic-gradient(
    from 0deg,
    transparent 0%, #5090ff 15%, transparent 30%,
    transparent 45%, #aa40ff 60%, transparent 75%,
    transparent 85%, #40c8ff 95%, transparent 100%
  );
  mask: radial-gradient(farthest-side, transparent calc(100% - 2px), #fff calc(100% - 2px));
  -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 2px), #fff calc(100% - 2px));
  animation: spin-ring 3s linear infinite;
}

@keyframes spin-ring { to { transform: rotate(360deg); } }

/* Orbit dots */
.orbit {
  position: absolute;
  inset: -22px;
  border-radius: 50%;
  border: 1px solid rgba(80,130,255,0.08);
  animation: orbit1 5s linear infinite;
  pointer-events: none;
}
.orbit::before {
  content: '';
  position: absolute;
  width: 10px; height: 10px; border-radius: 50%;
  background: #50a0ff;
  top: 50%; left: -6px;
  transform: translateY(-50%);
  box-shadow: 0 0 10px #50a0ff, 0 0 25px #50a0ff;
}

.orbit2 {
  position: absolute;
  inset: -28px;
  border-radius: 50%;
  animation: orbit2 9s linear infinite;
  pointer-events: none;
}
.orbit2::before {
  content: '';
  position: absolute;
  width: 6px; height: 6px; border-radius: 50%;
  background: #cc44ff;
  bottom: -3px; left: 50%;
  transform: translateX(-50%);
  box-shadow: 0 0 8px #cc44ff, 0 0 20px #cc44ff;
}

@keyframes orbit1 { to { transform: rotate(360deg); } }
@keyframes orbit2 { to { transform: rotate(-360deg); } }

/* ── 3D SCENE ── */
.scene {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  overflow: visible;
  perspective: 900px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* ── PHONE WRAPPER ── */
.phone-wrap {
  transform-style: preserve-3d;
  animation: rotate-phone 8s linear infinite;
  position: relative;
  width: 160px;
  height: 320px;
}

/* The true 3D infinite rotation */
@keyframes rotate-phone {
  0%   { transform: rotateY(0deg) translateY(0px); }
  25%  { transform: rotateY(90deg) translateY(-8px); }
  50%  { transform: rotateY(180deg) translateY(0px); }
  75%  { transform: rotateY(270deg) translateY(-8px); }
  100% { transform: rotateY(360deg) translateY(0px); }
}

/* ── PHONE FRONT FACE ── */
.phone-front {
  position: absolute;
  width: 160px; height: 320px;
  border-radius: 28px;
  background: #08080f;
  transform: translateZ(6px); /* Half overall depth of 12px */
  overflow: hidden;
  box-shadow:
    inset 0 0 0 1.5px rgba(60,100,255,0.5),
    inset 0 0 0 3px rgba(15,20,60,0.9),
    0 0 30px rgba(40,80,255,0.4);
  backface-visibility: hidden;
}

/* Screen area */
.phone-screen {
  position: absolute;
  inset: 4px;
  border-radius: 24px;
  overflow: hidden;
  background: #060618;
}

/* Wallpaper */
.wallpaper {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(ellipse at 20% 20%, rgba(60,0,180,0.7) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 60%, rgba(0,60,200,0.6) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 90%, rgba(120,0,160,0.5) 0%, transparent 50%),
    linear-gradient(160deg, #0a0820 0%, #0d1040 40%, #080820 100%);
}

.wallpaper::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    radial-gradient(1px 1px at 20% 15%, rgba(255,255,255,0.8) 0%, transparent 100%),
    radial-gradient(1px 1px at 70% 10%, rgba(255,255,255,0.6) 0%, transparent 100%),
    radial-gradient(1px 1px at 40% 25%, rgba(255,255,255,0.7) 0%, transparent 100%),
    radial-gradient(1px 1px at 85% 30%, rgba(255,255,255,0.5) 0%, transparent 100%),
    radial-gradient(1px 1px at 10% 40%, rgba(255,255,255,0.6) 0%, transparent 100%);
}

.dynamic-island {
  position: absolute;
  top: 10px; left: 50%;
  transform: translateX(-50%);
  width: 60px; height: 14px;
  background: #000;
  border-radius: 10px;
  z-index: 10;
  box-shadow: 0 0 0 1px rgba(255,255,255,0.05);
}

.status-bar {
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 36px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding: 0 14px 4px;
  z-index: 9;
}
.status-time { font-size: 9px; font-weight: 700; color: #fff; font-family: -apple-system, sans-serif; }
.status-icons { display: flex; align-items: center; gap: 3px; }
.signal-bar { width: 2.5px; background: rgba(255,255,255,0.9); border-radius: 1px; }
.wifi-icon { width: 8px; height: 6px; border: 1.5px solid rgba(255,255,255,0.9); border-bottom: none; border-radius: 6px 6px 0 0; position: relative; margin: 0 1px; }
.wifi-icon::before { content:''; position: absolute; width: 4px; height: 3px; border: 1.5px solid rgba(255,255,255,0.9); border-bottom: none; border-radius: 4px 4px 0 0; top: 1.5px; left: 0.5px; }
.battery { width: 14px; height: 7px; border: 1px solid rgba(255,255,255,0.7); border-radius: 1.5px; position: relative; margin-left: 2px; }
.battery::before { content:''; position: absolute; right: -4px; top: 50%; transform: translateY(-50%); width: 2px; height: 4px; background: rgba(255,255,255,0.5); border-radius: 0 1px 1px 0; }
.battery::after { content:''; position: absolute; inset: 1.5px 2.5px; background: #4eff6a; border-radius: 1px; }

.lock-time {
  position: absolute;
  top: 48px;
  width: 100%;
  text-align: center;
  color: #fff;
  font-family: -apple-system, sans-serif;
  font-size: 34px;
  font-weight: 200;
  letter-spacing: -1px;
  text-shadow: 0 0 20px rgba(100,150,255,0.5);
}
.lock-date {
  position: absolute;
  top: 90px;
  width: 100%;
  text-align: center;
  color: rgba(255,255,255,0.75);
  font-family: -apple-system, sans-serif;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.05em;
}

.notif-area {
  position: absolute;
  top: 112px;
  left: 8px; right: 8px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.notif {
  background: rgba(255,255,255,0.10);
  backdrop-filter: blur(20px);
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.12);
  padding: 7px 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.notif-icon {
  width: 24px; height: 24px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  flex-shrink: 0;
}
.notif-text { flex: 1; min-width: 0; text-align: left; }
.notif-app { font-size: 6.5px; color: rgba(255,255,255,0.6); font-family: -apple-system, sans-serif; margin-bottom: 1px; }
.notif-msg { font-size: 7.5px; color: #fff; font-family: -apple-system, sans-serif; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.notif-sub { font-size: 6.5px; color: rgba(255,255,255,0.55); font-family: -apple-system, sans-serif; }

.dock {
  position: absolute;
  bottom: 14px;
  left: 8px; right: 8px;
  background: rgba(255,255,255,0.10);
  backdrop-filter: blur(30px);
  border-radius: 18px;
  border: 1px solid rgba(255,255,255,0.12);
  padding: 7px 10px;
  display: flex;
  justify-content: space-around;
  align-items: center;
}
.dock-icon {
  width: 28px; height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
}

.home-bar {
  position: absolute;
  bottom: 6px;
  left: 50%; transform: translateX(-50%);
  width: 40px; height: 3px;
  background: rgba(255,255,255,0.5);
  border-radius: 2px;
}

.glare {
  position: absolute;
  top: -30%; left: -20%;
  width: 60%; height: 80%;
  background: linear-gradient(135deg, rgba(255,255,255,0.08) 0%, transparent 60%);
  border-radius: 50%;
  pointer-events: none;
  transform: rotate(-20deg);
}

/* ── PHONE BACK FACE ── */
.phone-back {
  position: absolute;
  width: 160px; height: 320px;
  border-radius: 28px;
  background: linear-gradient(145deg, #0e0e22 0%, #090914 50%, #0c0c1e 100%);
  transform: translateZ(-6px) rotateY(180deg);
  box-shadow: inset 0 0 0 1.5px rgba(40,70,200,0.4), inset 0 0 0 3px rgba(10,10,40,0.9);
  overflow: hidden;
  backface-visibility: hidden;
}

.phone-back::before {
  content: '';
  position: absolute;
  top: -20%; left: -30%;
  width: 80%; height: 60%;
  background: linear-gradient(135deg, rgba(60,80,255,0.08) 0%, transparent 60%);
  border-radius: 50%;
}

.cam-module {
  position: absolute;
  top: 24px; right: 14px;
  width: 52px; height: 52px;
  background: linear-gradient(135deg, #0a0a20, #111130);
  border-radius: 14px;
  border: 1px solid rgba(60,80,200,0.3);
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 4px;
  padding: 6px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.6);
}

.cam-lens {
  border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, #1a2050, #050510);
  border: 1px solid rgba(255,255,255,0.08);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cam-lens::after {
  content: '';
  width: 40%;
  height: 40%;
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, rgba(80,120,255,0.5), rgba(20,30,100,0.8));
}

.cam-flash {
  border-radius: 50%;
  background: radial-gradient(circle, #ffeeaa, #cc9900);
  border: 1px solid rgba(255,200,50,0.3);
  box-shadow: 0 0 6px rgba(255,180,0,0.4);
}

.bolt {
  position: absolute;
  bottom: 80px;
  left: 50%; 
  transform: translateX(-50%);
  width: 0;
  height: 0;
  opacity: 0.8;
}

.bolt svg {
  width: 40px; height: 70px;
  transform: translateX(-50%);
}

/* ── PHONE SIDES (Connecting Front & Back) ── */
.phone-side {
  position: absolute;
  background: linear-gradient(180deg, #1a2255, #0a0e28, #1a2255);
  top: 14px; bottom: 14px;
}
.phone-side-right {
  right: 0;
  width: 12px;
  transform: rotateY(90deg) translateZ(0px); /* Extrudes the side outwards */
  transform-origin: right center;
  border-radius: 0 6px 6px 0;
}
.phone-side-left {
  left: 0;
  width: 12px;
  transform: rotateY(-90deg) translateZ(0px); 
  transform-origin: left center;
  border-radius: 6px 0 0 6px;
}

/* ── PHONE FRAME EDGES (top/bottom) ── */
.phone-top {
  position: absolute;
  top: 0; left: 14px; right: 14px;
  height: 12px;
  background: linear-gradient(90deg, #1a2255, #0a0e28, #1a2255);
  transform: rotateX(90deg);
  transform-origin: top center;
  border-radius: 6px 6px 0 0;
}
.phone-bottom {
  position: absolute;
  bottom: 0; left: 14px; right: 14px;
  height: 12px;
  background: linear-gradient(90deg, #1a2255, #0a0e28, #1a2255);
  transform: rotateX(-90deg);
  transform-origin: bottom center;
  border-radius: 0 0 6px 6px;
}
</style>
