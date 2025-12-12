<script setup>
import { ref } from "vue";

// Режим: login или register
const mode = ref("login");
const email = ref("");
const password = ref("");
const message = ref("");

// Переключение режима
const toggleMode = () => {
  mode.value = mode.value === "login" ? "register" : "login";
  message.value = "";
};

// Отправка формы
const onSubmit = async () => {
  message.value = "Загрузка...";
  const url = `/api/auth/${mode.value}`;
  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email.value, password: password.value }),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || "Ошибка");
    }

    // Сохраняем токен и данные
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", JSON.stringify(data.user));

    message.value = `✅ Успешно! Добро пожаловать, ${
      data.user.username || data.user.email
    }`;
  } catch (err) {
    message.value = "❌ Ошибка: " + err.message;
  }
};
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-100 via-white to-purple-100 px-4"
  >
    <div
      class="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md border border-gray-100"
    >
      <!-- Заголовок -->
      <h1 class="text-3xl font-bold text-center text-gray-800 mb-2">
        {{ mode === "login" ? "Вход" : "Регистрация" }}
      </h1>
      <p class="text-center text-gray-500 text-sm mb-8">
        {{
          mode === "login" ? "Войдите, чтобы продолжить" : "Создайте аккаунт"
        }}
      </p>

      <!-- Форма -->
      <form @submit.prevent="onSubmit" class="space-y-6">
        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2"
            >Email</label
          >
          <input
            v-model="email"
            type="email"
            placeholder="you@example.com"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition duration-200 outline-none text-gray-700"
            required
          />
        </div>

        <!-- Пароль -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2"
            >Пароль</label
          >
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition duration-200 outline-none text-gray-700"
            required
          />
        </div>

        <!-- Сообщение -->
        <div
          v-if="message"
          class="text-sm"
          :class="{
            'text-green-600': message.startsWith('✅'),
            'text-red-600': message.startsWith('❌'),
            'text-blue-600':
              !message.startsWith('✅') && !message.startsWith('❌'),
          }"
        >
          {{ message }}
        </div>

        <!-- Кнопка -->
        <button
          type="submit"
          class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-3 rounded-lg transition duration-200 transform hover:scale-[1.02] active:scale-[0.98] focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          {{ mode === "login" ? "Войти" : "Зарегистрироваться" }}
        </button>
      </form>

      <!-- Переключение режима -->
      <div class="text-center mt-6">
        <button
          @click="toggleMode"
          class="text-indigo-600 hover:text-indigo-800 font-medium text-sm transition duration-150"
        >
          {{
            mode === "login"
              ? "Нет аккаунта? Зарегистрироваться"
              : "Уже есть аккаунт? Войти"
          }}
        </button>
      </div>
    </div>
  </div>
</template>
