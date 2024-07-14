<template>
	<main>
		<div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
			<div class="main-left">
				<div class="p-12 bg-white border border-gray-200 rounded-lg">
					<h1 class="mb-6 text-2xl">Change Password</h1>

					<p class="mb-6 text-gray-500">
                        Change your password here. Make sure it's strong!
                    </p>
				</div>
		</div>

		<div class="main-right">
				<div class="p-12 bg-white border border-gray-200 rounded-lg">
					<form class="space-y-6" v-on:submit.prevent="submitForm">
						<div>
								<label>Current Password</label><br>
								<input type="password" v-model="form.old_password" placeholder="..." class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
						</div>

                        <div>
								<label>New Password</label><br>
								<input type="password" v-model="form.new_password1" placeholder="..." class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
						</div>
                        <div>
								<label>Confirm Password</label><br>
								<input type="password" v-model="form.new_password2" placeholder="Type your new password again" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
						</div>

						<template v-if="errors.length > 0">
							<div class="bg-red-300 text-white rounded-lg p-6">
								<p v-for="error in errors" v-bind:key="error">
									{{ error }}
								</p>
							</div>
						</template>

						<div>
								<button class="py-4 px-6 bg-blue-600 text-white rounded-lg">Update</button>
						</div>
					</form>
				</div>
			</div>
		</div>
	</main>
</template>



<script>
    import { useToastStore } from '@/stores/toast';
    import { useUserStore } from '@/stores/user';
    import axios from 'axios'

    export default {
        setup() {
            const toastStore = useToastStore()
            const userStore = useUserStore()
            return {
                toastStore,
                userStore,
            }
        },
        data() {
            return {
                form: {
                    old_password: '',
                    new_password1: '',
                    new_password2: '',
                    
                },

                errors: [],
            }
        },
        methods: {
            submitForm() {
                this.errors = []

                if (this.form.password1 !== this.form.password2) {
                    this.errors.push('Your passwords don\'t match')
                }

                if (this.errors.length === 0) {
                    let formData = new FormData()
                    formData.append('old_password', this.form.old_password)
                    formData.append('new_password1', this.form.new_password1)
                    formData.append('new_password2', this.form.new_password2)


                    axios.post('/api/changepassword/', formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    })
                        .then( response => {
                            if (response.data.message === 'success') {
                                // this.toastStore.showToast(5000, 'Changes saved.', 'bg-emerald-500')
                                setTimeout(function() {
                                    alert('Password updated!')
                                }, 500);
                                    
                                this.$router.push(`/profile/${this.userStore.user.id}`)

                            } else {
                                const data = JSON.parse(response.data.message)
                                for (const key in data) {
                                    this.errors.push(data[key][0].message)
                                }
                                setTimeout(function() {
                                    alert('Something went wrong')
                                }, 500);
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