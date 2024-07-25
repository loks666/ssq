import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './style.css';
import 'simplebar/dist/simplebar.css';

createApp(App).use(router).mount('#app');
