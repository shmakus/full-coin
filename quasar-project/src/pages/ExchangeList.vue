<template>
  <q-layout view="hHh lpR fFf">

    <q-header class="bg-primary text-white" height-hint="98">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
          </q-avatar>
          Title
        </q-toolbar-title>
        <div>Всего курсов: {{ totalValues }}</div>
      </q-toolbar>

      <q-tabs align="center">
        <q-route-tab :to="{ path: '/' }" label="Главная" />
        <q-route-tab :to="{ path: '/exchanges' }" label="Список обменников" />
        <q-route-tab to="/page2" label="Page Two" />
        <q-route-tab to="/page3" label="Page Three" />
      </q-tabs>
    </q-header>

    <q-page-container>
      <div class="q-pa-md">
        <q-table
          grid
          flat bordered
          card-class="bg-primary text-white"
          title="Обменники"
          :rows="exchanges"
          :columns="columns"
          row-key="exchange_name"
          :filter="filter"
          hide-header
        >
          <template v-slot:top-right>
            <q-input borderless dense debounce="300" v-model="filter" placeholder="Поиск">
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
          </template>
        </q-table>
      </div>
    </q-page-container>

  </q-layout>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';

const columns = [
  { name: 'exchange_name', label: 'Обменник', align: 'left', field: 'exchange_name', sortable: true },
  { name: 'id', label: 'ID', field: 'id', sortable: true },
  { name: 'descriptions', label: 'Описание', field: 'descriptions', sortable: true },
  { name: 'link', label: 'Ссылка', field: 'link', sortable: true },
];

export default {
  setup() {
    const filter = ref('');
    const exchanges = ref([]);

    const loadData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/exchanges');
        exchanges.value = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке данных об обменниках:', error);
      }
    };

    onMounted(loadData);

    return {
      filter,
      columns,
      exchanges,
    };
  },
};
</script>

<style lang="sass" scoped>
.my-card
  width: 100%
  max-width: 350px
</style>
