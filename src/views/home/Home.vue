<template>
  <div id="home">
    <MineInfo
      class="item4"
      :mineInfo="mineInfo"
      v-if="Object.keys(mineInfo).length != 0"
    ></MineInfo>
    <Friend class="item0" @delClick_uInfo="delClick_uInfo"></Friend>
    <ShowUserInfo
      class="item1"
      v-if="isUserInfo"
      :userInfo="userInfo_s"
      @delClick_uInfo="delClick_uInfo"
      @send_message="send_message($event)"
    ></ShowUserInfo>
    <Video class="item1" v-else></Video>
    <Waite class="item3"></Waite>
    <SendMessage></SendMessage>
    <ShowMessage
      v-if="isMessage"
      :friendId="friendId"
      @delClick_message="delClick_message"
    ></ShowMessage>
    <AccessComm
      class="item1"
      v-if="isAccessComm"
      :UInfo="UInfo"
      @delClick_comm="delClick_comm"
    ></AccessComm>
  </div>
</template>

<script>
import Friend from "./comChild/Friend.vue";
import Video from "./comChild/Video.vue";
import Waite from "./comChild/Waite.vue";
import MineInfo from "./comChild/MineInfo.vue";
import ShowUserInfo from "./comChild/ShowUserInfo.vue";
import ShowMessage from "./comChild/ShowMessage.vue";
import SendMessage from "components/common/SendMessage.vue";
import AccessComm from "components/content/videoShow/AccessComm.vue";

import { getUserInfo, getMine} from "network/home.js";
import { setActive} from "network/app.js";
export default {
  name: "Home",
  components: {
    Friend,
    Video,
    Waite,
    ShowUserInfo,
    SendMessage,
    MineInfo,
    ShowMessage,
    AccessComm,
  },
  data() {
    return {
      isUserInfo: false,
      isMessage: false,
      isAccessComm: false,
      userInfo_s: null,
      mineInfo: {},
      friendId: 0,
      UInfo: {},
    };
  },
  methods: {
    get_user_info(uid) {
      getUserInfo(uid).then((res) => {
        this.userInfo_s = JSON.parse(res.replace(/'/g, '"')).data;
        this.isUserInfo = true;
      });
    },
    delClick_uInfo() {
      this.$bus.$emit("delClick_uInfo");
      this.isUserInfo = false;
      this.friendId = 0;
    },
    get_mine() {
      let cooike = this.$store.state.cooike;
      getMine(cooike).then((res) => {
        let data = JSON.parse(res.replace(/'/g, '"'));
        let status = data.status;
        if (status == 1) {
          this.mineInfo = data.data;
        }
      });
    },
    send_message(friendId) {
      this.delClick_uInfo();
      this.friendId = friendId;
      this.isMessage = true;
    },
    delClick_message() {
      this.isMessage = false;
    },
    delClick_comm(){
      this.isAccessComm = false
    },
  },
  created() {
    this.$bus.$on("friendItemClick", (params) => {
      this.get_user_info(params);
    });
    this.$bus.$on("refreshMine", (params) => {
      this.get_mine()
    });
    this.$bus.$on("haveComm", (params) => {
      let messageId = -1;
      let commFriendId;
      for (let item of params) {
        for (let item1 of item) {
          if (item1.id > messageId) {
            messageId = item1.id;
            commFriendId = item1.origin;
          }
        }
      }
      getUserInfo(commFriendId).then((res) => {
        this.UInfo = JSON.parse(res.replace(/'/g, '"')).data;
        this.isAccessComm = true;
        setActive(this.$store.state.cooike, 2).then((res) => {
          this.get_mine();
        });
      });
    });
    setActive(this.$store.state.cooike, 1).then((res) => {
      this.get_mine();
    });
  },
};
</script>

<style scoped>
#home {
  display: flex;
  width: 100%;
  height: calc(100vh);
  background-color: rgba(179, 177, 204, 0.377);
  justify-content: space-between;
}
.item0 {
  width: calc(100% * 0.16);
  height: 100%;
}

.item1 {
  flex: 1;
}

.item3 {
  width: 160px;
  height: 100%;
}
.item4 {
  position: absolute;
  top: 10px;
  width: calc(100% * 0.16);
  height: 12.5%;
  z-index: 2;
}
</style>