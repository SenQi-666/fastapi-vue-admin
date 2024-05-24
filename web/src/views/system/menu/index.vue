<template>
  <div>
    <page-header />
    <div class="table-wrapper">
      <a-card title="菜单列表" :bordered="false" :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
        :bodyStyle="{ padding: '0 24px', minHeight: 'calc(100vh - 400px)' }">
        <template #extra>
          <a-button type="primary" :icon="h(PlusOutlined)" @click="modalHandle('create')"  style="margin-right: 10px;">新建</a-button>
          <a-dropdown>
            <template #overlay>
              <a-menu @click="handleMoreClick">
                <a-menu-item key="1"><span style="margin-right: 10px;"><CheckOutlined /></span><span>批量启用</span></a-menu-item>
                <a-menu-item key="2"><span style="margin-right: 10px;"><StopOutlined /></span><span>批量停用</span></a-menu-item>
              </a-menu>
            </template>
            <a-button>更多<DownOutlined />
            </a-button>
          </a-dropdown>
        </template>
        <a-table :rowKey="record => record.id" :columns="columns" :data-source="menuTreeData" :row-selection="rowSelection":loading="tableLoading" 
          :scroll="{ x: 500, y: 'calc(100vh - 350px)' }" :pagination="false" :style="{ minHeight: '700px' }">
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
            <template v-if="column.dataIndex === 'operation'">
              <div style="display: flex; gap: 15px;">
                <a v-on:click="modalHandle('view', record)">查看</a>
                <a v-on:click="modalHandle('update', record)">修改</a>
                <a-popconfirm title="确定删除吗？" ok-text="确定" cancel-text="取消" @confirm="deleteRow(record)">
                  <a>删除</a>
                </a-popconfirm>
              </div>
            </template>
          </template>
        </a-table>
      </a-card>
    </div>

    <div>
      <a-modal v-model:open="openModal" @ok="handleModalSumbit" :width="800" :destroyOnClose="true" :confirmLoading="modalSubmitLoading" style="top: 30px"> 
        <template #title>
            <span>{{ modalTitle === 'create'? '新建菜单' : (modalTitle === 'view' ? '查看菜单' : '修改菜单' ) }}</span>
        </template>
        <div v-if="modalTitle === 'view'">
          <a-spin :spinning="detailStateLoading">
            <a-descriptions :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 1, xs: 1 }" :labelStyle="{ width: '140px' }" bordered>
              <a-descriptions-item label="菜单名称">{{ detailState.name }}</a-descriptions-item>
              <a-descriptions-item label="菜单类型">
                <a-tag :color="detailState.type === 1 ? 'blue' : (detailState.type === 2 ? 'green' : 'orange')">
                  {{ detailState.type === 1 ? '目录' : (detailState.type === 2 ? '功能' : '权限') }}
                </a-tag>
              </a-descriptions-item>
              <a-descriptions-item label="显示排序">{{ detailState.order }}</a-descriptions-item>
              <a-descriptions-item v-if="detailState.type !== 3" label="图标">
                <a-button type="text" size="small" :icon="h(icons[detailState.icon])">{{ detailState.icon }}</a-button>
              </a-descriptions-item>
              <a-descriptions-item label="父级菜单" :span="2">{{ detailState.parent_name }}</a-descriptions-item>
              <a-descriptions-item v-if="detailState.type !== 1" label="权限标识" :span="2">{{ detailState.permission }}</a-descriptions-item>
              <a-descriptions-item v-if="detailState.type !== 3" label="路由名称">{{ detailState.route_name }}</a-descriptions-item>
              <a-descriptions-item v-if="detailState.type !== 3" label="路由路径">{{ detailState.route_path }}</a-descriptions-item>
              <a-descriptions-item v-if="detailState.type === 1" label="重定向">{{ detailState.redirect }}</a-descriptions-item>
              <a-descriptions-item v-if="detailState.type === 2" label="组件地址">{{ detailState.component_path }}</a-descriptions-item>
              <a-descriptions-item v-if="detailState.type !== 3" label="是否缓存">{{ detailState.cache ? '是': '否' }}</a-descriptions-item>
              <a-descriptions-item v-if="detailState.type !== 3" label="是否隐藏">{{ detailState.hidden ? '是': '否' }}</a-descriptions-item>
              <a-descriptions-item label="状态">
                <a-badge :color="detailState.available ? 'green' : 'red'" />{{ detailState.available ? '启用' : '禁用' }}
              </a-descriptions-item>
              <a-descriptions-item label="创建时间">{{ detailState.created_at }}</a-descriptions-item>
              <a-descriptions-item label="修改时间">{{ detailState.updated_at }}</a-descriptions-item>
              <a-descriptions-item label="备注" :span="2">{{ detailState.description }}</a-descriptions-item>
            </a-descriptions>
          </a-spin>
        </div>
        <div v-else-if="modalTitle === 'create'">
          <a-form ref="createForm" :model="createState" v-bind="{ labelCol: { span: 5 }, wrapperCol: { span: 15 } }">
            <a-form-item name="name" label="名称" :rules="[{ required: true, message: '请输入名称' }]">
              <a-input v-model:value="createState.name" placeholder="请输入名称" allowClear></a-input>
            </a-form-item>
            <a-form-item name="type" label="类型" :rules="[{ required: true, message: '请选择类型' }]">
              <a-radio-group v-model:value="createState.type">
                <a-radio :value="1">目录</a-radio>
                <a-radio :value="2">功能</a-radio>
                <a-radio :value="3">权限</a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item
              v-if="createState.type !== 1"
              name="permission"
              label="权限标识"
              :rules="[{ required: createState.type !== 1 ? true : false, message: '请输入权限标识' }]"
            >
              <a-input v-model:value="createState.permission" placeholder="请输入权限标识" allowClear></a-input>
            </a-form-item>
            <a-form-item name="parent_id" label="父级菜单">
              <a-tree-select
                v-model:value="createState.parent_id"
                :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
                :tree-data="menuSelectorTreeData"
                :field-names="{ children: 'children', label: 'name', value: 'id' }"
                tree-node-filter-prop="name"
                style="width: 100%"
                show-search
                allow-clear
              ></a-tree-select>
            </a-form-item>
            <a-form-item name="icon" label="图标">
              <a-popover placement="right" trigger="click">
                <template #content>
                  <div class="icon-clear-btn-wrapper">
                    <a-button :icon="h(ClearOutlined)" @click="iconClearClickHandle" danger>清空</a-button>
                  </div>
                  <a-form-item-rest>
                    <a-input v-model:value="iconSelector.search" placeholder="搜索图标" allowClear />
                  </a-form-item-rest>
                  <a-tabs v-model:activeKey="iconSelector.activeTab" @change="iconTabHandleChange" tabPosition="left" style="margin-top: 20px;">
                    <a-tab-pane v-for="(item, index) in iconDataSource" :key="index" :tab="item.type">
                      <div class="icon-wrapper">
                        <a-flex wrap="wrap" gap="small">
                          <a-button
                            v-for="item in iconData.slice((pagination.current-1) * pagination.pageSize, pagination.current * pagination.pageSize)"
                            :icon="item.icon"
                            @click="iconHandleClick(item)"
                            :class="createState.icon === item.name ? 'active' : ''"
                          />
                        </a-flex>
                      </div>
                    </a-tab-pane>
                  </a-tabs>
                  <div class="icon-pagination-wrapper">
                    <a-pagination
                      size="small"
                      v-model:current="pagination.current"
                      v-model:pageSize="pagination.pageSize"
                      :total="pagination.total"
                      :showTotal="pagination.showTotal"
                      :showQuickJumper="pagination.showQuickJumper"
                      :showSizeChanger="false"
                    />
                  </div>
                </template>
                <a-button :icon="createState.icon ? h(icons[createState.icon]): ''" style="width: 250px;">{{ createState.icon ? createState.icon: '请选择图标' }}</a-button>
              </a-popover>
            </a-form-item>
            <a-form-item name="order" label="排序">
              <a-input-number v-model:value="createState.order" :min="1" />
            </a-form-item>
            <a-form-item name="description" label="备注">
              <a-textarea v-model:value="createState.description" placeholder="请输入备注" :rows="4" allowClear />
            </a-form-item>
            <div v-if="createState.type !== 3">
              <a-divider style="font-weight: 700">以下均为前端配置项</a-divider>
              <a-form-item name="route_name" label="路由名称" :rules="[{ required: createState.type !== 3 ? true : false, message: '请输入路由名称' }]">
                <a-input v-model:value="createState.route_name" placeholder="请输入路由名称" allowClear></a-input>
              </a-form-item>
              <a-form-item name="route_path" label="路由路径" :rules="[{ required: createState.type !== 3 ? true : false, message: '请输入路由路径' }]">
                <a-input v-model:value="createState.route_path" placeholder="请输入路由路径" allowClear></a-input>
              </a-form-item>
              <a-form-item  v-if="createState.type === 1" name="redirect" label="重定向" :rules="[{ required: createState.type === 1 ? true : false, message: '请输入重定向' }]">
                <a-input v-model:value="createState.redirect" placeholder="请输入重定向" allowClear></a-input>
              </a-form-item>
              <a-form-item v-if="createState.type === 2" name="component_path" label="组件地址" :rules="[{ required: createState.type === 2 ? true : false, message: '请输入组件地址' }]">
                <a-input v-model:value="createState.component_path" placeholder="请输入组件地址" allowClear></a-input>
              </a-form-item>
              <a-form-item name="cache" label="是否缓存" :rules="[{ required: createState.type !== 3 ? true : false, message: '请选择缓存状态' }]">
                <a-switch v-model:checked="createState.cache"></a-switch>
              </a-form-item>
              <a-form-item name="hidden" label="是否隐藏" :rules="[{ required: createState.type !== 3 ? true : false, message: '请选择隐藏状态' }]">
                <a-switch v-model:checked="createState.hidden"></a-switch>
              </a-form-item>
            </div>
          </a-form>
        </div>
        <div v-else>
          <a-form ref="updateForm" :model="updateState" v-bind="{ labelCol: { span: 5 }, wrapperCol: { span: 15 } }">
            <a-form-item name="name" label="名称" :rules="[{ required: true, message: '请输入名称' }]">
              <a-input v-model:value="updateState.name" placeholder="请输入名称" allowClear></a-input>
            </a-form-item>
            <a-form-item
              v-if="updateState.type !== 1"
              name="permission"
              label="权限标识"
              :rules="[{ required: updateState.type !== 1 ? true : false, message: '请输入权限标识' }]"
            >
              <a-input v-model:value="updateState.permission" placeholder="请输入权限标识" allowClear></a-input>
            </a-form-item>
            <a-form-item name="parent_id" label="父级菜单">
              <a-tree-select
                v-model:value="updateState.parent_id"
                :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
                :tree-data="menuSelectorTreeData"
                :field-names="{ children: 'children', label: 'name', value: 'id' }"
                tree-node-filter-prop="name"
                style="width: 100%"
                show-search
                allow-clear
              ></a-tree-select>
            </a-form-item>
            <a-form-item name="icon" label="图标">
              <a-popover placement="right" trigger="click">
                <template #content>
                  <div class="icon-clear-btn-wrapper">
                    <a-button :icon="h(ClearOutlined)" @click="iconClearClickHandle" danger>清空</a-button>
                  </div>
                  <a-form-item-rest>
                    <a-input v-model:value="iconSelector.search" placeholder="搜索图标" allowClear />
                  </a-form-item-rest>
                  <a-tabs v-model:activeKey="iconSelector.activeTab" @change="iconTabHandleChange" tabPosition="left" style="margin-top: 20px;">
                    <a-tab-pane v-for="(item, index) in iconDataSource" :key="index" :tab="item.type">
                      <div class="icon-wrapper">
                        <a-flex wrap="wrap" gap="small">
                          <a-button
                            v-for="item in iconData.slice((pagination.current-1) * pagination.pageSize, pagination.current * pagination.pageSize)"
                            :icon="item.icon"
                            @click="iconHandleClick(item)"
                            :class="updateState.icon === item.name ? 'active' : ''"
                          />
                        </a-flex>
                      </div>
                    </a-tab-pane>
                  </a-tabs>
                  <div class="icon-pagination-wrapper">
                    <a-pagination
                      size="small"
                      v-model:current="pagination.current"
                      v-model:pageSize="pagination.pageSize"
                      :total="pagination.total"
                      :showTotal="pagination.showTotal"
                      :showQuickJumper="pagination.showQuickJumper"
                      :showSizeChanger="false"
                    />
                  </div>
                </template>
                <a-button :icon="updateState.icon ? h(icons[updateState.icon]): ''" style="width: 250px;">{{ updateState.icon ? updateState.icon: '请选择图标' }}</a-button>
              </a-popover>
            </a-form-item>
            <a-form-item name="order" label="排序">
              <a-input-number v-model:value="updateState.order" :min="1" />
            </a-form-item>
            <a-form-item name="available" label="状态">
              <a-radio-group v-model:value="updateState.available">
                <a-radio :value="true">启用</a-radio>
                <a-radio :value="false">停用</a-radio>
              </a-radio-group>
            </a-form-item>
            <a-form-item name="description" label="备注">
              <a-textarea v-model:value="updateState.description" placeholder="请输入备注" :rows="4" allowClear />
            </a-form-item>
            <div v-if="updateState.type !== 3">
              <a-divider style="font-weight: 700">以下均为前端配置项</a-divider>
              <a-form-item name="route_name" label="路由名称" :rules="[{ required: updateState.type !== 3 ? true : false, message: '请输入路由名称' }]">
                <a-input v-model:value="updateState.route_name" placeholder="请输入路由名称" allowClear></a-input>
              </a-form-item>
              <a-form-item name="route_path" label="路由路径" :rules="[{ required: updateState.type !== 3 ? true : false, message: '请输入路由路径' }]">
                <a-input v-model:value="updateState.route_path" placeholder="请输入路由路径" allowClear></a-input>
              </a-form-item>
              <a-form-item v-if="updateState.type === 1" name="redirect" label="重定向" :rules="[{ required: updateState.type === 1 ? true : false, message: '请输入重定向' }]">
                <a-input v-model:value="updateState.redirect" placeholder="请输入重定向" allowClear></a-input>
              </a-form-item>
              <a-form-item v-if="updateState.type === 2" name="component_path" label="组件地址" :rules="[{ required: updateState.type === 2 ? true : false, message: '请输入组件地址' }]">
                <a-input v-model:value="updateState.component_path" placeholder="请输入组件地址" allowClear></a-input>
              </a-form-item>
              <a-form-item name="cache" label="是否缓存" :rules="[{ required: updateState.type !== 3 ? true : false, message: '请选择缓存状态' }]">
                <a-switch v-model:checked="updateState.cache"></a-switch>
              </a-form-item>
              <a-form-item name="hidden" label="是否隐藏" :rules="[{ required: updateState.type !== 3 ? true : false, message: '请选择隐藏状态' }]">
                <a-switch v-model:checked="updateState.hidden"></a-switch>
              </a-form-item>
            </div>
          </a-form>
        </div>
      </a-modal>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, unref, h, onMounted, watch } from 'vue';
