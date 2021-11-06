<template>
  <v-container class="page_wrapper" fluid fill-height>
    <v-fade-transition>
      <v-row v-if="dataLoading" class="main_form flex-column">
        <v-col cols="3" class="mx-auto text-center">
          <v-subheader><span>Пожалуйста, подождите пока закончится обработка</span></v-subheader>
          <v-subheader><span>В среднем занимает около 1 минуты.</span></v-subheader>
        </v-col>
        <v-col cols="3" class="mx-auto">
          <SpinnerLoader/>
        </v-col>
      </v-row>
      <template v-else>
        <v-row v-if="!job" class="main_form flex-column">
          <v-col class="mx-auto col-12 col-md-8">
            <v-card class="main_form-block px-10 py-5">
              <v-file-input
                v-model="files"
                :rules="rules"
                accept=".pdf,.docx, image/png"
                label="Выберите файлы"
                placeholder="Выберите файлы"
                prepend-icon=""
                truncate-length="25"
                counter
                multiple
                show-size
                small-chips
              />
            </v-card>
          </v-col>

          <v-col class="mx-auto col-12 col-md-8 my-md-5">
            <v-card class="main_form-block px-10 py-5">
              <v-subheader>Разрешение DPI (влияет на скорость выполнения)</v-subheader>
              <v-slider
                :tick-labels="[100, 200, 300, 400, 500, 600]"
                v-model="dpiValue"
                :min="100"
                :max="600"
                step="100"
                :thumb-label="true"
                ticks="always"
                tick-size="6"
              />
            </v-card>
          </v-col>

          <v-col class="d-flex">
            <v-btn
              @click="sendRequest"
              elevation="5"
              x-large
              class="main_form-btn_send mx-auto px-10"
            >Отправить</v-btn>
          </v-col>
        </v-row>
        <v-row v-else>
          <v-col class="d-flex">
            <v-btn
              @click="DownloadResultFiles"
              elevation="5"
              x-large
              class="main_form-btn_send mx-auto px-10"
            >Скачать результат</v-btn>
          </v-col>
        </v-row>
      </template>
    </v-fade-transition>
  </v-container>
</template>

<script>
import { mapMutations, mapActions } from 'vuex'

export default {
  name: 'MainPage',
  components: {
    SpinnerLoader: () => import('@components/SpinnerLoader.vue'),
  },
  data() {
    return {
      dataLoading: false,
      dpiValue: 300,
      files: [],
      rules: [
        array => (!array.length || array.every(file => file.size < 10240000)) || 'Размер каждого файла не должен превышать 10 MB!',
      ],
      job: null,
    }
  },
  methods: {
    ...mapMutations(['SET_STATE']),
    ...mapActions([
      'sendFiles',
      'checkJobStatus',
      'getJobResult',
    ]),

    async sendRequest() {
      if (!this.files.length || !this.dpiValue)
        return this.$snackbar({
					type: 'error',
					message: 'Сначала выберите файлы для отправки.'
				})

      this.dataLoading = true
      const request = await this.sendFiles({
        filesData: this.files,
        dpi: this.dpiValue,
      })
      console.log(`request`, request)

      if (request?.id) {
        this.$snackbar({
					type: 'success',
					message: 'Файл успешно доставлен на сервер.'
				})

        this.job = {
          id: request.id,
          loading: true,
          interval: 0,
          result: '',
        }
        this.job.interval = setInterval(async () => {
          const request = await this.checkJobStatus(this.job.id)
          console.log(`request`, request)

          if (request?.response?.status === 200) {
            this.job.loading = false
            clearInterval(this.job.interval)
            await this.requestJobResult()
          } else if (request?.response?.status === 422) {
            this.$snackbar({
              type: 'info',
              message: 'Файл обрабатывается.'
            })
          } else {
            clearInterval(this.job.interval)
            this.dataLoading = false
            this.job.loading = false
            this._vm.$snackbar({
              type: 'error',
              message: 'Не удалось проверить статус задачи.'
            })
          }
        }, 10000)
      } else
        this.dataLoading = false
    },
    async requestJobResult() {
      const request = await this.getJobResult(this.job)
      console.dir(request)
      if (request)
        this.job.result = request
      else
        this.$snackbar({
          type: 'error',
					message: 'При загрузке файла произошла ошибка.'
        })
      this.dataLoading = false
    },
    DownloadResultFiles () {
      if (!this.job?.result)
        return

      const blob = new Blob([this.job?.result])
      const file = new File([blob], this.files?.[0]?.name)  // {type: this.files?.[0]?.type}
      const a = document.createElement('a')
      a.href = URL.createObjectURL(file)
      a.download = this.files?.[0]?.name
      a.click()
    },
  },
}
</script>

<style lang="scss">
.content--wrapper {
  border: 1px solid black;
  border-radius: 1em;
}

.v-subheader > span {
  width: 100%;
}

.theme--light {
  .spinner-loader {
    min-height: unset !important;
    .spinner-loader__loader div {
      background-color: #151721 !important;
    }
  }

  .page_wrapper {
    background: #EBEBEC !important;
  }
  .main_form {
    &-block {
      background: #FFFFFF;
      box-shadow: inset 4px 4px 20px #EBEBEC;
      border-radius: 24px;

      .v-subheader {
        text-align: center;
        font-family: Roboto, sans-serif;
        font-style: normal;
        font-weight: normal;
        font-size: 18px;
        line-height: 16px;
        color: #000000;
        padding: 0;
      }
    }

    &-btn_send {
      background-color: #151721 !important;
      color: #EBEBEC !important;
      border-radius: 14px;
    }

    .v-slider__track-background {
      background-color: #CCCCCC !important;
    }
    .v-slider__track-fill {
      background-color: #9B9B9F !important;
    }
    .v-slider__thumb,
    .v-slider__thumb-label {
      background-color: #9B9B9F !important;
    }
  }
}
.theme--dark {
  .spinner-loader__loader div {
    background-color: #FFFFFF !important;
  }

  .page_wrapper {
    background: #191D28 !important;
  }

  .main_form {
    &-block {
      background: #2B3244;
      box-shadow: inset 4px 4px 20px #151721;
      border-radius: 24px;

      .v-subheader {
        text-align: center;
        font-family: Roboto, sans-serif;
        font-style: normal;
        font-weight: normal;
        font-size: 18px;
        line-height: 16px;
        color: #FFFFFF;
        padding: 0 5px;
      }
    }

    &-btn_send {
      background-color: #FFFFFF !important;
      color: #191D28 !important;
      border-radius: 14px;
    }

    .v-slider__thumb-label {
      color: #151721 !important;
    }
  }
}
</style>