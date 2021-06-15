
import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        // { path: '*', redirect: '/list' },
        {
            path: '/list',
            name: 'list',
            meta: {
                requiresLogin: true
            },
            component: () => import('@/views/List.vue')
        },
        {
            path: '/calculator',
            name: 'calculator',
            meta: {
                // requiresLogin: true
            },
            component: () => import('@/views/Calculator.vue')
        },
        {
            path: '/tes',
            name: 'home',
            component: () => import('@/views/Profile.vue')
        },
        {
            path: '/signup',
            name: 'signUp',
            meta: { requiresVisitor: true },
            component: () => import('@/views/Profile/SignUp.vue')
        },
        {
            path: '/signin',
            name: 'signIn',
            meta: {
                requiresVisitor: true
            },
            component: () => import('@/views/Profile/SignIn.vue')
        },
        {
            path: '/profile',
            name: 'profile',
            meta: { requiresLogin: true },

            component: () => import('@/views/Profile/Profile.vue'),
            children: [
                {
                    path: 'token',
                    name: 'token',
                    component: () => import('@/views/Profile/Token.vue')
                }
            ]


        },
    ]
})