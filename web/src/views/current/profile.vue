<template>
  <div>
    <page-header />
    <a-card :bordered="false" :bodyStyle="{ padding: '10px 0 0 0' }">
      <div style="display: flex;">
        <div class="settings-left">
          <a-menu v-model:selectedKeys="selectedKeys" @click="menuClick">
            <a-menu-item key="1">基本设置</a-menu-item>
            <a-menu-item key="2">密码设置</a-menu-item>
          </a-menu>
        </div>
        <div class="settings-right">
          <div class="settings-title">{{ selectedKeys[0] == 1 ? '基本设置' : '密码设置' }}</div>
          <div v-if="selectedKeys[0] == 1" class="settings-info">
            <div class="info-form">
              <a-form layout="vertical" :model="infoFormState" @finish="onInfoFormFinish">
                <a-form-item label="姓名" name="name" :rules="[{ required: true, message: '请输入姓名！' }]"  style="width: 350px;">
                  <a-input v-model:value="infoFormState.name" placeholder="请输入" allowClear />
                </a-form-item>
                <a-form-item label="性别" name="gender" style="width: 200px;" :rules="[{ required: true, message: '请选择性别！' }]">
                  <a-select v-model:value="infoFormState.gender" placeholder="请选择" allowClear>
                    <a-select-option :value="1">男</a-select-option>
                    <a-select-option :value="2">女</a-select-option>
                  </a-select>
                </a-form-item>
                <a-form-item label="联系电话" name="mobile" style="width: 350px;">
                  <a-input v-model:value="infoFormState.mobile" placeholder="请输入" allowClear />
                </a-form-item>
                <a-form-item label="邮箱" name="email" style="width: 350px;">
                  <a-input v-model:value="infoFormState.email" placeholder="请输入" allowClear />
                </a-form-item>
                <a-form-item label="用户名" style="width: 200px;">
                  <a-input v-model:value="infoFormState.username" :disabled="true" />
                </a-form-item>
                <a-form-item label="所属部门" style="width: 200px;">
                  <a-input v-model:value="infoFormState.deptName" :disabled="true" />
                </a-form-item>
                <a-form-item label="所属岗位">
                  <a-select mode="multiple" v-model:value="infoFormState.positions" :disabled="true"></a-select>
                </a-form-item>
                <a-form-item label="当前角色">
                  <a-select mode="multiple" v-model:value="infoFormState.roles" :disabled="true"></a-select>
                </a-form-item>
                <a-form-item>
                  <a-button type="primary" html-type="submit">更新基本信息</a-button>
                </a-form-item>
              </a-form>
            </div>
            <div class="info-avatar">
              <div style="margin-bottom: 10px;">头像</div>
              <div style="margin-bottom: 15px;">
                <a-avatar :src="infoFormState.avatar" :size="140" ></a-avatar>
              </div>
              <div style="text-align: center;">
                <a-upload
                  v-model:file-list="avatarFileList"
                  name="file"
                  action="/api/system/user/current/avatar/upload"
                  :showUploadList="false"
                  :headers="uploadHeaders"
                  @change="avatarHandleChange"
                >
                  <a-button>
                    <upload-outlined></upload-outlined>
                    上传头像
                  </a-button>
                </a-upload>
              </div>
            </div>
          </div>
          <div v-else>
            <a-form layout="vertical" :model="passwordFormState" @finish="onPasswordFormFinish">
              <a-form-item label="原密码" name="oldPassword" :rules="[{ required: true, message: '请输入原密码！' }]"  style="width: 350px;">
                <a-input-password v-model:value="passwordFormState.oldPassword" placeholder="请输入" allowClear />
              </a-form-item>
              <a-form-item label="新密码" name="newPassword" :rules="[{ required: true, message: '请输入新密码！' }]"  style="width: 350px;">
                <a-input-password v-model:value="passwordFormState.newPassword" placeholder="请输入" allowClear />
              </a-form-item>
              <a-form-item label="确认密码" name="repeatPassword" :rules="[{ required: true, message: '请再次输入密码！' }]"  style="width: 350px;">
                <a-input-password v-model:value="passwordFormState.repeatPassword" placeholder="请输入" allowClear />
              </a-form-item>
              <a-form-item>
                <a-button type="primary" html-type="submit" :loading="passwordChanging">提交</a-button>
              </a-form-item>
            </a-form>
          </div>
        </div>
      </div>
    </a-card>
  </div>
