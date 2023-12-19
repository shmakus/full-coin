<template>
  <div class="q-pa-md" >
    <q-table
            class="my-give_pairs-table"

      title="Отдаю"
      :rows="givePairs"
      :columns="columns"
      dense
      row-key="name"
      :rows-per-page-options="[150]"
      :filter="filter"
    >
      <template v-slot:top-right>
        <q-input borderless dense debounce="300" v-model="filter" placeholder="Поиск">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>
      <template v-slot:body="props" >
        <q-tr
          :props="props"
          @click="onGivePairSelected(props.row)"
          :class="{ 'selected-row': props.row.selected }"
        >
          <q-td v-for="col in props.cols" :key="col.name" :props="props">
            {{ props.row[col.name] }}
          </q-td>
        </q-tr>
      </template>

    </q-table>
  </div>
</template>

<script>
import api from '../services/api_backend.js';
import { bus } from '../services/EventBus.js';
import {ref, onMounted} from 'vue'

export default {
  data() {
    return {

      filter: ref(''),
      columns: [
        {
          name: 'name',
          align: 'left',
          sortable: false,
          field: row => row.name,
        },
      ],
      givePairs: [],
    };
  },
  created() {
    this.loadData('give_pair_name');
  },
  methods: {
    // Загрузка данных с сервера
    async loadData(parameter) {
  try {
    const response = await api.get('/currency-pairs', {
      params: {
        // Передаем параметр, если он есть
        some_parameter: parameter,
      },
    });
    this.givePairs = response.data.give_pair_name.map(pair => ({ ...pair, selected: false }));
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
},
    // Обработчик события выбора монеты для отдачи
    onGivePairSelected(row) {
    console.log('Метод onGivePairSelected вызван');
    console.log('Выбрана монета для получения:', row.name);

    // Сбросить selected для всех строк
    this.givePairs.forEach(pair => pair.selected = false);

    // Установить selected для выбранной строки
    row.selected = true;

    // Вызвать событие
    bus.emit('givePairSelected', row.name); // передаем только имя монеты, не весь объект
  },

  },
};

</script>

<style lang="sass">
.selected-row
  background-color: lightblue
.my-give_pairs-table
  /* height or max-height is important */
  max-height: 450px
</style>
