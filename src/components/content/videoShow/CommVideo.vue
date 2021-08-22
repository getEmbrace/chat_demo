<template>
  <div class="comm_video">
    <div class="content">
      <div :class="{big_v: isBig, small_v: !isBig}" id="big_v">
        <video src="" muted id="big_v1" :class="{video_hidden: !isBig_v1}" @ended="onEnded('v1')"></video>
        <video src="" muted id="big_v2" :class="{video_hidden: isBig_v1}" @ended="onEnded('v2')"></video>
      </div>
      <div :class="{small_v: isBig, big_v: !isBig}" id="small_v" @click="switch_bs">
        <video src="" muted id="small_v1"></video>
      </div>
    </div>
    <div class="btn_del" @click="delClick_comm">
      <span>&times;</span>
    </div>
  </div>
</template>

<script>
export default {
  data(){
    return {
      srcList: [],
      oldSrcList: [],
      isBig: true,
      isBig_v1: true,
      waiting: false,
      stratVideo: true,
    }
  },
  props: {
    videoInfo_b: {
      type: Object,
      default() {
        return {};
      },
    },
  },
  watch: {
    videoInfo_b: {
      handler(newValue, oldValue){
        let video_blob = this.videoInfo_b.videoData;
        this.srcList.push(URL.createObjectURL(video_blob))
        if(this.stratVideo){
          this.setVideo_big()
          this.stratVideo = false
        }
      },
      deep: true
    },
  },
  methods: {
    delClick_comm(){
      // this.$bus.$emit('closeComm_self')
      this.$bus.$emit('closeComm_self_ws')
    },
    setVideo_self(){
      let small_v = document.querySelector('#small_v').querySelector('#small_v1')
      if(small_v){
        this.$store.state.localStream && (small_v.srcObject = this.$store.state.localStream)
        small_v.play()
      }
    },
    onEnded(e){
      let big_v1 = document.querySelector('#big_v').querySelector('#big_v1')
      let big_v2 = document.querySelector('#big_v').querySelector('#big_v2')
      let video = e === 'v1'? big_v2: big_v1;
      let endVideo = e === 'v1'? big_v1: big_v2;
      this.oldSrcList.forEach((item, index) => {
        if(endVideo.src === item){
          URL.revokeObjectURL(item)
          this.oldSrcList.splice(index, 1)
        }
      })
      video.play()
      this.isBig_v1 = !this.isBig_v1
      this.loadNext()
    },
    loadNext(){
      let big_v1 = document.querySelector('#big_v').querySelector('#big_v1')
      let big_v2 = document.querySelector('#big_v').querySelector('#big_v2')
      let video = this.isBig_v1 == true? big_v2: big_v1;
      if(this.srcList.length > 1){
        this.oldSrcList.push(this.srcList[0])
        video.src = this.srcList.shift()
      }else{
        video.src = this.srcList[0]
      }
      video.addEventListener('canplay', e => e.target.pause(), {once: true})
    },
    setVideo_big(){
      let big_v1 = document.querySelector('#big_v').querySelector('#big_v1')
      if(this.srcList.length > 0){
        big_v1.src = this.srcList[0]
        big_v1.play()
        this.loadNext()
      }
    },
    switch_bs(){
      this.isBig = !this.isBig
    }
  },
  created(){
    this.$bus.$on('refreshSelf', () => {
      this.setVideo_self()
    })
  }
};
</script>

<style>
.comm_video {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
  background-color: rgba(15, 15, 15);
  z-index: 2;
}
.comm_video .btn_del{
  position: absolute;
  left: 0.5%;
  top: 0.5%;
  width: 40px;
  height: 40px;
  text-align: center;
  line-height: 40px;
  border-radius: 0 0 20px 0;
  background-color: rgba(255, 255, 255, 0.363);
}
.comm_video .btn_del span {
  color: #000;
  font-size: 45px;
}
.comm_video .content {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 99%;
  height: 99%;
  transform: translate(-50%, -50%);
  /* background-color: pink; */
}
.comm_video .content .big_v {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  /* background-color: rgba(255, 255, 255, 0.411); */
}
.comm_video .content .small_v {
  position: absolute;
  right: 0;
  top: 0;
  width: 25%;
  height: 25%;
  border: 1px dashed rgba(255, 255, 255, 0.582);
  border-radius: 0 0 0 5px;
  /* background-color: rgba(255, 255, 255, 0.753); */
}
.big_v video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
.video_hidden {
  position: absolute;
  z-index: -1;
}
.small_v video {
  width: 100%;
  height: 100%;
}
</style>