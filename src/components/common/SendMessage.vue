<template>
  <div class="send_message" v-if="isShow">
    <div class="message">
      {{ message }}
    </div>
    <div class="time_count">{{ timeCount }}秒...</div>
  </div>
</template>

<script>
export default {
  name: "SebdMessage",
  data() {
    return {
      message: "test",
      isShow: false,
      timeCount: 0,
      timer: null,
      setTime: 2
    };
  },
  created() {
    //data为数组:[status, message [, funBack]]
    //只有status=1 时回调函数才执行
    this.$bus.$on("sendMessage", (data) => {
      this.message = data[1];
      this.isShow = true;
      this.timeCount = this.setTime;
      this.setTimeCount()
      let t = (this.timeCount+1) * 1000
      setTimeout(() => {
        if (data[0] == 1) {
          if(data.length == 3){
            data[2]();
          }
        }
        this.isShow = false;
      }, t);
    });
  },
  methods: {
    setTimeCount() {
      if(this.timer) {
        clearInterval(this.timer)
      }
      this.timer = setInterval(() => {
        if (this.timeCount == 0) {
          clearInterval(this.timer)
        }
        this.timeCount--;
      }, 1000);
    },
  },
  destoryed(){
    console.log(78899);
  }
};
</script>

<style scoped>
.send_message {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 40%;
  height: 45%;
  transform: translate(-50%, -50%);
  border-radius: 25px;
  background-color: rgba(0, 0, 0, 0.932);
  z-index: 888;
}

.message {
  position: absolute;
  top: 50%;
  left: 50%;
  color: rgba(255, 255, 255, 0.911);
  font-size: 20px;
  transform: translate(-50%, -50%);
}
.time_count {
  position: absolute;
  bottom: 10%;
  right: 10%;
  color: rgba(255, 255, 255, 0.911);
  font-size: 18px;
}
</style>
