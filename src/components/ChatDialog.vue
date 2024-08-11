<!--
 * @Author: Jacob-biu 2777245228@qq.com
 * @Date: 2024-08-07 22:10:58
 * @LastEditors: Jacob-biu 2777245228@qq.com
 * @LastEditTime: 2024-08-11 22:55:16
 * @FilePath: \demo\llm_demo\src\components\ChatDialog.vue
 * @Description: 
 * Copyright (c) 2024 by Jacob John, All Rights Reserved. 
-->
<template>
  <div id="Total" :class="{'dark-mode': isDarkMode}">
    <div class="SlideButtonDiv">
      <button @click="toggleSidebar" id="slideBarButton" :class="{ active: isActive }"></button>
    </div>
    <div class="BarContainer" v-if="isSidebarOpen">
      <p>工具栏</P>
      <div class="Bar" >
        <button id="palmLogo" @click="navigateToPage"></button>
        <div :class="{'dark-mode': isDarkMode, 'white-mode': !isDarkMode}" id="mode">
          <button @click="toggleDarkMode" id="modeButton" :class="{ active: isDarkMode }">
          </button>
        </div>
      </div>
    </div>
    <div class="ChatContainer">
      <div class="container">
        <!-- <div v-if="!isChatBoxOpen" class="Picture">
          <button></button>
        </div> -->
        <div id="msg" >
          <p @mouseover="changeColor" @mouseout="resetColor" :style="{color: textColor}">{{ msg }}</p>
        </div>
        <div id="chatbox">
            <div id="chatlog">
              
            </div>
        </div>
        <div id="messagebox" >
          <input type="text" id="userInput" v-model="inputData" @keyup.enter="sendData" placeholder="尽管问！" autofocus>
          <button id="sendBtn" @click="sendData" :loading="loading">
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import axios from 'axios';
// import {ref} from 'vue'


