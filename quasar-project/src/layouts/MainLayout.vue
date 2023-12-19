<template>
  <q-layout view="lHh Lpr lFf">


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
    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >

      <q-list>
    <give-pairs-component></give-pairs-component>
    <receive-pairs-component></receive-pairs-component>
      </q-list>
    </q-drawer>

    <q-page-container>
      <CoursesComponent>

      </CoursesComponent>
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import new_table from "src/components/new_table.vue";
import CoursesComponent from 'src/components/CoursesComponent.vue';
import GivePairsComponent from 'src/components/GivePairsComponent.vue';
import ReceivePairsComponent from 'src/components/ReceivePairsComponent.vue';
import api from 'src/services/api_backend.js';



export default defineComponent({
  name: 'MainLayout',

  components: {
    CoursesComponent,
    GivePairsComponent,
    ReceivePairsComponent,



  },

  setup () {
    const leftDrawerOpen = ref(false)
    const totalValues = ref(0);
    // Запрос к API при монтировании компонента
    onMounted(async () => {
      try {
        const response = await api.get('/courses');
        const data = response.data;

        // Подсчитываем общее количество значений в массиве
        totalValues.value = Array.isArray(data) ? data.length : 0;
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
      }
    });
    return {
      leftDrawerOpen,
            totalValues,

      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
})
</script>
