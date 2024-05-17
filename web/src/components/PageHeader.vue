<template>
  <div class="page-header">
    <div class="page-header-breadcrumb">
      <a-breadcrumb :routes="routes">
        <template #itemRender="{ route, routes }">
          <span v-if="routes.indexOf(route) === routes.length - 1">{{ route.breadcrumbName }}</span>
          <router-link v-else :to="route.path">{{ route.breadcrumbName }}</router-link>
        </template>
      </a-breadcrumb>
    </div>
    <div class="page-header-title">
      {{ title }}
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRoute } from "vue-router";

const title = ref<string | undefined>('');

interface Route {
  path: string,
  breadcrumbName: string | undefined
}
const routes = ref<Route[]>([])
const route = useRoute();

const getBreadcrumb = () => {
  title.value = route.meta.title?.toString();
  routes.value.splice(0, routes.value.length);
  if (route.matched.length > 2) {
    route.matched.forEach((item, index) => {
      if (index !== 0) {
        routes.value.push({ path: item.path, breadcrumbName: item.meta.title?.toString() })
      }
    })
  }
}

onMounted(() => getBreadcrumb());
</script>

<style lang="scss" scoped>
.page-header {
  padding: 10px 0;
}
.page-header-title {
  font-size: 20px;
  font-weight: 600;
  padding: 10px 0;
}
</style>