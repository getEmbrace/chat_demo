<template>
  <div class="navBar">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>

<style>
 .navBar {
   border-top: 1px solid;
 }
</style>