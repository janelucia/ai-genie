import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Research from '../views/Research.vue'
import Events from "../views/Events.vue";
import Chat from "../views/Chat.vue";
import Researchers from "../views/Researchers.vue";
import NotFound from "../views/NotFound.vue";
import ResearchDetails from "../views/ResearchDetails.vue";
import ResearcherDetails from "../views/ResearcherDetails.vue";
import SignUpForm from "../views/SignUpForm.vue";


const routes = [
    { path: '/', name: 'Home', component: Home },
    { path: '/research', name: 'Research', component: Research },
    { path: '/research/:id', name: 'ResearchDetails', component: ResearchDetails },
    { path: '/chat', name: 'Chat', component: Chat },
    { path: '/events', name: 'Events', component: Events },
    { path: '/researchers', name: 'Researchers', component: Researchers },
    { path: '/researchers/:id', name: 'ResearcherDetails', component: ResearcherDetails },
    { path: '/events/:id', name: 'SignUp', component: SignUpForm },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
