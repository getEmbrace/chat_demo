<template>
  <div id="friend">
    <div class="friend">
      <div class="friend_title">
        {{ getTitle }}
        <span class="change" @click="change_click">{{ getContent }}</span>
      </div>
      <div class="friend_add" v-if="isChange">
        <input type="text" placeholder="输入用户名称" v-model="username" />
        <div class="search" @click="search_click"></div>
        <div class="serach_default" v-if="searchEmpty">
          <span>没有检索到该用户昵称...</span>
        </div>
      </div>
      <FriendList
        v-if="isLogin"
        :friendsData="friendsData"
        :haveFriend="haveFriend"
        :isChange="isChange"
      ></FriendList>
      <div class="default" v-if="!isLogin">
        <span>登录后才能使用该功能哦...</span>
      </div>
    </div>
    
  </div>
</template>

<script>
import FriendList from "components/content/FriendList.vue";
import { getFriends, findUser } from "network/home.js";
import { closeLongSrc } from "network/app.js";
export default {
  name: "Friend",
  data() {
    return {
      friendsData: [],
      isLogin: false,
      searchEmpty: false,
      haveFriend: false,
      message: [
        {
          title: "好友列表",
          content: "+",
        },
        {
          title: "搜索用户",
          content: "o",
        },
      ],
      isChange: false,
      username: "",
      commInfos: []
    };
  },
  components: {
    FriendList,
  },
  computed: {
    getTitle() {
      return this.isChange ? this.message[1].title : this.message[0].title;
    },
    getContent() {
      return this.isChange ? this.message[1].content : this.message[0].content;
    },
  },
  methods: {
    getFriend() {
      let cooike = this.$store.state.cooike;
      getFriends(cooike).then((res) => {
        let data = JSON.parse(res.replace(/'/g, '"'));
        let status = data.status;
        if (status == 0) {
          this.isLogin = false;
        } else if (status == 1) {
          this.isLogin = true;
          let friends = data.data;
          this.$store.commit("setFriends", friends);
          if (friends.length != 0) {
            this.friendsData = friends;
            this.haveFriend = true;
            this.haveComm()
          this.getFriend();
          } else {
            this.haveFriend = false;
          }
        }else if(status == -2){
          // console.log(-2);
        }
      });
    },
    haveComm(){
      // 判断是否有通讯请求
      this.commInfos = []
      for(let item of this.friendsData){
        if(item.commInfo){
          this.commInfos.push(item.commInfo)
        }
      }
      if(this.commInfos.length != 0){
        this.$bus.$emit('haveComm', this.commInfos)
      }
    },
    change_click() {
      this.isChange = !this.isChange;
      this.friendsData = [];
      //取消ShowUserInfo组件
      this.$emit("delClick_uInfo");
      closeLongSrc(this.$store.state.cooike, "/getFriends")
      if (!this.isChange) {
        this.getFriend();
      }
    },
    search_click() {
      findUser(this.$store.state.cooike, this.username).then((res) => {
        let data = JSON.parse(res.replace(/'/g, '"'));
        let status = data.status;
        if (status == -1) {
          this.isLogin = false;
        } else if (status == 0) {
          this.friendsData = [];
          this.searchEmpty = true;
        } else {
          this.friendsData = data.data;
          this.haveFriend = true;
        }
      });
    },
  },
  created() {
    closeLongSrc(this.$store.state.cooike, "/getFriends").then((res) => {
      this.getFriend();
    });
  }
};
</script>

<style scoped>
#friend {
  position: relative;
}
.friend {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 90%;
  height: 70%;
  border: 1px solid;
  border-radius: 0 30px 30px 0;
  line-height: 100%;
  overflow: auto;
}
.friend_title {
  position: sticky;
  top: 0;
  height: 60px;
  text-align: center;
  line-height: 60px;
  font-size: 18px;
  border-radius: 0 30px 0 0;
  color: #000;
  z-index: 2;
  background-color: rgb(203, 201, 223);
}
.friend_title .change {
  position: absolute;
  right: 10%;
  top: 2px;
  font-size: 28px;
  color: rgba(0, 0, 0, 0.664);
}
.friend_add {
  position: relative;
  height: 25px;
}
.friend_add input {
  position: absolute;
  left: 0px;
  width: 100%;
  height: 30px;
  padding-left: 20px;
}
.friend_add .search {
  position: absolute;
  top: 3px;
  right: 7%;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  border: 1px solid rgba(0, 0, 0, 0.623);
  background-color: rgba(187, 179, 179, 0.24);
}
.friend_add .search::after {
  position: absolute;
  right: -8px;
  bottom: -5px;
  content: "";
  width: 13px;
  height: 5px;
  transform: rotate(45deg);
  border: 1px solid rgba(0, 0, 0, 0.623);
  background-color: rgba(187, 179, 179, 0.178);
}
.friend_add .serach_default {
  position: absolute;
  top: 40px;
  text-align: center;
}
.default {
  margin-top: 25px;
  text-align: center;
}

</style>