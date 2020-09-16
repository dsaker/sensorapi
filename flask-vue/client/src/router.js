import Vue from 'vue';
import Router from 'vue-router';
import Sensors from './components/Sensors.vue';
import Ping from './components/Ping.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Sensors',
      component: Sensors,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
});
