<template>
  <div class="q-pa-md">
    <q-table
                  class="my-recive_pairs-table"

      title="Получаю"
      :rows="receivePairs"
      :columns="columns"
      dense
      row-key="name"
      :rows-per-page-options="[200]"
      :filter="filter"
    >
      <template v-slot:body="props">
        <q-tr
          :props="props"
          @click="onReceivePairSelected(props.row)"
          :class="{ 'selected-row': props.row.selected }"
          >
          <q-td v-for="col in props.cols" :key="col.name" :props="props">
            {{ props.row[col.name] }}
          </q-td>
        </q-tr>
      </template>
       <template v-slot:top-right>
        <q-input borderless dense debounce="300" v-model="filter" placeholder="Search">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>
    </q-table>
  </div>
</template>

<script>
import api from '../services/api_backend.js';
import { bus } from '../services/EventBus.js';
import {ref} from 'vue'

export default {
  data() {
    return {
      filter: ref(''),
      columns: [
        {
          name: 'name',
          align: 'left',
          label: 'Обменник',
          field: row => row.name,
        },
      ],
      receivePairs: [],
    };
  },
  created() {
    this.loadData('receive_pair_name');
  },
  methods: {
    async loadData(pairType) {
      try {
        const response = await api.get('/currency-pairs');
        this.receivePairs = response.data[pairType].map(pair => ({ ...pair, selected: false })); // Добавляем свойство selected со значением false
      } catch (error) {
        console.error('Ошибка при загрузке данных:', error);
      }
    },
    onReceivePairSelected(row) {
      console.log('Метод onReceivePairSelected вызван');
      console.log('Выбрана монета для получения:', row.name);
      // Сбросить selected для всех строк
      this.receivePairs.forEach(pair => pair.selected = false);

      // Установить selected для выбранной строки
      row.selected = true;

      // Вызвать событие
      bus.emit('receivePairSelected', row.name);
    },
  },
};
</script>
<style lang="sass">
.selected-row
  background-color: lightblue
.my-recive_pairs-table
  /* height or max-height is important */
  max-height: 430px
</style>
