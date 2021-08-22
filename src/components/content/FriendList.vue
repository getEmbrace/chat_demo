<template>
  <div class="friendList">
    <NavBar v-if="haveFriend">
      <NavBarItem
        v-for="(item) in friendsData"
        :status="item.active"
        :key="item.id"
        :uid="item.id"
        :messageCount="item.messageCount"
        :class="{clicked: item.id == isClick}"
      >
        <img slot="img" :src="item.picture" alt="" />
        <span slot="name">{{ item.username }}</span>
      </NavBarItem>
    </NavBar>
    <span v-if="!isChange && !haveFriend" class="default1">暂未添加好友哦...</span>
  </div>
</template>

<script>
import NavBar from "../common/navbar/NavBar.vue";
import NavBarItem from "../common/navbar/NavBarItem.vue";
export default {
  name: "FriendList",
  data(){
    return {
      isClick: null
    }
  },
  props: {
    friendsData: {
      type: Array,
      default() {
        return [];
      },
    },
    haveFriend: {
      type: Boolean,
      default: false,
    },
    isChange: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    NavBarItem,
    NavBar,
  },
  created(){
    this.$bus.$on('friendItemClick', (uid) => {
      this.isClick = uid
    })
    this.$bus.$on('delClick_uInfo', () => {
      this.isClick = null
    })
  }
};
</script>

<style scoped>
.default1 {
  position: absolute;
  width: 126px;
  left: 50%;
  top: 100px;
  transform: translateX(-50%);
}
.clicked {
  background-color: rgb(205, 203, 228);
}
</style>