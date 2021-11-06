import axios from 'axios'

const baseURL = 'https://eab9-188-243-159-197.ngrok.io'

export default {
	sendFiles({filesData, dpi}) {
		const formData = new FormData()
		filesData.forEach(item => formData.append('file', item))
		formData.append('dpi', dpi)
		return axios
			.post(`${baseURL}/api/Job`, formData,  {
				headers: { 'Content-Type': 'multipart/form-data' },
			})
			.then(r => r.data)
	},
	async checkJobStatus(id) {
		return await axios
			.get(`${baseURL}/api/Job/${id}`)
	},
	getJobResult(id) {
		return axios
			.get(`${baseURL}/api/Job/${id}/result`)
			.then(r => r.data)
	},
}
