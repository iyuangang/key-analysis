import { createRouter, createWebHistory } from 'vue-router'
import { auth } from './services/auth'
import { debug } from './utils/debug'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: () => import('./views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('./views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'root',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('./views/Dashboard.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  debug.log('Navigation guard:', { to, from, authenticated: auth.isAuthenticated() })

  if (to.meta.requiresAuth && !auth.isAuthenticated()) {
    debug.log('Unauthorized access, redirecting to login')
    next('/login')
  } else if (to.path === '/login' && auth.isAuthenticated()) {
    debug.log('Already authenticated, redirecting to dashboard')
    next('/dashboard')
  } else {
    debug.log('Navigation allowed:', to.path)
    next()
  }
})

export default router 