import PageHeader from '@/components/PageHeader.vue';
import { message, Modal } from 'ant-design-vue';
import { getMenuList, createMenu, updateMenu, deleteMenu, batchEnableMenu, batchDisableMenu } from '@/api/menu'
import { listToTree, cloneDeep, isEmpty } from '@/utils/util';
import type { TableColumnsType, MenuProps } from 'ant-design-vue';
import * as icons from '@ant-design/icons-vue';
import { PlusOutlined, DownOutlined, CheckOutlined, StopOutlined, ClearOutlined } from '@ant-design/icons-vue';
import type { tableDataType } from './types'
import axios from "axios"


const columns: TableColumnsType = [
  {
    title: '菜单名称',
    dataIndex: 'name',
  },
  {
    title: '图标',
    dataIndex: 'icon',
  },
  {
    title: '显示排序',
    dataIndex: 'order',
  },
  {
    title: '菜单类型',
    dataIndex: 'type',
  },
  {
    title: '权限标识',
    dataIndex: 'permission',
  },
  {
    title: '状态',
    dataIndex: 'available',
  },
  {
    title: '备注',
    dataIndex: 'description',
    ellipsis: true,
    width: 200
  },
  {
    title: '操作',
    dataIndex: 'operation',
    fixed: 'right',
    width: 150
  }
];

