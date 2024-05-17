<template>
  <a-layout>
    <div class="container">
      <a-layout-content :style="contentStyle">
        <div class="header">
          <div class="logo">
            <a-image src="/logo.png" :preview="false" />
          </div>
          <div class="title">FastAPI Vue Admin</div>
        </div>
        <div class="desc">FastAPI Vue Admin 是完全开源的权限管理系统</div>

        <div class="login-main" style="width: 330px; margin: 0 auto;">
          <a-tabs :v-model="activeKey" centered>
            <a-tab-pane :key="1" tab="账户密码登录">
              <a-form
                :model="formState"
                name="normal_login"
                class="login-form"
                @finish="onFinish"
                @finishFailed="onFinishFailed"
              >
                <a-form-item name="username" :rules="[{ required: true, message: '用户名是必填项！' }]">
                  <a-input v-model:value="formState.username" placeholder="用户名: senqi or test">
                    <template #prefix>
                      <UserOutlined class="site-form-item-icon" />
                    </template>
                  </a-input>
                </a-form-item>

                <a-form-item name="password" :rules="[{ required: true, message: '密码是必填项！' }]">
                  <a-input-password v-model:value="formState.password" placeholder="密码: gitee 或 github 查看">
                    <template #prefix>
                      <LockOutlined class="site-form-item-icon" />
                    </template>
                  </a-input-password>
                </a-form-item>

                <a-form-item>
                  <a-form-item name="remember" no-style>
                    <a-checkbox v-model:checked="formState.remember"
                      >自动登录</a-checkbox
                    >
                  </a-form-item>
                  <a class="login-form-forgot" href="">忘记密码 ?</a>
                </a-form-item>

                <a-form-item>
                  <a-button
                    type="primary"
                    html-type="submit"
                    class="login-form-button"
                    :loading="logging"
                  >
                    登录
                  </a-button>
                </a-form-item>
              </a-form>
            </a-tab-pane>
          </a-tabs>
        </div>
      </a-layout-content>

      <a-layout-footer :style="footerStyle">
        <div class="footer-list">
          <a-button type="link" href="https://gitee.com/senqi666/fastapi-vue-admin">Fastapi Vue Admin</a-button>
          <a-button type="link" href="https://github.com/SenQi-666/fastapi-vue-admin">
            <span>
              <icon-font type="icon-github-fill" :style="{ fontSize: '16px' }" />
            </span>
          </a-button>
          <a-button type="link" href="https://gitee.com/senqi666/fastapi-vue-admin">Fastapi Vue Admin</a-button>
        </div>
        <div class="footer-copyright">
          <icon-font type="icon-copyright" :style="{ fontSize: '16px' }" />
          Powered by senqi
        </div>
      </a-layout-footer>
    </div>
  </a-layout>
</template>

<script lang="ts" setup>
import type { CSSProperties } from "vue";
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue';
import { login } from "@/api/auth"
import { save_token } from "@/utils/util"
import md5 from "md5"

const router = useRouter()
const logging = ref(false);

const contentStyle: CSSProperties = {
  minHeight: 850,
  height: "850px",
  background: "none",
  padding: "35px 0",
};
const footerStyle: CSSProperties = {
  textAlign: "center",
  background: "none",
};

const activeKey = ref(1);

interface FormState {
  username: string;
  password: string;
  code: string;
  remember: boolean;
}
const formState = reactive<FormState>({
  username: "",
  password: "",
  code: "",
  remember: true,
});
const onFinish = (values: FormState) => {
  logging.value = true;

  values.password = md5(values.password);
  login(values).then(response => {
    let result = response.data;
    if (result.code === 200) {
      save_token(result.data.access_token, result.data.refresh_token, result.data.expires_in)
      logging.value = false;
      router.push('/');
    } else {
      logging.value = false;
    }
  }).catch(error => {
    logging.value = false;
  })
};

const onFinishFailed = (errorInfo: any) => {
  console.log("Failed:", errorInfo);
};
</script>

<style lang="scss" scoped>
.ant-btn-link {
  color: rgba(0, 0, 0, 0.65);
  margin-inline-end: 8px;
}
.ant-btn {
  padding: 0;
}
.container {
  background-image: url(https://mdn.alipayobjects.com/yuyan_qk0oxh/afts/img/V-_oS6r-i7wAAAAAAAAAAAAAFl94AQBr);
  background-size: 100% 100%;
  .desc {
    text-align: center;
    font-size: 15px;
    margin-block-start: 12px;
    margin-block-end: 40px;
  }
  .header {
    display: flex;
    line-height: 44px;
    justify-content: center;
    align-items: center;
    .logo {
      width: 44px;
      height: 44px;
      margin-inline-end: 16px;
    }
    .title {
      font-size: 33px;
      font-weight: 650;
    }
  }
}
.login-form-button {
  width: 100%;
}
.login-form-forgot {
  float: right;
}
</style>