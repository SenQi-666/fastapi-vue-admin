<template>
  <div>
    <page-header />

    <div class="table-search-wrapper">
      <a-card :bordered="false">
        <a-form :model="formState" @finish="onFinish">
          <a-row>
            <a-col flex="0 1 400px">
              <a-form-item name="name" label="名称" style="max-width: 300px;">
                <a-input v-model:value="formState.name" placeholder="请输入名称" allowClear></a-input>
              </a-form-item>
            </a-col>
            <a-col flex="0 1 400px">
              <a-form-item name="available" label="状态" style="max-width: 300px;">
                <a-select v-model:value="formState.available" placeholder="全部" allowClear>
                  <a-select-option value="true">启用</a-select-option>
                  <a-select-option value="false">停用</a-select-option>
                </a-select>
              </a-form-item>
            </a-col>
          </a-row>
          <a-row>
            <a-col>
              <a-button type="primary" html-type="submit" :loading="tableLoading">查询</a-button>
              <a-button style="margin: 0 8px" @click="resetFields">重置</a-button>
            </a-col>
          </a-row>
        </a-form>
      </a-card>
    </div>

    <div class="table-wrapper">
      <a-card title="角色列表" :bordered="false" :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
        :bodyStyle="{ padding: '0 24px', minHeight: 'calc(100vh - 400px)' }">
        <template #extra>
          <a-button type="primary" :icon="h(PlusOutlined)" @click="modalHandle('create')" style="margin-right: 10px;">新建</a-button>
          <a-dropdown>
            <template #overlay>
              <a-menu @click="handleMoreClick">
                <a-menu-item key="1"><span style="margin-right: 10px;"><CheckOutlined /></span><span>批量启用</span></a-menu-item>
                <a-menu-item key="2"><span style="margin-right: 10px;"><StopOutlined /></span><span>批量停用</span></a-menu-item>
              </a-menu>
            </template>
            <a-button>更多<DownOutlined /></a-button>
          </a-dropdown>
        </template>
        <a-table :rowKey="record => record.id" :columns="columns" :data-source="dataSource" :row-selection="rowSelection" :loading="tableLoading"
          @change="handleTableChange" :scroll="{ x: 500, y: 'calc(100vh - 500px)' }" :pagination="pagination" :style="{ minHeight: '500px' }">
          <template v-slot:bodyCell="{ column, record, index }">
            <template v-if="column.dataIndex === 'index'">
              <span>{{ index + 1 }}</span>
            </template>
            <template v-if="column.dataIndex === 'available'">
              <span><a-badge :color="record.available ? 'green' : 'red'" /> {{ record.available ? '启用' :
                '禁用' }}
              </span>
            </template>
            <template v-if="column.dataIndex === 'operation'">
              <div style="display: flex; gap: 15px;">
                <a v-on:click="modalHandle('view', index)">查看</a>
                <a v-on:click="modalHandle('update', index)">修改</a>
                <a v-on:click="permissionDrawer.init(record)">授权</a>
                <a-popconfirm title="确定删除吗？" ok-text="确定" cancel-text="取消" @confirm="deleteRow(record)">
                  <a>删除</a>
                </a-popconfirm>
              </div>
            </template>
          </template>
        </a-table>
      </a-card>
    </div>

    <a-modal v-model:open="openModal" @ok="handleModalSumbit" :width="800" :destroyOnClose="true" :confirmLoading="modalSubmitLoading" style="top: 30px">
      <template #title>
          <span>{{ modalTitle === 'create'? '新建岗位' : (modalTitle === 'view' ? '查看岗位' : '修改岗位' ) }}</span>
      </template>
      <div v-if="modalTitle === 'view'">
        <a-spin :spinning="detailStateLoading">
          <a-descriptions :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 1, xs: 1 }" :labelStyle="{ width: '140px' }" bordered>
            <a-descriptions-item label="序号">{{ detailState.index + 1 }}</a-descriptions-item>
            <a-descriptions-item label="名称">{{ detailState.name }}</a-descriptions-item>
            <a-descriptions-item label="排序">{{ detailState.order }}</a-descriptions-item>
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
          <a-form-item name="order" label="排序">
            <a-input-number v-model:value="createState.order" :min="1" />
          </a-form-item>
          <a-form-item name="description" label="备注">
            <a-textarea v-model:value="createState.description" placeholder="请输入备注" :rows="4" allowClear />
          </a-form-item>
        </a-form>
      </div>
      <div v-else>
        <a-form ref="updateForm" :model="updateState" v-bind="{ labelCol: { span: 5 }, wrapperCol: { span: 15 } }">
          <a-form-item name="name" label="名称" :rules="[{ required: true, message: '请输入名称' }]">
            <a-input v-model:value="updateState.name" placeholder="请输入名称" allowClear></a-input>
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
        </a-form>
      </div>
    </a-modal>
  
    <PermissionDrawer ref="permissionDrawer" @event="handlePermissionDrawerEvent" />
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, unref, onMounted, h } from 'vue';
import PageHeader from '@/components/PageHeader.vue';
import { Table, message, Modal } from 'ant-design-vue';
import { getRoleList, createRole, updateRole, deleteRole, batchEnableRole, batchDisableRole } from '@/api/role'
import { cloneDeep, isEmpty } from '@/utils/util';
import { PlusOutlined, DownOutlined, CheckOutlined, StopOutlined } from '@ant-design/icons-vue';
import type { TableColumnsType, MenuProps } from 'ant-design-vue';
import type { searchDataType, tableDataType } from './types'
import PermissionDrawer from './PermissionDrawer.vue'

