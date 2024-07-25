import { createRouter, createWebHistory } from 'vue-router';
import FrequencyTab from '../components/FrequencyTab.vue';
import ProbabilityTab from '../components/ProbabilityTab.vue';

const routes = [
    { path: '/', redirect: '/frequency' },
    { path: '/frequency', name: 'frequency', component: FrequencyTab },
    { path: '/probability', name: 'probability', component: ProbabilityTab },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
