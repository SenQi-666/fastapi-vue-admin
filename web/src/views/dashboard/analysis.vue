<template>
  <div style="padding: 15px 0;">
    <a-row :gutter="24">
      <a-col :xl="6" :lg="12" :md="12" :sm="24" :xs="24">
        <a-card :bodyStyle="{ padding: '20px 24px 8px' }">
          <a-skeleton :loading="loading">
            <div>
              <span style="color: rgba(0, 0, 0, 0.65)">总销售额</span>
              <div style="float: right;">
                <a-tooltip title="指标说明" placement="top">
                  <InfoCircleOutlined />
                </a-tooltip>
              </div>
              <div class="value">
                <span>¥ 126,560</span>
              </div>
            </div>
            <div style="display: flex; height: 45px; padding-top: 10px;">
              <div style="margin-right: 16px; align-self: flex-end;">
                <span>
                  周同比
                  <span style="margin-left: 8px;">
                    12%
                    <CaretUpOutlined style="color:red;" />
                    </span>
                  </span>
              </div>
              <div style="align-self: flex-end;">
                <span>
                  日同比
                  <span style="margin-left: 8px;">
                    11%
                    <CaretDownOutlined  style="color:green;" />
                  </span>
                </span>
              </div>
            </div>
            <div style="border-top: 1px solid rgba(5, 5, 5, 0.06); margin-top: 10px; padding-top: 10px;">
              <span>
                日销售额
                <span>￥12,423</span>
              </span>
            </div>
          </a-skeleton>
        </a-card>
      </a-col>
      <a-col :xl="6" :lg="12" :md="12" :sm="24" :xs="24">
        <a-card :bodyStyle="{ padding: '20px 24px 8px' }">
          <a-skeleton :loading="loading">
            <div>
              <span style="color: rgba(0, 0, 0, 0.65)">访问量</span>
              <div style="float: right;">
                <a-tooltip title="指标说明" placement="top">
                  <InfoCircleOutlined />
                </a-tooltip>
              </div>
              <div class="value">
                <span>8,846</span>
              </div>
            </div>
            <div style="height: 45px; padding-top: 10px;">
              <v-chart class="line-chart" :option="visitOption" autoresize />
            </div>
            <div style="border-top: 1px solid rgba(5, 5, 5, 0.06); margin-top: 10px; padding-top: 10px;">
              <span>
                日访问量
                <span>1,234</span>
              </span>
            </div>
          </a-skeleton>
        </a-card>
      </a-col>
      <a-col :xl="6" :lg="12" :md="12" :sm="24" :xs="24">
        <a-card :bodyStyle="{ padding: '20px 24px 8px' }">
          <a-skeleton :loading="loading">
            <div>
              <span style="color: rgba(0, 0, 0, 0.65)">支付笔数</span>
              <div style="float: right;">
                <a-tooltip title="指标说明" placement="top">
                  <InfoCircleOutlined />
                </a-tooltip>
              </div>
              <div class="value">
                <span>6,560</span>
              </div>
            </div>
            <div style="display: flex; height: 45px; padding-top: 10px;">
              <v-chart class="payment-chart" :option="paymentOption" autoresize />
            </div>
            <div style="border-top: 1px solid rgba(5, 5, 5, 0.06); margin-top: 10px; padding-top: 10px;">
              <span>
                转化率
                <span>60%</span>
              </span>
            </div>
          </a-skeleton>
        </a-card>
      </a-col>
      <a-col :xl="6" :lg="12" :md="12" :sm="24" :xs="24">
        <a-card :bodyStyle="{ padding: '20px 24px 8px' }">
          <a-skeleton :loading="loading">
            <div>
              <span style="color: rgba(0, 0, 0, 0.65)">运营活动效果</span>
              <div style="float: right;">
                <a-tooltip title="指标说明" placement="top">
                  <InfoCircleOutlined />
                </a-tooltip>
              </div>
              <div class="value">
                <span>78%</span>
              </div>
            </div>
            <div style="height: 45px; line-height: 45px; padding-top: 10px;">
              <a-progress :percent="78" status="active" :strokeColor="{ from: '#108ee9', to: '#87d068' }"/>
            </div>
            <div style="display: flex; border-top: 1px solid rgba(5, 5, 5, 0.06); margin-top: 10px; padding-top: 10px;">
              <div style="margin-right: 16px; align-self: flex-end;">
                <span>
                  周同比
                  <span style="margin-left: 8px;">
                    12%
                    <CaretUpOutlined style="color:red;" />
                    </span>
                  </span>
              </div>
              <div style="align-self: flex-end;">
                <span>
                  日同比
                  <span style="margin-left: 8px;">
                    11%
                    <CaretDownOutlined  style="color:green;" />
                  </span>
                </span>
              </div>
            </div>
          </a-skeleton>
        </a-card>
      </a-col>
    </a-row>
    <div style="margin-top: 25px;">
      <a-card :tab-list="tabList" :active-tab-key="barTypeKey" @tabChange="onTabChange">
        <a-skeleton :loading="loading">
          <template #tabBarExtraContent>
            <div class="extra-item" style="">
              <a>今日</a>
              <a>本周</a>
              <a>本月</a>
              <a>本年</a>
            </div>
            <a-range-picker :style="{ width: '256px'}" />
          </template>
          <div v-if="barTypeKey == 'sales' ">
            <a-row :gutter="24">
              <a-col :xl="16" :lg="12" :md="12" :sm="24" :xs="24">
                <v-chart :option="barOption" autoresize  style="width: 1060px; height: 300px;"/>
              </a-col>
              <a-col :xl="8" :lg="12" :md="12" :sm="24" :xs="24">
                <div class="rank">
                  <h4>门店销售额排名</h4>
                  <ul style="list-style: none; margin: 25px 0 0;">
                    <li :key="i" v-for="(item, i) in barRank">
                      <span class="active" v-if="i < 3">{{ i + 1 }}</span>
                      <span v-else>{{ i + 1 }}</span>
                      <span>{{ item }}</span>
                      <span>323,234</span>
                    </li>
                  </ul>
                </div>
              </a-col>
            </a-row>
          </div>
          <div v-else>
            <a-row :gutter="24">
              <a-col :xl="16" :lg="12" :md="12" :sm="24" :xs="24">
                <v-chart :option="barOption" autoresize  style="width: 1060px; height: 300px;"/>
              </a-col>
              <a-col :xl="8" :lg="12" :md="12" :sm="24" :xs="24">
                <div class="rank">
                  <h4>门店访问量排名</h4>
                  <ul style="list-style: none; margin: 25px 0 0;">
                    <li :key="i" v-for="(item, i) in barRank">
                      <span class="active" v-if="i < 3">{{ i + 1 }}</span>
                      <span v-else>{{ i + 1 }}</span>
                      <span>{{ item }}</span>
                      <span>323,234</span>
                    </li>
                  </ul>
                </div>
              </a-col>
            </a-row>
          </div>
        </a-skeleton>
      </a-card>
    </div>
    <a-row :gutter="24" style="margin-top: 25px;">
      <a-col :xl="12" :lg="24" :md="24" :sm="24" :xs="24">
        <a-card title="线上热门搜索">
          <a-skeleton :loading="loading">
            <template #extra>
              <a-dropdown placement="bottomRight">
                <template #overlay>
                  <a-menu>
                    <a-menu-item key="1">操作一</a-menu-item>
                    <a-menu-item key="2">操作二</a-menu-item>
                  </a-menu>
                </template>
                <EllipsisOutlined />
              </a-dropdown>
            </template>

            <a-row :gutter="68">
              <a-col :sm="12" :xs="24">
                <div style="color: rgba(0, 0, 0, 0.65);">
                  <span>搜索用户数</span>
                  <span style="margin-left: 8px;">
                    <a-tooltip title="指标说明" placement="top">
                      <InfoCircleOutlined />
                    </a-tooltip>
                  </span>
                </div>
                <div style="margin-top: 5px;">
                  <v-chart class="line-chart" :option="searchOption" autoresize />
                </div>
              </a-col>
              <a-col :sm="12" :xs="24">
                <div style="color: rgba(0, 0, 0, 0.65);">
                  <span>人均搜索次数</span>
                  <span style="margin-left: 8px;">
                    <a-tooltip title="指标说明" placement="top">
                      <InfoCircleOutlined />
                    </a-tooltip>
                  </span>
                </div>
                <div style="margin-top: 5px;">
                  <v-chart class="line-chart" :option="searchOption" autoresize />
                </div>
              </a-col>
            </a-row>
            <div style="margin-top: 10px;">
              <a-table row-key="index" size="small" :columns="searchColumns" :data-source="searchData" :pagination="{ pageSize: 5 }">
                <template v-slot:bodyCell="{ column, record }">
                  <template v-if="column.dataIndex === 'keyword'">
                      <a>{{ record.keyword }}</a>
                  </template>
                  <template v-if="column.dataIndex === 'range'">
                      <span v-if="record.status === 0">
                        {{ `${record.range}%` }}
                        <CaretUpOutlined style="color:red;" />
                        </span>
                      <span v-else>
                        {{ `${record.range}%` }}
                        <CaretDownOutlined style="color:green;" />
                        </span>
                  </template>
                </template>
              </a-table>
            </div>
          </a-skeleton>
        </a-card>
      </a-col>
      <a-col :xl="12" :lg="24" :md="24" :sm="24" :xs="24">
        <a-card title="销售额类别占比">
          <a-skeleton :loading="loading">
            <template #extra>
              <span>
                <a-radio-group v-model:value="salesType" @change="salesTabChange">
                  <a-radio-button value="all">全部渠道</a-radio-button>
                  <a-radio-button value="online">线上</a-radio-button>
                  <a-radio-button value="offline">门店</a-radio-button>
                </a-radio-group>
              </span>
              <span style="margin-left: 20px;">
                <a-dropdown placement="bottomRight">
                  <template #overlay>
                    <a-menu>
                      <a-menu-item key="1">操作一</a-menu-item>
                      <a-menu-item key="2">操作二</a-menu-item>
                    </a-menu>
                  </template>
                  <EllipsisOutlined />
                </a-dropdown>
              </span>
            </template>
            <span>
              销售额
              <v-chart class="pie-chart" :option="pieOptions" autoresize />
            </span>
          </a-skeleton>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue';
