<template>
  <div class="login_default">
    <div class="prompt" :class="{prompt_next: isNext}">
      <span>提示：因为有你，所以遇见。</span>
      <span v-show="!isNext" @click="next">继续...</span>
    </div>
    <InputInfo v-show="isNext"></InputInfo>
  </div>
</template>

<script>
import InputInfo from "./InputInfo.vue";
export default {
  name: 'LoginDefault',
  data(){
    return {
      isNext: false
    }
  },
  components: {
    InputInfo
  },
  methods: {
    next(){
      this.isNext = true
    }
  }
};
</script>

<style scoped>
.login_default {
  position: relative;
  height: 100%;
  width: 100%;
}
.prompt {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 335px;
  height: 125px;
  transition: all 2s;
  /* background-color: pink; */
}
.prompt_next {
  position: absolute;
  left: 50%;
  top: 20%;
  transform: translate(-50%, -50%);
  width: 335px;
  height: 125px;
  transition: all 2s;
  z-index: 1;
  /* background-color: pink; */
}
.prompt span:nth-child(1) {
  position: absolute;
  left: 0;
  font-size: 20px;
  color: #fff;
}
.login_default span:nth-child(2) {
  position: absolute;
  top: 80px;
  right: 15px;
  color: aquamarine;
}
</style>