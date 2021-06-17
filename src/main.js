import Vue from 'vue'
import App from '@/App.vue'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

// import axios from 'axios'
// axios.defaults.baseURL = '/api/'

import store from '@/store'
import router from '@/routes'

import { ToastPlugin } from 'bootstrap-vue'
Vue.use(ToastPlugin)


Vue.config.productionTip = false

import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import 'vue-material/dist/theme/default.css'

Vue.use(VueMaterial)

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresLogin)) {
    if (!store.getters.isLoggedIn) next({ name: 'signIn' })
    else next()
  }
  else if (to.matched.some(record => record.meta.requiresVisitor)) {
    if (store.getters.isLoggedIn) {
      next({ name: 'list' })
    } else next()
  } else next()

})


const vue = new Vue({
  router,
  store,
  render: h => h(App)
})

vue.$mount('#app')
