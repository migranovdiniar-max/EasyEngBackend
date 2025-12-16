import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { path: "/", redirect: "/auth/login" },
  {
    path: "/auth/login",
    component: () => import("../components/AuthForm.vue"),
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
