import Vue from 'vue'
import Vuex from 'vuex'
import Api from '@api/index'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    linkList: [],
  },
  mutations: {
		SET_STATE(state, { key, value }) {
			state[key] = value
		}
	},
  actions: {
    async sendFiles({ commit }, payload) {
			try {
				const res = await Api.sendFiles(payload)
				if (res.success)
          commit('SET_STATE', {
            key: 'linkList',
            value: res.data,
          })
				return res
			} catch (e) {
        this._vm.$snackbar({
					type: 'error',
					message: 'Не удалось отправить файлы. Повторите позже.'
				})
        console.error(e)
			}
		},
    async checkJobStatus({ commit }, id) {
			try {
				const res = await Api.checkJobStatus(id)
        return res
      } catch (e) {
        console.error(e)
        return e
			}
		},
    async getJobResult({ commit }, id) {
			try {
				const res = await Api.getJobResult(id)
        return res.data
			} catch (e) {
        console.error(e)
			}
		},
  },
})