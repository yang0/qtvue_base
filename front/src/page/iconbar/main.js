import { createApp } from 'vue'
import App from './App.vue'


import qtweb from '@/utils/qt-request'



let app = createApp(App)
app.use(qtweb)
app.mount('#app')


