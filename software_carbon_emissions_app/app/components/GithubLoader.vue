<template>
  <Transition name="fade">
    <div v-if="isLoading" class="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-black/60 backdrop-blur-sm">
      
      <div class="relative flex items-center justify-center mb-6">
        <div class="absolute w-16 h-16 border-4 border-white/20 rounded-full"></div>
        <div class="absolute w-16 h-16 border-4 border-transparent border-t-[#22c55e] border-r-[#22c55e] rounded-full animate-spin"></div>
        
        <svg class="w-6 h-6 text-white" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.929.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
        </svg>
      </div>

      <div class="h-8 overflow-hidden text-center relative w-64">
        <Transition name="slide-up" mode="out-in">
          <p :key="currentMessage" class="text-white text-base font-medium tracking-wide">
            {{ currentMessage }}
          </p>
        </Transition>
      </div>
      
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from 'vue';

const props = defineProps<{
  isLoading: boolean;
}>();

const messages = [
  'Fetching Git Repo data...',
  'Gathering Commits...',
  'Retrieving CI/CD runs...',
  'Analyzing contributors...',
  'Finalizing calculations...'
];

const currentIndex = ref(0);
const currentMessage = ref(messages[0]);
let intervalId: ReturnType<typeof setInterval> | null = null;

const startCycling = () => {
  // Extra safety net: exit if we somehow run on the server
  if (typeof window === 'undefined') return; 

  currentIndex.value = 0;
  currentMessage.value = messages[0];
  
  intervalId = setInterval(() => {
    if (currentIndex.value < messages.length - 1) {
      currentIndex.value++;
    } 
    currentMessage.value = messages[currentIndex.value];
  }, 5000);
};

const stopCycling = () => {
  if (intervalId) {
    clearInterval(intervalId);
    intervalId = null;
  }
};

// 1. Watch for changes without 'immediate: true'
watch(() => props.isLoading, (newVal) => {
  if (newVal) {
    startCycling();
  } else {
    stopCycling();
  }
});

// 2. Handle the initial load exclusively on the client side
onMounted(() => {
  if (props.isLoading) {
    startCycling();
  }
});

onUnmounted(() => {
  stopCycling();
});
</script>

<style scoped>
/* Overlay Fade */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Text Slide Animation */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}
.slide-up-enter-from {
  opacity: 0;
  transform: translateY(15px);
}
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-15px);
}
</style>