import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/components/Home.vue';
import Exchanges from '@/components/Exchanges.vue';
/*import Information from '@/components/Information.vue';
import Registration from '@/components/Registration.vue';
import Login from '@/components/Login.vue';*/

const routes = [
  { path: '/', component: Home },
  { path: '/exchanges', component: Exchanges },
/*  { path: '/information', component: Information },
  { path: '/registration', component: Registration },
  { path: '/login', component: Login },*/
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
