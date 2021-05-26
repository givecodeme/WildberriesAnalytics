import axios from "axios"

import router from "@/routes"

export default {
    state: {
        status: '',
        token: localStorage.getItem('token') || '',
        user: {}
    },

    actions: {
        LOGIN({ commit }, user) {
            axios
                .post("token/", {
                    'username': user.name,
                    'password': user.password,
                })
                // commit('auth_success',)
                .then((response) => {
                    localStorage.setItem('token', `Bearer ${response.data.access}`)
                    router.push({ name: "list" });


                    commit('auth_success', `Bearer ${response.data.access}`)

                    // this.$bvToast.toast(response.data.access, {
                    //     variant: "success",
                    //     autoHideDelay: 5000,
                    // });


                    //     console.log(response.data.access);
                    //     localStorage.setItem("token", response.data.access);
                })
        },

        register({ commit }, user) {
            axios
                .post("auth/users/", {
                    username: user.name,
                    password: user.password,
                })
                .then(() => console.log('success Register'))
        },

        logout({ commit }) {
            commit('logout')
            localStorage.removeItem('token')
            delete axios.defaults.headers.common['Authorization']
        }
    },

    mutations: {
        auth_request(state) {
            state.status = 'loading'
        },
        auth_success(state, token) {
            state.status = 'success'
            state.token = token
        },
        auth_error(state) {
            state.status = 'error'
        },
        logout(state) {
            state.status = ''
            state.token = ''
        },
    },
    getters: {
        isLoggedIn: state => !!state.token,
        authStatus: state => state.status,
    }
}