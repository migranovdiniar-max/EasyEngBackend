<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

// Обработчик клика по пункту меню
const onClick = (e) => {
  console.log("click ", e.key);
  // Перенаправление по маршруту
  router.push(`/${e.key}`);
};

// Элементы меню — адаптированы под EasyEng
const items = [
  {
    key: "learn",
    label: "?? Изучать",
    children: [
      { key: "learn", label: "Слово дня" },
      { key: "review", label: "Повторение" },
    ],
  },
  {
    key: "quiz",
    label: "?? Викторина",
    children: [
      { key: "quiz", label: "Тренировка слов" },
      { key: "speed", label: "Быстрый отклик" },
    ],
  },
  {
    key: "words",
    label: "?? Словарь",
    children: [
      { key: "all", label: "Все слова" },
      { key: "favorites", label: "Избранные" },
      { key: "categories", label: "Категории" },
    ],
  },
  {
    type: "divider",
  },
  {
    key: "stats",
    label: "?? Статистика",
    children: [
      { key: "stats", label: "Общая статистика" },
      { key: "streak", label: "Серии (streak)" },
    ],
  },
  {
    key: "settings",
    label: "?? Настройки",
    children: [
      { key: "profile", label: "Профиль" },
      { key: "theme", label: "Тема" },
      { key: "logout", label: "Выйти", danger: true },
    ],
  },
];
</script>

<template>
  <a-menu
    @click="onClick"
    style="width: 256px; height: 100%"
    :default-selected-keys="['learn']"
    :default-open-keys="['learn', 'quiz']"
    mode="inline"
    :items="items"
  />
</template>

<style scoped>
/* Дополнительный стиль для бокового меню */
.ant-menu {
  border-right: 0;
  background: #ffffff;
  font-size: 15px;
}

.ant-menu-item-active {
  background-color: #f0f9ff !important;
  border-radius: 8px !important;
  margin: 0 8px;
}

.ant-menu-item-selected {
  color: #1890ff !important;
}
</style>
