<template>
  <div
    class="mainCut"
    @click="CutClick(isMoving)"
    :class="{ CutClick: isOpen }"
  >
    <div class="mainCutItem">
      <slot></slot>
    </div>
    <div class="cut_title">{{ $route.name }}</div>
  </div>
</template>

<script scoped>
export default {
  name: "MainCut",
  data() {
    return {
      isOpen: false,
      isMoving: false,
      timer: null,
      isTop: false,
      isLeft: false,
    };
  },
  methods: {
    openCircle() {
      let title = document.querySelector(".cut_title");
      title.style.transform = "rotate(90deg) translate(-120%, 50%)";
      let cutItem = document.querySelectorAll(".cut_item");
      let deg = 180 / cutItem.length;
      let deg1 = deg;
      let backDeg = (deg1 * cutItem.length - 180) / 2;
      cutItem.forEach((item, index) => {
        item.style.width = "200px";
        item.style.height = "200px";
        item.style.transform =
          "rotate(" +(deg1 * index - backDeg) +"deg)  skew(" +(90 - deg1) +"deg, 0deg)";
        item.querySelector("div").style.display = "block";
        item.querySelector("div").style.transform =
          "skew(" +
          -(90 - deg1) +
          "deg, 0deg) rotate(" +
          (90 + deg1 / 2) +
          "deg)  scale(1)";
      });

      //变化后对齐
      let mainCut = document.querySelector(".mainCut");
      let offsetX = (Number(mainCut.style.left.replace('px', '')) - 100)
      let offsetY = (Number(mainCut.style.top.replace('px', '')) - 100)
      if(offsetX <= 0 && offsetY <= 0){
        this.isTop = true
        this.isLeft = true
        mainCut.style.left = 0 + "px";
        mainCut.style.top = 0 + "px";
      }
      else if(offsetY <= 0){
        this.isTop = true
        mainCut.style.left = offsetX + "px";
        mainCut.style.top = 0 + "px";
      }
      else if(offsetX <= 0){
        this.isLeft = true
        mainCut.style.left = 0 + "px";
        mainCut.style.top = offsetY + "px";
      }
      else{
        mainCut.style.left = offsetX  + "px";
        mainCut.style.top = offsetY + "px";
      }
    },

    closeCiecle() {
      let title = document.querySelector(".cut_title");
      title.style.transform = "rotate(90deg) translate(-50%, 50%)";
      let cutItem = document.querySelectorAll(".cut_item");
      cutItem.forEach((item) => {
        item.querySelector("div").style.display = "none";
        item.style.width = "0px";
        item.style.height = "0px";
        item.style.transform = "rotate(" + 0 + "deg)";
      });

      //变化后对齐
      let mainCut = document.querySelector(".mainCut");
      let offsetX = (Number(mainCut.style.left.replace('px', '')) + 100)
      let offsetY = (Number(mainCut.style.top.replace('px', '')) + 100)
      if(this.isTop && this.isLeft){
        this.isTop = false
        this.isLeft = false
        mainCut.style.left = (offsetX - 100) + "px";
        mainCut.style.top = (offsetY -100) + "px";
      }
      else if(this.isTop){
        this.isTop = false
        mainCut.style.left = (offsetX) + "px";
        mainCut.style.top = (offsetY -135) + "px";
      }
      else if(this.isLeft){
        this.isLeft = false
        mainCut.style.left = (offsetX - 135) + "px";
        mainCut.style.top = (offsetY) + "px";
      }
      else{
        mainCut.style.left = offsetX + "px";
        mainCut.style.top = offsetY + "px";
      }
    },

    CutClick(isMoving) {
      if (isMoving) return;
      let mainCut = document.querySelector(".mainCut");
      if (!this.isOpen) {
        this.openCircle();
        this.isOpen = !this.isOpen;
        mainCut.style.backgroundColor = 'rgba(29, 156, 194, 0.836)'
        if(this.timer) clearTimeout(this.timer);
        this.timer = setTimeout(() => {
          this.CutClick(this.isMoving);
        }, 500000);
      } else {
        if(this.timer) clearTimeout(this.timer);
        this.timer = null
        this.closeCiecle();
        mainCut.style.backgroundColor = 'rgba(29, 156, 194, 0.336)'
        this.isOpen = !this.isOpen;
      }
    },
  },
  mounted() {
    let isDown = false;

    let mainCut = document.querySelector(".mainCut");
    mainCut.addEventListener("mousedown", (e) => {
      isDown = true;
    });
    mainCut.addEventListener("mouseup", (e) => {
      isDown = false;
      mainCut.style.transition = 'all 0.5s'
      mainCut.style.backgroundColor = 'rgba(29, 156, 194, 0.336)'
      setTimeout(() => {
        this.isMoving = false;
      }, 200);
    });
    document.addEventListener("mousemove", (e) => {
      if (isDown && !this.isOpen) {
        this.isMoving = true;
        mainCut.style.transition = ''
        mainCut.style.backgroundColor = 'rgba(29, 156, 194, 0.636)'
        let X = e.clientX - mainCut.offsetWidth/2;
        let Y = e.clientY - mainCut.offsetHeight/2;
        if(X <= 0 ) X=-35;
        if(Y <= 0) Y=-35;
        mainCut.style.left = X + "px";
        mainCut.style.top = Y + "px";
      }
    });
    //初始化
    let height  = window.innerHeight
    mainCut.style.left = -35 + "px";
    mainCut.style.top = height/2 - 50 + "px";
  },
};
</script>

<style scoped>
.mainCut {
  position: absolute;
  top: 0px;
  left: 0px;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  /* overflow: hidden; */
  background-color: rgba(29, 156, 194, 0.336);
  transform: rotate(-90deg);
  z-index: 999;
}
.CutClick {
  position: absolute;
  width: 300px;
  height: 300px;
  color: #fff;
  overflow: hidden;
  background-color: rgba(29, 156, 194, 0.966);
  transform: rotate(-90deg);
  border-radius: 50%;
  transition: all 0.5s;
  z-index: 999;
}
.cut_title {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 100px;
  height: 100px;
  text-align: center;
  line-height: 100px;
  font-size: 35px;
  color: rgb(247, 243, 243);
  transition: all 0.5s;
  transform: rotate(90deg) translate(-50%, 50%);
}
</style>