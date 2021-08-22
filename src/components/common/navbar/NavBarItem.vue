<template>
  <div class="navBarItem" @click="itemClick">
    <div class="itemImg">
      <slot name="img"></slot>
      <div class="tip">
        <TipMessage :messageCount="messageCount"></TipMessage>
      </div>
    </div>
    <div class="itemName"><slot name="name"></slot></div>
    <div class="itemStatus"><span :style="{'backgroundColor': getColor}"></span></div>
  </div>
</template>

<script>
import TipMessage from "../TipMessage.vue"
export default {
  name: "NavBarItem",
  data(){
    return {
      color: {
        1: 'green',
        0: 'red',
        2: 'yellow'
      }
    }
  },
  components: {
    TipMessage
  },
  props: {
    status: {
      type: Number,
      default: 0,
    },
    uid: {
      type: Number,
      default: 0
    },
    messageCount: {
      type: Number,
      default: 0
    }
  },
  computed: {
    getColor(){
      return this.color[this.status]
    },
  },
  methods: {
    itemClick(){
      this.$bus.$emit('friendItemClick', this.uid)
    }
  }
};
</script>

<style>
.navBarItem {
  display: flex;
  padding-top: 0px;
  height: calc(100%);
  width: 100%;
  border-bottom: 1px solid ;
}
.navBarItem:hover {
  background-color: rgba(179, 177, 204, 0.699);
}
.itemImg {
  position: relative;
  width: 20%;
  height: 90%;
  margin-left: 10px;
  margin-top: 5px;
}
.itemImg img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}
.itemImg .tip {
  position: absolute;
  top: -1px;
  right: calc(-100%*0.45);
  width: 45%;
  height: 45%;
}
.itemName {
  flex: 1;
  position: relative;
}
.itemName span {
  position: absolute;
  top: 57%;
  left: 50%;
  font-size: 15px;
  color: rgba(0, 0, 0, 0.808);
  transform: translate(-50%, -50%);
}
.itemStatus {
  margin-top: 5px;
  position: relative;
  width: 30%;
}
.itemStatus span {
  position: absolute;
  display: block;
  left: 50%;
  top: 50%;
  width: 15px;
  height: 15px;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  background-color: red;
}
</style>