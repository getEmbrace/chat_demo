<template>
  <div class="cut_item" @click="itemClick">
    <div>
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    path: {
      type: String,
      defualt: "/home",
    },
  },
  methods: {
    itemClick() {
      if (this.$route.path !== this.path) {
        this.$router.push(this.path).catch((err) => {
          console.log("重复点击...");
        });
      }

    },
  },
};
</script>

<style scoped>
.cut_item {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 0px;
  height: 0px;
  border: 1px solid rgba(224, 208, 208, 0.24);
  background-color: rgba(0, 183, 255, 0.336);
  transform-origin: left top;
  transition: all 1s;
}
.cut_item:hover {
  background-color: aqua;
}
.cut_item div {
  display: none;
  position: absolute;
  left: 30px;
  top: 30px;
  text-align: center;
  transform-origin: 50% 50%;
}
</style>