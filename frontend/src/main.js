import { createApp } from "vue";
import "./index.css"; // ? Должно быть до App
import App from "./App.vue";
import { router } from "./router";

createApp(App).use(router).mount("#app"); // ? Исправил: один вызов
