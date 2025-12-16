<template>
  <div
    class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4"
  >
    <div class="max-w-md w-full space-y-8 bg-white p-10 rounded-2xl shadow-lg">
      <!-- Логотип -->
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-900">EasyEng</h1>
        <p class="text-gray-600 mt-2">Изучай английский легко</p>
      </div>

      <!-- Переключатель -->
      <div class="flex border-b">
        <button
          :class="[
            'flex-1 py-3 text-center font-medium',
            !isLogin
              ? 'text-indigo-600 border-b-2 border-indigo-600'
              : 'text-gray-500',
          ]"
          @click="isLogin = false"
        >
          Регистрация
        </button>
        <button
          :class="[
            'flex-1 py-3 text-center font-medium',
            isLogin
              ? 'text-indigo-600 border-b-2 border-indigo-600'
              : 'text-gray-500',
          ]"
          @click="isLogin = true"
        >
          Вход
        </button>
      </div>

      <!-- Форма -->
      <form @submit.prevent="submit" class="space-y-6">
        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-gray-700">Email</label>
          <input
            v-model="form.email"
            type="email"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required
          />
        </div>

        <!-- Пароль -->
        <div>
          <label class="block text-sm font-medium text-gray-700">Пароль</label>
          <input
            v-model="form.password"
            type="password"
            class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            required
            minlength="6"
          />
        </div>

        <!-- Кнопка -->
        <button
          type="submit"
          :disabled="loading"
          class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {{
            loading ? "Загрузка..." : isLogin ? "Войти" : "Зарегистрироваться"
          }}
        </button>
      </form>

      <!-- Сообщение об ошибке -->
      <div v-if="error" class="text-red-600 text-sm text-center">
        {{ error }}
      </div>

      <!-- Подтверждение email -->
      <div v-if="success" class="text-green-600 text-sm text-center">
        {{ success }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isLogin: true,
      form: {
        email: "",
        password: "",
      },
      loading: false,
      error: "",
      success: "",
    };
  },
  methods: {
    async submit() {
      this.error = "";
      this.success = "";
      this.loading = true;

      const url = this.isLogin ? "/api/auth/login" : "/api/auth/register";

      try {
        const response = await fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.form),
        });

        const data = await response.json();

        if (response.ok) {
          if (this.isLogin) {
            // Сохраняем токен
            localStorage.setItem("access_token", data.access_token);
            this.success = "Успешный вход! Переходим...";
            setTimeout(() => {
              window.location.href = "/learn";
            }, 1000);
          } else {
            this.success = "Проверьте почту и подтвердите email";
            this.isLogin = true; // переключаем на вход
          }
        } else {
          this.error = data.detail || "Ошибка";
        }
      } catch (err) {
        this.error = "Ошибка сети";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
