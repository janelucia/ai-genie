import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Research from '../views/Research.vue'
import Events from "../views/Events.vue";
import Chat from "../views/Chat.vue";
import Researchers from "../views/Researchers.vue";
import NotFound from "../views/NotFound.vue";


const routes = [
    { path: '/', name: 'Home', component: Home },
    { path: '/research', name: 'Research', component: Research },
    { path: '/chat', name: 'Chat', component: Chat },
    { path: '/events', name: 'Events', component: Events },
    { path: '/researchers', name: 'Researchers', component: Researchers },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
