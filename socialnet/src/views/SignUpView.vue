<script>
import { useToastStore } from '@/stores/toast';
import axios from 'axios'

export default {
	setup() {
		const toastStore = useToastStore()

		return {
			toastStore
		}
	},

	data() {
		return {
			form: {
				email: '',
				name: '',
				password1: '',
				password2: '',

			},

			errors: [],
		}
	},

	methods: {
		submitForm() {
			this.errors = []

			if (this.form.name === '') {
				this.errors.push('Your name is missing')
			}
			if (this.form.email === '') {
				this.errors.push('Your email is missing')
			}
			if (this.form.password1 === '') {
				this.errors.push('Your password is missing')
			}
			if (this.form.password1 !== this.form.password2) {
				this.errors.push('Your passwords don\'t match')
			}

			if (this.errors.length === 0) {
				axios.post('/api/signup/', this.form)
					.then( response => {
						if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'The user is registered. ', 'bg-emerald-500')
							setTimeout(function() {
								alert('The user is registered. Please activate your account via email.')
							}, 500);

                            this.form.email = ''
                            this.form.name = ''
                            this.form.password1 = ''
                            this.form.password2 = ''
                        } else {
							const data = JSON.parse(response.data.message)
							for (const key in data) {
								this.errors.push(data[key][0].message)
							}

							setTimeout(function() {
								alert('Something went wrong. Please try again.')
							
							}, 500);

                            this.toastStore.showToast(5000, 'Something went wrong. Please try again', 'bg-red-300')
                        }
					})
					.catch(err => {
						this.toastStore.showToast(5000, 'Something went wrong. Please try again', 'bg-red-300')
						console.log('Error!: ', err)
					})
			}
		}
	}
}
</script>

<template>
	<main>
		<div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
			<div class="main-left">
				<div class="p-12 bg-white border border-gray-200 rounded-lg">
					<h1 class="mb-6 text-2xl">Sign Up</h1>

					<p class="mb-6 text-gray-500">
							Lorem ipsum dolor sit, amet consectetur adipisicing elit. Atque officia laboriosam excepturi harum qui quo iste, tempora nesciunt, maiores velit officiis sequi fuga neque eveniet praesentium sint provident suscipit minima.
					</p>

					<p class="font-bold">
							Already have an account? <RouterLink :to="{'name':'login'}" class="underline">Click here</RouterLink> to log in!
					</p>
				</div>
		</div>

		<div class="main-right">
				<div class="p-12 bg-white border border-gray-200 rounded-lg">
					<form class="space-y-6" v-on:submit.prevent="submitForm">
						<div>
								<label>Name</label><br>
								<input type="text" v-model="form.name" placeholder="Your full name" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
						</div>
						<div>
								<label>E-mail</label><br>
								<input type="email" v-model="form.email" placeholder="Your e-mail address" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
						</div>

						<div>
								<label>Password</label><br>
								<input type="password" v-model="form.password1" placeholder="Your password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
						</div>
						<div>
								<label>Verify password</label><br>
								<input type="password" v-model="form.password2" placeholder="Retype your password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
						</div>

						<template v-if="errors.length > 0">
							<div class="bg-red-300 text-white rounded-lg p-6">
								<p v-for="error in errors" v-bind:key="error">
									{{ error }}
								</p>
							</div>
						</template>

						<div>
								<button class="py-4 px-6 bg-blue-600 text-white rounded-lg">Sign Up</button>
						</div>
					</form>
				</div>
			</div>
		</div>
	</main>
</template>

