<template>
  <div>
     <router-link to="/">Главная</router-link>
    <router-link to="/exchanges">Обменники</router-link>
    <router-link to="/information">Информация</router-link>
    <router-link to="/registration">Регистрация</router-link>
    <router-link to="/login">Авторизация</router-link>
    <h1>Главная страница</h1>

    <div v-for="course in courses" :key="course.id">
        Отдаете - {{ course.give }} : Получаете - {{ course.receive }} : Резерв {{ course.reserve }} : <a href="{{ course.link }}">Ссылка</a> :  Торговая пара - {{ course.trading_pair }}
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'HomeView', // Изменили имя компонента
  data() {
    return {
      courses: [],
    };
  },
  mounted() {
    this.fetchCourses();
    setInterval(this.fetchCourses, 15000); // Запрос каждые 15 секунд
  },
  methods: {
    async fetchCourses() {
      try {
        const response = await api.get('/courses');
        this.courses = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке данных', error);
      }
    },
  },
};
</script>
