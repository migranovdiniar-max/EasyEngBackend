<script setup>
import { ref, reactive } from "vue";

const isLogin = ref(true);
const form = reactive({
  email: "",
  password: "",
});
const loading = ref(false);
const error = ref("");
const success = ref("");

async function submit() {
  error.value = "";
  success.value = "";
  loading.value = true;

  const url = isLogin.value ? "/api/auth/login" : "/api/auth/register";

  const body = isLogin.value
    ? { username: form.email, password: form.password }
    : { email: form.email, password: form.password };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    let data;
    try {
      data = await response.json();
    } catch {
      error.value = "Ошибка ответа сервера";
      return;
    }

    if (response.ok) {
      if (isLogin.value) {
        if (data.access_token) {
          localStorage.setItem("access_token", data.access_token);
          success.value = "Вход успешен...";
          setTimeout(() => (window.location.href = "/learn"), 1200);
        } else {
          error.value = "Токен не получен";
        }
      } else {
        success.value = "Проверьте почту для подтверждения";
        setTimeout(() => (isLogin.value = true), 1500);
      }
    } else {
      error.value = data.detail || "Ошибка";
    }
  } catch {
    error.value = "Ошибка сети";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div
    class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 flex items-center justify-center px-4 py-12 relative overflow-hidden"
  >
    <!-- Декоративные круги -->
    <div
      class="absolute -top-24 -left-24 w-72 h-72 bg-indigo-200 rounded-full opacity-30 animate-pulse"
    ></div>
    <div
      class="absolute -bottom-24 -right-24 w-72 h-72 bg-cyan-200 rounded-full opacity-30 animate-pulse delay-1000"
    ></div>

    <!-- Контейнер формы -->
    <div class="w-full max-w-md relative z-10">
      <!-- Логотип -->
      <div class="text-center mb-8">
        <div
          class="inline-flex items-center justify-center w-14 h-14 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl shadow-lg mb-4"
        >
          <span class="text-white font-bold text-xl"></span>
        </div>
        <h1
          class="text-3xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent"
        >
          EasyEng
        </h1>
        <p class="text-gray-600 mt-1 text-sm">
          Изучайте английский с удовольствием
        </p>
      </div>

      <!-- Карточка -->
      <div
        class="bg-white/80 backdrop-blur-sm rounded-2xl shadow-xl border border-white/30 overflow-hidden"
      >
        <!-- Переключатель режимов -->
        <div
          class="flex bg-gradient-to-r from-gray-50 to-indigo-25 p-1 border-b border-gray-100"
        >
          <button
            @click="isLogin = false"
            :class="[
              'flex-1 py-3 text-center font-semibold rounded-xl transition-all duration-300',
              !isLogin
                ? 'bg-white text-indigo-600 shadow-sm scale-105'
                : 'text-gray-500 hover:text-gray-700',
            ]"
          >
            Регистрация
          </button>
          <button
            @click="isLogin = true"
            :class="[
              'flex-1 py-3 text-center font-semibold rounded-xl transition-all duration-300',
              isLogin
                ? 'bg-white text-indigo-600 shadow-sm scale-105'
                : 'text-gray-500 hover:text-gray-700',
            ]"
          >
            Вход
          </button>
        </div>

        <!-- Форма -->
        <form @submit.prevent="submit" class="p-8 space-y-5">
          <!-- Email -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Email</label>
            <div class="relative">
              <span
                class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400"
              >
                ✉️
              </span>
              <input
                v-model="form.email"
                type="email"
                class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                placeholder="you@example.com"
                required
              />
            </div>
          </div>

          <!-- Пароль -->
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Пароль</label>
            <div class="relative">
              <span
                class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-400"
              >
                🔒
              </span>
              <input
                v-model="form.password"
                type="password"
                class="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
                placeholder="••••••••"
                required
                minlength="6"
              />
            </div>
          </div>

          <!-- Кнопка -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 px-6 rounded-xl font-medium text-white bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 focus:outline-none focus:ring-4 focus:ring-indigo-200 transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-70 disabled:cursor-not-allowed"
          >
            <span v-if="loading" class="flex items-center justify-center">
              <span
                class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"
              ></span>
              Загрузка...
            </span>
            <span v-else>
              {{ isLogin ? "Войти" : "Зарегистрироваться" }}
            </span>
          </button>
        </form>

        <!-- Сообщения -->
        <div v-if="error" class="px-8 pb-6">
          <div
            class="bg-red-50 border border-red-200 text-red-700 text-sm p-3 rounded-xl flex items-center space-x-2"
          >
            <span>❌</span>
            <span>{{ error }}</span>
          </div>
        </div>
        <div v-if="success" class="px-8 pb-6">
          <div
            class="bg-green-50 border border-green-200 text-green-700 text-sm p-3 rounded-xl flex items-center space-x-2"
          >
            <span>✅</span>
            <span>{{ success }}</span>
          </div>
        </div>
      </div>

      <!-- Подпись -->
      <p class="text-center text-xs text-gray-500 mt-6">
        Используя EasyEng, вы соглашаетесь с
        <a href="#" class="text-indigo-600 hover:underline">условиями</a> и
        <a href="#" class="text-indigo-600 hover:underline"
          >политикой конфиденциальности</a
        >
      </p>
    </div>
  </div>
</template>
