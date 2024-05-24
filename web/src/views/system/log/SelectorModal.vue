<template>
  <a-modal title="选择创建人" v-model:open="openModal" :width="1200" :destroyOnClose="true" style="top: 30px">
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
              <a-form-item name="creator_name" label="姓名" style="max-width: 300px;">
                <a-input v-model:value="formState.name" placeholder="请输入姓名" allowClear></a-input>
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
      <a-card title="用户列表" :bordered="true" :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
      :bodyStyle="{ padding: '0 24px' }">
        <a-table :rowKey="record => record.id" :columns="columns" :data-source="dataSource" :loading="tableLoading"
          :row-selection="rowSelection" @change="handleTableChange" :scroll="{ x: 500, y: 'calc(100vh - 500px)' }" :pagination="pagination">
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
      </a-card>
    </div>
  </a-modal>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, unref } from 'vue';
import type { TableColumnsType } from 'ant-design-vue';
import { getUserList } from '@/api/user'
import type { searchCreatorDataType, creatorTableDataType } from './types'


const openModal = ref<boolean>(false);
const tableLoading = ref(false);

const formState: searchCreatorDataType = reactive({
  name: "",
  available: "true"
});


const columns: TableColumnsType = [
  {
    title: '序号',
    dataIndex: 'index',
    align: 'center',
    width: 80
  },
  {
    title: '姓名',
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
]
const dataSource = ref<creatorTableDataType[]>([]);

const loadingData = () => {
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

  getUserList(params).then(response => {
    const result = response.data;
    dataSource.value = result.data;
    pagination.total = result.total;
    tableLoading.value = false;
  }).catch(error => {
    tableLoading.value = false;
  })
}

const onFinish = () => {
  pagination.current = 1;
  loadingData();
}

const resetFields = () => {
  Object.keys(formState).forEach((key: string) => {
      delete formState[key];
  });
  formState.available = "true"
  pagination.current = 1;
  loadingData();
}

const pagination = reactive({
  current: 1,
  pageSize: 10,
  defaultPageSize: 10,
  showSizeChanger: true,
  total: dataSource.value.length,
  showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条 / 总共 ${total} 条`
})

const handleTableChange = (values: any) => {
  pagination.current = values.current;
  pagination.pageSize = values.pageSize;
  loadingData();
}

const selectedRowKeys = ref<creatorTableDataType['id'][]>([]);
const selectedRowName = ref<creatorTableDataType['name']>('');

const onSelectChange = (selectingRowKeys: creatorTableDataType['id'][], selectingRows: creatorTableDataType[]) => {
  selectedRowKeys.value = selectingRowKeys;
  selectedRowName.value = selectingRows[0].name;
}

const rowSelection = computed(() => {
  return {
      selectedRowKeys: unref(selectedRowKeys),
      onChange: onSelectChange,
      hideDefaultSelections: true,
      type: 'radio'
  }
});

const emit = defineEmits(['event']);

const  handleModalCancel = () => {
  openModal.value = false;
  Object.keys(formState).forEach((key: string) => {
    delete formState[key];
  });
  formState.available = "true"
  pagination.current = 1;
  pagination.pageSize = pagination.defaultPageSize;
  selectedRowKeys.value = [];
  selectedRowName.value = undefined;
}

const handleModalClear = () => {
  handleModalCancel();
  emit('event', selectedRowKeys.value, selectedRowName.value);
}

const handleModalSumbit = () => {
  emit('event', selectedRowKeys.value, selectedRowName.value);
  handleModalCancel();
}


defineExpose({
  openModal,
  selectedRowKeys,
  selectedRowName,
  loadingData
});

</script>

<style lang="scss" scoped>
.table-search-wrapper {
  margin-block-end: 16px;
}
</style>