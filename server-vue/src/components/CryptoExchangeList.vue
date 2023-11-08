<template>
  <div>
    <h1>Crypto Exchanges</h1>
    <ul>
      <li v-for="exchange in exchanges" :key="exchange.id">{{ exchange.name }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      exchanges: [], // Ваши данные о курсах криптовалют будут здесь
    };
  },
  mounted() {
    // В этом хуке вы можете загрузить данные с вашего API и сохранить их в переменной exchanges
    // Пример: вызов this.fetchExchanges() для загрузки данных
  },
  methods: {
    fetchExchanges() {
      // Здесь можно выполнить запрос к вашему API с помощью axios или другой библиотеки
    },
  },
};
</script>

<style scoped>
/* Стили для компонента */
</style>