const menuTreeData = ref<tableDataType[]>([]);
const menuSelectorTreeData = ref<tableDataType[]>([])
const tableLoading = ref(false);
const detailStateLoading = ref(false);
const openModal = ref(false);
const modalTitle = ref('');
const modalSubmitLoading = ref(false);
const createForm = ref();
const updateForm = ref();
const iconSelector = ref({ activeTab: 0, search: undefined });

let iconDataSource = [];
const iconData = ref([]);

const createState: tableDataType = reactive({
  name: '',
  type: 1,
  icon: '',
  order: 1,
  permission: '',
  route_name: '',
  route_path: '',
  component_path: '',
  redirect: '',
  parent_id: undefined,
  cache: true,
  hidden: false,
  description: ''
})
const updateState: tableDataType = reactive({
  id: undefined,
  name: '',
  type: 1,
  icon: '',
  order: 1,
  permission: '',
  route_name: '',
  route_path: '',
  component_path: '',
  redirect: '',
  parent_id: undefined,
  cache: true,
  hidden: false,
  available: true,
  description: ''
})
const detailState = ref<tableDataType>({});

const pagination = reactive({
  current: 1,
  pageSize: 70,
  showQuickJumper: true,
  showSizeChanger: false,
  total: 0,
  showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条 / 总共 ${total} 条`
})

const loadingData = () => {
  tableLoading.value = true;

  getMenuList().then(response => {
    const result = response.data;
    menuSelectorTreeData.value = listToTree(result.data.filter((item) => item.type !== 3));
    menuTreeData.value = listToTree(result.data);
    tableLoading.value = false;
  }).catch(error => {
    console.log(error);
    tableLoading.value = false;
  })
}

onMounted(() => {
  loadingData();
  axios.get('/icons.json').then(response => {
    response.data.forEach((item, index) => {
      iconDataSource.push({ type: item.type, icons: [] });
      item.icons.forEach(icon => {
        iconDataSource[index].icons.push({ name: icon, icon: h(icons[icon]) })
      })
    });
    iconData.value = iconDataSource[iconSelector.value.activeTab].icons;
    pagination.total = iconData.value.length;
    
  }).catch(error => {
    console.log(error)
  })
});

const selectedRowKeys = ref<tableDataType['id'][]>([]);

const onSelectChange = (selectingRowKeys: tableDataType['id'][]) => {
  console.log(selectingRowKeys);
  
  selectedRowKeys.value = selectingRowKeys;
}

const rowSelection = computed(() => {
  return {
    selectedRowKeys: unref(selectedRowKeys),
    checkStrictly: false,
    onChange: onSelectChange
  }
});

const modalHandle = (modalType: string, record?: tableDataType) => {
  modalTitle.value = modalType;
  openModal.value = true;

  if (modalType === 'view' && record !== undefined) {
    detailStateLoading.value = true;
    detailState.value = record;
    detailStateLoading.value = false;

  } else if (modalType === 'update' && record !== undefined) {
    Object.keys(updateState).forEach(key => {
      updateState[key] = record[key];
    })
  }
  iconSelector.value = {
    activeTab: 0,
    search: undefined
  }
}

const deleteRow = (row: tableDataType) => {
  deleteMenu({ id: row.id }).then(response => {
    message.success(response.data.message);
    loadingData();

  }).catch(error => {
    console.log(error)
  })
}


const handleMoreClick: MenuProps['onClick'] = e => {
  if (!selectedRowKeys.value || !(selectedRowKeys.value.length > 0) ) {
    message.warning('请先勾选数据');
    return;
  }

  Modal.confirm({
    title: '提示',
    content: e.key == 1 ? '是否确定启用选择项？' : '是否确定停用选择项？',
    onOk() {
      const body = { ids: selectedRowKeys.value };
      const batchApi = e.key == 1 ? batchEnableMenu(body) : batchDisableMenu(body);
      batchApi.then(response => {
        message.success(response.data.message);
        selectedRowKeys.value = [];
        loadingData();
      }).catch(error => {
        console.log(error);
      })
    }
  });
}

const handleModalSumbit = () => {
  modalSubmitLoading.value = true;
  if (modalTitle.value === 'view') {
    modalSubmitLoading.value = false;
    openModal.value = false;

  } else if (modalTitle.value === 'create') {
    createForm.value.validate().then(() => {
      const createBody = cloneDeep(createState);
      Object.keys(createBody).forEach(key => {
        if (isEmpty(createBody[key])) {
          delete createBody[key];
        }
      })

      createMenu(createBody).then(response => {
        modalSubmitLoading.value = false;
        openModal.value = false;
        Object.keys(createState).forEach(key => delete createState[key])
        createState.type = 1;
        createState.order = 1;
        createState.cache = true;
        createState.hidden = false;
        message.success(response.data.message);
        loadingData();

      }).catch(error => {
        modalSubmitLoading.value = false;
        console.log(error)
      })

    }).catch(error => {
      modalSubmitLoading.value = false;
      console.log(error)
    })

  } else {
    updateForm.value.validate().then(() => {
      updateMenu(updateState).then(response => {
        modalSubmitLoading.value = false;
        openModal.value = false;
        message.success(response.data.message);
        loadingData();

      }).catch(error => {
        modalSubmitLoading.value = false;
        console.log(error)
      })

    }).catch(error => {
      modalSubmitLoading.value = false;
      console.log(error)
    })
  }
}

watch(() => createState.type, (newType) => {
  Object.keys(createState).forEach(key => delete createState[key])
  createState.type = newType;
  createState.order = 1;
  createState.cache = true;
  createState.hidden = false;
})

watch(() => iconSelector.value.search, (newSearchField) => iconSearch(newSearchField));

const iconSearch = (field) => {
  let activeIcons = iconDataSource[iconSelector.value.activeTab].icons;
  if (field) {
    activeIcons = activeIcons.filter(item => item.name.toLowerCase().includes(field.toLowerCase()));
  }

  iconData.value = activeIcons;
  pagination.current = 1;
  pagination.total = iconData.value.length;
}

const iconTabHandleChange = () => iconSearch(iconSelector.value.search);

const iconHandleClick = (values) => {
  if (modalTitle.value === 'create') {
    createState.icon = values.name;
  } else if (modalTitle.value === 'update') {
    updateState.icon = values.name;
  }
}

const iconClearClickHandle = () => {
  if (modalTitle.value === 'create') {
    createState.icon = '';
  } else if (modalTitle.value === 'update') {
    updateState.icon = '';
  }
}

</script>

<style lang="scss" scoped>
.table-search-wrapper {
  margin-block-end: 16px;
}
.icon-wrapper {
  min-width: 420px;
  max-width: 420px;
  min-height: 270px;
  max-height: 270px;
}
.icon-clear-btn-wrapper {
  margin-bottom: 10px;
  display: flex;
  justify-content: flex-end;
}
.icon-pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.active {
  color: #4096ff;
  border-color: #4096ff;
}
</style>