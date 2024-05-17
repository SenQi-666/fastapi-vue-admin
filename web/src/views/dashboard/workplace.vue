<template>
  <page-header />
  <div class="container">
    <div class="page-header-content" style="display: flex; justify-content: space-between; padding-bottom: 20px;">
      <a-row align="middle">
        <a-col class="avatar">
          <a-avatar :size="75" src="https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png" />
        </a-col>
        <a-col class="content" style="margin-left: 20px;">
          <div class="content-title" style="font-size: 20px; font-weight: 500; color: rgba(0, 0, 0, 0.88); margin-bottom: 12px;"> 
            {{ timefix }}，{{ username }}<span class="welcome-text">，{{ welcome }}</span>
          </div>
          <div style="color: rgba(0, 0, 0, 0.65);">开发工程师 | Fastapi-Vue-Admin团队 - 某某某事业群 - 某某技术部</div>
        </a-col>
      </a-row>
      <a-row class="extra-content" justify="space-around">
        <a-col class="stat-item">
          <a-statistic title="项目数" :value="56" />
        </a-col>
        <a-col class="stat-item">
          <a-statistic title="团队内排名" :value="8" suffix="/ 24" />
        </a-col>
        <a-col class="stat-item">
          <a-statistic title="项目访问" :value="2223" />
        </a-col>
      </a-row>
    </div>
    <div>
      <a-row :gutter="24">
        <a-col :xl="16" :lg="24" :md="24" :sm="24" :xs="24">
          <a-card title="进行中的项目">
            <template #extra>
              <a>全部项目</a>
            </template>
            <a-card-grid :key="i" v-for="(item, i) in projectItems" style="width: 33.33%;">
              <a-skeleton :loading="loading">
                <a-card-meta>
                  <template #title>
                    <a-avatar :size="30" :src="item.avatar" />
                    <a class="a-hover" style="margin-left: 10px; color: rgba(0, 0, 0, 0.88);">{{ item.title }}</a>
                  </template>
                  <template #description><div style="min-height: 45px;">{{ item.description }}</div></template>
                </a-card-meta>
                <div class="project-item">
                  <a class="a-hover" style="color: rgba(0, 0, 0, 0.65)">{{ item.author }}</a>
                  <span class="item-datetime">{{ item.datetime }}</span>
                </div>
              </a-skeleton>
            </a-card-grid>
          </a-card>
          <a-card title="动态" :bordered="false" :bodyStyle="{ padding: '10px' }" style="margin-top: 20px;">
            <a-list item-layout="horizontal" :data-source="activities">
              <template #renderItem="{ item }">
                <a-list-item>
                  <a-skeleton :loading="loading" active avatar>
                    <a-list-item-meta>
                      <template #avatar>
                        <a-avatar :src="item.avatar" />
                      </template>
                      <template #title>
                        <a class="a-hover">{{ item.username }}</a>
                        <span>
                          在
                          <a>{{ item.project }}</a>
                          {{ item.action }}
                          <a>{{ item.event }}</a>
                        </span>
                      </template>
                      <template #description>
                        <span class="item-datetime">几秒前</span>
                      </template>
                    </a-list-item-meta>
                  </a-skeleton>
                </a-list-item>
              </template>
            </a-list>
          </a-card>
        </a-col>

        <a-col :xl="8" :lg="24" :md="24" :sm="24" :xs="24">
          <a-card title="快速开始 / 便捷导航" :bodyStyle="{ padding: '20px 0 8px 24px'}">
            <a-button type="primary" size="small" ghost>
              <template #icon>
                <PlusOutlined />
              </template>
              添加
            </a-button>
          </a-card>
          <a-card title="XX 指数" style="margin-top: 20px;">
            <a-skeleton :loading="loading">
              <v-chart class="chart" :option="chartOptions" autoresize />
            </a-skeleton>
          </a-card>
          <a-card title="团队" :bodyStyle="{ padding: '10px' }" style="margin-top: 20px;">
            <a-skeleton :loading="loading">
              <div class="members">
                <a-row>
                  <a-col :span="12" v-for="(item, index) in teams" :key="index" style="padding-left: 10px">
                    <a>
                      <a-avatar size="small" :src="item.avatar" />
                      <span class="member">{{ item.name }}</span>
                    </a>
                  </a-col>
                </a-row>
              </div>
            </a-skeleton>
          </a-card>
        </a-col>
      </a-row>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue';
import PageHeader from '@/components/PageHeader.vue'
import { timeFix } from '@/utils/util';
import { PlusOutlined } from '@ant-design/icons-vue';

const loading = ref(true);

let timefix = timeFix();
const username = ref<string>("吴彦祖");
const welcome = '祝你开心每一天！';

const projectItems = [
  { title: 'Ant Design Vue', avatar: 'https://aliyuncdn.antdv.com/favicon.ico', description: '城镇中有那么多的酒馆，她却偏偏走进了我的酒馆', author: '中二少女团', datetime: '几秒前' },
  { title: 'Ant Design Pro', avatar: 'https://gw.alipayobjects.com/zos/rmsportal/sfjbOqnsXXJgNCjCzDBL.png', description: '那时候我只会想自己想要什么，从不想自己拥有什么', author: '程序员日常', datetime: '7年前' },
  { title: 'Fastapi', avatar: 'https://fastapi.tiangolo.com/img/favicon.png', description: '那是一种内在的东西，他们到达不了，也无法触及的', author: '科学搬砖组', datetime: '几秒前' },
  { title: 'Vite', avatar: 'https://vitejs.dev/logo.svg', description: '生命就像一盒巧克力，结果往往出人意料', author: '骗你来学计算机', datetime: '7年前' },
  { title: 'Vue', avatar: 'https://gw.alipayobjects.com/zos/rmsportal/ComBAopevLwENQdKWiIn.png', description: '希望是一个好东西，也许是最好的，好东西是不会消亡的', author: '全组都是吴彦祖', datetime: '几秒前' },
  { title: 'Python', avatar: 'https://python.p2hp.com/static/favicon.ico', description: '人生苦短，我用Python', author: '高逼格语言天团', datetime: '7年前' }
]

