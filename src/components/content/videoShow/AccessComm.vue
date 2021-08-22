<template>
  <div class="accessComm" v-if="Object.keys(UInfo).length != 0">
    <div class="friend_img">
      <img :src="UInfo.picture" alt="" />
    </div>
    <div class="hint">
      <span>{{ UInfo.username }} 发来链接请求...</span>
    </div>
    <div class="operate">
      <button class="access" @click="btn_access">接受</button>
      <button class="refuse" @click="btn_refuse">拒绝</button>
    </div>
  </div>
</template>

<script>
import {
  sendMessage,
  commHouse,
  setHouseMessage,
  commWebsocket,
} from "network/home.js";
import { setActive, closeLongSrc } from "network/app.js";
export default {
  data() {
    return {
      count: 0,
      recorder: null,
      socket: null
    };
  },
  props: {
    UInfo: {
      type: Object,
      default() {
        return {};
      },
    },
  },
  methods: {
    btn_refuse() {
      this.commClick_refuse();
      this.$emit("delClick_comm");
    },
    btn_access() {
      this.commClick_access();
    },
    commClick_refuse() {
      // 发送拒绝消息
      let todayStr = this.$date();
      sendMessage(
        this.$store.state.cooike,
        this.UInfo.id,
        "refuseComm/" + todayStr
      );
      // 改变状态
      setActive(this.$store.state.cooike, 1).then((res) => {
        this.$bus.$emit("refreshMine");
      });
    },
    commClick_access() {
      // 发送接受消息
      let todayStr = this.$date();
      sendMessage(
        this.$store.state.cooike,
        this.UInfo.id,
        "accessComm/" + todayStr
      ).then((res) => {
        let data = JSON.parse(res.replace(/'/g, '"'));
        let status = data.status;
        console.log(status);
        if (status == 1) {
          // 开启通讯房间
          // this.comm_house();
          this.comm_websocket()
          console.log("接收方: 链接开始...");
        }
      });
    },
    comm_websocket() {
      this.socket = commWebsocket(this.$store.state.cooike, this.UInfo.id, (ws) => {
        ws.onmessage = (ev) => {
          let data = ev.data;
          let message = new Blob([data], { type: "video/webm;codecs=vp8,opus" });
          this.$bus.$emit("setVideoData", message);
        };
        ws.onclose = (ev) => {
          this.$bus.$emit("closeCommVideo");
          this.$bus.$emit("sendMessage", [0, "链接断开..."]);
        };
        this.$emit("delClick_comm");
        this.$bus.$emit("openCommVideo");
        this.set_house_message(ws);
      });
    },
    comm_house() {
      commHouse(this.$store.state.cooike, this.UInfo.id, this.houseNum).then(
        async (res) => {
          let data = 0;
          let status;
          if (res[1] == 1) {
            data = res[0];
            status = 3;
          } else {
            let content = await this.blobToStr(res);
            data = JSON.parse(content.replace(/'/g, '"'));
            status = data.status;
          }
          // console.log(222, status);
          if (status == 1) {
            console.log("开启房间...");
            this.houseNum = data.data.houseNum;
            this.$emit("delClick_comm");
            this.$bus.$emit("openCommVideo");
            this.comm_house();
          } else if (status == 2) {
            console.log("加入房间...");
            this.houseNum = data.data.houseNum;
            this.set_house_message();
            this.count++;
            this.$emit("delClick_comm");
            // 打开CommVideo组件
            this.$bus.$emit("openCommVideo");
            this.comm_house();
          } else if (status == 3) {
            let message;
            if (res[1] == 1) {
              message = new Blob([data], { type: "video/webm;codecs=vp8" });
              this.$bus.$emit("setVideoData", message);
            } else {
              message = data.data;
            }
            // console.log("通讯中");
            if (message == "close") {
              console.log("close");
              this.$bus.$emit("closeCommVideo");
              this.$bus.$emit("sendMessage", [0, "链接断开..."]);
            } else {
              this.comm_house();
            }
            // 辨别是否需要打开摄像头
            if (this.count == 0) {
              this.set_house_message();
              this.count++;
            }
          } else if (status == -2) {
            console.log("退出房间...");
            this.$bus.$emit("closeCommVideo");
          }
        }
      );
    },
    set_house_message(ws) {
      let timer;
      navigator.mediaDevices
        .getUserMedia({ video: true, audio: false })
        .then((stream) => {
          this.$store.commit("setLocalStream", stream);
          this.$bus.$emit("refreshSelf");
          var options = {
            audioBitsPerSecond: 128000,
            videoBitsPerSecond: 2500000,
            mimeType: "video/webm;codecs=vp8",
          };
          let recorder = new MediaRecorder(stream, options);
          recorder.ondataavailable = (event) => {
            console.log('accese');
            //从事件中获取Blob
            let blob = event.data;
            // 并将该blob发送到服务器...
            // setHouseMessage(
            //   this.$store.state.cooike,
            //   this.UInfo.id,
            //   this.houseNum,
            //   blob
            // ).catch((err) => {
            //   // 发送失败
            //   setTimeout(() => {
            //     recorder.stop();
            //   }, 500);
            //   console.log("errr");
            // });
            ws.send(blob)
          };
          //每秒钟使数据可用事件触发
          recorder.start();
          timer = setInterval(() => {
            if (stream.active == false) {
              clearInterval(timer);
              this.$bus.$emit("closeSelf");
            } else {
              recorder.stop();
              recorder.start();
            }
          }, 500);
        });
    },
    blobToStr(blob) {
      return new Promise((resolve) => {
        let content;
        let reader = new FileReader();
        reader.onload = function (e) {
          content = reader.result;
          resolve(content);
        };
        reader.readAsText(blob);
      });
    },
  },
  created() {
    closeLongSrc(this.$store.state.cooike, "/commHouse");
    this.$bus.$on("closeComm_self", (res) => {
      setHouseMessage(
        this.$store.state.cooike,
        this.UInfo.id,
        this.houseNum,
        "close"
      );
      setHouseMessage(
        this.$store.state.cooike,
        this.$store.state.user.id,
        this.houseNum,
        "close"
      );
    });
    this.$bus.$on('closeComm_self_ws', () =>{
      this.socket.close()
    })
  },
};
</script>

<style>
.accessComm {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 500px;
  height: 300px;
  transform: translate(-50%, -50%);
  overflow: hidden;
  background-color: #000;
}
.accessComm .friend_img {
  position: absolute;
  left: 50%;
  top: 10px;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  transform: translateX(-50%);
  background-color: rgba(15, 15, 15);
}
.accessComm .friend_img img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}
.accessComm .hint {
  position: absolute;
  left: 50%;
  top: 120px;
  width: 200px;
  transform: translateX(-50%);
  text-align: center;
  /* background-color: rgba(15, 15, 15); */
}
.accessComm .hint span {
  font-size: 17px;
  color: rgba(255, 255, 255, 0.733);
}
.accessComm .operate {
  position: absolute;
  left: 50%;
  bottom: 20px;
  width: 250px;
  height: 100px;
  transform: translateX(-50%);
  /* background-color: rgba(15, 15, 15); */
}
.accessComm .operate button {
  position: absolute;
  top: 50%;
  width: 100px;
  height: 45px;
  border-radius: 20px;
  transform: translateY(-50%);
  background-color: rgba(255, 255, 255, 0.753);
}
.accessComm .operate .access {
  left: 0%;
  background-color: rgb(166, 220, 241);
}
.accessComm .operate .refuse {
  right: 0%;
}
</style>