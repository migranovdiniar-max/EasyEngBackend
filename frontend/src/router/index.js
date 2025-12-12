import { createRouter, createWebHistory } from "vue-router";
import AuthForm from "../components/AuthForm.vue";
import Dashboard from "../views/Dashboard.vue";

const routes = [
  { path: "/", component: AuthForm },
  { path: "/dashboard", component: Dashboard },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
});
