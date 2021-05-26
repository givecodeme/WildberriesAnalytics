
import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/list',
            name: 'list',
            component: () => import('@/views/List.vue')
        },
        {
            path: '/tes',
            name: 'home',
            component: () => import('@/views/Profile.vue')
        },
        {
            path: '/signup',
            name: 'signUp',
            component: () => import('@/views/Profile/SignUp.vue')
        },
        {
            path: '/signin',
            name: 'signIn',
            component: () => import('@/views/Profile/SignIn.vue')
        },
        {
            path: '/profile',
            name: 'profile',
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