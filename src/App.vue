<!--
 * @Author: Jacob-biu 2777245228@qq.com
 * @Date: 2024-08-07 21:52:26
 * @LastEditors: Jacob-biu 2777245228@qq.com
 * @LastEditTime: 2024-08-15 12:11:43
 * @FilePath: \llm-demo-0.1.1\llm_demo\src\App.vue
 * @Description: 
 * Copyright (c) 2024 by Jacob John, All Rights Reserved. 
-->
<template>
  <!-- <div class="background"></div> -->
  <!-- <router-view/> -->
  <p id="Sen">大模型AI 也可能会犯错哦。请核查重要信息。</p>
  <ChatDialog msg="Version 0.1.1"/>
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
  padding-top: 10px;
  padding-bottom:5px;
}

/* 样式设置：语言标签 */
.code-header {
  background-color: #333;
  color: #fff;
  padding: 2px 8px;
  font-size: 12px;
  font-family: monospace;
  border-bottom: 1px solid #555;
  border-radius: 3px 3px 0 0;
  display: inline-block;
  margin-bottom: -1px; /* 防止与代码块产生间距 */
}

/* 让代码块的顶部和语言标签对齐 */
pre {
  position: relative;
  margin-top: 0;
}

pre code {
  padding-top: 20px; /* 为了确保语言标注不会遮挡代码 */
  display: block;
  overflow-x: auto;
}
pre code::-webkit-scrollbar {
	width: 8px;
	height: 8px;
}
::-webkit-scrollbar-button {
	display: none;
}
::-webkit-scrollbar-track {
	background-color: rgba(70, 166, 255, 0.1);
	display: none;
}
::-webkit-scrollbar-thumb {
	background-color: rgba(70, 166, 255, 0.4);
	border: 2px solid transparent;
	border-radius: 6px;
	background-clip: padding-box;
}
::-webkit-scrollbar-thumb:hover {
	background-color: rgba(0, 0, 0, 0.5);
}

h1, h2, h3, h4, h5, h6, strong, p, pre, ol, ul {
  margin: 0;
}
</style>
