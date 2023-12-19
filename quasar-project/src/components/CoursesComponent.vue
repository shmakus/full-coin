<template>
  <div class="q-pa-md">
    <q-table
        ref="myTable"

      class="my-courses-table"
      title="Курсы"
      :rows="filteredRows"
      :columns="columns"
      dense
      row-key="name"
      :rows-per-page-options="[50]"
    >
      <template v-slot:body="props">
        <q-tr :props="props" @click="onRowClicked(props.row)">
          <q-td v-for="col in props.cols" :key="col.name" :props="props">
            <div v-if="col.field === 'give_count'">
              {{ props.row.give_count }} {{ props.row.give_name_coin }}
            </div>
            <div v-else-if="col.field === 'receive_count'">
              {{ props.row.receive_count }} {{ props.row.receive_name_coin }}
            </div>
            <div v-else-if="col.field === 'reserve_count'">
              {{ props.row.reserve_name_coin ? `${props.row.reserve_count} ${props.row.reserve_name_coin}` : `${props.row.reserve_count} ${props.row.receive_name_coin}` }}
            </div>
            <div v-else>
              {{ props.row[col.field] }}
            </div>
          </q-td>
        </q-tr>
      </template>
    </q-table>
  </div>
</template>

<style lang="sass">
</style>

<script>
import api from '../services/api_backend.js';
import { bus } from '../services/EventBus.js';

export default {
  data() {
    return {
      columns: [
        {
          name: 'exchange_name',
          align: 'left',
          label: 'Обменник',
          field: 'exchange_name',
                      sortable: true,

        },
        {
          name: 'give_count',
          label: 'Отдаете',
          field: 'give_count',
          sortable: true,
        },
        {
          name: 'receive_count',
          label: 'Получаете',
          field: 'receive_count',
          sortable: true,
        },
        {
          name: 'reserve_count',
          label: 'Резерв',
          field: 'reserve_count',
          sortable: true,
        },
      ],
      rows: [],
      filteredRows: [], // массив для отфильтрованных данных
      selectedGivePair: null,
      selectedReceivePair: null,
      sortBy: 'give_count'
    };
  },
  created() {
    // Подписываемся на события EventBus
    bus.on('givePairSelected', this.handleGivePairSelected);
    bus.on('receivePairSelected', this.handleReceivePairSelected);

    // Загружаем данные при создании компонента
    this.loadData();
  },
  beforeUnmount() {
    // Отписываемся от событий EventBus при уничтожении компонента
    bus.off('givePairSelected', this.handleGivePairSelected);
    bus.off('receivePairSelected', this.handleReceivePairSelected);
      this.clearUpdateInterval(); // Очищаем интервал при размонтировании

  },
  methods: {
    // Обработчик события выбора монеты для отдачи
    handleGivePairSelected(givePair) {
      console.log('Выбрана монета для отдачи:', givePair);
      this.selectedGivePair = givePair;
      this.filterData();
      this.setupUpdateInterval(); // Устанавливаем интервал обновления
    },

    // Обработчик события выбора монеты для получения
    handleReceivePairSelected(receivePair) {
      console.log('Выбрана монета для получения:', receivePair);
      this.selectedReceivePair = receivePair;
      this.filterData();
        this.setupUpdateInterval(); // Устанавливаем интервал обновления
    },

    // Очищение интервала обновления
clearUpdateInterval() {
  if (this.updateInterval) {
    clearInterval(this.updateInterval);
    this.updateInterval = null;
  }
},
    // Устанавливаем интервал обновления для /currency-rates
// Устанавливаем интервал обновления для /currency-rates
setupUpdateInterval() {
  // Если уже установлен интервал, очищаем его
  this.clearUpdateInterval();

  // Устанавливаем новый интервал обновления каждые 5 секунд
  this.updateInterval = setInterval(() => {
    this.loadData();
  }, 5000);
},
    // Обработка клика по строке таблицы
onRowClicked(row) {
  if (row.link) {
    window.open(row.link, '_blank');
  }
},

    // Загрузка данных с сервера
async loadData() {
  try {
    // Очищаем интервал перед загрузкой данных
    this.clearUpdateInterval();

    // Проверяем, выбраны ли обе монеты
    if (this.selectedGivePair && this.selectedReceivePair) {
      // Если обе монеты выбраны, отправляем запрос на /currency-rates
      const response = await api.get('/currency-rates/', {
        params: {
          give_pair_name: this.selectedGivePair,
          receive_pair_name: this.selectedReceivePair,
        },
      });

      // Проверяем, есть ли ошибки в ответе от сервера
      if (response.status === 400) {
        throw new Error('Ошибка в запросе');
      }

      // Сортируем данные по колонке give_count перед присвоением
      this.filteredRows = response.data.sort((a, b) => a.give_count - b.give_count);
    } else {
      // Если не выбраны обе монеты, отправляем запрос на /courses
      const response = await api.get('/courses');

      // Проверяем, есть ли ошибки в ответе от сервера
      if (response.status === 400) {
        throw new Error('Ошибка в запросе');
      }

      // Сортируем данные по колонке give_count перед присвоением
      this.filteredRows = response.data.sort((a, b) => a.give_count - b.give_count);
    }

    // Устанавливаем интервал обновления после успешной загрузки данных
    this.setupUpdateInterval();
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
},






    // Фильтрация данных на основе выбранных монет
    filterData() {
        this.filteredRows = this.rows;
    },
  },
  // Слежение за изменениями выбранных монет
  watch: {
    selectedGivePair() {
      this.loadData(); // При изменении монеты отдачи перезагружаем данные
    },
    selectedReceivePair() {
      this.loadData(); // При изменении монеты получения перезагружаем данные
    },
  },
};
</script>

<style lang="sass">
.selected-row
  background-color: lightblue
.my-courses-table
  /* height or max-height is important */
  max-height: 550px
</style>
