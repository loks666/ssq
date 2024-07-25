<template>
  <div id="app">
    <div class="menu">
      <button
          :class="activeIndex === 'frequency' ? 'active' : 'inactive'"
          @click="handleSelect('frequency')"
      >
        频率
      </button>
      <button
          :class="activeIndex === 'probability' ? 'active' : 'inactive'"
          @click="handleSelect('probability')"
      >
        概率
      </button>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  data() {
    return {
      activeIndex: 'frequency',
    };
  },
  methods: {
    handleSelect(key) {
      this.activeIndex = key;
      this.$router.push({ name: key });
    },
  },
};
</script>

<style scoped>
#app {
  text-align: center;
  padding-top: 20px;
}

.menu {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 10px; /* 减少间距 */
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 16px;
}

button.active {
  background-color: #007bff;
  color: white;
}

button.inactive {
  background-color: #f2f2f2;
  color: black;
  border: 1px solid #ddd;
}
</style>
