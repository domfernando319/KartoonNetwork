import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'

//later when we include django views we wont have to include base url each time
axios.defaults.baseURL = 'htt://127.0.0.1:8000' 

const app = createApp(App)

app.use(createPinia())
app.use(router, axios)

app.mount('#app')