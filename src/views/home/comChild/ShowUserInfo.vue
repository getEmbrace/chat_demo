<template>
  <div class="userInfo">
    <div class="show">
      <div class="baseInfo">
        <div class="del" @click="delClick">
          <span>&times;</span>
        </div>
        <div class="img">
          <img :src="userInfo.picture" alt="" />
        </div>
        <div class="name">
          昵称:<span>{{ userInfo.username }}</span>
        </div>
        <div class="id">
          ID:<span>{{ userInfo.id }}</span>
        </div>
        <div class="introdution">
          简介:
          <span>{{ userInfo.sex }}</span>
          <span>{{ userInfo.age }}岁</span>
          <span>{{ userInfo.birthday }}</span>
          <span>{{ userInfo.cons }}</span>
        </div>
        <div class="signature">
          个性签名:<span>{{ userInfo.signature_m }}</span>
        </div>
        <div class="selectedPic">
          <span>精选照片:</span>
          <img :src="userInfo.selectedPic" alt="" />
        </div>
        <div class="other" v-if="isFriend(userInfo.id)">
          <button @click="del_friend(userInfo.id)">删好友</button>
          <button @click="send_message(userInfo.id)">发消息</button>
        </div>
        <div class="other" v-else>
          <button @click="add_friend(userInfo.id)">加好友</button>
          <button @click="send_message(userInfo.id)">发消息</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { addFriend, delFriend } from "network/home.js";

export default {
  name: "ShowUserInfo",
  data() {
    return {};
  },
  props: {
    userInfo: {
      type: Object,
      default() {
        return {};
      },
    },
  },
  methods: {
    add_friend(addFriendId) {
      addFriend(this.$store.state.cooike, addFriendId).then((res) => {
        let data = JSON.parse(res.replace(/'/g, '"'));
        let status = data.status;
        let message;
        if (status == 1) {
          message = "添加好友成功...";
        } else if (status == 0) {
          message = "添加好友失败...";
        } else if (status == -1) {
          message = "该用户已是您的好友...";
        }
        this.$bus.$emit("sendMessage", [status, message]);
        this.$bus.$emit('refreshFriends')
      });
    },
    del_friend(delFriendId) {
      delFriend(this.$store.state.cooike, delFriendId).then((res) => {
        let data = JSON.parse(res.replace(/'/g, '"'));
        let status = data.status;
        let message;
        if (status == 1) {
          message = "删除好友成功...";
        } else if (status == 0) {
          message = "删除好友失败...";
        } else if (status == -1) {
          message = "未添加该用户为好友...";
        }
        this.$bus.$emit("sendMessage", [status, message]);
        this.$bus.$emit('refreshFriends')
      });
    },
    delClick() {
      this.$emit("delClick_uInfo");
    },
    send_message(friendId){
      this.$emit("send_message", friendId)
    }
  },
  computed: {
    isFriend() {
      return (uid) => {
        for (let item of this.$store.state.friends) {
          if(uid == item.id){
            return true;
          }
        }
        return false;
      };
    },
  },
};
</script>

<style>
.userInfo {
  position: relative;
}
.show {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 100%;
  height: 80%;
  background-color: rgba(15, 15, 15, 0.904);
  color: rgba(255, 255, 255, 0.719);
}
.show .baseInfo {
  position: absolute;
  top: 0px;
  left: 45%;
  width: calc(100% * 0.5);
  height: calc(100%);
  border: 1px solid;
  overflow: hidden;
  transform: translateX(-50%);
}
.show .baseInfo .del {
  position: absolute;
  top: calc(100% * 0.01);
  right: 20px;
  width: 50px;
  text-align: center;
}
.show .baseInfo .del span {
  font-size: 32px;
}
.show .baseInfo .img {
  position: absolute;
  top: calc(100% * 0.01);
  left: 20px;
  width: 100px;
  border-radius: 50%;
}
.show .baseInfo .img img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}
.show .baseInfo .name {
  position: absolute;
  top: calc(100% * 0.05);
  left: 140px;
  width: 200px;
  line-height: 30px;
}
.show .baseInfo .name span {
  margin-left: 5px;
}
.show .baseInfo .id {
  position: absolute;
  top: calc(100% * 0.1);
  left: 140px;
  width: 200px;
  line-height: 30px;
}
.show .baseInfo .id span {
  margin-left: 5px;
}
.show .baseInfo .introdution {
  position: absolute;
  top: calc(100% * 0.2);
  left: 20px;
  width: 300px;
  height: 30px;
  line-height: 30px;
}
.show .baseInfo .introdution span {
  padding: 0 13px;
}
.show .baseInfo .introdution span:nth-child(2) {
  border-right: 2px solid rgba(0, 0, 0, 0.507);
}
.show .baseInfo .introdution span:nth-child(1) {
  padding: 0;
  margin-left: 5px;
}
.show .baseInfo .signature {
  position: absolute;
  top: calc(100% * 0.26);
  left: 20px;
  width: 300px;
  height: 30px;
  line-height: 30px;
}
.show .baseInfo .signature span {
  margin-left: 5px;
}

.show .selectedPic {
  position: absolute;
  top: calc(100% * 0.36);
  left: 20px;
  width: 100%;
  height: 245px;
}
.show .selectedPic span {
  position: absolute;
  top: 0px;
  font-size: 20px;
}
.show .selectedPic img {
  position: absolute;
  top: 35px;
  width: 200px;
  height: 200px;
}
.show .baseInfo .other {
  position: absolute;
  top: calc(100% * 0.8);
  left: calc(100% * 0.56);
  width: 80%;
  height: 50px;
  text-align: center;
  transform: translateX(-50%);
}
.show .baseInfo .other button {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 80px;
  height: 100%;
  transform: translate(-50%, -50%);
  border-radius: 10px;
  color: rgba(0, 0, 0, 0.705);
  border-width: 1px;
  background-color: rgba(255, 255, 255, 0.623);
}
.show .baseInfo .other button:nth-child(1) {
  left: 25%;
}
.show .baseInfo .other button:nth-child(2) {
  left: 70%;
  color: #000;
  background-color: rgba(53, 191, 223, 0.71);
}
</style>