import App from './App.vue'
import { createApp } from 'vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import { createPinia } from "pinia"
import { useUserStore } from './stores'
import axios from "axios"

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

const routes = [
    { path: '/', component: HomeView },
    { path: '/about', component: AboutView },
]

const router = createRouter({
    history: createMemoryHistory(),
    routes,
  })

router.beforeEach((to, from, next) => {
    next()
})

export const api = axios.create({
    baseURL: "http://localhost:8000/api/",
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
})

api.interceptors.request.use(async (config) => {
    const csrfToken = getCookie("csrftoken")

    // Ajouter le token CSRF si disponible
    if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken
    }

    // Ajouter le token d'authentification (si nécessaire)
    if (!config.url.endsWith('token/') && !config.url.endsWith('token/refresh/')) {
        const token = getTokenWithExpiry("access_token")
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
    }

    return config
})

api.interceptors.response.use(r => r, async (error) => {
    const config = error.config
    const userStore = useUserStore()

    // Vérifie si c'est une erreur 401 (Non authentifié)
    if (error.response && error.response.status === 401) {
        // Essayer de rafraîchir le token
        const tokenRefreshed = await userStore.refreshToken()

        if (tokenRefreshed) {
            const newToken = getTokenWithExpiry("access_token")

            // Mettre à jour le header avec le nouveau token
            if (newToken) {
                config.headers.Authorization = `Bearer ${newToken}`
            }

            // Relancer la requête
            return api(config)
        } else {
            //Déconnecter l'utilisateur si le rafraîchissement du token a échoué
            userStore.logout()
            return Promise.reject(error)
        }
    }

    // Dans le cas où ce n'est pas une erreur 401, on rejette l'erreur normalement
    return Promise.reject(error)
})

const pinia = createPinia()

createApp(App).use(router).use(pinia).mount('#app')
