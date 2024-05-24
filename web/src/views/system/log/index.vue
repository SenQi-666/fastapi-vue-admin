<template>
  <div>
    <page-header />
    <div class="table-search-wrapper">
      <a-card :bordered="false">
        <a-form :model="formState" @finish="onFinish">
          <a-row>
            <a-col flex="0 1 500px">
              <a-form-item name="request_path" label="请求路径" style="max-width: 300px;">
                <a-input v-model:value="formState.request_path" placeholder="请输入请求路径" allowClear></a-input>
              </a-form-item>
            </a-col>
            <a-col flex="0 1 500px">
              <a-form-item name="creator" label="创建人" style="max-width: 300px;">
                <a-select v-model:value="formState.creator_name" placeholder="请选择创建人" :open="false" @click="selectModalHandle">
                  <template #suffixIcon>
                    <search-outlined />
                  </template>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col flex="0 1 500px">
              <a-form-item name="date-range-picker" label="创建日期" style="max-width: 350px;">
                <a-range-picker v-model:value="formState.date_range" value-format="YYYY-MM-DD" />
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
      <a-card title="日志列表" :bordered="false" :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
        :bodyStyle="{ padding: '0 24px', minHeight: 'calc(100vh - 400px)' }">
        <a-table :rowKey="record => record.id" :columns="columns" :data-source="dataSource" :loading="tableLoading"
          @change="handleTableChange" :scroll="{ x: 500, y: 'calc(100vh - 500px)' }" :pagination="pagination" :style="{ minHeight: '500px' }">
          <template v-slot:bodyCell="{ column, record, index }">
            <template v-if="column.dataIndex === 'index'">
              <span>{{ index + 1 }}</span>
            </template>
            <template v-if="column.dataIndex === 'response_code'">
              <a-tag :color="record.response_code === 200 ? 'green' : 'red'">{{ record.response_code }}</a-tag>
            </template>
            <template v-if="column.dataIndex === 'operation'">
              <a v-on:click="modalHandle(index)">查看</a>
            </template>
          </template>
        </a-table>
      </a-card>
    </div>

    <a-modal v-model:open="openModal" @ok="openModal = false" :width="800" :destroyOnClose="true" style="top: 30px">
      <template #title>
        <span>查看日志</span>
      </template>
      <a-spin :spinning="detailStateLoading">
        <a-descriptions :column="{ xxl: 2, xl: 2, lg: 2, md: 2, sm: 1, xs: 1 }" :labelStyle="{ width: '140px' }" bordered>
          <a-descriptions-item label="序号">{{ detailState.index + 1 }}</a-descriptions-item>
          <a-descriptions-item label="请求地址" :span="2">{{ detailState.request_path }}</a-descriptions-item>
          <a-descriptions-item label="请求方法">{{ detailState.request_method }}</a-descriptions-item>
          <a-descriptions-item label="操作人">{{ detailState.creator ? detailState.creator.name : undefined }}</a-descriptions-item>
          <a-descriptions-item label="IP地址">{{ detailState.request_ip }}</a-descriptions-item>
          <a-descriptions-item label="浏览器">{{ detailState.request_browser }}</a-descriptions-item>
          <a-descriptions-item label="系统">{{ detailState.request_os }}</a-descriptions-item>
          <a-descriptions-item label="响应码">
            <a-tag :color="detailState.response_code === 200 ? 'green' : 'red'">{{ detailState.response_code }}</a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="请求体" :span="2">{{ detailState.request_payload }}</a-descriptions-item>
          <a-descriptions-item label="返回信息" :span="2">{{ detailState.response_json }}</a-descriptions-item>
          <a-descriptions-item label="创建时间">{{ detailState.created_at }}</a-descriptions-item>
          <a-descriptions-item label="修改时间">{{ detailState.updated_at }}</a-descriptions-item>
        </a-descriptions>
      </a-spin>
    </a-modal>

    <SelectorModal ref="selectorModal" @event="handleSelectorModalEvent" />
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted } from 'vue';
import PageHeader from '@/components/PageHeader.vue';
import type { TableColumnsType } from 'ant-design-vue';
import { getLogList } from '@/api/log'
import { SearchOutlined } from '@ant-design/icons-vue';
import type { searchDataType, tableDataType, creatorTableDataType } from './types'
import SelectorModal from './SelectorModal.vue'

const tableLoading = ref(false);
const dataSource = ref<tableDataType[]>([]);
const detailStateLoading = ref(false);
const openModal = ref(false);
const selectorModal = ref();
const formState: searchDataType = reactive({});
const detailState = ref<tableDataType>()
const pagination = reactive({
  current: 1,
  pageSize: 10,
  defaultPageSize: 10,
  showSizeChanger: true,
  total: dataSource.value.length,
  showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条 / 总共 ${total} 条`
})

const columns: TableColumnsType = [
  {
    title: '序号',
    dataIndex: 'index',
    width: 80
  },
  {
    title: '请求地址',
    dataIndex: 'request_path',
    width: 300
  },
  {
    title: '请求方法',
    dataIndex: 'request_method',
    width: 80
  },
  {
    title: 'IP地址',
    dataIndex: 'request_ip',
    width: 100
  },
  {
    title: '浏览器',
    dataIndex: 'request_browser',
    width: 200
  },
  {
    title: '系统',
    dataIndex: 'request_os',
    width: 150
  },
  {
    title: '响应码',
    dataIndex: 'response_code',
    width: 80
  },
  {
    title: '返回信息',
    dataIndex: 'response_json',
    ellipsis: true,
    width: 500
  },
  {
    title: '操作',
    dataIndex: 'operation',
    align: 'center',
    fixed: 'right',
    width: 80
  }
];

const loadingData = () => {
  tableLoading.value = true;
  
  let params = {};
  
  if (formState.request_path) {
    params['request_path'] = formState.request_path
  }

  if (formState.creator) {
    params['creator'] = formState.creator
  }

  if (formState.date_range) {
    params['start_time'] = `${formState.date_range[0]} 00:00:00`;
    params['end_time'] = `${formState.date_range[1]} 23:59:59`;
  }
  params['page'] = pagination.current;
  params['page_size'] = pagination.pageSize;
  
  getLogList(params).then(response => {
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
  loadingData();
}

const handleTableChange = (values: any) => {
  pagination.current = values.current;
  pagination.pageSize = values.pageSize;
  loadingData();
}

const modalHandle = (index: number) => {
  openModal.value = true;
  
  detailStateLoading.value = true;

  detailState.value = dataSource.value[index];
  detailState.value.index = index;

  detailStateLoading.value = false;
}

const selectModalHandle = () => {
  selectorModal.value.openModal = true;
  selectorModal.value.selectedRowKeys = [formState.creator];
  selectorModal.value.selectedRowName = formState.creator_name;
  selectorModal.value.loadingData();
}

const handleSelectorModalEvent = (selectedSelectorRowKeys?: creatorTableDataType['id'][], selectedSelectorRowName?: creatorTableDataType['name']) => {
  const creator = selectedSelectorRowKeys.length ? selectedSelectorRowKeys[0] : undefined;
  const creator_name = selectedSelectorRowName || undefined;

  formState.creator = creator;
  formState.creator_name = creator_name;
}

</script>

<style lang="scss" scoped>
.table-search-wrapper {
  margin-block-end: 16px;
}
</style>