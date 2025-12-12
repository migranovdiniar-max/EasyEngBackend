<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const mode = ref("login");
const email = ref("");
const password = ref("");
const message = ref("");
const isLoading = ref(false);

const toggleMode = () => {
  mode.value = mode.value === "login" ? "register" : "login";
  message.value = "";
};

const onSubmit = async () => {
  if (!email.value || !password.value) {
    message.value = "Заполните все поля";
    return;
  }

  isLoading.value = true;
  message.value = "Подключаемся...";

  const url = `/api/auth/${mode.value}`;

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: email.value, password: password.value }),
    });

    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || "Ошибка сервера");

    // Успешный вход
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("user", JSON.stringify(data.user));

    message.value = `Добро пожаловать, ${data.user.name || data.user.email}!`;

    setTimeout(() => {
      router.push("/dashboard");
    }, 1200);
  } catch (err) {
    message.value = err.message;
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center px-4 py-12 bg-gradient-to-br from-violet-900 via-purple-900 to-indigo-900 overflow-hidden relative"
  >
    <!-- Анимированный градиентный фон -->
    <div class="absolute inset-0">
      <div
        class="absolute inset-0 bg-gradient-to-tr from-pink-600/20 via-purple-600/20 to-cyan-600/20 animate-pulse"
      ></div>
      <div
        class="absolute top-0 left-0 w-96 h-96 bg-pink-500 rounded-full mix-blend-screen filter blur-3xl opacity-30 animate-blob"
      ></div>
      <div
        class="absolute top-0 right-0 w-96 h-96 bg-purple-500 rounded-full mix-blend-screen filter blur-3xl opacity-30 animate-blob animation-delay-2000"
      ></div>
      <div
        class="absolute -bottom-8 left-20 w-96 h-96 bg-cyan-500 rounded-full mix-blend-screen filter blur-3xl opacity-30 animate-blob animation-delay-4000"
      ></div>
    </div>

    <!-- Карточка формы -->
    <div class="relative w-full max-w-md">
      <div
        class="bg-white/10 backdrop-blur-2xl rounded-3xl shadow-2xl border border border-white/20 p-10 transform transition-all duration-700 hover:scale-105"
      >
        <!-- Логотип / Иконка -->
        <div
          class="mx-auto w-20 h-20 bg-gradient-to-br from-pink-500 to-violet-600 rounded-2xl shadow-lg flex items-center justify-center mb-8 transform hover:rotate-12 transition-transform duration-500"
        >
          <svg
            class="w-12 h-12 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
            />
          </svg>
        </div>

        <!-- Заголовок с анимацией -->
        <h2
          class="text-4xl font-bold text-center text-white text-center mb-2 bg-clip-text text-transparent bg-gradient-to-r from-pink-400 to-violet-400"
        >
          {{ mode === "login" ? "С возвращением!" : "Присоединяйтесь" }}
        </h2>
        <p class="text-center text-purple-200 mb-10">
          {{
            mode === "login"
              ? "Войдите в свой аккаунт"
              : "Создайте новый аккаунт"
          }}
        </p>

        <!-- Форма -->
        <form @submit.prevent="onSubmit" class="space-y-6">
          <!-- Email -->
          <div class="group">
            <div class="relative">
              <input
                v-model="email"
                type="email"
                required
                placeholder="you@example.com"
                class="w-full px-5 py-4 bg-white/10 border border-white/20 rounded-2xl text-white placeholder-purple-300 focus:outline-none focus:ring-4 focus:ring-pink-500/50 focus:border-pink-400 transition-all duration-300 backdrop-blur-xl text-lg"
              />
              <div
                class="absolute inset-0 rounded-2xl bg-gradient-to-r from-pink-500/20 to-violet-500/20 opacity-0 group-focus-within:opacity-100 blur-xl transition-opacity duration-500 -z-10"
              ></div>
            </div>
          </div>

          <!-- Пароль -->
          <div class="group">
            <div class="relative">
              <input
                v-model="password"
                type="password"
                required
                placeholder="••••••••"
                class="w-full px-5 py-4 bg-white/10 border border-white/20 rounded-2xl text-white placeholder-purple-300 focus:outline-none focus:ring-4 focus:ring-pink-500/50 focus:border-pink-400 transition-all duration-300 backdrop-blur-xl text-lg"
              />
              <div
                class="absolute inset-0 rounded-2xl bg-gradient-to-r from-pink-500/20 to-violet-500/20 opacity-0 group-focus-within:opacity-100 blur-xl transition-opacity duration-500 -z-10"
              ></div>
            </div>
          </div>

          <!-- Сообщение -->
          <transition name="fade">
            <div
              v-if="message"
              class="text-center py-3 px-6 rounded-2xl font-medium text-lg"
              :class="{
                'bg-green-500/20 text-green-300 border border-green-500/50':
                  message.includes('Добро') || message.includes('Подключаемся'),
                'bg-red-500/20 text-red-300 border border-red-500/50':
                  message.includes('Ошибка') || message.includes('Заполните'),
              }"
            >
              {{ message }}
            </div>
          </transition>

          <!-- Кнопка -->
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full py-4 px-8 bg-gradient-to-r from-pink-500 to-violet-600 text-white font-bold text-xl rounded-2xl shadow-2xl hover:shadow-pink-500/25 transform hover:-translate-y-1 active:translate-y-0 transition-all duration-300 disabled:opacity-70 disabled:cursor-not-allowed relative overflow-hidden group"
          >
            <span class="relative z-10">
              {{
                isLoading
                  ? "Подождите..."
                  : mode === "login"
                  ? "Войти"
                  : "Создать аккаунт"
              }}
            </span>
            <div
              class="absolute inset-0 bg-white/20 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"
            ></div>
          </button>

          <!-- Переключение режима -->
          <div class="text-center mt-8">
            <button
              type="button"
              @click="toggleMode"
              class="text-purple-300 hover:text-white font-medium text-lg transition duration-300 relative group"
            >
              {{ mode === "login" ? "Нет аккаунта? " : "Уже есть аккаунт? " }}
              <span
                class="text-pink-400 font-bold underline decoration-2 underline-offset-4"
              >
                {{ mode === "login" ? "Зарегистрируйтесь" : "Войти" }}
              </span>
            </button>
          </div>
        </form>
      </div>

      <!-- Декоративные элементы -->
      <div
        class="absolute -bottom-10 -left-10 w-40 h-40 bg-pink-500 rounded-full blur-3xl opacity-20"
      ></div>
      <div
        class="absolute -top-10 -right-10 w-40 h-40 bg-violet-500 rounded-full blur-3xl opacity-20"
      ></div>
    </div>
  </div>
</template>

<style scoped>
@keyframes blob {
  0% {
    transform: translate(0px, 0px) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  100% {
    transform: translate(0px, 0px) scale(1);
  }
}
.animate-blob {
  animation: blob 7s infinite;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
.animation-delay-4000 {
  animation-delay: 4s;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
