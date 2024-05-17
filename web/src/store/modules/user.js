import { getCurrentUserInfo } from '@/api/user'

const user = {
  state: {
    basicInfo: {},
    routeList: [],
    hasGetRoute: false
  },
  mutations: {
    setRoute(state, routers) {
      state.routeList = routers
      state.hasGetRoute = true
    },
    setAvatar(state, avatar) {
      state.basicInfo.avatar = avatar
    }
  },
  actions: {
    getUserInfo({ commit, state }) {
      return new Promise((resolve) => {
        getCurrentUserInfo().then(response => {
          const result = response.data;
          const routers = result.data.menus;
          delete result.data.menus;
          commit('setRoute', routers)
          state.basicInfo = Object.assign(state.basicInfo || {}, result.data);
          resolve()
        }).catch(error => {
          console.log(error)
        })
      })
    },

    clearUserInfo({ state }) {
      state.basicInfo = {};
      state.routeList = [];
      state.hasGetRoute = false;
    }
  }
}

export default user