export default {
  name: 'ChatDialog',
  props: {
    msg: String
  },
  data() {
    return {
      messageStream: '',
      textColor: 'white',
      inputData: '',
      loading: false,
      isStopped:false,
      messages:'',
      returnMessage:'',
      isDarkMode: false,
      isSidebarOpen: false,
      isChatBoxOpen: false,
      isFirstImage: true, // 用于跟踪当前使用的 SVG 图片
      isActive: false,
      svg1: 'url(../assets/white_mode.svg)',
      svg2: 'url(../assets/dark_mode.svg)',
      gif: {url: require('../assets/loading2.gif')},
    };
  },

  methods:{
    async navigateToPage(){
      const url = 'https://palm.seu.edu.cn/';
      window.open(url, '_blank');
    },
    
    async toggleSidebar() {
      this.isSidebarOpen = !this.isSidebarOpen;
      this.isActive = !this.isActive;
    },
    async toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      if (this.isDarkMode) {
        document.body.classList.add('dark-mode');
      } else {
        document.body.classList.remove('dark-mode');
      }
    },
    async changeColor(){
      this.textColor = 'blue';
    },
    async resetColor(){
      this.textColor = 'black';
      setTimeout(() => {
        this.textColor = 'white';
      }, 3000);
    },
    async displayMessage(message,sender){
      //sender == user
      let messContainer = document.createElement('div');
      messContainer.style.textAlign = 'right';
      messContainer.style.display = 'flex';
      messContainer.style.right = '0';
      document.getElementById('chatlog').appendChild(messContainer);


      let messageElement = document.createElement('div');
      messageElement.className = 'message ' + sender;
      messageElement.textContent = message;

      messContainer.appendChild(messageElement);
      document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;
    },
    
    async waitSeveralSeconds() {
      await new Promise(resolve => setTimeout(resolve, Math.random() * 100 + 10));
    },

    async sendData() {
      if (this.loading) {
        return;
      }
      // if(this.isChatBoxOpen == false) {
      //     this.isChatBoxOpen = true;
      // }
      this.loading = true;

      if (this.inputData.trim() !== "") {
        if(this.isChatBoxOpen == false) {
          this.isChatBoxOpen = true;
        }        
        let usermessage = this.inputData;
        this.displayMessage(usermessage, 'user');
        this.inputData = ''; // 清空输入框

        // // 创建一个子元素，用于加载动画
        // const spinner = document.createElement('div');
        // spinner.className = 'spinner';

        // spinner.style.backgroundImage = 'url("../assets/logo.png")';
        // spinner.style.width = '100px';
        // spinner.style.height = '40px';
        // spinner.style.backgroundSize = 'cover';
        // spinner.style.zIndex = '9999'; // 使加载动画位于最前面
        // spinner.style.alignItems = 'center';

        // // 将 spinner 添加到 loadingDiv 中
        // document.getElementById('chatlog').appendChild(spinner);

        // 创建一个新的img元素
        var img = document.createElement('img');
        img.style.width = "100px";
        img.style.height = "auto";
 
        // 设置img的src属性
        img.src = this.gif.url;
  
        // 将img元素添加到div中
        document.getElementById('chatlog').appendChild(img);

        const response = await fetch('http://127.0.0.1:5000/sendData', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ data: usermessage })
        });
        //非流式输出
        // console.log(response.data.data);
        // const data = await response.json();

        // // const num = response.data;
        // if(data && data.flag == false){
        //   this.displayMessage(data.data.trim(), 'system');
        // }

        console.log(response.ok);
        let messageElement = document.createElement('div');
        messageElement.id = usermessage;
        // messageElement.textContent = '';
        messageElement.innerHTML+='';
        document.getElementById('chatlog').appendChild(messageElement);
        document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;
        


        if (response.ok) {
          document.getElementById('chatlog').removeChild(img);
          
          const reader = response.body.getReader();
          const decoder = new TextDecoder('utf-8');
          // let text = '';
          
          
          reader.read().then(async function processText({ done, value }) {
            if (done) return;

            // text += decoder.decode(value, { stream: true });
            // const parts = text.split("\n\n").filter(part => part.startsWith('data:')).map(part => part.replace('data: ', ''));
            const parts = decoder.decode(value, { stream: true }).split("\n\n").filter(part => part.startsWith('data:')).map(part => part.replace('data: ', ''));

            console.log('parts:'+ parts);
            for (const part of parts) {
              console.log(part);
              // messageElement.textContent+=part;
              // console.log(`AI: ${part}`);
              this.returnMessage += part;
              
              await this.waitSeveralSeconds();
              messageElement.innerHTML += part;
              document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;
            }
            console.log('this:'+this.returnMessage);
            messageElement.className = 'message system';

            return reader.read().then(processText.bind(this));
          }.bind(this));
          this.loading = false;
        }
        else{
          this.loading = false;
        }

        // else{
        //   const reader = response.body.getReader();
        //   const decoder = new TextDecoder('utf-8');
        //   let text = '';

        //   reader.read().then(function processText({ done, value }) {
        //     if (done) return;

        //     text += decoder.decode(value, { stream: true });
        //     const parts = text.split("\n\n").filter(part => part.startsWith('data:')).map(part => part.replace('data: ', ''));

        //     // 动态创建一个div
        //     const messageDiv = document.createElement('div');
        //     // 将div添加到#chat-container
        //     document.getElementById('chatlog').appendChild(messageDiv);
        //     document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;

        //     for (const part of parts) {
        //       // this.addMessageToDiv(`AI: ${part}`);
        //       this.messages.push(part);
        //       messageDiv.className = this.messages + 'system';
        //       messageDiv.textContent += part;
        //     }

        //     return reader.read().then(processText.bind(this));
        //   }.bind(this));
        //   // let messageElement = document.createElement('div');
        //   // messageElement.className = this.stream + 'system';
        //   // messageElement.textContent = this.stream;
        //   // document.getElementById('chatlog').appendChild(messageElement);
        //   // document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;
        // }
        // console.log(data);
      }
    },
    
    async addMessageToDiv(message,div) {
      this.messages.push(message);
      div.textContent += message;
    }


  }
}
</script>

<style>

#Total{
  display: flex;
  justify-content: center;
  text-align: center;
  width: 100%;
  height: 100%;
  margin-bottom: 0;;
}

.SlideButtonDiv{
  display: inline-block;
  width:20px;
  height: 20px;
  text-align: center;
  justify-content: center;
  margin-top:15px;
  margin-right: 5px;
}

#slideBarButton{
  width:25px;
  height:25px;
  border-radius: 50%;
  border:none;
  cursor: pointer;
  background-image: url("../assets/green_icon.svg"); /* 替换为点击后 SVG 图片路径 */
  background-size: auto 70%;
  background-position: center;
  background-repeat: no-repeat;
  background-color: transparent;
}
/* 切换后的背景图片 */
#slideBarButton.active {
  background-image: url("../assets/red_x.svg"); /* 替换为点击后 SVG 图片路径 */
}
#slideBarButton:hover {
  background-color: green;
}
#slideBarButton.active:hover {
  background-color: red;
}

