<template>
  <div class="tip_message" v-if="messageCount != '0'">
    <span>{{messageCount}}</span>
  </div>
</template>

<script>
export default {
  name: "TipMessage",
  props: {
    messageCount: {
      type: Number,
      default: 0
    }
  }
}
</script>

<style>
  .tip_message{
    position: relative;
    width: 100%;
    height: 100%;
    border-radius: 50% 50% 50% 0;
    transform: rotate(0deg);
    background-color: red;
  }
  .tip_message span {
    position: absolute;
    top: 50%;
    left: 50%;
    color: #fff;
    font-size: small;
    transform: translate(-50%, -50%);
  }
</style>