const createForm = ref();
const updateForm = ref();
const tableLoading = ref(false);
const openModal = ref(false);
const permissionDrawer = ref();
const modalTitle = ref('');
const modalSubmitLoading = ref(false);
const detailStateLoading = ref(false);
const dataSource = ref<tableDataType[]>([]);
const selectedRowKeys = ref<tableDataType['id'][]>([]);
const formState: searchDataType = reactive({
  name: "",
  available: "true"
});
const pagination = reactive({
  current: 1,
  pageSize: 10,
  defaultPageSize: 10,
  showSizeChanger: true,
  total: dataSource.value.length,
  showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条 / 总共 ${total} 条`
})
const createState: tableDataType = reactive({
  name: '',
  order: 1,
  description: ''
})
const updateState: tableDataType = reactive({
  id: undefined,
  name: '',
  order: 1,
  available: true,
  description: ''
})
const detailState = ref<tableDataType>({})

const columns: TableColumnsType = [
  {
    title: '序号',
    dataIndex: 'index',
    align: 'center',
    width: 80
  },
  {
    title: '名称',
    dataIndex: 'name',
    align: 'center'
  },
  {
    title: '排序',
    dataIndex: 'order',
    align: 'center'
  },
  {
    title: '状态',
    dataIndex: 'available',
    align: 'center'
  },
  {
    title: '备注',
    dataIndex: 'description',
    align: 'center',
    ellipsis: true,
    width: 500
  },
  {
    title: '操作',
    dataIndex: 'operation',
    align: 'center',
    fixed: 'right',
    width: 180
  }
];


const loadingData = () => {
  tableLoading.value = true;

  let params = {};
  if (formState.name) {
    params['name'] = formState.name
  }
  if (formState.available) {
    params['available'] = formState.available == "true" ? true : false;
  }
  params['page'] = pagination.current
  params['page_size'] = pagination.pageSize

  getRoleList(params).then(response => {
    const result = response.data;
    dataSource.value = result.data;
    pagination.total = result.total;
    tableLoading.value = false;
  }).catch(error => {
    console.log(error);
    tableLoading.value = false;
  })
}

onMounted(() => loadingData());

const onFinish = () => {
  pagination.current = 1;
  loadingData();
};

const resetFields = () => {
  Object.keys(formState).forEach((key: string) => {
    delete formState[key];
  });
  pagination.current = 1;
  formState.available = "true"
  loadingData();
}


const handleTableChange = (values: any) => {
  pagination.current = values.current;
  pagination.pageSize = values.pageSize;
  loadingData();
}


const onSelectChange = (selectingRowKeys: tableDataType['id'][]) => {
  selectedRowKeys.value = selectingRowKeys;
}

const rowSelection = computed(() => {
  return {
    selectedRowKeys: unref(selectedRowKeys),
    onChange: onSelectChange,
    hideDefaultSelections: true,
    selections: [
      Table.SELECTION_ALL,
      Table.SELECTION_INVERT,
      Table.SELECTION_NONE
    ]
  }
});

const modalHandle = (modalType: string, index?: number) => {
  modalTitle.value = modalType;
  openModal.value = true;

  if (modalType === 'view' && index !== undefined) {
    detailStateLoading.value = true;

    detailState.value = dataSource.value[index];
    detailState.value.index = index;

    detailStateLoading.value = false;

  } else if (modalType === 'update' && index !== undefined) {
    const selected = dataSource.value[index];
    Object.keys(updateState).forEach(key => {
      updateState[key] = selected[key];
    })
  } else if (modalType === 'permission' && index !== undefined) {

  }
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

      createRole(createBody).then(response => {
        modalSubmitLoading.value = false;
        openModal.value = false;
        Object.keys(createState).forEach(key => delete createState[key]);
        createState.order = 1;
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
      updateRole(updateState).then(response => {
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

const deleteRow = (row: tableDataType) => {
  deleteRole({ id: row.id }).then(response => {
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
      const batchApi = e.key == 1 ? batchEnableRole(body) : batchDisableRole(body);
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

const handlePermissionDrawerEvent = () => loadingData();
</script>

<style lang="scss" scoped>
.table-search-wrapper {
  margin-block-end: 16px;
}
</style>