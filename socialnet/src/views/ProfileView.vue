<script>

import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import FeedItem from '@/components/FeedItem.vue';
import axios from 'axios';
import { useUserStore } from '../stores/user';
import { useToastStore } from '@/stores/toast';
import { RouterLink } from 'vue-router';
export default {
    name: 'FeedView',
    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore
        }
    },
    components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem,
    PeopleYouMayKnow,
    RouterLink
},

    data() {
        return {
            posts: [],
            user:{
                id: null
            },
            body: '',
            url: '',

        }
    },

    mounted() {
        this.getFeed()
    },

    
    watch: {
        '$route.params.id': {
            handler: function() {
                console.log('changed!')
                this.getFeed()
            },
            deep: true,
            immediate: true
        }
    },

    methods: {
        onFileChange(e) {
            const file = e.target.files[0]
            this.url = URL.createObjectURL(file)
        },

        sendDM() {
            console.log("send dm")

            axios   
                .get(`/api/chat/${this.$route.params.id}/get-or-create/`)
                .then(res => {
                    console.log(res.data)

                    this.$router.push('/chat')
                })
                .catch(err => {
                    console.log(err)
                })
        },

        getFeed() {
           axios
            .get(`/api/posts/profile/${this.$route.params.id}/`)
            .then(response => {
                console.log('data', response.data)
                this.posts = response.data.posts
                this.user = response.data.user
            })
            .catch(error => {
                console.log('error', error)
            })
        },
        submitForm() {
            console.log('submitForm', this.body)
            let formData = new FormData()
            formData.append('image', this.$refs.file.files[0])
            formData.append('body', this.body)

            axios
                .post('/api/posts/create/', formData, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                })
                .then(response => {
                    console.log('data', response.data)
                    this.posts.unshift(response.data)
                    this.body = ''
                    this.$refs.file.value = null
                    this.url = null
                    this.user.post_count += 1
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        sendFriendRequest() {
            axios
                .post(`/api/friends/${this.$route.params.id}/request/`)
                .then(response => {
                    console.log("ahhhhh")
                    if (response.data.message == 'request already sent') {
                        this.toastStore.showToast(5000, 'A request has already been sent!', 'bg-red-300')
                    } else {
                        this.toastStore.showToast(5000, 'Friend request sent!', 'bg-emerald-300')
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        logout() {
            console.log("log out")
            this.userStore.removeToken()
            this.$router.push('/login')
        }



    }
}

</script>



<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">

                <img :src="user.get_avatar" class="mb-6 rounded-full">
                <p><strong>{{user.name}}</strong></p>
                <div class="mt-6 flex space-x-8 justify-around" v-if="user.id">
                    <RouterLink :to="{name: 'friends', params: {id: user.id}}" class="text-xs text-gray-500">{{user.friends_count}} friends</RouterLink>
                    <p class="text-xs text-gray-500">{{user.post_count}} posts</p>
                </div>

                <div class="mt-6 flex flex-col items-center space-y-4" >
                    <button 
                        class="inline-block py-1 px-4 bg-purple-600 text-xs text-white rounded-lg" 
                        style="white-space: nowrap;" 
                        @click="sendFriendRequest"
                        v-if="userStore.user.id !== user.id"
                    >
                        Add Friend
                    </button>

                    <button 
                        class="inline-block py-1 px-4 bg-purple-600 text-xs text-white rounded-lg" 
                        style="white-space: nowrap;" 
                        @click="sendDM"
                        v-if="userStore.user.id !== user.id"
                    >
                        Send Message
                    </button>

                    <RouterLink 
                        class="inline-block py-1 px-4 bg-blue-600 text-xs text-white rounded-lg" 
                        to="/profile/edit"
                        v-if="userStore.user.id === user.id"
                    >
                        Edit Profile
                    </RouterLink>

                    <button 
                        class="inline-block py-1 px-4 bg-red-600 text-xs text-white rounded-lg" 
                        style="white-space: nowrap;" 
                        @click="logout"
                        v-if="userStore.user.id === user.id"
                    >
                        Log Out
                    </button>

                </div>
            </div>
        </div>

        <div v-if="user" class="main-center col-span-2 space-y-4">

            <div class="bg-white border border-gray-200 rounded-lg" v-if="userStore.user.id === user.id">
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">  
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
                        <div id="preview" v-if="url">
                            <img :src="url" class="w-[150px] mt-3 rounded-xl"/>


                        </div>
                    </div>


    
                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        
                        <label class="custom-file-upload inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                            <input type="file" ref="file" @change="onFileChange">
                            Attach Image
                        </label>
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                    
                    </div>
                </form>
            </div>
            
            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg"
                v-for="post in posts"
                v-bind:key="post.id"
            >
                <FeedItem v-bind:post="post"/>
            </div>
            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg"
                v-if="posts.length == 0"
            >
                <p class="text-lg"><strong>No Posts Yet</strong></p>
            </div>
        </div>
        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow/>
            <Trends/>
        </div>
    </div>
</template>

<style>
    input[type='file'] {
        display: none;
    }

    .custom-file-upload {
        border: 1px solid #ccc;
        display: inline-block;
        padding: 14px 12px;
        cursor: pointer;

    }
</style>