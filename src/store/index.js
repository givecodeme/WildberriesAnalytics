import Vue from 'vue'
import Vuex from 'vuex'

import auth from '@/store/modules/auth'
import calculator from '@/store/modules/calculator'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: [
        auth,
        calculator
    ],
})