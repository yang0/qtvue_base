<template>
  <div id="nav">
    test
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>

<script>
import { onMounted } from "vue";
import {qt_request} from "@/utils/qt-request"

export default {
  setup( ) {
    const printTest = (data) => {
        console.warn("[iconbar vue] [printTest] [data]", data)
    }

    onMounted(() => {
      qt_request('p', null, printTest)
    });
  },
};
</script>
