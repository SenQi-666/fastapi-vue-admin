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
          <a-tabs centered>
            <a-tab-pane :key="1" tab="账户密码登录">
              <a-form
                :model="loginForm"
                name="normal_login"
                class="login-form"
                @finish="onFinish"
              >
                <a-form-item name="username" :rules="[{ required: true, message: '用户名是必填项！' }]">
                  <a-input v-model:value="loginForm.username" placeholder="用户名: senqi or test">
                    <template #prefix>
                      <UserOutlined class="site-form-item-icon" />
                    </template>
                  </a-input>
                </a-form-item>

                <a-form-item name="password" :rules="[{ required: true, message: '密码是必填项！' }]">
                  <a-input-password v-model:value="loginForm.password" placeholder="密码: gitee 或 github 查看">
                    <template #prefix>
                      <LockOutlined class="site-form-item-icon" />
                    </template>
                  </a-input-password>
                </a-form-item>

                <a-form-item name="captcha" :rules="[{ required: captchaState.enable, message: '验证码是必填项！' }]">
                  <a-input v-model:value="loginForm.captcha" placeholder="验证码">
                    <template #addonAfter>
                      <div class="login-form-captcha" @click="requestCaptcha">
                        <a-image :src="captchaState.img_base" :preview="false" />
                      </div>
                    </template>
                  </a-input>
                </a-form-item>

                <a-form-item>
                  <a-form-item name="remember" no-style>
                    <a-checkbox v-model:checked="loginForm.remember">自动登录</a-checkbox>
                  </a-form-item>
                  <a class="login-form-forgot">忘记密码 ?</a>
                </a-form-item>

                <a-form-item>
                  <a-button
                    type="primary"
                    html-type="submit"
                    class="login-form-button"
                    :loading="loginFlag"
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
              <GithubOutlined />
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
import { ref, reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { UserOutlined, LockOutlined, GithubOutlined } from '@ant-design/icons-vue';
import { login, getCaptcha } from "@/api/auth"
import type { loginFormType, captchaStateType } from './types';
import { save_token } from "@/utils/util"
import md5 from "md5"

const router = useRouter()
const loginFlag = ref(false);

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


const loginForm = reactive<loginFormType>({
  username: "",
  password: "",
  captcha: "",
  captcha_key: "",
  remember: true
});


const captchaState = reactive<captchaStateType>({
  enable: true,
  key: "",
  img_base: ""
});

const onFinish = (values: loginFormType) => {
  loginFlag.value = true;

  values.password = md5(values.password);
  values.captcha_key = captchaState.key;
  login(values).then(response => {
    let result = response.data;
    if (result.code === 200) {
      save_token(result.data.access_token, result.data.refresh_token, result.data.expires_in)
      loginFlag.value = false;
      router.push('/');
    } else {
      loginFlag.value = false;
    }
  }).catch(error => {
    if (error.data.code === 410) {
      requestCaptcha();
    }
    loginFlag.value = false;
  })
};

const requestCaptcha = () => {
  getCaptcha().then(response => {
    let result = response.data;
    if (result.code === 200) {
      captchaState.key = result.data.key;
      captchaState.img_base = result.data.img_base;
    } else {
      captchaState.enable = false;
    }
  }).catch(error => {
    console.log(error);
    captchaState.enable = false;
  })
}

onMounted(() => requestCaptcha());
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
  background-image: url("/background.png");
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
.login-form-captcha {
  width: 80px;

  &:hover {
    cursor: pointer;
  }
}
.login-form-forgot {
  float: right;
}
:deep(.ant-input-group .ant-input-group-addon) {
  padding: 0;
}
</style>