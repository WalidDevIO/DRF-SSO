import { computed, ref } from 'vue'
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import { api } from '../main';

export function setTokenWithExpiry(key, value, ttl) {
    // ttl est en secondes, convertir en millisecondes et ajouter au temps actuel
    const expires = Date.now() + ttl * 1000;
    const item = {
        value: value,
        expires: expires
    };
    localStorage.setItem(key, JSON.stringify(item));
}

export function getTokenWithExpiry(key) {
    const item = JSON.parse(localStorage.getItem(key)) ?? null;
    if (!item) return null;
    // Comparer la date d'expiration actuelle avec la date d'expiration enregistrée
    if (Date.now() > item.expires) {
        // Si le token est expiré, supprimer l'item de localStorage et retourner null
        localStorage.removeItem(key);
        return null;
    }
    return item.value;
}

export const useUserStore = defineStore('UserStore', () => {

    const user = ref({})
    const groups = ref([])
    const logged = ref(false)
    const initialized = ref(false)
    const router = useRouter()
    const group = computed(() => user.value.group)

    const fetchUser = async () => {
        try {
            const { data } = await api.get("core/me/")
        } catch {
            return false
        }
        logged.value = true
        user.value = data
        fetchGroups()
        return true
    }

    const fetchGroups = async () => {
        if(!user.value.is_staff) return
        const { data } = await api.get("core/groups/")
        groups.value = data
    }

    const login = async (username, password) => {
        try { 
            const { access, refresh, access_expires_in, refresh_expires_in } = await api.post("token/", {username, password})
            setTokenWithExpiry('access_token', access, access_expires_in)
            setTokenWithExpiry('refresh_token', refresh, refresh_expires_in)
            await fetch()
            router.push("/")
        } catch {
            return false
        }
    }

    const logout = () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        user.value = {}
        groups.value = []
        logged.value = false
        router.push("/login")
    }

    const refreshToken = async () => {
        const refreshToken = getTokenWithExpiry('refresh_token');
        if (!refreshToken) return false;
        try {
            const { access, access_expires_in } = await api.post('token/refresh/', { refresh: refreshToken });
            setTokenWithExpiry('access_token', access, access_expires_in)
            await fetch();
            return true;
        } catch {
            return false;
        }
    }

    return {
        user,
        groups,
        logged,
        group,
        initialized,
        login,
        logout,
        refreshToken,
        fetchUser
    };

})