import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      animation: {
        // Floating animations
        'float-smooth': 'floatSmooth 3s ease-in-out infinite',
        'float-particle-1': 'floatParticle1 4s ease-in-out infinite',
        'float-particle-2': 'floatParticle2 5s ease-in-out infinite',
        'float-particle-3': 'floatParticle3 6s ease-in-out infinite',
        'float-particle-4': 'floatParticle4 4.5s ease-in-out infinite',

        // Pulsing animations
        'pulse-slow': 'pulseSlow 4s ease-in-out infinite',
        'pulse-glow': 'pulseGlow 2s ease-in-out infinite',

        // Spinning animations
        'spin-slow': 'spin 8s linear infinite',
        'spin-reverse': 'spinReverse 10s linear infinite',
        'spin-slow-reverse': 'spinReverse 6s linear infinite',

        // 3D tilt animation
        'tilt-3d': 'tilt3d 6s ease-in-out infinite',

        // Blinking animations
        'blink': 'blink 4s ease-in-out infinite',
        'blink-delayed': 'blink 4s ease-in-out 2s infinite',

        // Wave animations for arms
        'wave-left': 'waveLeft 2s ease-in-out infinite',
        'wave-right': 'waveRight 2s ease-in-out infinite',

        // Twinkle animations
        'twinkle-1': 'twinkle 1.5s ease-in-out infinite',
        'twinkle-2': 'twinkle 2s ease-in-out 0.5s infinite',
        'twinkle-3': 'twinkle 1.8s ease-in-out 1s infinite',
      },
      keyframes: {
        floatSmooth: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        floatParticle1: {
          '0%, 100%': { transform: 'translate(0, 0)', opacity: '0.3' },
          '25%': { transform: 'translate(10px, -20px)', opacity: '1' },
          '50%': { transform: 'translate(-5px, -40px)', opacity: '0.5' },
          '75%': { transform: 'translate(-15px, -20px)', opacity: '1' },
        },
        floatParticle2: {
          '0%, 100%': { transform: 'translate(0, 0)', opacity: '0.4' },
          '33%': { transform: 'translate(-15px, -25px)', opacity: '1' },
          '66%': { transform: 'translate(10px, -35px)', opacity: '0.6' },
        },
        floatParticle3: {
          '0%, 100%': { transform: 'translate(0, 0)', opacity: '0.3' },
          '50%': { transform: 'translate(20px, -30px)', opacity: '1' },
        },
        floatParticle4: {
          '0%, 100%': { transform: 'translate(0, 0)', opacity: '0.5' },
          '40%': { transform: 'translate(-20px, -15px)', opacity: '1' },
          '80%': { transform: 'translate(15px, -25px)', opacity: '0.7' },
        },
        pulseSlow: {
          '0%, 100%': { opacity: '0.6', transform: 'scale(1)' },
          '50%': { opacity: '1', transform: 'scale(1.05)' },
        },
        pulseGlow: {
          '0%, 100%': { opacity: '0.5', transform: 'scale(0.95)' },
          '50%': { opacity: '0.8', transform: 'scale(1.1)' },
        },
        spinReverse: {
          '0%': { transform: 'rotate(360deg)' },
          '100%': { transform: 'rotate(0deg)' },
        },
        tilt3d: {
          '0%, 100%': { transform: 'perspective(1000px) rotateY(0deg) rotateX(0deg)' },
          '25%': { transform: 'perspective(1000px) rotateY(5deg) rotateX(2deg)' },
          '50%': { transform: 'perspective(1000px) rotateY(0deg) rotateX(5deg)' },
          '75%': { transform: 'perspective(1000px) rotateY(-5deg) rotateX(2deg)' },
        },
        blink: {
          '0%, 90%, 100%': { transform: 'scaleY(1)' },
          '95%': { transform: 'scaleY(0.1)' },
        },
        waveLeft: {
          '0%, 100%': { transform: 'translateY(-50%) rotate(-5deg)' },
          '50%': { transform: 'translateY(-50%) rotate(-15deg)' },
        },
        waveRight: {
          '0%, 100%': { transform: 'translateY(-50%) rotate(5deg)' },
          '50%': { transform: 'translateY(-50%) rotate(15deg)' },
        },
        twinkle: {
          '0%, 100%': { opacity: '0.2', transform: 'scale(0.8)' },
          '50%': { opacity: '1', transform: 'scale(1.2)' },
        },
      },
    },
  },
  plugins: [],
};

export default config;
