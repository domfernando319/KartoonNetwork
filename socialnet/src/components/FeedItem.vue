<template>
    <div class="mb-6 flex items-center justify-between">
        <div class="flex items-center space-x-6">
            <img :src="post.created_by.get_avatar" class="w-[40px] rounded-full" :style="{ width: '40px', height: '40px', objectFit: 'cover', borderRadius: '50%' }">
            
            <p>
                <strong>
                    <RouterLink :to="{name: 'profile', params:{'id': post.id}}">{{ post.created_by.name }}</RouterLink>
                </strong>
            </p>
        </div>

        <p class="text-gray-600">{{post.created_at_formatted}} ago</p>
    </div>

    <template v-if="post.attachments.length">
        <img v-for="image in post.attachments" v-bind:key="image.id" :src="image.get_image" class="w-full mb-4 rounded-xl">
    </template>
    <p>
        {{ post.body }}
    </p>

    <div class="my-6 flex justify-between">
        <div class="flex space-x-6">
            <div class="flex items-center space-x-2"  @click="likePost(post.id)">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                </svg>  
                
                <span class="text-gray-500 text-xs">{{post.likes_count}} likes</span>
            </div> 
            
            <div class="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z" />
                </svg> 

                <RouterLink :to="{name: 'postview', params: {id: post.id}}" class="text-gray-500 text-xs">{{  post.comments_count }} comments</RouterLink>
            </div>
        </div>
        
        <div>
            <div @click="togglePostOptions">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z" />
                </svg>   

            </div>
        </div>   
    </div>

    <div v-if="showPostOptions">
        <div class="flex space-x-6 items-center">
            <div class="flex items-center space-x-2"  @click="deletePost" v-if="userStore.user.id == post.created_by.id">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6 text-red-500">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                </svg>
 
                
                <span class="text-red-500 text-xs">Delete Post</span>
            </div> 
        </div>
    </div> 
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'
export default (await import('vue')).defineComponent({
    props: {
        post: Object
    },

    emits: ['deletePost'],

    data() {
        return {
            showPostOptions: false,
        }
    },

    setup() {
        const userStore = useUserStore()

        return {
            userStore,
        }
    },

    methods: {
        likePost(id) {
            axios
                .post(`/api/posts/${id}/like/`)
                .then( res => {
                    if (res.data.message == "Post liked") {
                        this.post.likes_count += 1
                    }
                })
                .catch(err => {
                    console.log("error:", err)
                })
        },

        deletePost() {
            this.$emit('deletePost', this.post.id)
            axios  
                .delete(`/api/posts/${this.post.id}/delete/`)
                .then( res => {
                    console.log(res.data)
                })
                .catch(err => {
                    console.log("error:", err)
                })
        },

        togglePostOptions() {
            console.log('click')
            this.showPostOptions = !this.showPostOptions
        }
    }
})
</script>