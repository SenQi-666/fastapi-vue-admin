<template>
  <a-modal title="选择" v-model:open="openModal" :width="1200" :destroyOnClose="true" style="top: 30px">
    <template #footer>
      <a-button @click="handleModalCancel">取消</a-button>
      <a-button @click="handleModalClear">清空</a-button>
      <a-button type="primary" @click="handleModalSumbit">确定</a-button>
    </template>
    <div class="table-search-wrapper">
      <a-card :bordered="true">
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

    <div>
      <a-table :rowKey="record => record.id" :columns="columns" :data-source="dataSource" :row-selection="rowSelection" :loading="tableLoading"
        @change="handleTableChange" :scroll="{ x: 500, y: 330 }" :pagination="pagination" :style="{ minHeight: '330px' }">
        <template v-slot:bodyCell="{ column, record, index }">
          <template v-if="column.dataIndex === 'index'">
            <span>{{ index + 1 }}</span>
          </template>
          <template v-if="column.dataIndex === 'available'">
            <span><a-badge :color="record.available ? 'green' : 'red'" /> {{ record.available ? '启用' : '禁用' }}
            </span>
          </template>
        </template>
      </a-table>
    </div>
  </a-modal>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, unref } from 'vue';
import { Table } from 'ant-design-vue';
import { getPositionOptions } from '@/api/position'
import { getRoleOptions } from '@/api/role'
import type { TableColumnsType } from 'ant-design-vue';
import type { searchSelectDataType, roleSelectorType, positionSelectorType } from './types';

const subject = ref('');
const openModal = ref(false);
const tableLoading = ref(false);
const dataSource = ref<roleSelectorType[] | positionSelectorType[]>([]);
const selectedRowKeys = ref<roleSelectorType['id'][] | positionSelectorType['id'][]>([]);
const selectedRowItemNames = ref<roleSelectorType['name'][] | positionSelectorType['name'][]>([]);
const formState: searchSelectDataType = reactive({
  name: "",
  available: "true"
});

const pagination = reactive({
  current: 1,
  pageSize: 20,
  defaultPageSize: 20,
  showSizeChanger: true,
  total: dataSource.value.length,
  showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条 / 总共 ${total} 条`
})

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
  }
];

const loadingData = () => {
  if (!subject.value) {
    return;
  }

  tableLoading.value = true;
  dataSource.value = [];

  let params = {};
  if (formState.name) {
    params['name'] = formState.name
  }
  if (formState.available) {
    params['available'] = formState.available == "true" ? true : false;
  }
  params['page'] = pagination.current
  params['page_size'] = pagination.pageSize

  const requestApi = subject.value == 'role' ? getRoleOptions(params) : getPositionOptions(params);
  requestApi.then(response => {
    const result = response.data;
    dataSource.value = result.data;
    pagination.total = result.total;
    tableLoading.value = false;
  }).catch(error => {
    console.log(error);
    tableLoading.value = false;
  })
}

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

const onSelectChange = (
  selectingRowKeys: roleSelectorType['id'][] | positionSelectorType['id'][],
  selectingRows: roleSelectorType[] | positionSelectorType[],
) => {
  selectedRowKeys.value = selectingRowKeys;
  selectedRowItemNames.value = selectingRows.map(row => row.name);
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

const emit = defineEmits(['event']);

const handleModalSumbit = () => {
  emit('event', subject.value, selectedRowKeys.value, selectedRowItemNames.value);
  handleModalCancel();
}

const handleModalClear = () => {
  handleModalCancel();
  emit('event', subject.value, selectedRowKeys.value, selectedRowItemNames.value);
}

const handleModalCancel = () => {
  openModal.value = false;
  Object.keys(formState).forEach((key: string) => {
    delete formState[key];
  });
  formState.available = "true"
  pagination.current = 1;
  pagination.pageSize = pagination.defaultPageSize;
  selectedRowKeys.value = [];
  selectedRowItemNames.value = [];
}

defineExpose({
  subject,
  openModal,
  selectedRowKeys,
  selectedRowItemNames,
  loadingData
});

</script>

<style lang="scss" scoped>
.table-search-wrapper {
  margin-block-end: 16px;
}
</style>