.BarContainer {
  display: inline-block;
  width: 100px;
  height: 512px;
  margin-top: 15px;
  margin-right: 5px;
  padding: 0;
  text-align: center;
  background: rgba(255,255,255,0.75);
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.Bar {
  position:relative;
  width:100%;
  height:90%;
  text-align: center;
}

.ChatContainer {
  display: inline-block;
  width:700px;
  text-align: center;
  justify-content: center;
}

.container {
  /*background: rgba(255,255,255,0.75);*/
  top:10px;
  position: relative;
  background-color: transparent;
  padding-top:0;
  padding-right: 5px;
  padding-left: 5px;
  padding-bottom: 10px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 600px;
  height: 502px;
  text-align: center;
  margin-top: 5px;
  margin-bottom: 5px;
}

.Picture{
  position: absolute;
  top:200px;
  left:280px;
}

#palmLogo{
  width:60px;
  height:60px;
  border-radius: 10px;
  border: none;
  background-color: rgba(255,255,255,0.8);
  background-image: url("../assets/PALMLogo.png");
  background-size: auto 100%;
  background-position: center;
  background-repeat: no-repeat;
  cursor: pointer;
}

#msg {
  background-color: thistle;
  opacity: 0.8;

  border-radius: 10px;
  height:25px;
  text-align: center;
  justify-content: center;
  padding-top:7px;
  margin-top: 7px;
  margin-bottom: 2.5px;
}
#msg p{
  font-size: 100%;
  text-size-adjust: 100%;
  margin-top:0.5px;
  margin-bottom:0.5px;
}

#chatbox {
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 2.5px;
  height: 420px;
  overflow-y: scroll;
  margin-bottom: 2.5px;
  overflow-y: auto;
  background: rgba(255,255,255,0.8);
}


#chatbox::-webkit-scrollbar {
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

#chatlog {
  border-radius: 10px;
  list-style-type: none;
  padding: 0;
  margin-right: 15px;
  margin-left: 15px;
  margin-top: 10px;
  margin-bottom: 10px;
  overflow-y: auto;

}

#messagebox {
  position: absolute;
  right:-2.2px;
  bottom: 3.5px;
  border-radius: 10px;
  height: 45px;
  width: 100%;
  display: flex;
  align-items: right;
  background: rgba(255,255,255,0);
  display: inline-block; /* 如果需要行内显示 */
}

.message {
  border-radius: 10px;
  margin-bottom: 10px;
}

.user {
  text-indent:2em;
  white-space: pre-wrap;
  margin-left:auto;
  padding-left:10%;
  text-align: left;
}

.system {
  text-indent:2em;
  white-space: pre-wrap;
  text-align: left;
  padding-right: 10%;
}

#userInput {
  height: 25px;
  width: 580px;
  padding: 10px;
  margin-right: 5px;
  border: none;
  border-radius: 5px;
  position: relative;
  opacity: 0.7;
}
#userInput:focus {
  outline: none;
}

#sendBtn {
  padding: 10px;
  width: 40px;
  height:40px;
  border: none;
  margin-left: 5px;
  background-color: rgba(255,255,255,0.8);
  background-image: url("../assets/button_gray_plane.svg");
  background-size: auto 70%;
  background-position: center;
  background-repeat: no-repeat;
  color: black;
  border-radius: 50%;
  cursor: pointer;

  position: absolute;
  right: 15px; /* 定位到容器的右侧 */
  top: 3px;
}

#sendBtn:hover {
  background-color: rgb(240,248,255);
}

/*dark mode*/
#mode{
  position:absolute;
  left:30px;
  bottom:10px;
  text-align: center;
  padding: 0;
}

:root {
  --bg-color: white;
  --text-color: black;
}
 
.dark-mode {
  --bg-color: black;
  --text-color: white;
}

body {
  background-color: var(--bg-color);
  color: var(--text-color);
}

#modeButton {
  text-align: center; /* 文本居中对齐*/ 
  font-size: 13px; /* 设置字体大小*/ 
  width: 40px;
  height: 40px; 
  cursor: pointer;
  background-image: url("../assets/white_mode.svg"); /* 替换为默认 SVG 图片路径 */
  background-size: auto 70%;
  background-position: center;
  background-repeat: no-repeat;
  background-color: transparent;
  color: white;
  border: none;
  border-radius: 50%;
}
/* 切换后的背景图片 */
#modeButton.active {
  background-image: url("../assets/dark_mode.svg"); /* 替换为点击后 SVG 图片路径 */
}
/*#modeButton:hover {
  background-color: #0056b3;
}*/
</style>