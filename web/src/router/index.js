import Vue from 'vue'
import Router from 'vue-router'

// in development-env not use lazy-loading, because lazy-loading too many pages will cause webpack hot update too slow. so only in production use lazy-loading;
// detail: https://panjiachen.github.io/vue-element-admin-site/#/lazy-loading

Vue.use(Router)

/* Layout */
import Layout from '../views/layout/Layout'

/**
* hidden: true                   if `hidden:true` will not show in the sidebar(default is false)
* alwaysShow: true               if set true, will always show the root menu, whatever its child routes length
*                                if not set alwaysShow, only more than one route under the children
*                                it will becomes nested mode, otherwise not show the root menu
* redirect: noredirect           if `redirect:noredirect` will no redirect in the breadcrumb
* name:'router-name'             the name is used by <keep-alive> (must set!!!)
* meta : {
    title: 'title'               the name show in subMenu and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if false, the item will hidden in breadcrumb(default is true)
  }
**/
export const constantRouterMap = [
  { path: '/login', component: () => import('@/views/login/index'), hidden: true },
  { path: '/404', component: () => import('@/views/404'), hidden: true },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    name: 'Dashboard',
    hidden: true,
    children: [{
      path: 'dashboard',
      component: () => import('@/views/dashboard/index')
    }]
  },

  // {
  //   path: '/example',
  //   component: Layout,
  //   redirect: '/example/table',
  //   name: 'Example',
  //   meta: { title: 'Example', icon: 'example' },
  //   children: [
  //     {
  //       path: 'table',
  //       name: 'Table',
  //       component: () => import('@/views/table/index'),
  //       meta: { title: 'Table', icon: 'table' }
  //     },
  //     {
  //       path: 'tree',
  //       name: 'Tree',
  //       component: () => import('@/views/tree/index'),
  //       meta: { title: 'Tree', icon: 'tree' }
  //     }
  //   ]
  // },
  // {
  //   path: '/form',
  //   component: Layout,
  //   children: [
  //     {
  //       path: 'index',
  //       name: 'Form',
  //       component: () => import('@/views/form/index'),
  //       meta: { title: 'Form', icon: 'form' }
  //     }
  //   ]
  // },
  {
    path: '/retrieval',
    component: Layout,
    redirect: '/retrieval/index',
    children: [
      {
        path: 'index',
        component: () => import('@/views/retrieval/index'),
        name: 'retrievalOptions',
        meta: { title: '人脸检索', icon: 'form', noCache: true }
      },
      {
        path: ':retrievalID/start',
        component: () => import('@/views/retrieval/start'),
        hidden: true,
        props: true,
        name: 'retrievalStart',
        meta: { title: '人脸检索', icon: 'form', noCache: true }
      }
    ]
  },
  {
    path: '/history',
    component: Layout,
    name: 'history',
    children: [{ path: 'log', component: () => import('@/views/history/index'), name: 'history', meta: { title: '检索记录', icon: 'bug' }}]
  },
  {
    path: '/library',
    component: Layout,
    name: 'library',
    // redirect: '/library/index',
    children: [
      // {path: ':libraryID/feature',component: () => import('@/views/library/feature'),hidden: true,  name: 'feature',meta: {title: '特征',icon: 'eye-open' }},
      // {path: ':libraryID/distance',component: () => import('@/views/library/distance'),hidden: true, name: 'distance',meta: {title: '距离',icon: 'eye-open' }},
      { path: 'index', component: () => import('@/views/library/index'), name: 'libraryIndex', meta: { title: '图像库', icon: 'eye-open' }},
      { path: ':libraryID', component: () => import('@/views/library/library'), name: 'library', props: true, hidden: true, meta: { title: '图像库', icon: 'list' }}
    ]
  },
  {
    path: '/feature',
    component: Layout,
    name: 'feature',
    redirect: '/feature/index',
    children: [
      { path: 'index', component: () => import('@/views/feature/index'), name: 'feature', meta: { title: '特征管理', icon: 'eye' }}
      // {path: ':libraryID',component: () => import('@/views/library/library'),name: 'library',props: true,hidden: true,meta: {title: '图像库',icon: 'list'}}
    ]
  },
  {
    path: '/distance',
    component: Layout,
    name: 'distance',
    redirect: '/distance/index',
    children: [
      { path: 'index', component: () => import('@/views/distance/index'), name: 'distance', meta: { title: '距离管理', icon: 'eye' }}
      // {path: ':libraryID',component: () => import('@/views/library/library'),name: 'library',props: true,hidden: true,meta: {title: '图像库',icon: 'list'}}
    ]
  },
  // {
  //   path: '/nested',
  //   component: Layout,
  //   redirect: '/nested/menu1',
  //   name: 'Nested',
  //   meta: {
  //     title: 'Nested',
  //     icon: 'nested'
  //   },
  //   children: [
  //     {
  //       path: 'menu1',
  //       component: () => import('@/views/nested/menu1/index'), // Parent router-view
  //       name: 'Menu1',
  //       meta: { title: 'Menu1' },
  //       children: [
  //         {
  //           path: 'menu1-1',
  //           component: () => import('@/views/nested/menu1/menu1-1'),
  //           name: 'Menu1-1',
  //           meta: { title: 'Menu1-1' }
  //         },
  //         {
  //           path: 'menu1-2',
  //           component: () => import('@/views/nested/menu1/menu1-2'),
  //           name: 'Menu1-2',
  //           meta: { title: 'Menu1-2' },
  //           children: [
  //             {
  //               path: 'menu1-2-1',
  //               component: () => import('@/views/nested/menu1/menu1-2/menu1-2-1'),
  //               name: 'Menu1-2-1',
  //               meta: { title: 'Menu1-2-1' }
  //             },
  //             {
  //               path: 'menu1-2-2',
  //               component: () => import('@/views/nested/menu1/menu1-2/menu1-2-2'),
  //               name: 'Menu1-2-2',
  //               meta: { title: 'Menu1-2-2' }
  //             }
  //           ]
  //         },
  //         {
  //           path: 'menu1-3',
  //           component: () => import('@/views/nested/menu1/menu1-3'),
  //           name: 'Menu1-3',
  //           meta: { title: 'Menu1-3' }
  //         }
  //       ]
  //     },
  //     {
  //       path: 'menu2',
  //       component: () => import('@/views/nested/menu2/index'),
  //       meta: { title: 'menu2' }
  //     }
  //   ]
  // },

  // {
  //   path: 'external-link',
  //   component: Layout,
  //   children: [
  //     {
  //       path: 'https://panjiachen.github.io/vue-element-admin-site/#/',
  //       meta: { title: 'External Link', icon: 'link' }
  //     }
  //   ]
  // },

  { path: '*', redirect: '/404', hidden: true }
]

export default new Router({
  // mode: 'history', //后端支持可开
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRouterMap
})
