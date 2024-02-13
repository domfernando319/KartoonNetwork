<script>

import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import FeedItem from '@/components/FeedItem.vue';
import axios from 'axios';
import { useUserStore } from '../stores/user';
import { RouterLink } from 'vue-router';
export default {
    name: 'FeedView',
    setup() {
        const userStore = useUserStore()

        return {
            userStore
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
            user:{},
            body: '',

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
            axios
                .post('/api/posts/create/', {
                    'body': this.body
                })
                .then(response => {
                    console.log('data', response.data)
                    this.posts.unshift(response.data)
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        sendFriendRequest() {
            axios
                .post(`/api/friends/${this.$route.params.id}/request/`)
                .then(response => {
                    console.log('data', response.data)
                    this.user = response.data.user
                })
                .catch(error => {
                    console.log('error', error)
                })
        }
    }
}

</script>



<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <div class="main-left col-span-1">
            <div v-if="user" class="p-4 bg-white border border-gray-200 text-center rounded-lg">

                <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">
                <p><strong>{{user.name}}</strong></p>
                <div class="mt-6 flex space-x-8 justify-around">
                    <RouterLink :to="{name: 'friends', params: {id: user.id}}" class="text-xs text-gray-500">{{user.friends_count}} friends</RouterLink>
                    <p class="text-xs text-gray-500">120 posts</p>
                </div>

                <div class="mt-6">
                    <button class="inline-block py-1 px-4 bg-purple-600 text-xs text-white rounded-lg" style="white-space: nowrap;" @click="sendFriendRequest">Add friend</button>
                </div>
            </div>
        </div>

        <div v-if="user" class="main-center col-span-2 space-y-4">

            <div class="bg-white border border-gray-200 rounded-lg" v-if="userStore.user.id === user.id">
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">  
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
                    </div>
    
                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach image</a>
    
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