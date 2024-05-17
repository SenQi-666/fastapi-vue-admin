import { createRouter, createWebHistory } from 'vue-router'
import BasicLayout from '@/layouts/basicLayout.vue'
import Login from '@/views/system/auth/login.vue'
import storage from 'store'
import store from '@/store'
import { generator } from './generateRouter'
import { listToTree } from '@/utils/util'


const routes = [
  { path: '/login', name: 'Login', component: Login },
  { path: '/:catchAll(.*)', name: '404', meta: { title: '404' }, component: () => import('../views/exception/404.vue') },
]

const rootRouter = {
  path: '/',
  name: 'Index',
  redirect: '/dashboard/workplace',
  component: BasicLayout,
  children: [
    {
      path: '/profile',
      name: 'Profile',
      meta: {
        title: '个人中心',
        keepAlive: true,
      },
      component: () => import('../views/current/profile.vue')
    }
  ]
}

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach(to => {
  const token = storage.get('Access-Token')

  if (!token && to.name !== 'Login') {
    return { name: 'Login' }
  } else if (token && to.name === 'Login') {
    return { name: 'Index' }
  } else if (token && !store.state.user.hasGetRoute) {
    return store.dispatch('getUserInfo').then(() => {
      const routersTree = listToTree(store.state.user.routeList);
      const routerMap = generator(routersTree)
      rootRouter.children = [ ...rootRouter.children, ...routerMap ];
      router.addRoute(rootRouter)
      return to.fullPath
    })
  }
})
export default router