</template>

<script lang="ts">
import PageHeader from '@/components/PageHeader.vue';
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import type { MenuProps, UploadChangeParam } from "ant-design-vue";
import { UploadOutlined } from '@ant-design/icons-vue';
import store from '@/store'
import storage from 'store'
import request from "@/utils/axios"
import md5 from "md5"
import { updateCurrentUserInfo, changeCurrentUserPassword } from '@/api/user'


export default {
  name: "Profile",
  components: {
    PageHeader: PageHeader,
    UploadOutlined: UploadOutlined
  },

  setup() {
    const passwordChanging = ref(false);
    const selectedKeys = ref<string[]>(['1']);

    const infoFormState = reactive({});
    const passwordFormState = ref({});

    const avatarFileList = ref([]);

    const token = storage.get('Access-Token');
    const uploadHeaders = token ? { Authorization: 'Bearer ' + token } : {};

    const menuClick: MenuProps["onClick"] = ({ key }) => {
      if (key == 1) {
        initInfoForm();
      } else {
        initpasswordForm();
      }
    }

    const onInfoFormFinish = (values: any) => {
      values.avatar = infoFormState.avatar;
      updateCurrentUserInfo(values).then(response => {
        const result = response.data;
        message.success(result.message);
        store.dispatch('getUserInfo');
      }).catch(error => {
        console.log(error)
      })
    };

    const onPasswordFormFinish = (values: any) => {
      if (values.newPassword !== values.repeatPassword) {
        message.error('两次密码输入不一致');
        return;
      }

      passwordChanging.value = true;

      const data = { old_password: md5(values.oldPassword), new_password: md5(values.newPassword) };
      changeCurrentUserPassword(data).then(response => {
        const result = response.data;
        passwordChanging.value = false;
        message.success(result.message);
        initpasswordForm();
      }).catch(error => {
        console.log(error);
        passwordChanging.value = false;
      })
    };

    const avatarHandleChange = (info: UploadChangeParam) => {
      if (info.file.status === 'done') {
        const response = info.file.response;
        const apiUrl = request.defaults.baseURL;
        const newAvatar = apiUrl + '/' + response.data;
        infoFormState.avatar = newAvatar
        message.success('上传成功');
      } else if (info.file.status === 'error') {
        message.error('上传失败');
      }
    };

    const initInfoForm = () => {
      const basicInfo = store.state.user.basicInfo;
      infoFormState.name = basicInfo.name;
      infoFormState.gender = basicInfo.gender;
      infoFormState.mobile = basicInfo.mobile;
      infoFormState.email = basicInfo.email;
      infoFormState.username = basicInfo.username;
      infoFormState.deptName = basicInfo.dept_name;
      infoFormState.positions = basicInfo.positions.map(item => item.name);
      infoFormState.roles = basicInfo.roles.map(item => item.name);
      infoFormState.avatar = basicInfo.avatar;
    }

    const initpasswordForm = () => {
      passwordFormState.value = {};
    }

    onMounted(() => {
      initInfoForm();
    })

    return {
      passwordChanging,
      selectedKeys,
      infoFormState,
      passwordFormState,
      avatarFileList,
      uploadHeaders,
      menuClick,
      onInfoFormFinish,
      onPasswordFormFinish,
      avatarHandleChange
    }
  },
};
</script>

<style lang="scss" scoped>
.settings-left {
  width: 250px;
  border-right: 1px solid rgba(5, 5, 5, 0.06);
}

.settings-right {
  flex: 1 1;
  padding: 8px 40px;

  .settings-title {
    color: rgba(0,0,0,.88);
    font-size: 20px;
    font-weight: 500;
    line-height: 28px;
    margin-bottom: 12px;
  }

  .settings-info {
    display: flex;

    .info-form {
      width: 500px;
    }

    .info-avatar {
      padding-left: 104px;
    }
  }
}

</style>