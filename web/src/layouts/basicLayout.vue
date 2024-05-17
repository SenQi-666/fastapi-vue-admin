<template>
  <a-layout>
    <a-layout-header class="header" style="display: flex">
      <div class="left-header">
        <a-button type="link" class="logo-btn">
          <a-image src="/logo.png" :preview="false" :width="28" :height="28" />
          <h1 style="margin-left: 10px;">fastapi-vue-admin</h1>
        </a-button>
      </div>
      <div style="flex: 1 0 0%"></div>
      <div class="right-header">
        <a-dropdown>
          <a class="ant-dropdown-link" @click.prevent>
            <a-avatar :src="store.state.user.basicInfo.avatar" :size="30" ></a-avatar>
            <span style="margin-left: 10px;">{{ store.state.user.basicInfo.username }}</span>
          </a>
          <template #overlay>
            <a-menu @click="dropDownClick">
              <a-menu-item key="1">个人中心</a-menu-item>
              <a-menu-item key="2">退出登录</a-menu-item>
            </a-menu>
          </template>
        </a-dropdown>
      </div>
    </a-layout-header>
    <a-layout>
      <a-layout-sider width="200" :v-model="menuState.collapsed">
        <a-menu :open-keys="menuState.openKeys" v-model:selectedKeys="menuState.selectedKeys" mode="inline" theme="light"
          :style="{ height: '100%', borderRight: 0 }" :items="menuState.menus" @click="handleClick"></a-menu>
      </a-layout-sider>
      <a-layout style="padding: 0 24px 0 24px">
        <a-layout-content :style="{ minHeight: 'calc(100vh - 64px)' }">
          <router-view v-slot="{ Component, route }">
            <keep-alive v-if="route.meta.keepAlive">
              <component :is="Component" />
            </keep-alive>
            <component :is="Component" v-if="!route.meta.keepAlive" />
          </router-view>
        </a-layout-content>
      </a-layout>
    </a-layout>
  </a-layout>
</template>

<script lang="ts" setup>
import { reactive, watch, onMounted } from "vue";
import type { MenuProps } from "ant-design-vue";
import { useRouter, useRoute } from "vue-router";
import storage from 'store'
import store from '@/store'
import * as icons from '@ant-design/icons-vue';
import { h } from 'vue'
import { listToTree } from '@/utils/util'

const router = useRouter();
const route = useRoute();

const menuState = reactive({
  collapsed: false,
  rootSubmenuKeys: [],
  openKeys: [],
  selectedKeys: [route.path],
  menus: []
})

interface MenuItemType {
  key: string,
  title: string,
  label: string,
  icon?: any,
  children?: MenuItemType[]
}

const menus: MenuItemType[] = reactive([])

const dropDownClick: MenuProps["onClick"] = ({ key }) => {
  if (key == 1) {
    router.push('/profile')

  } else {
    storage.remove('Access-Token');
    storage.remove('Refresh-Token');
    store.dispatch('clearUserInfo').then(() => {
      router.push('/login');
    })
  }
};

const handleClick: MenuProps['onClick'] = (menuInfo: any) => {
  menuState.openKeys = [menuInfo.keyPath[0]]
  router.push(menuInfo.key)
}

watch(() => route.path, (newPath) => {
  const routePath = store.state.user.routeList.map(item => item.route_path);
  if (!routePath.includes(newPath)) {
    menuState.openKeys = [];
    menuState.selectedKeys = [];
  }
})

onMounted(() => {
  const menuTree = listToTree(store.state.user.routeList);
  let userMenus = menuGenerator(menuTree);
  menuState.menus = userMenus;
})

let currentParentPath = '';
let findCurrentParentPathStop = false;

const menuGenerator = (routers) => {
  const routerList = [];
  for (const item of routers) {
    if (item.hidden) {
      continue;
    }

    let icon = null;
    if (item.icon) {
      icon = () => h(icons[item.icon])
    }
    
    if (item.route_path == route.path) {
      findCurrentParentPathStop = true;
      menuState.openKeys = [currentParentPath];
    }
    const routerItem: MenuItemType = {
      key: item.route_path,
      title: item.name,
      label: item.name,
      icon: icon,
    }
    if (item.children && item.children.length > 0) {
      if (!findCurrentParentPathStop) {
        currentParentPath = item.route_path;
      }
      menuState.rootSubmenuKeys.push(item.key)
      routerItem.children = menuGenerator(item.children)
    }

    routerList.push(routerItem)
  }
  
  return routerList;
}
</script>

<style lang="scss" scoped>
.left-header {
  display: flex;
  align-items: center;
  height: 100%;
  padding-left: 10px;
}

.right-header {
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.ant-dropdown-trigger {
  height: 50px;
  line-height: 50px;
}

.ant-dropdown-trigger:hover {
  border-radius: 10px;
  background-color: rgba(0, 0, 0, 0.03);
}

.ant-dropdown-link {
  color: rgba(0, 0, 0, 0.65);
}

.logo-btn {
  display: flex;
  align-items: center;
  width: 300px;
}

.header {
  background: rgba(255, 255, 255, 0.6);
}

.ant-btn-link {
  color: rgba(0, 0, 0, 0.65);
}

.ant-btn-link:hover {
  color: rgba(0, 0, 0, 0.65);
}

.ant-layout-header {
  padding-inline: 0;
}
.ant-layout-sider-children .ant-menu-light {
  color: rgba(0, 0, 0, 0.65);
}
:deep(.ant-layout-sider-children .ant-menu-light .ant-menu-item-selected) {
  color: rgba(0, 0, 0, 0.95);
  background-color: rgba(0, 0, 0, 0.04);
}
:deep(.ant-layout-sider-children .ant-menu-light .ant-menu-submenu-selected >.ant-menu-submenu-title) {
  color: rgba(0, 0, 0, 0.95);
}
:deep(.ant-layout-sider-children .ant-menu-light:not(.ant-menu-horizontal) .ant-menu-item:not(.ant-menu-item-selected):active) {
  background-color: rgba(0, 0, 0, 0.15);
}
:deep(.ant-layout-sider-children .ant-menu-light:not(.ant-menu-horizontal) .ant-menu-submenu-title:active) {
  background-color: rgba(0, 0, 0, 0.15);
}
</style>