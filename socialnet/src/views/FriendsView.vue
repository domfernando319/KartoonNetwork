<script>

import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import FeedItem from '@/components/FeedItem.vue';
import axios from 'axios';
import { useUserStore } from '../stores/user';
export default (await import('vue')).defineComponent ({
    name: 'FriendsView',
    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },
    components: {
        PeopleYouMayKnow,
        Trends
    },

    data() {
        return {
            user: {},
            friendRequests: [],
            friends: [],
        }
    },

    mounted() {
        this.getFriends
    },

    methods: {
        getFriends() {
           axios
            .get(`/api/posts/profile/${this.$route.params.id}/friends/`)
            .then(response => {
                console.log('data', response.data)
                this.friendRequests = response.data.requests
                this.friends = response.data.friends
                this.user = response.data.user
            })
            .catch(error => {
                console.log('error', error)
            })
        }
    }
})

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
            blahblah blah
        </div>
        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow/>
            <Trends/>
        </div>
    </div>
</template>