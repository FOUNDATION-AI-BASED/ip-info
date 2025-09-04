import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';
import App from './App.vue';
import Home from './views/Home.vue';
import IPDetails from './views/IPDetails.vue';
import About from './views/About.vue';
import ApiDocs from './views/ApiDocs.vue';

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Home },
    { path: '/ip/:ip', component: IPDetails, props: true },
    { path: '/about', component: About },
    { path: '/docs', component: ApiDocs },
  ]
});

// Create and mount the app
createApp(App)
  .use(router)
  .mount('#app');
