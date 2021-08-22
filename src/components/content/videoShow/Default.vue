<template>
  <div class="video_default">
    <div class="content">
      <div class="operate">
        <input type="text" v-model="uid" placeholder="请输入用户id" />
        <button @click="btnClickCommit">发送</button>
        <button @click="btnClickReset">清空</button>
      </div>
      <div class="prompt">
        请登录以获得更好的体验 or 以匿名方式发送通讯请求。。。
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "VideoDefault",
  data(){
    return {
      uid: ''
    }
  },
  methods: {
    btnClickCommit(){
      this.$emit('tryComm', this.uid)
    },
    btnClickReset(){
      this.uid = ''
    }
  },
};
</script>

<style scoped>
.video_default {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: rgba(15, 15, 15, 0.904);
}
.video_default .content {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
.prompt {
  width: 350px;
  font-size: 15px;
  color: rgba(248, 246, 246, 0.212);
}
.operate {
  width: 309px;
  height: 120px;
}
.operate input {
  padding-left: 15px;
  width: 100%;
  height: 50px;
  border-radius: 20px;
  background-color: rgba(255, 255, 255, 0.877);
}
.operate button {
  margin-top: 10px;
  margin-left: 35px;
  width: 100px;
  height: 45px;
  border-radius: 20px;
  background-color: rgba(255, 255, 255, 0.753);
}
.operate button:nth-child(2){
  background-color: rgba(148, 205, 228, 0.76);
}
</style>