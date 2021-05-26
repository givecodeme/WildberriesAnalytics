import axios from "axios";

export default axios.create({
    baseURL: '/api',
    headers: {
        Authorization: localStorage.getItem('token') || ''
    }
})