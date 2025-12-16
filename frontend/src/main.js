import { createApp } from "vue";
import App from "./App.vue";
import { router } from "./router";

// Добавь Ant Design Vue
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css'; // Стили (новая версия)

createApp(App).use(router).use(Antd).mount("#app");
