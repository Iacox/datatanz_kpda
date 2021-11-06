import Vue from 'vue'
import App from './App.vue'

import router from './router'
import store from './store'
import vuetify from './middleware/plugins/vuetify'
import './middleware/plugins/snackbar.js'

Vue.config.productionTip = false

new Vue({
  router,
  store,
	vuetify,
  render: h => h(App)
}).$mount('#app')
