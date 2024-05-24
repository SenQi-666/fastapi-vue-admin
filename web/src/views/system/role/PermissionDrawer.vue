<template>
  <a-drawer
    v-model:open="openDrawer"
    :destroyOnClose="true"
    title="授权"
    placement="right"
    :width="1500"
    :bodyStyle="{ padding: 'none' }"
  >
    <template #extra>
      <a-button type="primary" @click="handleDrawerSave" :loading="drawerSaving">保存</a-button>
    </template>

    <div style="display: flex;">
      <div style="min-width: 300px;">
        <div style="display: flex; gap: 10px; ">
          <div style="width: 10px; background-color: #1677ff;"></div>
          <div>
            <span style="font-size: 16px;">数据授权</span>
            <a-tooltip placement="right">
              <template #title>
                <span>授权用户可操作的数据范围</span>
              </template>
              <QuestionCircleOutlined style="margin-left: 5px;" />
            </a-tooltip>
          </div>
        </div>

        <a-select v-model:value="permissionState.data_scope" style="width: 80%; margin-top: 15px;">
          <a-select-option :value="1">仅本人数据权限</a-select-option>
          <a-select-option :value="2">本部门数据权限</a-select-option>
          <a-select-option :value="3">本部门及以下数据权限</a-select-option>
          <a-select-option :value="4">全部数据权限</a-select-option>
          <a-select-option :value="5">自定义数据权限</a-select-option>
        </a-select>

        <a-tree
          v-if="permissionState.data_scope === 5 && deptTreeData.length"
          :checkedKeys="permissionState.dept_ids"
          :rowKey="record => record.id"
          :tree-data="deptTreeData"
          :defaultExpandAll="true"
          :field-names="{ children: 'children', title: 'name', key: 'id' }"
          @check="deptTreeCheck"
          checkable
          checkStrictly
          style="margin-top: 15px;"
        />
      </div>

      <a-divider type="vertical" style="height: 80vh;" />

      <div>
        <div style="display: flex; gap: 10px;">
          <div style="width: 10px; background-color: #1677ff;"></div>
          <div>
            <span style="font-size: 16px;">菜单授权</span>
            <a-tooltip placement="right">
              <template #title>
                <span>授权用户在菜单中可操作的范围</span>
              </template>
              <QuestionCircleOutlined style="margin-left: 5px;" />
            </a-tooltip>
          </div>
        </div>

        <div style="margin-top: 15px;">
          <a-table :rowKey="record => record.id" :columns="menuColumns" :data-source="menuTreeData" :row-selection="menuRowSelection":loading="tableLoading" 
            :scroll="{ x: 500, y: 'calc(100vh - 270px)' }" :pagination="false" :style="{ minHeight: '700px'  }">
            <template v-slot:bodyCell="{ column, record, index }">
              <template v-if="column.dataIndex === 'type'">
                <a-tag :color="record.type === 1 ? 'blue' : (record.type === 2 ? 'green' : 'orange')">
                  {{ record.type === 1 ? '目录' : (record.type === 2 ? '功能' : '权限') }}
                </a-tag>
              </template>
              <template v-if="column.dataIndex === 'available'">
                <span><a-badge :color="record.available ? 'green' : 'red'" /> {{ record.available ? '启用' : '禁用' }}
                </span>
              </template>
            </template>
          </a-table>
        </div>
      </div>
    </div>

    <template #footer>
      <div style="height: 50px;"></div>
    </template>
  </a-drawer>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';
import { getRolePermission, setPermission } from '@/api/role';
import { getDeptOptions } from '@/api/dept';
import { getMenuOptions } from '@/api/menu';
import { listToTree } from '@/utils/util';
import { message } from 'ant-design-vue';
import { QuestionCircleOutlined } from '@ant-design/icons-vue';
import type { tableDataType, permissionDataType, permissionDeptType, permissionMenuType } from './types'
import type { TableColumnsType } from 'ant-design-vue';

const openDrawer = ref(false);
const permissionState = ref<permissionDataType>();

const deptTreeData = ref<permissionDeptType[]>([]);
const menuTreeData = ref<permissionMenuType[]>([]);
const tableLoading = ref(false);
const drawerSaving = ref(false);

const menuColumns: TableColumnsType = [
  {
    title: '菜单名称',
    dataIndex: 'name'
  },
  {
    title: '菜单类型',
    dataIndex: 'type',
    width: 100
  },
  {
    title: '权限标识',
    dataIndex: 'permission',
  },
  {
    title: '状态',
    dataIndex: 'available',
    width: 100
  },
  {
    title: '备注',
    dataIndex: 'description',
    ellipsis: true,
    width: 400
  }
];

const init = (record: tableDataType) => {
  if (!record) {
    message.error()
    return
  }

  openDrawer.value = true;
  tableLoading.value = true;

  deptTreeData.value = [];
  menuTreeData.value = [];
  permissionState.value = {
    role_ids: record ? [ record.id ] : [],
    menu_ids: [],
    data_scope: record ? record.data_scope : 1,
    dept_ids: []
  }

  getDeptOptions().then(response => {
    const result = response.data;
    deptTreeData.value = listToTree(result.data);
  }).catch(error => {
    console.log(error);
  })

  getMenuOptions().then(response => {
    const result = response.data;
    menuTreeData.value = listToTree(result.data);
    tableLoading.value = false;
  }).catch(error => {
    console.log(error);
    tableLoading.value = false;
  })

  if (record) {
    getRolePermission({ id: record.id }).then(response => {
      const result = response.data;
      permissionState.value.menu_ids = result.data.menus.map(menu => menu.id);
      permissionState.value.dept_ids = result.data.depts.map(dept => dept.id);
    }).catch(error => {
      console.log(error);
    })
  }
}

const deptTreeCheck = (checkedKeys) => permissionState.value.dept_ids = checkedKeys.checked;

const emit = defineEmits(['event']);


const handleDrawerSave = () => {
  openDrawer.value = true;
  drawerSaving.value = true;

  setPermission(permissionState.value).then(response => {
    message.success(response.data.message);
    drawerSaving.value = false;
    openDrawer.value = false;
    emit('event');
  }).catch(error => {
    console.log(error);
    drawerSaving.value = false;
  })
}

const onMenuSelectChange = (selectingRowKeys: permissionMenuType['id'][]) => {
  permissionState.value.menu_ids = selectingRowKeys;
}

const menuRowSelection = computed(() => {
  return {
    selectedRowKeys: permissionState.value.menu_ids,
    checkStrictly: false,
    onChange: onMenuSelectChange
  }
});

defineExpose({
  init,
  permissionState
});

</script>

<style lang="scss" scoped>

</style>