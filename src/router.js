import { createMemoryHistory, createRouter } from 'vue-router'

import Login  from './Login.vue';
import UserInfo from './UserInfo.vue';

const routes = [
  { path: '/', component: Login },
  { path: '/user-info', component: UserInfo },
]

const router = createRouter({
  history: createMemoryHistory(),
  routes,
})

export default router