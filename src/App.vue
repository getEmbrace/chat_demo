<template>
  <div id="app">
    <router-view />
    <MainCut></MainCut>
  </div>
</template>

<script>
import MainCut from "components/content/MainCut.vue";
import { setActive, closeLongSrc } from "network/app.js";

export default {
  name: "App",
  components: {
    MainCut,
  },
  created() {
    //在页面加载时读取localStorage里的状态信息
    if (localStorage.getItem("userCooike")) {
      closeLongSrc(localStorage.getItem("userCooike"), "/getFriends");
      closeLongSrc(localStorage.getItem("userCooike"), "/getMessage_f");
      this.$store.commit("setCooike", localStorage.getItem("userCooike"));  
    }
  },
  mounted() {
    //监听页面卸载
    window.addEventListener("visibilitychange", () => {
      let cooike = this.$store.state.cooike
      if (document.visibilityState === "hidden") {
        setActive(cooike, 0);
      } else if (document.visibilityState === "visible") {
        setActive(cooike, 1);
        closeLongSrc(cooike, "/getFriends");
        closeLongSrc(cooike, "/sendMessage_f");
      }
    }),
      window.addEventListener("beforeunload", () => {
        //监听浏览器关闭事件发送fetch请求保证握手成功
        fetch("http://127.0.0.1:8083/setActive", {
          method: "POST",
          body: JSON.stringify({ cooike: this.$store.state.cooike, active: 0 }),
          keepalive: true,
        });
        fetch("http://127.0.0.1:8083/closeLongSrc", {
          method: "POST",
          body: JSON.stringify({ cooike: this.$store.state.cooike, url: '/getFriends' }),
          keepalive: true,
        });
        fetch("http://127.0.0.1:8083/closeLongSrc", {
          method: "POST",
          body: JSON.stringify({ cooike: this.$store.state.cooike, url: '/sendMessage_f' }),
          keepalive: true,
        });
      }),
      window.addEventListener("load", () => {
        let cooike = this.$store.state.cooike;
        setActive(cooike, 1);
        closeLongSrc(cooike, "/getFriends");
        closeLongSrc(cooike, "/sendMessage_f");
      });
  },
};
</script>

<style>
@import "assets/css/base.css";
input:focus {
  outline: none;
}
</style>
