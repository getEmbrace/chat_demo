<template>
  <div class="inputInfo">
    <div class="login" v-if="isLogin">
      <input type="text" placeholder="请输入用户名" v-model="username" />
      <input type="text" placeholder="请输入密码" v-model="password" />
      <button @click="btnClick_login">登录</button>
      <button @click="btnClick_reset">重置</button>
    </div>
    <div class="regist" v-if="!isLogin">
      <input type="text" placeholder="请输入用户名" v-model="username" />
      <input type="text" placeholder="请输入密码" v-model="password" />
      <input type="text" placeholder="请输入邮箱" v-model="email" />
      <button @click="btnClick_regist">提交</button>
      <button @click="btnClick_reset">重置</button>
    </div>
    <div class="change" @click="click_change">
      <span>{{ changeTitle }}</span>
    </div>
    <div class="grement">
      <span>提示：登录即默认同意并明了免责声明，一切责任与本网站无关</span>
    </div>
  </div>
</template>

<script>
import { login, regist } from "network/login.js";

export default {
  name: "InputInfo",
  data() {
    return {
      username: "",
      password: "",
      email: "",
      isLogin: true,
      loginData: null,
    };
  },
  computed: {
    changeTitle() {
      return this.isLogin ? "注册" : "登录";
    },
  },
  methods: {
    btnClick_login() {
      login(this.username, this.password).then((res) => {
        let message;
        let loginData = JSON.parse(res.replace(/'/g, '"'));
        let status = loginData.status;
        if (status == 1) {
          this.$store.commit("setCooike", loginData.data.cooike);
          message = "登录成功，即将跳转首页...";
        } else if (status == 0) {
          message = "登录失败，用户名或密码错误...";
        } else {
          message = "登录失败，请重新尝试...";
        }
        this.$bus.$emit("sendMessage", [
          status,
          message,
          () => {
            this.$router.push("/home").catch((err) => {
              console.log("重复点击:", err);
            });
          },
        ]);
      });
    },
    btnClick_reset() {
      this.username = "";
      this.password = "";
      this.email = "";
    },
    click_change() {
      this.isLogin = !this.isLogin;
    },
    btnClick_regist() {
      regist(this.username, this.password, this.email).then((res) => {
        let message;
        let registData = JSON.parse(res.replace(/'/g, '"'));
        let status = registData.status;
        if (status == 1) {
          this.$store.commit("setCooike", registData.data.cooike);
          message = "注册成功，即将跳转首页...";
        } else if (status == 0) {
          message = "注册失败，用户名重复...";
        } else {
          message = "注册失败，请重新尝试...";
        }
        this.$bus.$emit("sendMessage", [
          status,
          message,
          () => {
            this.$router.push("/home").catch((err) => {
              console.log("重复点击:", err);
            });
          },
        ]);
      });
    },
  },
};
</script>

<style>
.inputInfo {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 40%;
  height: 45%;
  transform: translate(-50%, -50%);
  transition: all 2s;
  /* overflow: hidden; */
  z-index: 2;
  border-radius: 20px;
  background-color: #000;
}
.inputInfo .login input {
  position: absolute;
  top: 13%;
  left: 50%;
  padding: 0 20px;
  width: 370px;
  height: 50px;
  transform: translate(-50%, -50%);
  border-radius: 20px;
  background-color: rgba(255, 255, 255, 0.829);
}
.inputInfo .login input:nth-child(2) {
  top: 30%;
}
.inputInfo .login button {
  position: absolute;
  top: 62%;
  left: 50%;
  width: 80px;
  height: 45px;
  transform: translateX(50%);
  border-radius: 15px;
  background-color: rgba(255, 255, 255, 0.829);
}
.inputInfo .login button:nth-child(3) {
  background-color: rgba(148, 205, 228, 0.76);
  transform: translateX(-150%);
}
.inputInfo .regist input {
  position: absolute;
  top: 13%;
  left: 50%;
  padding: 0 20px;
  width: 370px;
  height: 45px;
  transform: translate(-50%, -50%);
  border-radius: 20px;
  background-color: rgba(255, 255, 255, 0.829);
}
.inputInfo .regist input:nth-child(2) {
  top: 28%;
}
.inputInfo .regist input:nth-child(3) {
  top: 43%;
}
.inputInfo .regist button {
  position: absolute;
  top: 62%;
  left: 50%;
  width: 80px;
  height: 45px;
  transform: translateX(50%);
  border-radius: 15px;
  background-color: rgba(255, 255, 255, 0.829);
}
.inputInfo .regist button:nth-child(4) {
  background-color: rgba(148, 205, 228, 0.76);
  transform: translateX(-150%);
}
.inputInfo .grement {
  position: absolute;
  right: -50%;
  top: 120%;
  width: 260px;
}
.inputInfo .change {
  position: absolute;
  bottom: 20px;
  right: 5px;
  width: 35px;
  color: rgba(127, 255, 212, 0.658);
}
</style>
