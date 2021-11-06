import Vue from 'vue'
import Vuetify from 'vuetify'
//  Colors
import colors from 'vuetify/lib/util/colors'
//  i11e Ru
import ru from 'vuetify/lib/locale/ru'
import en from 'vuetify/lib/locale/en'
//  Styles
import 'vuetify/dist/vuetify.min.css'

Vue.use(Vuetify)

//  Config
const opts = {
	lang: {
		locales: { ru, en },
		current: 'ru'
	},
	icons: {
    iconfont: 'mdi',
  },

	theme: {
		dark: false,
		themes: {
			light: {
				primary: '#EBEBEC',
				secondary: '#9B9B9F',
				accent: '#151721',
			},
			dark: {
				primary: '#191D28',
				secondary: '#2B3244',
				accent: '#FFFFFF',
			}
		}
	}
}
export default new Vuetify(opts)