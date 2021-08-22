<template>
  <div class="showMessage">
    <div class="topBan">
      <div class="del" @click="delClick">
        <span>&times;</span>
      </div>
    </div>
    <div class="s_content">
      <CShowMessage
        v-for="(item, index) in messageInfos"
        :key="index"
        :messageInfo="item"
        @show_load="show_load"
        :otherInfo="getOtherInfo(item.origin)"
      ></CShowMessage>
    </div>
    <div class="banner">
      <input type="text" v-model="message" placeholder="输入内容..." />
      <button @click="sendMessage_f">发送</button>
    </div>
    <div class="mask" v-if="isMask">
      <span> 正在读取信息... </span>
    </div>
  </div>
</template>

<script>
import CShowMessage from "./c_ShowMessage.vue";
import { getMessage_f, sendMessage, getUserInfo } from "network/home.js";
import { closeLongSrc } from "network/app.js";
export default {
  name: "ShowMessage",
  data() {
    return {
      messageInfos: [],
      message: "",
      timer: null,
      isMask: true,
      otherInfos: [],
      haveitem: 1,
    };
  },
  components: {
    CShowMessage,
  },
  props: {
    friendId: {
      type: Number,
      default: 0,
    },
  },
  methods: {
    get_message() {
      getMessage_f(this.$store.state.cooike, this.friendId).then( async res => {
        let data = JSON.parse(res.replace(/'/g, '"'));
        let status = data.status;
        if (status == 1) {
          this.messageInfos = [...this.messageInfos, ...data.data];
          for(let item of data.data){
            this.haveitem = 0;
            for(let item1 of this.otherInfos){
              if (item1.id == Number(item.origin)) {
                this.haveitem = 1;
              }
            }
            //不在列表里
            if (this.haveitem == 0) {
              await this.get_user_info(item.origin);
            }
          }
        } else if (status == 0) {
          this.isMask = false;
        } else if (status == -1) {
          //登录失效
        } else {
          //关闭长链接
        }
        if (status != -2) {
          this.get_message();
        }
      });
    },
    sendMessage_f() {
      sendMessage(this.$store.state.cooike, this.friendId, this.message).then(
        (res) => {
          let data = JSON.parse(res.replace(/'/g, '"'));
          let status = data.status;
          if (status == 0) {
            console.log("失败");
          } else {
            this.messageInfos.push({
              origin: this.$store.state.user.id,
              dest: this.friendId,
              content: this.message,
              originKind: 0,
              destKind: 1,
            });
            this.message = "";
          }
        }
      );
    },
    get_user_info(origin) {
      return new Promise(resolve => {
        getUserInfo(origin).then((res) => {
          let data = JSON.parse(res.replace(/'/g, '"'));
          let status = data.status;
          if (status == 1) {
            this.otherInfos.push(data.data);
          }
          resolve('ok')
        });
      })
    },
    getOtherInfo(origin) {
      for (let item of this.otherInfos) {
        if (origin == item.id) {
          return item;
        }
      }
    },
    delClick() {
      this.$emit("delClick_message");
      closeLongSrc(this.$store.state.cooike, "/getMessage_f");
    },
    setBottom() {
      let content = document.querySelector(".s_content");
      content.scrollTop = content.scrollHeight;
    },
    show_load() {
      this.timer && clearTimeout(this.timer);
      this.timer = setTimeout(() => {
        this.setBottom();
        this.isMask = false;
      }, 100);
    },
  },
  created() {
    this.otherInfos = [];
    this.otherInfos.push(this.$store.state.user);
    closeLongSrc(this.$store.state.cooike, "/getMessage_f").then((res) => {
      this.get_message();
    });
  },
};
</script>

<style>
.showMessage {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 45%;
  max-width: 600px;
  height: 70%;
  transform: translate(-50%, -50%);
  background-color: rgba(0, 0, 0, 0.932);
}
.showMessage .topBan {
  width: 100%;
  height: 6%;
  text-align: right;
}
.showMessage .topBan .del {
  margin-right: 21px;
  font-size: 28px;
  color: rgba(240, 248, 255, 0.726);
}
.showMessage .s_content {
  width: 100%;
  height: 79%;
  overflow: auto;
}
.showMessage .banner {
  width: 100%;
  height: 15%;
  text-align: center;
  padding: 5px 20px;
  background-color: rgba(0, 0, 0, 0.932);
}
.showMessage .banner input {
  margin-right: 10px;
  width: 80%;
  max-width: 400px;
  height: 60%;
  border-radius: 10px;
  padding-left: 15px;
  background-color: rgba(255, 255, 255, 0.87);
}
.showMessage .banner button {
  width: 13%;
  height: 60%;
  border-radius: 13px;
  background-color: rgb(184, 231, 245);
}
.showMessage .mask {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.973);
  text-align: center;
  padding-top: 50%;
  color: #fff;
}
</style>