<template>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
</template>



<script>

import { getCurrentInstance, onMounted } from "vue";
export default {

  

  setup( ) {
    const { proxy, ctx } = getCurrentInstance(); //获取上下文实例，ctx=vue2的this
    onMounted(() => {
      console.warn(proxy, "proxy");
      console.warn(proxy.$request)
      proxy.$request('p');
    });
  },
};
</script>
