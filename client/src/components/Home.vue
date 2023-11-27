<template>
  <div>
    <router-link to="/">Главная</router-link>
    <router-link to="/exchanges">Обменники</router-link>
    <router-link to="/information">Информация</router-link>
    <router-link to="/registration">Регистрация</router-link>
    <router-link to="/login">Авторизация</router-link>
    <h1>Главная страница</h1>

    <label>Выберите валюту для отправки:</label>
    <select v-model="selectedGivePair" @change="fetchCourses">
      <option v-for="give_pair_name in currencyPairs.give_pair_name_method" :key="give_pair_name" :value="give_pair_name">{{ give_pair_name }}</option>
    </select>

    <label>Выберите валюту для получения:</label>
    <select v-model="selectedReceivePair" @change="fetchCourses">
      <option v-for="receive_pair_name in currencyPairs.receive_pair_name_method" :key="receive_pair_name" :value="receive_pair_name">{{ receive_pair_name }}</option>
    </select>

    <div>
      <h2>Список курсов:</h2>
      <table>
  <thead>
    <tr>
      <th @click="sortTable('exchange_name')">
        Название обменника
        <span v-if="currentSortColumn === 'exchange_name'">
          {{ sortDirection === 'asc' ? '▲' : '▼' }}
        </span>
      </th>
      <th @click="sortTable('give_count')">
        Отдаете
        <span v-if="currentSortColumn === 'give_count'">
          {{ sortDirection === 'asc' ? '▲' : '▼' }}
        </span>
      </th>
      <th @click="sortTable('receive_count')">
        Получаете
        <span v-if="currentSortColumn === 'receive_count'">
          {{ sortDirection === 'asc' ? '▲' : '▼' }}
        </span>
      </th>
      <th @click="sortTable('reserve')">
        Резерв
        <span v-if="currentSortColumn === 'reserve'">
          {{ sortDirection === 'asc' ? '▲' : '▼' }}
        </span>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr v-for="course in filteredCourses" :key="course.id">
      <td>{{ course.exchange_name }}</td>
      <td>{{ course.give_count }}</td>
      <td>{{ course.receive_count }}</td>
      <td>{{ course.reserve }}</td>
    </tr>
  </tbody>
</table>


    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'HomeView',
  data() {
    return {
      currencyPairs: { give_pair_name_method: [], receive_pair_name_method: [] },
      courses: [],
      currentSortColumn: null,
      sortDirection: 'asc',
      sortDirections: {}, // новый объект для хранения направлений сортировки по колонкам
      selectedGivePair: null,
      selectedReceivePair: null,
      sortSettings: { column: null, direction: 'asc' },

    };
  },
  beforeUpdate() {
    // Применяем сортировку
    this.applySort();
  },
  mounted() {
    this.fetchCurrencyPairs();
    this.fetchCourses();
    setInterval(this.fetchCourses, 5000);
  },
  computed: {
    filteredCourses() {
      const selectedGivePair = this.selectedGivePair?.toLowerCase().trim();
      const selectedReceivePair = this.selectedReceivePair?.toLowerCase().trim();

      if (selectedGivePair && selectedReceivePair) {
        return this.courses.filter(course =>
          course.give_pair_name.toLowerCase().trim() === selectedGivePair &&
          course.receive_pair_name.toLowerCase().trim() === selectedReceivePair
        );
      }
      return this.courses;
    },
  },
  methods: {
    async fetchCurrencyPairs() {
      try {
        const response = await api.get('/currency-pairs');
        if (response.data && response.data.give_pair_name && response.data.receive_pair_name) {
          this.currencyPairs.give_pair_name_method = response.data.give_pair_name.sort();
          this.currencyPairs.receive_pair_name_method = response.data.receive_pair_name.sort();
        } else {
          console.error('Отсутствуют ожидаемые свойства в ответе сервера:', response.data);
        }
      } catch (error) {
        console.error('Ошибка при загрузке списка валютных пар', error);
      }
    },
    async fetchCourses() {
      try {
        const response = await api.get('/courses');
        this.courses = response.data;

        // Восстанавливаем текущее состояние сортировки из sortSettings
        if (this.sortSettings.column) {
          this.sortTable(this.sortSettings.column);
        }
      } catch (error) {
        console.error('Ошибка при загрузке курсов', error);
      }
    },
      applySort() {
      if (this.sortSettings.column) {
        // Глубокое клонирование массива перед сортировкой
        const clonedCourses = JSON.parse(JSON.stringify(this.courses));

        // Сортировка массива clonedCourses в соответствии с выбранными параметрами
        clonedCourses.sort((a, b) => {
          const modifier = this.sortSettings.direction === 'desc' ? -1 : 1;
          const aValue = isNaN(a[this.sortSettings.column]) ? a[this.sortSettings.column] : parseFloat(a[this.sortSettings.column]);
          const bValue = isNaN(b[this.sortSettings.column]) ? b[this.sortSettings.column] : parseFloat(b[this.sortSettings.column]);

          if (aValue < bValue) return -1 * modifier;
          if (aValue > bValue) return 1 * modifier;
          return 0;
        });

        // Обновление состояния Vue
        this.courses = clonedCourses;
      }
    },

    sortTable(column) {
      if (this.sortSettings.column === column) {
        this.sortSettings.direction = this.sortSettings.direction === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortSettings.column = column;
        this.sortSettings.direction = 'asc';
      }

      // Сохраняем состояние сортировки в localStorage
      localStorage.setItem('sortColumn', this.sortSettings.column);
      localStorage.setItem('sortDirection', this.sortSettings.direction);

      // Применяем сортировку
      this.applySort();
    },


  },
};
</script>


<style scoped>
/* Ваши стили здесь */
</style>
