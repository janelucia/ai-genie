import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Search from '../views/Search.vue'
import Events from "../views/Events.vue";
import Chat from "../views/Chat.vue";
import Bookmarks from "../views/Bookmarks.vue";
import NotFound from "../views/NotFound.vue";


const routes = [
    { path: '/', name: 'Home', component: Home },
    { path: '/search', name: 'Search', component: Search },
    { path: '/chat', name: 'Chat', component: Chat },
    { path: '/events', name: 'Events', component: Events },
    { path: '/bookmarks', name: 'Bookmarks', component: Bookmarks },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