const activities = [
  {
    username: '曲丽丽',
    avatar: 'https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',
    project: '高逼格设计天团',
    action: '新建项目',
    event: '六月迭代'
  },
  {
    username: '付小小',
    avatar: 'https://gw.alipayobjects.com/zos/rmsportal/cnrhVkzwxjPwAaCfPbdc.png',
    project: '高逼格设计天团',
    action: '更新项目',
    event: '六月迭代'
  },
  {
    username: '林东东',
    avatar: 'https://gw.alipayobjects.com/zos/rmsportal/gaOngJwsRYRaVAuXXcmB.png',
    project: '中二少女团',
    action: '新建项目',
    event: '六月迭代'
  },
  {
    username: '周星星',
    avatar: 'https://gw.alipayobjects.com/zos/rmsportal/WhxKECPNujWoWEFNdnJE.png',
    project: '白鹭酱油开发组',
    action: '更新项目',
    event: '番组计划'
  },
  {
    username: '朱偏右',
    avatar: 'https://gw.alipayobjects.com/zos/rmsportal/ubnKSIfAJTxIgXOKlciN.png',
    project: '工程效能',
    action: '发布了',
    event: '留言'
  },
  {
    username: '乐哥',
    avatar: 'https://gw.alipayobjects.com/zos/rmsportal/jZUIxmJycoymBprLOUbT.png',
    project: '程序员日常',
    action: '新建项目',
    event: '品牌迭代'
  }
];

const chartOptions = {
  tooltip: {
    trigger: 'item'
  },
  legend: {
    icon: 'path://M773.12 870.4c-163.84 0-225.28-184.32-276.48-343.04C440.32 363.52 399.36 256 312.32 256 225.28 256 179.2 256 102.4 558.08c-5.12 25.6-35.84 46.08-61.44 35.84-25.6-5.12-46.08-35.84-35.84-61.44C76.8 230.4 143.36 153.6 312.32 153.6c163.84 0 225.28 184.32 276.48 343.04 56.32 163.84 97.28 271.36 184.32 271.36 40.96 0 117.76 0 143.36-174.08 5.12-25.6 30.72-46.08 56.32-40.96 25.6 5.12 46.08 30.72 40.96 56.32-20.48 174.08-102.4 261.12-240.64 261.12z',
    data: ['个人', '团队', '部门'],
    bottom: 10,
    itemHeight: 7,
  },
  radar: {
    shape: 'circle',
    indicator: [
      { name: '引用', max: 10 },
      { name: '热度', max: 10 },
      { name: '贡献', max: 10 },
      { name: '产量', max: 10 },
      { name: '口碑', max: 10 }
    ]
  },
  series: [
    {
      name: 'Budget vs spending',
      type: 'radar',
      areaStyle: {},
      symbol: 'none',
      emphasis: {
        focus: 'self'
      },
      data: [
        {
          value: [10, 7, 5, 4, 8],
          name: '个人'
        },
        {
          value: [3, 1, 3, 6, 9],
          name: '团队'
        },
        {
          value: [4, 7, 5, 6, 1],
          name: '部门'
        }
      ]
    }
  ]
}

const teams = [
  { avatar: 'https://aliyuncdn.antdv.com/favicon.ico', name: '中二少女团' },
  { avatar: 'https://gw.alipayobjects.com/zos/rmsportal/sfjbOqnsXXJgNCjCzDBL.png', name: '程序员日常' },
  { avatar: 'https://fastapi.tiangolo.com/img/favicon.png', name: '科学搬砖组' },
  { avatar: 'https://vitejs.dev/logo.svg', name: '骗你来学计算机' },
  { avatar: 'https://gw.alipayobjects.com/zos/rmsportal/ComBAopevLwENQdKWiIn.png', name: '全组都是吴彦祖' },
  { avatar: 'https://python.p2hp.com/static/favicon.ico', name: '高逼格语言天团' }
]

setTimeout(() => {
  loading.value = false;
}, 500);
</script>

<style lang="scss" scoped>
.stat-item:not(:last-child)::after {
  position: absolute;
  top: 8px;
  right: 0;
  width: 1px;
  height: 45px; 
  background-color: rgba(5, 5, 5, 0.06);
  content: '';
}
.stat-item {
  padding: 0 25px;
}
.project-item {
  margin-top: 10px;
  font-size: 12px;
  display: flex;
  gap: 8px;
}
.item-datetime {
  float: right;
  color: rgba(0, 0, 0, 0.25);
}
.a-hover:hover {
  color: #1890ff !important;
}
:deep(.ant-list-item-meta-content) {
  h4 {
    color: rgba(0, 0, 0, 0.88);
    font-size: 14px;
    font-weight: normal;
  }
}
.chart {
  width: 450px;
  height: 350px;
}
.members {
  a {
    display: block;
    margin: 12px 0;
    line-height: 24px;
    height: 24px;

    .member {
      font-size: 14px;
      color: rgba(0, 0, 0, 0.88);
      line-height: 24px;
      max-width: 100px;
      vertical-align: top;
      margin-left: 12px;
      transition: all 0.3s;
      display: inline-block;
    }

    &:hover {
      span {
        color: #1890ff;
      }
    }
  }
}
</style>