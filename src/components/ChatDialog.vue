<!--
 * @Author: Jacob-biu 2777245228@qq.com
 * @Date: 2024-08-07 22:10:58
 * @LastEditors: Jacob-biu 2777245228@qq.com
 * @LastEditTime: 2024-08-14 17:00:28
 * @FilePath: \NewDemo\llm_demo\src\components\ChatDialog.vue
 * @Description: 
 * Copyright (c) 2024 by Jacob John, All Rights Reserved. 
-->
<template>
  <div id="Total">
    <div id="SlideButtonDiv">
      <button @click="toggleSidebar" id="slideBarButton" :class="{ active: isActive }"></button>
    </div>
    <div id="BarContainer" v-if="isSidebarOpen" :class="{ active: isDarkMode }">
      <p>工具栏</P>
      <div id="Bar" >
        <button id="palmLogo" @click="navigateToPage"></button>
        <div :class="{'dark-mode': isDarkMode, 'white-mode': !isDarkMode}" id="mode">
          <button @click="toggleDarkMode" id="modeButton" :class="{ active: isDarkMode }">
          </button>
        </div>
      </div>
    </div>
    <div id="ChatContainer">
      <div id="container">
        <!-- <div v-if="!isChatBoxOpen" class="Picture">
          <button></button>
        </div> -->
        <div id="msg"  v-show="isChatBoxOpen" :class="{ active: isDarkMode }">
          <p @mouseover="changeColor" @mouseout="resetColor" :style="{color: textColor}">{{ msg }}</p>
        </div>
        <div id="chatbox" v-show="isChatBoxOpen" :class="{ active: isDarkMode }">
            <div id="chatlog" >
              
            </div>
        </div>
        <div id="messagebox" >
          <input type="text" id="userInput" v-model="inputData" @keyup.enter="sendData" placeholder="尽管问！" autofocus :class="{ active: isDarkMode }">
          <button id="sendBtn" @click="sendData" :loading="loading" :class="{ active: isDarkMode }">
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { marked } from 'marked';
import hljs from 'highlight.js';
import 'highlightjs-line-numbers.js';      // 引入行号插件
// import 'highlight.js/styles/monokai-sublime.css';
// import 'highlight.js/styles/atom-one-dark.css'; // 选择你喜欢的样式
import 'highlight.js/styles/github.css'; // 引入你喜欢的代码高亮样式

