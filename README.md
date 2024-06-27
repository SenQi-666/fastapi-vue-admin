<div align="center">
  <p align="center">
    <img src="web/public/logo.png" height="150" alt="logo"/>
  </p>
</div>

## 介绍

<b>fastapi-vue-admin</b> 是一套全部开源的快速开发平台，提供免费使用

- 后端采用 <a href="https://fastapi.tiangolo.com/zh/">FastAPI</a>（现代、高性能异步框架） + <a href="https://swagger.io/docs/specification/about/">Swagger</a>（自动生成交互式API文档） + <a href="https://docs.pydantic.dev/2.5/">Pydantic</a>（强制类型约束） + <a href="https://docs.sqlalchemy.org/en/20/">SQLAlchemy 2.0</a>；
- 前端采用 <a href="https://cn.vuejs.org/guide/introduction.html">Vue3</a> + <a href="https://antdv.com/docs/vue/introduce-cn">Ant Design Vue</a> + <a href="https://www.typescriptlang.org/">TypeScript</a> + <a href="https://vitejs.dev/">Vite</a> 等主流技术开发；
- 权限认证使用（哈希）密码和 JWT Bearer 令牌的 OAuth2
- 基于 RBAC 权限架构设计。支持加载动态权限菜单、按钮级别权限控制、数据级别权限控制
- 开箱即用的中后台解决方案，可以用来作为新项目的启动模版，也可用于学习参考

如果觉得项目不错的话，欢迎大家 Star 支持一下！

## 在线体验

PC端演示地址：https://fastapi-vue-admin.senqiweb.cn

管理员账户：

- 账号：senqi
- 密码：senqi1010

测试账户：

- 账号：test
- 密码：test1010

## 安装和使用

### 获取代码

> git clone https://github.com/SenQi-666/fastapi-vue-admin.git

### 准备工作

```
Python == 3.10（其他版本均未测试）
nodejs >= 20.0（推荐使用最新版）
PgSQL（推荐使用最新版）
Redis（推荐使用最新版）
```

### 后端

1. 安装依赖
   
   ```shell
   cd backend
   pip3 install -r requirements.txt
   ```

2. 修改项目数据库配置信息
   在`app/core/config.py`文件中的`SQL_DB_URL`和`REDIS_URL`

3. 创建名为`fastapi_vue_admin`的数据库

4. 初始化数据库数据
   
   ```shell
   # 进入后端根目录 backend 下运行
   # 运行命令后会自动生成数据库内的表和数据
   # 如已初始化数据库数据，此命令可不执行
   python3 main.py init
   ```

5. 启动
   
   ```shell
   # 进入后端根目录 backend 下运行
   python3 main.py run
   ```

### 前端

1. 安装依赖
   
   ```shell
   cd web
   npm install
   ```

2. 运行
   
   ```shell
   npm run dev
   ```

3. 打包
   
   ```shell
   npm run build
   ```

### 访问项目

- 前端地址：http://127.0.0.1:5180
- 账号：`senqi`密码：`senqi1010`
- 接口地址：http://127.0.0.1:8080/docs

## 微信群

在下方放一个微信群二维码，可以用于技术交流，也可以一起讨论在项目使用过程中遇到的各种问题。真心希望大家加入，积极讨论，让我们一起抱团取暖！

如果微信群二维码已过期，需要进群的可以先扫我个人的二维码，备注admin，我看到后会同意申请并拉你进群。

![](https://mp-imgs.senqiweb.cn/project/images/fv_group_qrcode.jpg)
![](https://mp-imgs.senqiweb.cn/project/images/wechat.jpg)