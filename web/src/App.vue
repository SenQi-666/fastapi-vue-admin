<template>
  <ConfigProvider :locale="zhCN">
    <div id="app">
      <router-view />
    </div>
  </ConfigProvider>
</template>

<script lang="ts" setup>
import { ConfigProvider } from 'ant-design-vue';
import zhCN from 'ant-design-vue/es/locale/zh_CN';
import dayjs from 'dayjs';
import 'dayjs/locale/zh-cn';
import { useRouter } from "vue-router";

dayjs.locale('zh-cn');

// 禁用Promise reject输出控制台
window.addEventListener('unhandledrejection', function browserRejectionHandler(event) {
  event && event.preventDefault()
})

</script>

<style>
 * {
  margin: 0;
  padding: 0;
 }
 body,html {
  margin: 0;
  width: 100%;
  height: 100vh;
}
.ant-page-header {
  padding: 20px 0;
}
.ant-table-thead>tr>th {
  padding: 12px 8px !important;
}
.ant-table-wrapper .ant-table-tbody>tr>td {
  padding: 12px 8px;
}
.ant-modal .ant-modal-header {
  margin-bottom: 20px;
}
</style>