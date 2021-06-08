import axios from "axios"
import router from "@/routes"

export default {
    state: {
        status: null,
        token: localStorage.getItem('token') || null,
        user: {}
    },

    actions: {
        LOGIN({ commit }, user) {
            axios
                .post("token/", {
                    'username': user.name,
                    'password': user.password,
                })
                .then((response) => {
                    localStorage.setItem('token', `Bearer ${response.data.access}`)
                    commit('auth_success', `Bearer ${response.data.access}`)
                    router.push({ name: "list" });
                })
        },

        register({ commit }, user) {
            axios
                .post("auth/users/", user)
                .then(() => console.log('success Register'))
        },

        logout({ commit }) {
            commit('logout')
            localStorage.removeItem('token')
            // delete axios.defaults.headers.common['Authorization']
        }
    },
    // COMMITS
    mutations: {
        auth_success(state, token) {
            state.status = 'success'
            state.token = token
        },
        auth_error(state) {
            state.status = 'error'
        },
        logout(state) {
            state.status = null
            state.token = null
        },
    },
    getters: {
        isLoggedIn: state => !!state.token,
        authStatus: state => state.status,
        token: state => state.token,
    }
}