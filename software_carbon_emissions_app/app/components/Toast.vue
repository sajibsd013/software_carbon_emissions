<template>
  <Transition>
    <div
      v-if="visible"
      :class="['toast', `toast-${type}`]"
    >
      {{ message }}
    </div>
  </Transition>
</template>

<script setup lang="ts">
const message = ref('');
const type = ref('error');
const visible = ref(false);

const show = (msg, toastType = 'error') => {
  message.value = msg;
  type.value = toastType;
  visible.value = true;

  setTimeout(() => {
    visible.value = false;
  }, 4000);
};

defineExpose({ show });
</script>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.3s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
