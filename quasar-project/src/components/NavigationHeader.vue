<!-- Header.vue -->
<template>
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
</template>

<script>
export default {
  name: 'AppHeader',
};
</script>

<style scoped>
/* Стили для заголовка могут быть добавлены здесь */
</style>
