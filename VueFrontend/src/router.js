import { createWebHistory, createRouter } from 'vue-router'

import Login  from './pages/Login.vue';
import UserInfo from './pages/UserInfo.vue';
import CreateUser from './pages/CreateUser.vue';
import { getUsersData } from '@/controllers/usersController'
import { useLoginStore } from '@/stores/auth'

const routes = [
  { path: '/', component: Login, meta: { requiresAuth: false }  },
  { path: '/user-info', component: UserInfo, meta: { requiresAuth: true } },
  { path: '/sign-up', component: CreateUser, meta: { requiresAuth: false } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})


router.beforeEach(async (to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (!requiresAuth) return next()

  const token = localStorage.getItem('token')
  if (!token) {
    return next('/')
  }

  const user = await getUsersData()
  if (!user) {
    localStorage.clear()
    return next('/')
  }

  const authStore = useLoginStore()
  authStore.successfulLogin(user.username)
  return next()
})

export default router