import Vue from 'vue'
import Router from 'vue-router'
//import HelloWorld from '@/components/HelloWorld'

const routerOptions = [
	{ path: '/', component: 'Home' },
  	{ path: '/reg', component: 'Reg' },
  	{ path: '/ver', component: 'Ver' },
  	{ path: '/iden', component: 'Iden' },
  	{ path: '*', component: 'NotFound' }
]
const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})


Vue.use(Router)

/*
export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    }
  ]
})
*/

export default new Router({
  routes,
  mode: 'history'
})