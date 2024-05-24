<template>
  <div>
    <page-header />
    <a-row :gutter="24">
      <a-col :span="14">
        <div class="tree-wrapper">
          <a-spin :spinning="treeLoading">
            <a-card title="部门列表" :bordered="true" :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
              :bodyStyle="{ padding: '0 24px 20px', minHeight: 'calc(100vh - 240px)' }">
              <template #extra>
                <a-button type="primary" :icon="h(PlusOutlined)"  @click="openModal = true" style="margin-right: 10px;">新建</a-button>
                <a-dropdown>
                  <template #overlay>
                    <a-menu @click="handleActionsClick">
                      <a-menu-item key="1"><span style="margin-right: 10px;"><ArrowsAltOutlined /></span><span>展开所有</span></a-menu-item>
                      <a-menu-item key="2"><span style="margin-right: 10px;"><ShrinkOutlined /></span><span>折叠所有</span></a-menu-item>
                      <a-menu-item key="3"><span style="margin-right: 10px;"><CheckOutlined /></span><span>全选</span></a-menu-item>
                      <a-menu-item key="4"><span style="margin-right: 10px;"><StopOutlined /></span><span>取消选择</span></a-menu-item>
                      <a-menu-item key="5"><span style="margin-right: 10px;"><SwapOutlined /></span><span>反选</span></a-menu-item>
                    </a-menu>
                  </template>
                  <a-button style="margin-right: 10px;">操作<DownOutlined />
                  </a-button>
                </a-dropdown>
                <a-dropdown>
                  <template #overlay>
                    <a-menu @click="handleMoreClick">
                      <a-menu-item key="1"><span style="margin-right: 10px;"><CheckOutlined /></span><span>批量启用</span></a-menu-item>
                      <a-menu-item key="2"><span style="margin-right: 10px;"><StopOutlined /></span><span>批量停用</span></a-menu-item>
                    </a-menu>
                  </template>
                  <a-button style="margin-right: 10px;">更多<DownOutlined />
                  </a-button>
                </a-dropdown>
                <a-switch v-model:checked="switchStatus" checked-children="显示全部" un-checked-children="显示启用" @change="handleSwitchChange" />
              </template>
              <a-tree
                v-if="!treeLoading"
                v-model:checkedKeys="checkedKeys"
                v-model:expandedKeys="expandedKeys"
                :rowKey="record => record.id"
                :tree-data="deptTreeData"
                :show-line="true"
                :field-names="{ children: 'children', title: 'name', key: 'id' }"
                @select="handleTreeSelect"
                checkable
                checkStrictly
              >
                <template #title="{ name, available }">
                  <span v-if="!available" style="color: rgb(255, 77, 79)">{{ name }}</span>
                  <span v-else style="color: rgba(0, 0, 0, .88)">{{ name }}</span>
                </template>
              </a-tree>
            </a-card>
          </a-spin>
        </div>
      </a-col>
      
      <a-col v-if="showEditForm" :span="10">
        <div class="item-form">
          <a-spin :spinning="editFormLoading">
            <a-card title="编辑" :bordered="true" :headStyle="{ borderBottom: 'none', padding: '20px 24px' }"
              :bodyStyle="{ padding: '0 24px 20px' }">
              <a-form ref="updateForm" :model="updateState" @finish="onFinish" v-bind="{ labelCol: { span: 5 }, wrapperCol: { span: 15 } }">
                <a-form-item name="name" label="名称" :rules="[{ required: true, message: '请输入名称' }]">
                  <a-input v-model:value="updateState.name" placeholder="请输入名称" allowClear></a-input>
                </a-form-item>
                <a-form-item name="order" label="排序">
                  <a-input-number v-model:value="updateState.order" :min="1" />
                </a-form-item>
                <a-form-item name="parent_id" label="上级部门">
                  <a-tree-select
                    v-model:value="updateState.parent_id"
                    :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
                    :tree-data="deptTreeData"
                    :field-names="{ children: 'children', label: 'name', value: 'id' }"
                    tree-node-filter-prop="name"
                    style="width: 100%"
                    show-search
                    allow-clear
                  ></a-tree-select>
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
                <a-form-item :wrapper-col="{ span: 15, offset: 5 }" style="text-align: center;">
                  <a-button type="primary" html-type="submit" :loading="editFormLoading">保存</a-button>
                  <a-button @click="resetItem" style="margin-left: 10px">重置</a-button>
                  <a-button @click="deleteItem" style="margin-left: 10px" :loading="editFormLoading" danger>删除</a-button>
                </a-form-item>
              </a-form>
            </a-card>
          </a-spin>
        </div>
      </a-col>
    </a-row>

    <a-modal title="新建部门" v-model:open="openModal" @ok="handleModalSumbit" :width="800" :destroyOnClose="true" :confirmLoading="modalSubmitLoading" style="top: 30px">
      <a-form ref="createForm" :model="createState" v-bind="{ labelCol: { span: 5 }, wrapperCol: { span: 15 } }">
        <a-form-item name="name" label="名称" :rules="[{ required: true, message: '请输入名称' }]">
          <a-input v-model:value="createState.name" placeholder="请输入名称" allowClear></a-input>
        </a-form-item>
        <a-form-item name="order" label="排序">
          <a-input-number v-model:value="createState.order" :min="1" />
        </a-form-item>
        <a-form-item name="parent_id" label="上级部门">
          <a-tree-select
            v-model:value="createState.parent_id"
            :dropdown-style="{ maxHeight: '400px', overflow: 'auto' }"
            :tree-data="deptTreeData"
            :field-names="{ children: 'children', label: 'name', value: 'id' }"
            tree-node-filter-prop="name"
            style="width: 100%"
            show-search
            allow-clear
          ></a-tree-select>
        </a-form-item>
        <a-form-item name="description" label="备注">
          <a-textarea v-model:value="createState.description" placeholder="请输入备注" :rows="4" allowClear />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, h } from 'vue';
