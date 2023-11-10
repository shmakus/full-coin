<template>
  <div>
    <h1>Страница обменников</h1>
    <div v-for="exchange in exchanges" :key="exchange.id">
      {{ exchange.exchange_name }} - {{ exchange.descriptions }} - {{ exchange.link }}
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'ExchangesName', // Изменили имя компонента
  data() {
    return {
      exchanges: [],
    };
  },
  mounted() {
    this.fetchExchanges();
    setInterval(this.fetchExchanges, 15000);
  },
  methods: {
    async fetchExchanges() {
      try {
        const response = await api.get('/exchanges');
        this.exchanges = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке данных', error);
      }
    },
  },
};
</script>

<style>
/* Добавьте стили, если необходимо */
</style>
