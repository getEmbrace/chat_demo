<template>
  <div id="login">
    <LoginDefault></LoginDefault>
    <SendMessage></SendMessage>
  </div>
</template>

<script>
import LoginDefault from './comChild/Default.vue'
import SendMessage from 'components/common/SendMessage.vue'
export default {
  name: 'Login',
  components: {
    LoginDefault,
    SendMessage
  }
};
</script>

<style scoped>
#login {
  position: relative;
  width: 100%;
  height: calc(100vh);
  background-color: rgba(7, 7, 7, 0.952);
}
</style>