export default {
  name: 'ChatDialog',
  props: {
    msg: String
  },

  data() {
    return {
      textColor: 'white',
      inputData: '',
      loading: false,
      isStopped:false,
      messages:[],
      wholeMessage: '',
      isDarkMode: false,
      isSidebarOpen: false,
      isChatBoxOpen: false,
      isFirstImage: true, // 用于跟踪当前使用的 SVG 图片
      isActive: false,
      svg1: 'url(../assets/white_mode.svg)',
      svg2: 'url(../assets/dark_mode.svg)',
      gif: {url: require('../assets/loading2.gif')},
      //对话历史
      history: [],
      API_URL: "http://localhost:9999/v1/chat/completions",
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
      let messContainerUser = document.createElement('div');
      messContainerUser.style.textAlign = 'right';
      messContainerUser.style.display = 'flex';
      messContainerUser.style.right = '0';
      messContainerUser.style.paddingLeft = '10%';
      document.getElementById('chatlog').appendChild(messContainerUser);


      let messageElementUser = document.createElement('div');
      messageElementUser.className = 'message ' + sender;
      messageElementUser.textContent = message;

      messContainerUser.appendChild(messageElementUser);
      document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;
    },
    
    async waitSeveralSeconds() {
      await new Promise(resolve => setTimeout(resolve, Math.random() * 100 + 10));
    },

    async sendData() {
      if (this.loading) {
        return;
      }

      // 配置marked，使其与highlight.js集成
      marked.setOptions({
        renderer: new marked.Renderer(),
        highlight: function(code, lang) {
          if (hljs.getLanguage(lang)) {
            return hljs.highlight(lang, code).value;
          } else {
            return hljs.highlightAuto(code).value;
          }
        },
        pedantic: false,
        gfm: true, // 开启gfm
        breaks: false,
        sanitize: false,
        smartLists: true,
        tables: true,
        smartypants: false,
      });

      if (this.inputData.trim() !== "") {
        this.loading = true;
        this.isChatBoxOpen = true;
        let usermessage = this.inputData;
        this.displayMessage(usermessage, 'user'); //展示用户问题
        this.inputData = ''; // 清空输入框

        // 创建一个新的img元素，用于加载动画
        var img = document.createElement('img');
        img.style.width = "100px";
        img.style.height = "auto";
        // 设置img的src属性
        img.src = this.gif.url;
        // 将img元素添加到div中
        document.getElementById('chatlog').appendChild(img);
        document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;

        if(!this.history){
          this.history.push({role: "system", content: "you are a helpful assistant"});
        }
        // 更新对话历史
        this.history.push({"role": "user", "content": usermessage});
        // 构建请求数据
        var data = {
          "model": "qwen2-7b",
          "messages": this.history,
          "temperature": 0.8,
          "top_p": 0.95,
          "repetition_penalty":1.1,
          "stream":true,
        };

        const response = await fetch(this.API_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
        });

        console.log(response.ok);

        let messContainerSystem = document.createElement('div');
        messContainerSystem.style.textAlign = 'right';
        messContainerSystem.style.display = 'flex';
        messContainerSystem.style.left = '0';
        messContainerSystem.style.paddingRight = '10%';
        messContainerSystem.style.height = 'fit-content';
        document.getElementById('chatlog').appendChild(messContainerSystem);

        let messageElementSystem = document.createElement('div');
        messageElementSystem.id = usermessage;
        messageElementSystem.innerHTML = '';
        messageElementSystem.className = 'message system';
        messageElementSystem.style.maxWidth = '530px';
        messContainerSystem.appendChild(messageElementSystem);
        document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;
        
        if (response.ok) {
          document.getElementById('chatlog').removeChild(img);

          const reader = response.body.getReader();
          const decoder = new TextDecoder('utf-8');
          let buffer = '';

          while (true) {  //eslint-disable-line no-constant-condition
            const { done, value } = await reader.read();
            if (done) {
              this.wholeMessage = '';
              break;
            }

            buffer += decoder.decode(value, { stream: true });

            // Split buffer by lines
            const lines = buffer.split('\n');

            // Keep the last incomplete line in buffer
            buffer = lines.pop() || '';

            // Process each line
            for (const line of lines) {
              const trimmedLine = line.trim();
              if (trimmedLine.startsWith('data: ')) {
                const dataStr = trimmedLine.slice('data: '.length);
                if (dataStr !== '[DONE]') {
                  try {
                    const jsonData = JSON.parse(dataStr);
                    if (jsonData.choices && jsonData.choices.length > 0) {
                      const delta = jsonData.choices[0].delta || {};
                      const content = delta.content || '';
                      if (content) {
                        this.wholeMessage += content;
                        let handledMessage = '';                   
                        handledMessage = marked(this.wholeMessage);
                        messageElementSystem.innerHTML = handledMessage;

                            
                        // 高亮代码块
                        document.querySelectorAll('pre code').forEach(function(block) {
                          // 添加语言标签，确保只添加一次
                          if (!block.hasAttribute('data-language-tagged')) {
                            // 通过类名获取语言
                            const language = block.className.replace('language-', '');
                
                            // 创建一个新的 div 元素来显示语言名称
                            const header = document.createElement('div');
                            header.className = 'code-header';
                            header.innerText = language.toUpperCase(); // 将语言名称转换为大写

                            // 在 pre 元素的顶部插入这个 div 元素
                            block.parentNode.insertBefore(header, block.parentNode.firstChild);
                            // 标记代码块为已添加语言标签
                            block.setAttribute('data-language-tagged', 'true');
                          }

                          if(!block.hasAttribute('line-number-tagged')) {
                            //为行插入行号
                            const lines = block.innerHTML.split('\n');
                            // 移除最后一个空行
                            if (lines[lines.length - 1].trim() === '') {
                              lines.pop();
                            }
                            let numberedLines = '';

                            lines.forEach((line, index) => {
                              numberedLines += `<span class="line-number">${index + 1}  </span>${line}\n`;
                            });

                            block.innerHTML = numberedLines;
                            block.setAttribute('line-number-tagged', 'true');
                          }
                          //高亮代码
                          hljs.highlightBlock(block);
                        });
                        document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;
                        console.log(content);
                      }
                    }
                  } catch (error) {
                    console.error('Error parsing JSON:', error);
                  }
                }
              }
            }
          }
          this.history.push({'role': 'assistant', 'content': this.wholeMessage})
          this.loading = false;
          // this.returnMessage = '';
        }
        else{
          this.loading = false;
        }
      }
    },

    async addLineNumbersToBlock(block){
      //为行插入行号
      const lines = block.innerHTML.split('\n');
      // 移除最后一个空行
      if (lines[lines.length - 1].trim() === '') {
        lines.pop();
      }
      let numberedLines = '';

      lines.forEach((line, index) => {
        numberedLines += `<span class="line-number">${index + 1}  </span>${line}\n`;
      });

      block.innerHTML = numberedLines;
    }
  },
}
</script>

