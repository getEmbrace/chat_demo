<template>
  <div class="c_ShowMessage" v-if="Object.keys(messageInfo).length != 0">
    <div class="left">
      <img v-if="!isMyMessage" @load="show_load" :src="$path + otherInfo.picture" alt="" />
    </div>
    <div class="center" :class="{myCenter: isMyMessage}">
      <div class="m_name">
        <span>{{ otherInfo.username }}</span>
      </div>
      <div class="m_content">
        <span>{{ messageInfo.content }}</span>
      </div>
    </div>
    <div class="right">
      <img v-if="isMyMessage" @load="show_load"  :src="$path + otherInfo.picture" alt="" />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    messageInfo: {
      type: Object,
      default() {
        return {};
      },
    },
    otherInfo: {
      type: Object,
      default() {
        return {};
      },
    },
  },
  computed: {
    isMyMessage(){
      let mineId =  this.$store.state.user.id
      return this.otherInfo.id == mineId
    }
  },
  methods: {
    show_load(){
      // console.log(456);
      this.$emit('show_load')
    }
  },
  mounted(){
    this.$emit('show_load')
  },
};
</script>

<style>
.c_ShowMessage {
  display: flex;
  margin-bottom: 20px;
  width: 100%;
  height: auto;
}
.c_ShowMessage .left {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}
.c_ShowMessage .left img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}
.c_ShowMessage .center {
  flex: 1;
  width: 60px;
  height: auto;
  padding: 0 10px;
}
.c_ShowMessage .myCenter {
  flex: 1;
  width: 60px;
  height: auto;
  padding: 0 10px;
  text-align: right;
}
.c_ShowMessage .myCenter .m_content {
  border-color: rgba(127, 255, 217, 0.733);
}
.c_ShowMessage .m_name {
  height: 30px;
  font-size: 15px;
  padding-left: 5px;
  line-height: 36px;
  border-radius: 2px;
  color: rgba(255, 255, 255, 0.719);
  /* background-color: #fff; */
}
.c_ShowMessage .m_content {
  display: inline-block;
  *display: inline;
  *zoom: 1;
  max-width: 40%;
  margin-top: 3px;
  padding: 10px 5px;
  border-radius: 8px;
  border: 1px solid #fff;
  color: #fff;
  font-size: 14px;
  text-align: left;
  /* 文字溢出换行 */
  word-wrap: break-word;
  word-break: break-all;
}
.c_ShowMessage .right {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}
.c_ShowMessage .right img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}
</style>