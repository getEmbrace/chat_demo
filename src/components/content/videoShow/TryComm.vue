<template>
  <div class="tryComm">
    <div class="comm_content">
      <div class="loading">
        <div class="mask"></div>
        <div class="mask1"></div>
      </div>
      <div class="comm_title">
        <span>正在请求中，请稍候 {{ timeCount }}秒...</span>
      </div>
      <div class="operate" @click="delClick">
        <span>&times;</span>
      </div>
    </div>
  </div>
</template>

<script>
import {
  sendMessage,
  startLink_v,
  commHouse,
  setHouseMessage,
  commWebsocket
} from "network/home.js";
import { closeLongSrc, setActive } from "network/app.js";

export default {
  name: "TryComm",
  data() {
    return {
      timer: null,
      timer1: null,
      addDeg: 8,
      interval: 20,
      timeCount: 0,
      houseNum: null,
      count: 0,
      socket: null
    };
  },
  props: {
    uid: {
      type: Number,
      default: 0,
    },
  },
  methods: {
    startloading() {
      let deg = 0;
      this.timeCount = 0;
      let loading = document.querySelector(".loading");
      this.timer = setInterval(() => {
        deg += this.addDeg;
        loading.style.transform =
          "translate(-50%, -50%) rotate(" + deg + "deg)";
        if (deg == 360) deg = 0;
      }, this.interval);
      this.timer1 = setInterval(() => {
        this.timeCount += 1;
      }, 1000);
    },
    delClick() {
      closeLongSrc(this.$store.state.cooike, "/commHouse");
      this.$emit("delClick_tComm");
    },
    try_commit() {
      //向服务器发送链接请求
      this.start_link_v();
    },
    // 开启长链接
    start_link_v() {
      startLink_v(this.$store.state.cooike, this.uid).then((res) => {
        let data = JSON.parse(res.replace(/'/g, '"'));
        let status = data.status;
        if (status == 1) {
          // 就绪开始尝试链接
          this.quiry_message();
        } else if (status == 2) {
          // 对方拒绝链接，关闭长链接，弹出提示框, 改变状态
          let message = "对方拒绝链接...";
          closeLongSrc(this.$store.state.cooike, "/startLink_v");
          this.$bus.$emit("sendMessage", [status, message]);
          setActive(this.$store.state.cooike, 1).then((res) => {
            this.$bus.$emit("refreshMine");
          });
          this.delClick();
        } else if (status == 3) {
          // 对方接受链接
          console.log("请求方: 链接成功开启链接通道...");
          // 改变状态
          setActive(this.$store.state.cooike, 2).then((res) => {
            this.$bus.$emit("refreshMine");
          });
          // 关闭询问链接
          closeLongSrc(this.$store.state.cooike, "/startLink_v");
          // 开启通讯房间
          this.comm_websocket()
        }
      });
    },
    comm_websocket(){
      this.socket = commWebsocket(this.$store.state.cooike, this.uid, (ws) => {
        ws.onmessage = (ev) => {
          let data = ev.data
          let message = new Blob([data], { type: "video/webm;codecs=vp8,opus" });
          this.$bus.$emit("setVideoData", message);
        }
        ws.onclose = (ev) => {
          this.$bus.$emit("closeCommVideo");
          this.$bus.$emit("sendMessage", [0, "链接断开..."]);
        }
        this.$emit("delClick_tComm");
        this.$bus.$emit("openCommVideo");
        this.set_house_message(ws);
      })
    },
    comm_house() {
      commHouse(this.$store.state.cooike, this.uid, this.houseNum).then(
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
          if (status == 1) {
            console.log("开启房间...");
            this.houseNum = data.data.houseNum;
            this.$emit("delClick_tComm");
            this.$bus.$emit("openCommVideo");
            // console.log(this.houseNum);
            this.comm_house();
          } else if (status == 2) {
            console.log("加入房间...");
            // 记录房间号
            this.houseNum = data.data.houseNum;
            // 发送通讯消息
            this.set_house_message();
            this.$emit("delClick_tComm");
            this.$bus.$emit("openCommVideo");
            this.count++;
            this.comm_house();
          } else if (status == 3) {
            let message;
            if (res[1] == 1) {
              message = new Blob([data], { type: "video/webm;codecs=vp8,opus" });
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
    quiry_message() {
      let todayStr = this.$date();
      sendMessage(
        this.$store.state.cooike,
        this.uid,
        "tryComm/" + todayStr
      ).then((res) => {
        let message;
        let data = JSON.parse(res.replace(/'/g, '"'));
        let status = data.status;
        if (status != 1) {
          // 关闭长链接
          closeLongSrc(this.$store.state.cooike, "/startLink_v");
          if (status == "0") {
            message = "用户不存在，请求失败...";
          } else if (status == "2") {
            message = "用户为离线状态，转为未读消息...";
          } else if (status == "3") {
            message = "用户忙碌，转为未读消息...";
          }
          // 弹出提示框
          this.$bus.$emit("sendMessage", [status, message]);
          this.delClick();
        } else {
          this.start_link_v();
        }
      });
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
            console.log('try');
            //从事件中获取Blob
            let blob = event.data
            // 并将该blob发送到服务器...
            // setHouseMessage(
            //   this.$store.state.cooike,
            //   this.uid,
            //   this.houseNum,
            //   blob
            // ).catch((res) => {
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
            if(stream.active == false){
              clearInterval(timer)
              this.$bus.$emit('closeSelf')
            }else{
              recorder.stop();
              recorder.start();
            }
          }, 400);
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
  mounted() {
    this.try_commit();
    this.startloading();
  },
  created() {
    closeLongSrc(this.$store.state.cooike, "/commHouse");
    this.$bus.$on("closeComm_self", (res) => {
      console.log(456);
      setHouseMessage(
        this.$store.state.cooike,
        this.uid,
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
  destoryed() {
    clearInterval(this.timer);
    clearInterval(this.timer1);
  },
};
</script>

<style>
.tryComm {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: #000;
}
.tryComm .comm_content {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 500px;
  height: 300px;
  transform: translate(-50%, -50%);
  background-color: rgba(15, 15, 15);
}
.comm_content .loading {
  position: relative;
  left: 50%;
  top: 30%;
  width: 140px;
  height: 140px;
  overflow: hidden;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background-image: linear-gradient(
    0deg,
    rgb(30, 218, 224) 1%,
    rgb(15, 15, 15) 99%
  );
}
.comm_content .loading .mask {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 90%;
  height: 90%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background-color: rgb(15, 15, 15);
  z-index: 1;
}
.comm_content .loading .mask1 {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 100%;
  height: 100%;
  transform-origin: right bottom;
  transform: rotate(-70deg) skew(-50deg);
  background-color: rgb(15, 15, 15);
  z-index: 2;
}
.comm_content .comm_title {
  position: absolute;
  top: 70%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
}
.comm_content .operate {
  position: absolute;
  top: 5%;
  right: 10%;
  font-size: 35px;
}
</style>