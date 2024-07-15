<script>

import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import FeedItem from '@/components/FeedItem.vue';
import CommentItem from '@/components/CommentItem.vue';

import axios from 'axios';

export default {
    name: 'PostView',
    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
        CommentItem
    },

    data() {
        return {
            post: {
                id: null,
                comments: []
            },
            body: ''

        }
    },

    mounted() {
        this.getPost()
    },

    methods: {
        getPost() {
           axios
            .get(`/api/posts/${this.$route.params.id}/`)
            .then(response => {
                console.log('data', response.data)
                this.post = response.data.post
            })
            .catch(error => {
                console.log('error', error)
            })
        },
        submitForm() {
            console.log('submitForm', this.body)
            axios
                .post(`/api/posts/${this.$route.params.id}/comment/`, {
                    'body': this.body
                })
                .then(response => {
                    console.log('data', response.data)

                    this.post.comments.push(response.data)
                    this.post.comments_count += 1
                    // when form is submitted reset body to empty
                    this.body = ''
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

        <div class="main-center col-span-3 space-y-4">
            
            <div 
                class="p-4 bg-white border border-gray-200 rounded-lg"
                v-if="post.id"
            >
                <FeedItem v-bind:post="post"/>
            </div>

            <div
                class="p-4 ml-6 bg-white border border-gray-200 rounded-lg"
                v-for="comment in post.comments"
                v-bind:key="comment.id"
            >
                <CommentItem v-bind:comment="comment"/>
            </div>

            <div class="bg-white border border-gray-200 rounded-lg">
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">  
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="Add a comment..."></textarea>
                    </div>
    
                    <div class="p-4 border-t border-gray-100">
                        <button class="inline-block py-4 px-6 bg-blue-600 text-white rounded-lg">Comment</button>
                    </div>
                </form>
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

                        <a href="#" class="py-2 px-3 bg-blue-600 text-white text-xs rounded-lg">Show</a>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                            
                            <p class="text-xs"><strong>Code With Stein</strong></p>
                        </div>

                        <a href="#" class="py-2 px-3 bg-blue-600 text-white text-xs rounded-lg">Show</a>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                            
                            <p class="text-xs"><strong>Code With Stein</strong></p>
                        </div>

                        <a href="#" class="py-2 px-3 bg-blue-600 text-white text-xs rounded-lg">Show</a>
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

                        <a href="#" class="py-2 px-3 bg-blue-600 text-white text-xs rounded-lg">Explore</a>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <p class="text-xs">
                                <strong>#codewithstein</strong><br>
                                <span class="text-gray-500">180 posts</span>
                            </p>
                        </div>

                        <a href="#" class="py-2 px-3 bg-blue-600 text-white text-xs rounded-lg">Explore</a>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <p class="text-xs">
                                <strong>#codewithstein</strong><br>
                                <span class="text-gray-500">180 posts</span>
                            </p>
                        </div>

                        <a href="#" class="py-2 px-3 bg-blue-600 text-white text-xs rounded-lg">Explore</a>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <p class="text-xs">
                                <strong>#codewithstein</strong><br>
                                <span class="text-gray-500">180 posts</span>
                            </p>
                        </div>

                        <a href="#" class="py-2 px-3 bg-blue-600 text-white text-xs rounded-lg">Explore</a>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <p class="text-xs">
                                <strong>#codewithstein</strong><br>
                                <span class="text-gray-500">180 posts</span>
                            </p>
                        </div>

                        <a href="#" class="py-2 px-3 bg-blue-600 text-white text-xs rounded-lg">Explore</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>