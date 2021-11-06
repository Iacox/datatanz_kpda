<template>
  <v-app>
		<v-app-bar
			absolute
      prominent
			class="px-4"
		>
			<v-col cols="2" class="my-auto">
				<!-- <img :src="logo"> -->
			</v-col>
			<v-spacer></v-spacer>

			<div class="d-flex flex-column my-auto">
				<h1 class="mb-4">Kvirin Personal Data Analise</h1>
				<h2>Защита персональных данных в документах</h2>
			</div>
			<v-spacer></v-spacer>

			<v-col cols="2" class="my-auto d-flex">
				<v-btn @click="ToggleTheme" icon class="ml-auto">
					<v-icon x-large>{{ $vuetify.theme.isDark ? 'mdi-weather-night' : 'mdi-white-balance-sunny'}}</v-icon>
				</v-btn>
			</v-col>
		</v-app-bar>

		<v-main>
			<router-view />
		</v-main>
	</v-app>
</template>


<script>
import light from '@assets/image/logo_for_light.png'
import dark from '@assets/image/logo_for_dark.png'

export default {
	name: 'App',
	computed: {
		logo() {
			return this.$vuetify.theme.isDark ? dark : light
		},
	},
	methods: {
		ToggleTheme() {
			this.$vuetify.theme.isDark = !this.$vuetify.theme.isDark
		},
	},
}
</script>

<style lang="scss">
h1 {
	font-family: Roboto, sans-serif;
	font-style: normal;
	font-weight: 700;
	font-size: 48px;
	line-height: 44px;
	text-align: center;
}
h2 {
	font-family: Roboto, sans-serif;
	font-style: normal;
	font-weight: 500;
	font-size: 24px;
	line-height: 22px;
	text-align: center;
}
.v-toolbar {
	box-shadow: unset !important;
	background: transparent !important;
}

.snackbar {
	&-container {
		transition: all 500ms ease;
		transition-property: top, right, bottom, left, opacity;
		position: fixed;
		justify-content: space-between;
		align-items: center;
		text-align: center;
		line-height: 22px;
		bottom: -100px;
		top: -100px;
		opacity: 0;
		z-index: 500;
		display: inline-flex;
		margin: 24px 0;
		max-width: calc(100% - 50px);

		min-height: 49px;
		background: #424242;
		border-radius: 4px;
		color: #fff;
		box-sizing: border-box;
		padding: 10px 24px;
		font-size: 14px;
		box-shadow: 0px 6px 10px rgba(0, 0, 0, 0.14),
			0px 1px 18px rgba(0, 0, 0, 0.12), 0px 3px 5px rgba(0, 0, 0, 0.2);

		&.success {
			background-color: #186218;
		}

		&.error {
			background-color: #9d1c1c;
		}
	}

	&-pos {
		bottom: auto !important;
		top: 0;
		left: 50%;
		transform: translate(-50%, 0);

		&.bottom-center {
			top: auto !important;
			bottom: 0;
		}
	}
}
</style>