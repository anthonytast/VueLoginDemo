import { createWebHistory, createRouter } from 'vue-router'

import Login  from './pages/Login.vue';
import UserInfo from './pages/UserInfo.vue';

const routes = [
  { path: '/', component: Login },
  { path: '/user-info', component: UserInfo },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

/*
createWebHistory uses the browser's HTML5 History API, 
which updates the URL in the address bar and allows natural 
browser navigation (back/forward). In contrast, createMemoryHistory 
keeps the navigation history in memory without altering the URL, 
making it more suitable for non-browser environments or testing.
*/