import { message, Modal } from 'ant-design-vue';
import { PlusOutlined, DownOutlined, CheckOutlined, StopOutlined, ArrowsAltOutlined, ShrinkOutlined, SwapOutlined } from '@ant-design/icons-vue';
import PageHeader from '@/components/PageHeader.vue'
import { listToTree } from '@/utils/util';
import { getDeptList, createDept, updateDept, deleteDept, batchEnableDept, batchDisableDept } from '@/api/dept';
import type { MenuProps } from 'ant-design-vue';
import type { treeDataType } from './types';
import { cloneDeep, isEmpty } from '@/utils/util';


const createForm = ref();
const updateForm = ref();
const treeLoading = ref(false);
const editFormLoading = ref(false);
const showEditForm = ref(false);
const switchStatus = ref(false);
const deptTreeData = ref<treeDataType[]>([]);
const checkedKeys = ref<treeDataType['id'][]>([]);
const expandedKeys = ref<treeDataType['id'][]>([]);
const openModal = ref(false);
const modalSubmitLoading = ref(false);


let dataSource: treeDataType[] = [];

const createState: treeDataType = reactive({
  name: '',
  order: 1,
  parent_id: undefined,
  description: ''
})
const updateState = ref<treeDataType>({
  id: undefined,
  name: '',
  order: 1,
  parent_id: undefined,
  available: true,
  description: ''
})

const loadingData = () => {
  treeLoading.value = true;

  getDeptList().then(response => {
    const result = response.data;
    dataSource = result.data;
    dataSource.forEach((item: treeDataType) => {
      expandedKeys.value.push(item.id);
    })
    handleSwitchChange();
    treeLoading.value = false;
  }).catch(error => {
    console.log(error);
    treeLoading.value = false;
  })
}

onMounted(() => loadingData());


