import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Antd from 'ant-design-vue';
import VChart from 'vue-echarts';
import 'echarts'


const app = createApp(App)
app.use(router)
app.use(Antd)
app.component('VChart', VChart)
app.mount('#app')
