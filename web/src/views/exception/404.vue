<template>
  <a-result status="404" title="404" sub-title="Sorry, the page you visited does not exist.">
    <template #extra>
      <a-button type="primary" @click="toHome">返回首页</a-button>
    </template>
  </a-result>
</template>

<script lang="ts", setup>
import { useRouter } from "vue-router";

const router = useRouter();
const toHome = () => {
  router.push('/')
}
</script>

<style lang="scss" scoped>

</style>
