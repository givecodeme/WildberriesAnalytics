import Vue from 'vue'
import App from '@/App.vue'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

import axios from 'axios'
axios.defaults.baseURL = '/api/'

Vue.config.productionTip = false

const vue = new Vue({
  render: h => h(App)
})

vue.$mount('#app')
