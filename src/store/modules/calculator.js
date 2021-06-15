import _ from 'lodash';

export default {
    state: {
        products_calc: JSON.parse(localStorage.getItem('products_calc')) || [],
    },

    actions: {
        ADD_TO_CART: ({ commit }, product) => commit('ADD_TO_CART', product)
    },
    mutations: {
        ADD_TO_CART(state, product) {
            // let found = state.products_calc.find(item => (item.name) == (product.name))
            let found = state.products_calc.find(item => JSON.stringify(item) == JSON.stringify(product))
            if (!found) {
                state.products_calc.unshift(JSON.parse(JSON.stringify(product)))
            }
            this.commit('saveProducts')
        },
        saveProducts: state => localStorage.setItem('products_calc', JSON.stringify(state.products_calc))
    },
    getters: {
        products_calc: state => state.products_calc
    }
}