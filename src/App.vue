<!--
 * @Author: Jacob-biu 2777245228@qq.com
 * @Date: 2024-08-07 21:52:26
 * @LastEditors: Jacob-biu 2777245228@qq.com
 * @LastEditTime: 2024-08-13 11:01:05
 * @FilePath: \demo\llm_demo\src\App.vue
 * @Description: 
 * Copyright (c) 2024 by Jacob John, All Rights Reserved. 
-->
<template>
  <!-- <div class="background"></div> -->
  <!-- <router-view/> -->
  <p id="Sen">大模型AI 也可能会犯错哦。请核查重要信息。</p>
  <ChatDialog msg="LLM-demo"/>
</template>

<script>
import ChatDialog from './components/ChatDialog.vue'

export default {
  name: 'App',
  components: {
    ChatDialog,
  }
}
</script>

<style>
html{
  height: 100%;
  width: 100%;

}
body{
  height: 100%;
  margin: 0;
}
#app {
  font-family: 'LiSu', 'SimSun', 'KaiTi_GB2312', 'Songti SC', 'Avenir', 'Helvetica', 'Arial', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /*display: flex;*/
  justify-content: center;
  text-align: center;
  width: 100%;
  height: 100%;
  color: #2c3e50;
  margin: 0;
  padding: 0;
  position:relative;
}
#background{
  width: 100%;
  height: 100%;
  background-image: url("./assets/image.jpg");
  background-size: cover;
  background-position: center;
  filter: blur(3px);
  position:fixed;
  z-index:-1;
}

#Sen{
  position: absolute;
  text-align: center;
  top: 515px;
  left:36%;
  right: 36%;
}
</style>
