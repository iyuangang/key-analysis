import { createRouter, createWebHistory } from 'vue-router'
import { auth } from './services/auth'
import { debug } from './utils/debug'
import type { RouteRecordRaw } from 'vue-router'
import type { NavigationGuardNext, RouteLocationNormalized } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'login',
    component: () => import('./views/Login.vue'),
    meta: {
      requiresAuth: false,
      title: '登录'
    }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('./views/Register.vue'),
    meta: {
      requiresAuth: false,
      title: '注册'
    }
  },
  {
    path: '/',
    component: () => import('./layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'root',
        redirect: '/dashboard'
      },
      {
        path: 'dashboard',
        name: 'dashboard',
        component: () => import('./views/Dashboard.vue'),
        meta: {
          requiresAuth: true,
          title: '仪表盘'
        }
      },
      {
        path: 'analysis',
        name: 'analysis',
        component: () => import('./views/Analysis.vue'),
        meta: {
          requiresAuth: true,
          title: '密钥分析'
        }
      },
      {
        path: 'statistics',
        name: 'statistics',
        component: () => import('./views/Statistics.vue'),
        meta: {
          requiresAuth: true,
          title: '统计报告'
        }
      },
      {
        path: 'about',
        name: 'about',
        component: () => import('./views/About.vue'),
        meta: {
          requiresAuth: false,
          title: '关于系统'
        }
      },
      {
        path: 'user',
        name: 'user',
        component: () => import('./views/User.vue'),
        meta: {
          requiresAuth: true,
          title: '个人中心'
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
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
