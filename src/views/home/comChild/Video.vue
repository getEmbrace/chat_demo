<template>
  <div class="video">
    <div class="show">
      <VideoDefault v-if="isDefault" @tryComm="tryComm($event)"></VideoDefault>
      <TryComm
        v-if="!isDefault"
        :uid="uid"
        @delClick_tComm="delClick"
      ></TryComm>
      <CommVideo
        v-if="isCommVideo"
        :videoInfo_b="videoInfo_b"
      ></CommVideo>
    </div>
  </div>
</template>

<script>
import VideoDefault from "components/content/videoShow/Default.vue";
import TryComm from "components/content/videoShow/TryComm.vue";
import CommVideo from "components/content/videoShow/CommVideo.vue";

import { closeLongSrc, setActive } from "network/app.js";
export default {
  name: "Video",
  data() {
    return {
      uid: 0,
      isDefault: true,
      isAccess: false,
      isCommVideo: false,
      videoInfo_b: {},
      videoInfoArr: [],
      setVideo: true
    };
  },
  props: {},
  components: {
    VideoDefault,
    TryComm,
    CommVideo,
  },
  methods: {
    tryComm(uid) {
      // // 设置状态为忙碌
      // setActive(this.$store.state.cooike, 2).then((res) => {
      //   this.$bus.$emit("refreshMine");
      // });
      this.isDefault = false;
      this.uid = Number(uid);
    },
    delClick() {
      this.isDefault = true;
    },
    delClick_comm(){
      // 关闭摄像头
      this.$store.state.localStream && this.$store.state.localStream.getTracks().forEach(function (track) {
        track.stop();
      });
      // 改变状态
      setActive(this.$store.state.cooike, 1).then((res) => {
        this.$bus.$emit("refreshMine");
      });
      closeLongSrc(this.$store.state.cooike, '/commHouse')
      this.videoInfo_b = {}
      this.isCommVideo = false;
    },
  },
  created() {
    this.$bus.$on("setVideoData", (videoBlob) => {
      if(videoBlob != null){
        this.videoInfo_b = {videoData: videoBlob}
      }
    });
    this.$bus.$on("closeCommVideo", res => {
      this.delClick_comm()
    })
    this.$bus.$on("openCommVideo", res => {
      this.isCommVideo = true;
    })
  },
};
</script>

<style scoped>
.video {
  position: relative;
}
.show {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 100%;
  height: 80%;
}
</style>