<template>
  <Transition
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="transform translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
    enter-to-class="transform translate-y-0 opacity-100 sm:translate-x-0"
    leave-active-class="transition duration-200 ease-in"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="visible"
      class="fixed bottom-5 right-5 z-50 flex items-start gap-3 max-w-md w-full sm:w-auto p-4 rounded-xl border shadow-lg font-formal-sans backdrop-blur-md"
      :class="styles.wrapper"
    >
      <!-- State Icon -->
      <div class="flex-shrink-0 mt-0.5">
        <svg class="w-5 h-5" :class="styles.iconColor" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <!-- Success Icon -->
          <template v-if="type === 'success'">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
            <polyline points="22 4 12 14.01 9 11.01" />
          </template>
          <!-- Info Icon -->
          <template v-else-if="type === 'info'">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="16" x2="12" y2="12" />
            <line x1="12" y1="8" x2="12.01" y2="8" />
          </template>
          <!-- Error Icon -->
          <template v-else>
            <circle cx="12" cy="12" r="10" />
            <line x1="15" y1="9" x2="9" y2="15" />
            <line x1="9" y1="9" x2="15" y2="15" />
          </template>
        </svg>
      </div>

      <!-- Text Payload -->
      <div class="flex-1">
        <p class="text-xs font-bold uppercase tracking-wider text-gray-400 font-formal-sans">System Notification</p>
        <p class="text-sm font-medium mt-0.5" :class="styles.textColor">
          {{ message }}
        </p>
      </div>

      <!-- Dismiss Button Trigger -->
      <button
        @click="visible = false"
        class="flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors rounded p-0.5"
      >
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// Define explicit dictionary types for Toast Configurations
type ToastType = 'success' | 'error' | 'info';

const message = ref<string>('');
const type = ref<ToastType>('error');
const visible = ref<boolean>(false);

let timeoutId: ReturnType<typeof setTimeout> | null = null;

// Design mapping corresponding directly to your new corporate design syntax
const styles = computed(() => {
  switch (type.value) {
    case 'success':
      return {
        wrapper: 'bg-emerald-50/95 border-emerald-200 shadow-emerald-950/5',
        iconColor: 'text-emerald-600',
        textColor: 'text-emerald-950'
      };
    case 'info':
      return {
        wrapper: 'bg-blue-50/95 border-blue-200 shadow-blue-950/5',
        iconColor: 'text-blue-600',
        textColor: 'text-blue-950'
      };
    case 'error':
    default:
      return {
        wrapper: 'bg-orange-50/95 border-orange-200 shadow-orange-950/5',
        iconColor: 'text-orange-600',
        textColor: 'text-orange-950'
      };
  }
});

/**
 * Triggers the notification overlay
 * @param msg The string description loaded into the body
 * @param toastType Strict string notification state
 */
const show = (msg: string, toastType: ToastType = 'error'): void => {
  // Clear any active hanging schedules first to prevent premature vanishing
  if (timeoutId) {
    clearTimeout(timeoutId);
  }

  message.value = msg;
  type.value = toastType;
  visible.value = true;

  timeoutId = setTimeout(() => {
    visible.value = false;
    timeoutId = null;
  }, 4500);
};

// Explicitly export operational method safely onto component reference context
defineExpose({ show });
</script>

<style>
/* Font bindings for standalone environments if missing from primary index view */
.font-formal-sans {
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
}
</style>