import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

function date(){
  let date = new Date()
  let year = date.getFullYear().toString();
  let month = (date.getMonth()+1).toString();
  let datas = date.getDate().toString();
  let hours = date.getHours().toString();
  let minutes = date.getMinutes().toString();
  let seconds = date.getSeconds().toString();
  let today = [[year, month, datas].join('-'), [hours, minutes, seconds].join('.')]
  let todayStr = today.join('  ');
  return todayStr
}

Vue.config.productionTip = false
Vue.prototype.$bus = new Vue()
Vue.prototype.$date = date
Vue.prototype.$path = 'https://boygirl.top'
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
