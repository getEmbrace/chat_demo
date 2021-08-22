import Vue from 'vue'
import Vuex from 'vuex'
import {setActive, closeLongSrc} from 'network/app.js'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: {},
    cooike: '4d5gtg84b5sbbbcbfgrg',
    friends: [],
    localStream: null
  },
  mutations: {
    setCooike(state, payload){
      //切换用户时调用closeLongSrc结束长链接
      if(state.cooike != '4d5gtg84b5sbbbcbfgrg'){
        closeLongSrc(state.cooike, '/getFriends')
        closeLongSrc(state.cooike, '/getMessage_f')
        setActive(state.cooike, 0)
      }
      state.cooike = payload
      localStorage.setItem("userCooike", state.cooike);
    },
    setFriends(state, payload){
      state.friends = payload
    },
    setUser(state, payload){
      state.user = payload
    },
    setLocalStream(state, payload){
      state.localStream = payload
    },
  },
  actions: {
  },
  modules: {
  }
})