import { InfoCircleOutlined,CaretUpOutlined,CaretDownOutlined,EllipsisOutlined  } from '@ant-design/icons-vue';
import { getRangeDate } from '@/utils/util'

const loading = ref(true);

let y: number[] = [];
for (let i = 0; i < 15; i += 1) {
  y.push(Math.ceil(Math.random()*10%9))
}
let x: string[] = getRangeDate('2024-03-01', '2024-03-15');

const visitOption = {
  color: '#2289ff',
  grid: {
    left: '-5%',
    right: '0%',
    bottom: '100%',
    containLabel: true
  },
  tooltip: {
    trigger: 'axis',
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    show: false,
    data: x
  },
  yAxis: {
    type: 'value',
    show: false,
    splitLine: {
      show: false
    }
  },
  series: [
    {
      data: y,
      type: 'line',
      smooth: true,
      lineStyle: {
        width: 0
      },
      showSymbol: false,
      areaStyle: {},
    }
  ]
};

const paymentOption = {
  color: '#2289ff',
  grid: {
    left: '-5%',
    right: '0%',
    bottom: '100%',
    containLabel: true
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  xAxis: {
    type: 'category',
    show: false,
    data: x
  },
  yAxis: {
    type: 'value',
    show: false,
    splitLine: {
      show: false
    }
  },
  series: [
    {
      data: y,
      type: 'bar'
    }
  ]
};

const tabList = [
  {
    key: 'sales',
    tab: '销售额',
  },
  {
    key: 'visit',
    tab: '访问量',
  },
];
const barTypeKey = ref('sales');

let bar_x: string[] = [];
let bar_y = [1106, 505, 845, 778, 1098, 762, 615, 345, 343, 1177, 431, 813];

for (let i = 1; i < 13; i += 1) {
  bar_x.push(`${i}月`)
}

const barOption = reactive({
  color: '#2289ff',
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  grid: {
    left: '3%',
    right: '0%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: [
    {
      type: 'category',
      data: bar_x,
      axisTick: {
        alignWithLabel: true
      }
    }
  ],
  yAxis: [
    {
      type: 'value'
    }
  ],
  series: [
    {
      name: '销售量',
      type: 'bar',
      barWidth: '50%',
      data: bar_y
    }
  ]
});

let barRank: string[] = [];
for (let i = 0; i < 7; i += 1) {
  barRank.push(`工专路${i}号店`)
}

const onTabChange = (value: string) => {
  barTypeKey.value = value;
  barOption.series[0].name = value == 'sales'? '销售量' : '访问量';
};

let search_y: number[] = [];
for (let i = 0; i < 7; i += 1) {
  search_y.push(Math.ceil(Math.random()*10%9))
}
let search_x: string[] = getRangeDate('2024-03-01', '2024-03-07');

const searchOption = {
  color: '#2289ff',
  grid: {
    left: '-6%',
    right: '0%',
    bottom: '100%',
    containLabel: true
  },
  tooltip: {
    trigger: 'axis',
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    show: false,
    data: search_x
  },
  yAxis: {
    type: 'value',
    show: false,
    splitLine: {
      show: false
    }
  },
  series: [
    {
      data: search_y,
      type: 'line',
      smooth: true,
      lineStyle: {
        width: 0
      },
      showSymbol: false,
      areaStyle: {},
    }
  ]
};

const searchColumns = [
  {
    dataIndex: 'index',
    title: '排名',
    width: 90
  },
  {
    dataIndex: 'keyword',
    title: '搜索关键词'
  },
  {
    dataIndex: 'count',
    title: '用户数',
    sorter: (a, b) => a.count - b.count
  },
  {
    dataIndex: 'range',
    title: '周涨幅',
    sorter: (a, b) => a.range - b.range
  }
];
const searchData = [];
for (let i = 0; i < 50; i += 1) {
  searchData.push({
    index: i + 1,
    keyword: `搜索关键词-${i}`,
    count: Math.floor(Math.random() * 1000),
    range: Math.floor(Math.random() * 100),
    status: Math.floor((Math.random() * 10) % 2)
  })
}

const salesType = ref('all');

const salesTabChange = (item: any) => {
  if (item.target.value == 'all') {
    pieOptions.value.series[0].data = [
      { value: 1231, name: '其他' },
      { value: 1231, name: '母婴产品' },
      { value: 2341, name: '服饰箱包' },
      { value: 3113, name: '个护健康' },
      { value: 3321, name: '食用酒水' },
      { value: 4544, name: '家用电器' }
    ]
  } else if (item.target.value == 'online') {
    pieOptions.value.series[0].data = [
      { value: 111, name: '其他' },
      { value: 121, name: '母婴产品' },
      { value: 41, name: '服饰箱包' },
      { value: 311, name: '个护健康' },
      { value: 321, name: '食用酒水' },
      { value: 244, name: '家用电器' }
    ]
  } else {
    pieOptions.value.series[0].data = [
      { value: 65, name: '其他' },
      { value: 0, name: '母婴产品' },
      { value: 255, name: '服饰箱包' },
      { value: 344, name: '个护健康' },
      { value: 188, name: '食用酒水' },
      { value: 99, name: '家用电器' }
    ]
  }
}
const pieOptions = ref({
  tooltip: {
    trigger: 'item'
  },
  series: [
    {
      type: 'pie',
      radius: ['40%', '70%'],
      data: [
        { value: 1231, name: '其他' },
        { value: 1231, name: '母婴产品' },
        { value: 2341, name: '服饰箱包' },
        { value: 3113, name: '个护健康' },
        { value: 3321, name: '食用酒水' },
        { value: 4544, name: '家用电器' }
      ],
      itemStyle: {
        normal: {
          color: function (colors) {
           var colorList = [
             '#68c738',
             '#7f6bff',
             '#d787ff',
             '#f18e56',
             '#0dcccc',
             '#2389ff'
            ];
            return colorList[colors.dataIndex];
          }
        }
      }
    }
  ]
})

setTimeout(() => {
  loading.value = false;
}, 500);
</script>

<style lang="scss" scoped>
.value {
    height: 38px;
    padding-top: 4px;
    color: rgba(0, 0, 0, 0.88);
    font-size: 30px;
    line-height: 38px;
    word-break: break-all;
}
.line-chart {
  width: 100%;
  height: 45px;
}
.payment-chart {
  width: 100%;
  height: 45px;
}
.extra-item {
  display: inline-block;

  a {
    margin-right: 25px;
    color: rgba(0, 0, 0, 0.88);
  }

  a:hover {
    color: #1890ff;
  }
}

.rank {
  padding: 0 32px 32px 72px;

  h4 {
    color: rgba(0, 0, 0, 0.88);
    font-size: 14px;
    font-weight: normal;
  }

  ul li {
    margin-top: 16px;
  }

  ul li span {
    &:first-child {
      background-color: #f5f5f5;
      border-radius: 20px;
      display: inline-block;
      font-size: 12px;
      font-weight: 600;
      margin-right: 24px;
      height: 20px;
      line-height: 20px;
      width: 20px;
      text-align: center;
    }

    &:last-child {
      float: right;
    }

    &.active {
      background-color: #314659;
      color: #fff;
    }
  }
}

.pie-chart {
  width: 725px;
  height: 350px;
}
</style>
