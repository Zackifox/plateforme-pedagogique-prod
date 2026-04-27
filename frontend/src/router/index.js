import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  // ── Pages publiques ──
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/public/HomeView.vue'),
  },
  {
    path: '/instituts/:id',
    name: 'Institut',
    component: () => import('@/views/public/InstitutView.vue'),
  },
  {
    path: '/filieres/:id',
    name: 'Filiere',
    component: () => import('@/views/public/FiliereView.vue'),
  },
  {
    path: '/niveaux/:id',
    name: 'Niveau',
    component: () => import('@/views/public/NiveauView.vue'),
  },
  {
    path: '/matieres/:id',
    name: 'Matiere',
    component: () => import('@/views/public/MatiereView.vue'),
  },
  {
    path: '/recherche',
    name: 'Recherche',
    component: () => import('@/views/public/RechercheView.vue'),
  },
  // ── Admin ──
  {
    path: '/admin/login',
    name: 'Login',
    component: () => import('@/views/admin/LoginView.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/admin',
    name: 'Dashboard',
    component: () => import('@/views/admin/DashboardView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/upload',
    name: 'Upload',
    component: () => import('@/views/admin/UploadView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/ressources',
    name: 'AdminRessources',
    component: () => import('@/views/admin/RessourcesView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/catalogue',
    name: 'AdminCatalogue',
    component: () => import('@/views/admin/CatalogueView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/communiques',
    name: 'Communiques',
    component: () => import('@/views/public/CommuniquesView.vue'),
  },
  {
    path: '/a-propos',
    name: 'APropos',
    component: () => import('@/views/public/AProposView.vue'),
  },
  {
    path: '/admin/communiques',
    name: 'AdminCommuniques',
    component: () => import('@/views/admin/CommuniquesAdminView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) return { name: 'Login' }
  if (to.meta.guestOnly && auth.isAuthenticated) return { name: 'Dashboard' }
})

export default router