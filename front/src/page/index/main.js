import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import qtweb from '@/utils/qt-request'

createApp(App).use(router).use(qtweb)


