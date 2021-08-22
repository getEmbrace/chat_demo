<template>
  <Cut>
      <CutItem class="item" path="/home">首页</CutItem>
      <CutItem class="item" path="/login">登录</CutItem>
      <CutItem class="item" path="/mine">我的</CutItem>
     
  </Cut>
</template>

<script>
import Cut from '../common/cut/Cut.vue'
import CutItem from '../common/cut/CutItem.vue'
export default {
  name: 'MainCut',
  components: {
    Cut,
    CutItem
  }
}
</script>

<style scoped>

</style>