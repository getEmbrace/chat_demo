<template>
  <div id="mineInfo">
    <div class="mineInfo">
      <div class="mine_img">
        <img :src="$path + mineInfo.picture" alt="">
      </div>
      <div class="other">
        <div class="name">
          <span>{{mineInfo.username}}</span>
        </div>
        <div class="status" :style="{backgroundColor: getColor}"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "MineInfo",
  props: {
    mineInfo: {
      type: Object,
      default(){
        return {}
      }
    }
  },
  computed: {
    getColor(){
      this.$store.commit('setUser', this.mineInfo)
      return this.mineInfo.active == 1 ? 'green': this.mineInfo.active == 0 ? 'red': 'yellow'
    }
  },
};
</script>

<style>
.mineInfo {
  display: flex;
  width: 97%;
  height: 100%;
  border: 1px solid;
  overflow: hidden;
  border-radius: 0 30px 30px 0;
  /* background-color: pink; */
}
.mine_img {
  flex: 1;
  position: relative;
}
.mine_img img {
  position: absolute;
  top: 50%;
  left: 50%;
  width: calc(100% * 0.63);
  transform: translate(-50%, -50%);
  border-radius: 50%;
}
.other {
  width: calc(100% * 0.50);
}
.other .name {
  position: relative;
  width: 100%;
  height: 50%;
}
.other .name span {
  position: absolute;
  top: 50%;
  font-size: 26px;
  color: rgba(0, 0, 0, 0.932);
}
.other .status {
  position: relative;
  top: calc(100% * 0.20);
  width: 20px;
  height: 20px;
  border-radius: 50%;
}
</style>