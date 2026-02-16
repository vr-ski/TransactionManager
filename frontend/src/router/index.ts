import {
  createRouter,
  createWebHistory,
  RouteLocationNormalized,
  NavigationGuardNext,
} from "vue-router";
import { useAuthStore } from "@/stores/auth";
import TransactionsLayout from "@/layouts/TransactionsLayout.vue";
import ContractorsLayout from "@/layouts/ContractorsLayout.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/transactions" },
    { path: "/login", component: () => import("@/views/LoginView.vue") },
    {
      path: "/transactions",
      component: TransactionsLayout,
      meta: { requiresAuth: true },
      children: [
        { path: "", component: () => import("@/views/TransactionsView.vue") },
        {
          path: ":id",
          component: () => import("@/views/TransactionDetailView.vue"),
        },
      ],
    },
    {
      path: "/contractors",
      component: ContractorsLayout,
      meta: { requiresAuth: true },
      children: [
        { path: "", component: () => import("@/views/ContractorsView.vue") },
        {
          path: ":id",
          component: () => import("@/views/ContractorDetailView.vue"),
        },
      ],
    },
  ],
});

router.beforeEach(
  (
    to: RouteLocationNormalized,
    _from: RouteLocationNormalized,
    next: NavigationGuardNext,
  ) => {
    const authStore = useAuthStore();
    if (to.meta.requiresAuth && !authStore.isAuthenticated()) {
      next("/login");
    } else {
      next();
    }
  },
);

export default router;
