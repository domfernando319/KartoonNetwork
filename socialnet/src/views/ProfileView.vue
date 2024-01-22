<script>

import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import FeedItem from '@/components/FeedItem.vue';
import axios from 'axios';
import { useUserStore } from '../stores/user';
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
        FeedItem
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

    // beforeRouteUpdate (to, from, next) {
    //     if (from.name === to.name) {
    //         this.getFeed()
    //     }
    // },
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
            .get(`/api/posts/profile/${this.$route.params.id}`)
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
        }
    }
}

</script>



<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">
                
                <p><strong>{{user.name}}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <p class="text-xs text-gray-500">182 friends</p>
                    <p class="text-xs text-gray-500">120 posts</p>
                </div>
            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">

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
            <div class="p-4 bg-white border border-gray-200 rounded-lg">
                <h3 class="mb-6 text-xl">People you may know</h3>

                <div class="space-y-4">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                            
                            <p class="text-xs"><strong>Code With Stein</strong></p>
                        </div>

                        <a href="#" class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Show</a>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                            
                            <p class="text-xs"><strong>Code With Stein</strong></p>
                        </div>

                        <a href="#" class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Show</a>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                            
                            <p class="text-xs"><strong>Code With Stein</strong></p>
                        </div>

                        <a href="#" class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Show</a>
                    </div>
                </div>
            </div>

            <div class="p-4 bg-white border border-gray-200 rounded-lg">
                <h3 class="mb-6 text-xl">Trends</h3>

                <div class="space-y-4">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <p class="text-xs">
                                <strong>#codewithstein</strong><br>
                                <span class="text-gray-500">180 posts</span>
                            </p>
                        </div>

                        <a href="#" class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Explore</a>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <p class="text-xs">
                                <strong>#codewithstein</strong><br>
                                <span class="text-gray-500">180 posts</span>
                            </p>
                        </div>

                        <a href="#" class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Explore</a>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <p class="text-xs">
                                <strong>#codewithstein</strong><br>
                                <span class="text-gray-500">180 posts</span>
                            </p>
                        </div>

                        <a href="#" class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Explore</a>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <p class="text-xs">
                                <strong>#codewithstein</strong><br>
                                <span class="text-gray-500">180 posts</span>
                            </p>
                        </div>

                        <a href="#" class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Explore</a>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <p class="text-xs">
                                <strong>#codewithstein</strong><br>
                                <span class="text-gray-500">180 posts</span>
                            </p>
                        </div>

                        <a href="#" class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Explore</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>