<style>
/* 你可以根据需要自定义样式 */
.hljs {
  border-radius: 5px; /* 圆角边框 */
  border: 2px solid black; /* 黑框 */
}

/* 确保代码文本颜色高亮 */
.hljs-keyword,
.hljs-selector-tag,
.hljs-literal,
.hljs-section,
.hljs-link {
  color: #333; /* 设置文本颜色 */
}

#Total{
  display: flex;
  justify-content: center;
  text-align: center;
  width: 100%;
  height: 100%;
  margin-bottom: 0;;
}

#SlideButtonDiv{
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

#BarContainer {
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
#BarContainer.active{
  background: rgba(0,0,0,0.5);
}
#BarContainer.active >p{
  color:white;
}

#Bar {
  position:relative;
  width:100%;
  height:90%;
  text-align: center;
}

#ChatContainer {
  display: inline-block;
  width:700px;
  text-align: center;
  justify-content: center;
}

#container {
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
#msg.active {
  background-color: rgba(0,0,0,0.5);
}

#chatbox {
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 2.5px;
  height: 420px;
  overflow-y: scroll;
  margin-bottom: 2.5px;
  overflow-y: auto;
  overflow-x: auto;
  background: rgba(255,255,255,0.8);
}
#chatbox.active{
  border: 1px solid transparent;
  border-radius: 10px;
  padding: 2.5px;
  height: 420px;
  overflow-y: scroll;
  margin-bottom: 2.5px;
  overflow:auto;
  background-color: rgba(0,0,0,0.5);
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
  margin-left:auto;
  padding: 5px;
  text-align: left;
  background: rgba(255,255,255,0.9);
}

.system {
  white-space: pre-wrap;
  text-align: left;
  padding: 5px;
  background: rgba(255,255,255,0.9)
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
  background-color: transparent;
}
#userInput.active{
  background-color: rgba(0,0,0,0.5);
}
#userInput.active::placeholder{
  color: white;
}

#sendBtn {
  padding: 10px;
  width: 40px;
  height:40px;
  border: none;
  margin-left: 5px;
  background-color: transparent;
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
  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
}

/*dark mode*/
#mode{
  position:absolute;
  left: 30%;
  right: 30%;
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
</style>