const onFinish = () => {
  editFormLoading.value = true;
  updateForm.value.validate().then(() => {
    updateDept(updateState.value).then(response => {
      editFormLoading.value = false;
      showEditForm.value = false;
      message.success(response.data.message);
      loadingData();

    }).catch(error => {
      editFormLoading.value = false;
      console.log(error)
    })

  }).catch(error => {
    editFormLoading.value = false;
    console.log(error)
  })
};

const resetItem = () => {
  for (const item of dataSource) {
    if (item.id === updateState.value.id) {
      const data = cloneDeep(item);
      delete data.children;
      updateState.value = data;
      break;
    }
  }
  
}

const deleteItem = () => {
  Modal.confirm({
    title: '提示',
    content: '是否确定删除吗？',
    onOk() {
      editFormLoading.value = true;
      deleteDept({ id: updateState.value.id }).then(response => {
        editFormLoading.value = false;
        showEditForm.value = false;
        message.success(response.data.message);
        loadingData();

      }).catch(error => {
        editFormLoading.value = false;
        console.log(error)
      })
    }
  });

}

const handleTreeSelect = (selectedKeys, e) => {
  if (selectedKeys.length === 0) {
    showEditForm.value = false;
    editFormLoading.value = false;
    return;
  }
  
  showEditForm.value = true;
  editFormLoading.value = true;
  setTimeout(() => {
    const node = cloneDeep(e.selectedNodes[0]);
    delete node.children;
    updateState.value = node;
    editFormLoading.value = false;
  }, 300);
}

const handleActionsClick: MenuProps['onClick'] = e => {
  if (e.key == 1) {
    // 展开所有
    dataSource.forEach((item: treeDataType) => {
      expandedKeys.value.push(item.id);
    })

  } else if (e.key == 2) {
    // 折叠所有
    expandedKeys.value = [];

  } else if (e.key == 3) {
    // 全选
    checkedKeys.value = [];
    dataSource.forEach(item => {
      if (switchStatus.value || item.available) {
        checkedKeys.value.push(item.id);
      }
    })

  } else if (e.key == 4) {
    // 取消选择
    checkedKeys.value = [];

  } else {
    // 反选
    const existsKeys = checkedKeys.value instanceof Array ? checkedKeys.value : checkedKeys.value['checked'];
    checkedKeys.value = [];

    dataSource.forEach(item => {
      if ((switchStatus.value || item.available) && !existsKeys.includes(item.id)) {
        checkedKeys.value.push(item.id);
      }
    })
  }
}

const handleMoreClick: MenuProps['onClick'] = e => {
  const existsKeys = checkedKeys.value instanceof Array ? checkedKeys.value : checkedKeys.value['checked'];
  if (!existsKeys || !(existsKeys.length > 0) ) {
    message.warning('请先勾选数据');
    return;
  }

  Modal.confirm({
    title: '提示',
    content: e.key == 1 ? '是否确定启用选择项？' : '是否确定停用选择项？',
    onOk() {
      const body = { ids: existsKeys };
      const batchApi = e.key == 1 ? batchEnableDept(body) : batchDisableDept(body);
      batchApi.then(response => {
        showEditForm.value = false;
        message.success(response.data.message);
        checkedKeys.value = [];
        loadingData();
      }).catch(error => {
        console.log(error);
      })
    }
  });
}

const handleSwitchChange = () => {
  checkedKeys.value = [];
  if (switchStatus.value) {
    deptTreeData.value = listToTree(dataSource);
  } else {
    const result = dataSource.filter(item => item.available);
    deptTreeData.value = listToTree(result);
  }
}

const handleModalSumbit = () => {
  modalSubmitLoading.value = true;

  createForm.value.validate().then(() => {
    const createBody = cloneDeep(createState);
    Object.keys(createBody).forEach(key => {
      if (isEmpty(createBody[key])) {
        delete createBody[key];
      }
    })

    createDept(createBody).then(response => {
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
}

</script>

<style lang="scss" scoped>

</style>