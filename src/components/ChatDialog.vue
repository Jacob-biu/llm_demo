<!--
 * @Author: Jacob-biu 2777245228@qq.com
 * @Date: 2024-08-15 09:15:52
 * @LastEditors: Jacob-biu 2777245228@qq.com
 * @LastEditTime: 2024-09-09 19:37:30
 * @FilePath: \llm_demo\src\components\ChatDialog.vue
 * @Description: ./src/components/ChatDialog.vue
 * Copyright (c) 2024 by Jacob John, All Rights Reserved. 
-->

<template>
  <div id="Total">
    <div id="SlideButtonDiv">
      <button @click="toggleSidebar" id="slideBarButton" :class="{ active: isActive }"></button>
    </div>
    <div id="BarContainer" v-show="isSidebarOpen" :class="{ active: isDarkMode }">
      <p>工具栏</P>
      <div id="Bar">
        <button id="palmLogo" @click="navigateToPage"></button>
        <!-- <div id="knowledgeDB" style="display:flex;  flex-direction: column;  justify-content: center;  align-items: center;">
          <el-dropdown id="KnowledgeDBButton">
            <button>
              <i class="el-icon-arrow-down el-icon--right"></i>
            </button> -->
        <!-- 下拉菜单 -->
        <!-- <template #dropdown>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click.native="triggerKnowledgeDBView" style="display: flex; align-items: center;">
                  <i>选择</i>
                </el-dropdown-item>
                <el-dropdown-item @click.native="triggerKnowledgeDBPreview" style="display: flex; align-items: center;">
                  <i>预览</i>
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
</el-dropdown> -->
        <!-- <button @click="triggerKnowledgeDBView" id="KnowledgeDBButton"></button> -->
        <!-- <span>知识库</span>
        </div> -->
        <div
          style="display:flex; flex-direction:column; justify-content:center; align-items:center;  width:100%; aspect-ratio: 1 / 1;">
          <button @click="triggerKnowledgeDBView" id="KnowledgeDBButton"></button>
          <span>编辑知识库</span>
          <button @click="triggerKnowledgeDBPreview" id="KnowledgeDBButton"></button>
          <span>预览知识库</span>
        </div>

        <div :class="{ 'dark-mode': isDarkMode, 'white-mode': !isDarkMode }" id="mode">
          <button @click="toggleDarkMode" id="modeButton" :class="{ active: isDarkMode }">
          </button>
        </div>
      </div>
    </div>
    <div id="sideBarOfDB" v-if="isSidebarOpen" :class="{ active: isDarkMode }">
      <sideBarOfDB style="width: 100%; height: 100%;" ref="sidebarOfDB" @selectedDB-sent-from-side="handleValueUpdate"
        @filePaths-sent-from-side="handlePathsUpdate" />
    </div>
    <div id="ChatContainer">
      <div id="container">
        <div id="msg" v-show="isChatBoxOpen" :class="{ active: isDarkMode }">
          <p @mouseover="changeColor" @mouseout="resetColor" :style="{ color: textColor }">{{ msg }}</p>
        </div>
        <div id="chatbox" v-show="isChatBoxOpen" :class="{ active: isDarkMode }">
          <div id="chatlog">

          </div>
        </div>
        <div id="messagebox">
          <input type="file" id="fileInput" ref="fileInput" @change="handleFileChange" class="file-upload"
            style="display: none;" />
          <!-- 自定义文件上传按钮 -->
          <button @click="triggerFileUpload" class="custom-file-upload" :class="{ active: isDisabled }">
          </button>
          <input type="text" id="userInput" v-model="inputData" @keyup.enter="sendData" placeholder="尽管问！" autofocus
            :class="{ active: isDarkMode }">
          <div style="height:80%;   aspect-ratio: 1 / 1;">
            <button v-if="!loading" id="sendBtn" @click="sendData" :loading="loading"
              :class="{ active: isDarkMode }"></button>
            <button v-else id="sendBtnStop" @click="stopSendMessage"></button>
          </div>
        </div>
      </div>
    </div>

    <div id="buttonDiv" v-show="isPreview">
      <button @click="toggleFilePreview" id="fileViewButtonTwo"></button>
    </div>
    <!-- 文件预览区 -->
    <div v-show="isPreviewFile" class="fileView">
      <img class="preview-image" v-if="isImageFile" :src="previewUrl" alt="File Preview" />
      <iframe v-else-if="isPdfFile" id="ifm" :src="this.previewUrl" width="100%" height="100%" />
      <div v-else-if="isTxtFile" id="txtFileContent" class="txtPage" v-html="txtFileContentPage"></div>
      <div v-else-if="isDocxFile" class="docx-preview" v-html="docxContent"></div>
      <div v-else-if="isDocFile" class="doc-preview" v-html="docContent"></div>
      <span v-else>文件预览不可用</span>
      <div id="buttonDiv">
        <button @click="toggleFilePreview" id="fileViewButton"></button>
      </div>
    </div>
    <!-- 知识库 -->
    <div id="knowledgeDBdiv" v-show="isKnowledgeDB">
      <knowledgeDB style="width: 97%; margin-left:5px;" @selectedOption="receiveDBContentFromChild" ref="knowledgeDB" />
      <div id="buttonDiv">
        <button @click="triggerKnowledgeDBView" id="fileViewButton"></button>
      </div>
    </div>
    <!-- 知识库预览 -->
    <div id="knowledgeDBPreviewDiv" v-show="isKnowledgeDBPreview">
      <knowledgeDBPreview style="width: 97%; height:100%" ref="knowledgeDBPreview" />
      <div id="buttonDiv">
        <button @click="triggerKnowledgeDBPreview" id="fileViewButton"></button>
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
import katex from 'katex';
import 'katex/dist/katex.min.css'; // 必须引入 KaTeX 的 CSS
// import { isPdfFile } from 'pdfjs-dist/build/pdf';
import { reactive } from 'vue';
import * as pdfjs from 'pdfjs-dist/build/pdf';
import * as pdfjsViewer from 'pdfjs-dist/web/pdf_viewer';
import { GlobalWorkerOptions } from 'pdfjs-dist/webpack';
// import { TextLayerBuilder } from 'pdfjs-dist/web/pdf_viewer';
import 'pdfjs-dist/web/pdf_viewer.css';
import mammoth from "mammoth";
// import docx4js from "docx4js";
import knowledgeDB from './knowledgeDB.vue';
import knowledgeDBPreview from './knowledgeDBPreview.vue';
import sideBarOfDB from './sidebarOfDB.vue'
import { ElMessage, ElDropdown, ElDropdownMenu, ElDropdownItem, ElButton } from 'element-plus';
import { EventBusOne } from '../event-bus.js';
import axios from 'axios';

GlobalWorkerOptions.workerSrc = 'https://unpkg.com/pdfjs-dist/build/pdf.worker.js';
// const eventBus = new pdfjsViewer.EventBus();

export default {
  name: 'ChatDialog',
  props: {
    msg: String
  },
  components: {
    knowledgeDB,
    knowledgeDBPreview,
    sideBarOfDB,
    ElDropdown,
    ElDropdownMenu,
    ElDropdownItem,
    ElButton,
  },
  data() {
    return {
      textColor: 'white',
      inputData: '',
      loading: false,
      isStopped: false,
      messages: [],
      wholeMessage: '',
      isDarkMode: false,
      isSidebarOpen: false,
      isChatBoxOpen: false,
      isFirstImage: true, // 用于跟踪当前使用的 SVG 图片
      isActive: false,
      svg1: 'url(../assets/white_mode.svg)',
      svg2: 'url(../assets/dark_mode.svg)',
      gif: { url: require('../assets/loading2.gif') },
      //对话历史
      history: [],
      API_URL: "http://localhost:8009/v1/chat/completions",
      fileName: '',   //存储当前文件名
      set: '',   //存储上一个文件名
      selectedFile: null,
      isPreview: false,
      isPreviewFile: false,
      previewUrl: '', // 文件预览的 URL
      isPdfFile: false,
      isImageFile: false,
      isTxtFile: false,
      isDocxFile: false,
      isDocFile: false,
      textLayerFactory: {
        createTextLayerBuilder: function (textLayerDiv, viewport, enhanceTextSelection) {
          return new pdfjsViewer.TextLayerBuilder({
            textLayerDiv,
            viewport,
            enhanceTextSelection,
          });
        },
      },

      pdfParams: reactive({
        currentPageNumber: 1,
        pdfScale: 1.0,
        pdfPageTotal: 0,
      }),
      extractedPDFText: "", // 存储pdf提取的文本内容
      pdfDocumentContent: "", // 保存加载的PDF实例
      pdfFileOpen: false, // 用于跟踪 PDF 文件是否已加载

      txtFileContent: "", // 保存 txt 文件的内容
      txtFileContentPage: "", //保存解析的txt HTML的内容
      txtFileOpen: false, // 用于跟踪 txt 文件是否已加载

      docxContent: '', //// 保存docx解析后的 HTML 内容
      docxFileOpen: false, // 用于跟踪 docx 文件是否已加载

      docContent: '', //// 保存doc解析后的 HTML 内容
      docxPlainTextContent: "", // 保存docx纯文本内容
      docPlainTextContent: '',// 保存doc纯文本内容
      keywords: [],
      isHighlighted: false, //是否高亮
      isKnowledgeDB: false, //是否展示知识库
      selectedOption: '', //知识库内容
      isKnowledgeDBPreview: false, //是否预览所有知识库内容
      selectedButton: { label: '不使用知识库', value: 'null', description: '' }, // 选中的知识库按钮
      selectedButtonHistory: { label: '不使用知识库', value: 'null', description: '' },
      isDisabled: false,
      disabledHistory: false,
      filePaths: [],  //知识库文件路径
      RAG: '',
      userMessageHistory: '',
      parameters: {},
    };
  },

  mounted() {
    // 在 mounted 时设置初始滚动位置
    this.$nextTick(() => {
      this.centerScroll();
    });
  },

  methods: {
    handlePathsUpdate(newValue) {
      this.filePaths = newValue;
    },

    async submitFormForRAG() {
      try {
        console.log("paths: " + this.filePaths);
        const requestBody = {
          datasetName: this.selectedButton.value,
          question: this.inputData,
          file_abs_paths: this.filePaths,
        };
        const res = await axios.post('http://localhost:8999/es/rag_prompt', requestBody, {
          headers: {
            'Content-Type': 'application/json'
          }
        });

        // console.log("responseFromServer: " + res.data);
        console.log(res.data);
        this.RAG = res.data.prompt;
        // console.log("RAG:" + this.RAG);

        this.parameters = {};
        for (const [key, value] of Object.entries(res.data.source)) {
          const filePath = key;
          const fileName = key.split('/').pop(); // Extract the file name
          const content = value.content;
          const fileScore = value.file_score;

          this.parameters[fileName] = { 'content': content, 'fileScore': fileScore };
        }

        console.log('parameters: ' + this.parameters);
      } catch (error) {
        console.error('Error:', error);
        this.response = '请求失败，请检查控制台获取更多信息。';
      }
    },

    handleValueUpdate(newValue) {
      this.selectedButtonHistory.label = this.selectedButton.label;
      this.selectedButtonHistory.value = this.selectedButton.value;
      this.selectedButtonHistory.description = this.selectedButton.description;

      this.selectedButton.label = newValue.label;
      this.selectedButton.value = newValue.value;
      this.selectedButton.description = newValue.description;
      console.log("Update-selectedButton: " + this.selectedButton);

      this.$refs.knowledgeDB.selectedOption = this.selectedButton.value;
      this.disabledHistory = this.isDisabled;
      if (this.selectedButton.value == 'null') {
        this.isDisabled = false;
      } else {
        this.isDisabled = true;
      }
    },

    async navigateToPage() {
      const url = 'https://palm.seu.edu.cn/';
      window.open(url, '_blank');
    },

    async triggerKnowledgeDBView() {
      this.isKnowledgeDB = !this.isKnowledgeDB;
    },

    triggerKnowledgeDBPreview() {
      this.$refs.knowledgeDBPreview.fetchFileTree();
      this.isKnowledgeDBPreview = !this.isKnowledgeDBPreview;
      this.$refs.knowledgeDBPreview.isShow = false;
      this.$refs.knowledgeDBPreview.isDocxShow = false;
      this.$refs.knowledgeDBPreview.showSen = true;
      this.$refs.knowledgeDBPreview.selectedFile = null;
    },

    receiveDBContentFromChild(payload) {
      // 接收传递过来的知识库value
      this.selectedOption = payload;
      console.log("knowledgeDB: " + this.selectedOption);
    },

    async toggleSidebar() {
      if (this.isSidebarOpen) {
        this.$refs.sidebarOfDB.selectedDB.label = this.selectedButton.label;
        this.$refs.sidebarOfDB.selectedDB.value = this.selectedButton.value;
        this.$refs.sidebarOfDB.selectedDB.description = this.selectedButton.description;
        this.$refs.sidebarOfDB.activeButton = this.selectedButton.value;

        console.log("关闭：" + this.selectedButton);
        this.isSidebarOpen = !this.isSidebarOpen;
        this.isActive = !this.isActive;
      } else {
        this.isSidebarOpen = !this.isSidebarOpen;
        this.isActive = !this.isActive;
        this.$nextTick(() => {
          this.$refs.sidebarOfDB.selectedDB.label = this.selectedButton.label;
          this.$refs.sidebarOfDB.selectedDB.value = this.selectedButton.value;
          this.$refs.sidebarOfDB.selectedDB.description = this.selectedButton.description;
          this.$refs.sidebarOfDB.activeButton = this.selectedButton.value;
          console.log("开启： " + this.selectedButton);
        });
      }
    },

    async toggleFilePreview() {
      this.isPreviewFile = !this.isPreviewFile;
      this.isPreview = !this.isPreviewFile;
    },

    async toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      if (this.isDarkMode) {
        document.body.classList.add('dark-mode');
      } else {
        document.body.classList.remove('dark-mode');
      }
    },

    async changeColor() {
      this.textColor = 'blue';
    },

    async resetColor() {
      this.textColor = 'black';
      setTimeout(() => {
        this.textColor = 'white';
      }, 3000);
    },

    async displayMessage(message, sender) {
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

    async stopSendMessage() {
      this.loading = false;
      if (document.getElementById('img')) {
        document.getElementById('chatlog').removeChild(document.getElementById('img'));
      }
    },

    async sendData() {
      if (this.loading) {
        return;
      }
      if (!this.pdfFileOpen && this.isPdfFile) {
        alert('请等待pdf加载完毕');
        return;
      }
      if (!this.docxFileOpen && this.isDocxFile) {
        alert('请等待文档加载完毕');
        return;
      }
      if (!this.txtFileOpen && this.isTxtFile) {
        alert('请等待文档加载完毕');
        return;
      }
      console.log("isDisabled：" + this.isDisabled);
      if (this.isDisabled) {
        console.log('datasetName: ' + this.selectedButton.value);
        console.log('question: ' + this.inputData);
        console.log('file_abs_paths: ' + this.filePaths);
        await this.submitFormForRAG();
      }

      // 配置marked，使其与highlight.js集成
      marked.setOptions({
        renderer: new marked.Renderer(),
        highlight: function (code, lang) {
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
        math: function (text, math) {
          // 使用katex渲染数学公式
          katex.render(math, document.createElement('div'), {
            displayMode: true
          });
          return text;
        }
      });

      if (this.inputData.trim() !== "") {
        this.loading = true;
        this.isChatBoxOpen = true;
        let usermessage = this.inputData;
        this.displayMessage(usermessage, 'user'); //展示用户问题
        this.inputData = ''; // 清空输入框

        // 创建一个新的img元素，用于加载动画
        var img = document.createElement('img');
        img.id = "img";
        img.style.width = "100px";
        img.style.height = "auto";
        // 设置img的src属性
        img.src = this.gif.url;
        // 将img元素添加到div中
        document.getElementById('chatlog').appendChild(img);
        document.getElementById('chatbox').scrollTop = document.getElementById('chatbox').scrollHeight;

        if (!this.history) {
          this.history.push({ role: "system", content: "you are a helpful assistant" });
        }

        //合成用户发送的信息
        var userMessageContent = '';

        if (!this.isDisabled) {
          if (this.set != this.fileName) {
            this.isHighlighted = false;
            this.set = this.fileName;
            if (this.isImageFile) {
              userMessageContent = "问题：" + usermessage;
            } else if (this.isPdfFile) {
              userMessageContent = this.cleanPdfText(this.pdfDocumentContent) + '\n\n' + "问题：" + usermessage;
            } else if (this.isTxtFile) {
              userMessageContent = this.txtFileContent + '\n\n' + "问题：" + usermessage;
            } else if (this.docxPlainTextContent) {
              userMessageContent = this.docxPlainTextContent + '\n\n' + "问题：" + usermessage;
            } else {
              userMessageContent = "问题：" + usermessage;
            }
          } else {
            userMessageContent = "问题：" + usermessage;
          }
        } else {
          userMessageContent = this.RAG + '\n\n' + "问题：" + usermessage;
        }

        if (this.history.length >= 10) {
          this.history.shift();
        }

        if ((this.disabledHistory == this.isDisabled && this.isDisabled) || (this.disabledHistory && !this.isDisabled)) {
          if (!(this.history.length === 1)) {
            let lastElement = this.history.pop();
            this.history.push({ "role": "user", "content": this.userMessageHistory });
          }
        }
        this.userMessageHistory = usermessage;
        // 更新对话历史
        this.history.push({ "role": "user", "content": userMessageContent });

        // console.log("Question History: " + this.history);
        // console.log("userMessageContent: " + userMessageContent);
        // 构建请求数据
        var data = {
          "model": "qwen2-7b",
          "messages": this.history,
          "temperature": 0.8,
          "top_p": 0.95,
          "repetition_penalty": 1.1,
          "stream": true,
        };

        try {
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
          messContainerSystem.style.width = 'auto';
          // messContainerSystem.style.display = 'flex';
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
            this.wholeMessage = '';

            while (true) {  //eslint-disable-line no-constant-condition
              const { done, value } = await reader.read();
              if (done) {
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
                          // console.log(this.wholeMessage);
                          let handledMessage = '';
                          let latexMessage = '';
                          latexMessage = this.renderMath(this.wholeMessage);
                          handledMessage = marked(latexMessage);
                          messageElementSystem.innerHTML = handledMessage;

                          // 高亮代码块
                          document.querySelectorAll('pre code').forEach(function (block) {
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

                            if (!block.hasAttribute('line-number-tagged')) {
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
                          // console.log(content);
                        }
                      }
                    } catch (error) {
                      console.error('Error parsing JSON:', error);
                    }
                  }
                }
              }
            }
            console.log(this.wholeMessage);

            //仅知识库状态下可用
            if (this.isDisabled && !(Object.keys(this.parameters).length === 0)) {
              let tool = document.createElement('div');
              tool.id = 'tool';
              tool.style.textAlign = 'right';
              tool.style.width = '100%';

              let span = document.createElement('span');
              span.id = 'span';
              span.innerHTML = '✨';

              let toolTip = document.createElement('div');
              toolTip.className = 'el-tooltip';
              toolTip.innerHTML = '这是一个提示框';
              toolTip.style.position = 'absolute';
              toolTip.style.backgroundColor = '#fff';
              toolTip.style.color = '#000';
              toolTip.style.padding = '5px 10px';
              toolTip.style.borderRadius = '4px';
              toolTip.style.display = 'none'; // 初始隐藏
              toolTip.style.width = '40%';
              toolTip.style.maxHeight = '500px';
              toolTip.style.overflowY = 'auto';
              toolTip.style.border = '1px solid #ccc';
              document.body.appendChild(toolTip);

              // 示例数据
              var parameters = {};

              for (const [key, value] of Object.entries(this.parameters)) {
                const filePath = key;
                const fileName = key.split('/').pop(); // Extract the file name
                const content = value.content;
                const fileScore = value.fileScore;

                parameters[fileName] = { 'path': filePath, 'content': content, 'fileScore': fileScore };
              }

              // 格式化参数为 HTML
              const formatParameters = (params) => {
                let content = '';
                // Convert the object to an array and sort by fileScore in descending order
                const sortedEntries = Object.entries(params).sort((a, b) => b[1].fileScore - a[1].fileScore);

                // Format the sorted entries into HTML
                for (const [file, values] of sortedEntries) {
                  console.log(values.fileScore);
                  content += `<strong style="color: blue;">${file}:</strong> <br> Content: <pre>${values.content.join('\n\n')}</pre> <br>`;
                }
                return content;
              };

              console.log("tooltip content: " + formatParameters(parameters));

              // 设置 tooltip 内容
              toolTip.innerHTML = formatParameters(parameters);


              span.addEventListener('mouseover', function (event) {
                toolTip.style.left = event.pageX + 'px';
                toolTip.style.top = event.pageY + 'px';
                toolTip.style.display = 'block';

                // 确保 tooltip 在界面内
                const tooltipRect = toolTip.getBoundingClientRect();
                const viewportWidth = window.innerWidth;
                const viewportHeight = window.innerHeight;

                if (tooltipRect.right > viewportWidth) {
                  toolTip.style.left = (viewportWidth - tooltipRect.width) + 'px';
                }
                if (tooltipRect.bottom > viewportHeight) {
                  toolTip.style.top = (viewportHeight - tooltipRect.height) + 'px';
                }
              });

              span.addEventListener('mouseout', function () {
                toolTip.style.display = 'none';
              });

              toolTip.addEventListener('mouseover', function () {
                toolTip.style.display = 'block';
              });

              toolTip.addEventListener('mouseout', function () {
                toolTip.style.display = 'none';
              });



              tool.appendChild(span);
              messageElementSystem.appendChild(tool);



              //添加文件行
              let fileDiv = document.createElement('div');
              fileDiv.style.height = 'auto';
              fileDiv.style.maxWidth = '250px';
              fileDiv.style.padding = '0.05%';
              fileDiv.style.borderRadius = '10px';
              fileDiv.style.border = '1px solid #ccc';

              for (const [key, value] of Object.entries(parameters)) {
                const fileName = key;
                const filepath = value.path;
                let fileContainer = document.createElement('div');
                fileContainer.style.borderRadius = '10px';
                fileContainer.style.border = 'none';
                fileContainer.style.display = 'flex';
                fileContainer.style.padding = '1px';
                fileContainer.style.overflowX = 'auto';

                let icon = document.createElement('div');
                icon.style.width = '18px';
                icon.style.height = '18px';
                icon.style.backgroundImage = "url('/assets/fileIcon.svg')";
                icon.style.backgroundSize = 'contain'; // 使用 contain 以保持长宽比
                icon.style.backgroundPosition = 'center';
                icon.style.backgroundRepeat = 'no-repeat'; // 防止图片重复

                fileContainer.appendChild(icon);

                let span = document.createElement('span');
                span.innerHTML = fileName;

                fileContainer.appendChild(span);
                fileDiv.appendChild(fileContainer);

                // 添加点击事件监听器
                fileContainer.addEventListener('click', () => {
                  console.log(`File clicked: ${fileName}`);
                  // 你可以在这里添加更多的逻辑，例如打开文件或显示文件详情
                  this.isKnowledgeDBPreview = !this.isKnowledgeDBPreview;
                  this.$refs.knowledgeDBPreview.fetchFileTree();
                  const fileExtension = fileName.split('.').pop().toLowerCase();
                  var isDocx = false;

                  if (fileExtension === 'docx') {
                    this.$refs.knowledgeDBPreview.isDocxShow = true;
                    this.$refs.knowledgeDBPreview.isShow = false;
                  }else{
                    this.$refs.knowledgeDBPreview.isShow = true;
                    this.$refs.knowledgeDBPreview.isDocxShow = false;
                  }
                  this.$refs.knowledgeDBPreview.showSen = false;
                  const relativePath = `${this.selectedButton.label}/${fileName}`;
                  this.$refs.knowledgeDBPreview.selectedFile = relativePath;
                });
              }


              messContainerSystem.appendChild(fileDiv);
            }


            if (!this.isHighlighted) {
              this.isHighlighted = true;
              //返回消息在预览文档中高亮文字
              if (this.isTxtFile) {
                this.isPreviewFile = true;
                this.isPreview = false;
                await this.sendDataToBackendForKeys(this.txtFileContent, this.wholeMessage, usermessage);
                this.txtFileContentPage = this.highlightedContent(this.txtFileContent);
              } else if (this.isPdfFile) {
                if (!this.pdfDocumentContent) {
                  console.log("pdfDocumentContent Null!");
                  return;
                }
                this.isPreviewFile = true;
                this.isPreview = false;
                await this.sendDataToBackendForKeys(this.cleanPdfText(this.pdfDocumentContent), this.wholeMessage, usermessage);
                this.searchFile();
              } else if (this.isDocxFile) {
                this.isPreviewFile = true;
                this.isPreview = false;
                await this.sendDataToBackendForKeys(this.docxPlainTextContent, this.wholeMessage, usermessage);
                this.docxContent = this.highlightKeySentences(this.docxContent);
              }
            }
            // this.history.push({'role': 'assistant', 'content': this.wholeMessage});
            this.loading = false;
            // this.returnMessage = '';
          }
          else {
            this.loading = false;
          }
        } catch (error) {
          console.error('Error parsing JSON:', error);
        }
      }
    },

    renderMath(text) {
      // 匹配并处理块级公式，例如 $$...$$ 或 \[...\]
      text = text.replace(/(\$\$|\\\[)([\s\S]+?)(\$\$|\\\])/g, function (_, delimiter, math) {
        return katex.renderToString(math, {
          displayMode: true,
          throwOnError: false,
        });
      });

      // 匹配并处理行内公式，例如 $...$ 或 \(...\)
      text = text.replace(/(\$|\\\()(.+?)(\$|\\\))/g, function (_, delimiter, math) {
        return katex.renderToString(math, {
          displayMode: false,
          throwOnError: false,
        });
      });

      return text;
    },

    async addLineNumbersToBlock(block) {
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
    },

    async handleFileChange(event) {
      this.isPreviewFile = true;
      this.isPreview = false;
      const file = event.target.files[0];
      this.fileName = file.name;  // 获取文件名称
      // var pdfPath = encodeURIComponent(file);
      if (file) {
        if (file.type === 'application/pdf') {
          this.isPdfFile = true;
          this.isImageFile = false;
          this.isTxtFile = false;
          this.isDocxFile = false;
          this.isDocFile = false;

          this.selectedFile = file;

          const reader = new FileReader();
          reader.onload = async (e) => {
            const viewerUrl = `${process.env.BASE_URL}lib/pdfjs/web/viewer.html?file=`;
            const typedArray = new Uint8Array(e.target.result);
            const pdfUrl = URL.createObjectURL(new Blob([typedArray], { type: 'application/pdf' }));
            this.previewUrl = `${viewerUrl}${encodeURIComponent(pdfUrl)}`;

            await this.loadPdfContent(pdfUrl);

            // 使用 PDF.js 的 viewer.html 来展示 PDF
            console.log(pdfUrl);
            try {
              await this.loadPdf(pdfUrl);
              // console.log(this.extractedPDFText);
            } catch (error) {
              console.error('从PDF提取文本时出错', error);
            }
            this.pdfFileOpen = true;
            ElMessage.success('PDF上传成功！');
            // alert("PDF上传成功！");
          };
          reader.readAsArrayBuffer(file);
        } else if (file.type === "text/plain") {
          this.isPdfFile = false;
          this.isImageFile = false;
          this.isTxtFile = true;
          this.isDocxFile = false;
          this.isDocFile = false;

          const reader = new FileReader();
          reader.onload = (e) => {
            this.txtFileContent = e.target.result; // 读取到的内容赋值给 fileContent
            this.txtFileContentPage = this.txtFileContent;
            console.log(this.txtFileContent);
          };
          reader.readAsText(file); // 以文本形式读取文件
          this.txtFileOpen = true;
          ElMessage.success('Txt上传成功！');
          // alert("Txt上传成功！");
        } else if (file.name.endsWith(".docx")) {
          this.isPdfFile = false;
          this.isImageFile = false;
          this.isTxtFile = false;
          this.isDocxFile = true;
          this.isDocFile = false;

          try {
            const arrayBuffer = await file.arrayBuffer();
            const result = await mammoth.convertToHtml({ arrayBuffer });
            this.docxContent = result.value; // 将解析后的 HTML 内容赋值给 docxContent

            // 解析纯文本内容
            this.docxPlainTextContent = this.extractPlainText(this.docxContent);
            console.log(this.docxPlainTextContent);
          } catch (error) {
            console.error("文档解析失败:", error);
            alert("文档解析失败，请检查文件格式或内容！");
          }
          this.docxFileOpen = true;
          ElMessage.success('docx文档上传成功！');
          // alert("docx文档上传成功！");
        } else if (this.isImage()) {
          this.isPdfFile = false;
          this.isImageFile = true;
          this.isTxtFile = false;
          this.isDocxFile = false;
          this.isDocFile = false;
          const reader = new FileReader();
          reader.onload = (e) => {
            this.previewUrl = e.target.result;
          };
          reader.readAsDataURL(file);
        } else {
          this.isImageFile = false;
          this.isPdfFile = false;
          this.isTxtFile = false;
          this.isDocxFile = false;
          this.isDocFile = false;

          alert('请选择一个有效的文件');
          this.isPreviewFile = false;
          this.isPreview = false;
        }
      }
    },
    extractPlainText(htmlContent) {
      // 创建一个虚拟的 DOM 元素
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = htmlContent;

      // 提取纯文本内容
      return tempDiv.textContent || tempDiv.innerText || "";
    },

    async loadPdfContent(pdfUrl) {
      const self = this;
      // 使用 pdf.js 获取 PDF 文件
      pdfjs.getDocument(pdfUrl).promise.then(function (pdf) {
        const numPages = pdf.numPages;
        const textPromises = [];

        // 遍历每一页获取文本内容
        for (let i = 1; i <= numPages; i++) {
          textPromises.push(
            pdf.getPage(i).then(function (page) {
              return page.getTextContent().then(function (textContent) {
                // 将文本内容拼接成字符串
                return textContent.items.map(item => item.str).join(' ');
              });
            })
          );
        }

        // 等待所有页面的文本内容解析完毕
        Promise.all(textPromises).then(function (pagesText) {
          // 将所有页面的文本合并成一个完整的字符串
          const fullText = pagesText.join('\n');
          self.pdfDocumentContent = fullText;
          console.log(self.cleanPdfText(self.pdfDocumentContent)); // 在这里可以对文本进行操作
        });
      }).catch(function (error) {
        console.error('Error loading PDF:', error);
      });
    },


    async loadPdf(url) {
      try {
        const loadingTask = pdfjs.getDocument(url);
        this.pdfDocument = await loadingTask.promise;
        // 确保 pdfDoc 已经加载成功
        if (!this.pdfDocument) {
          console.error('PDF 文档未加载成功!!');
          return;
        }
        console.log(this.pdfDocument);

        this.pdfParams.pdfPageTotal = this.pdfDocument.numPages;

        for (let pageNum = 1; pageNum <= this.pdfParams.pdfPageTotal; pageNum++) {
          await this.renderPdfPage(pageNum);
        }

        // 渲染成功后设置滚动条位置
        this.centerScroll();
      } catch (error) {
        console.error('加载PDF时出错', error);
      }
    },

    // // 提取PDF中的文本内容
    // async extractTextFromPdf() {
    //   const totalText = []; // 用于存储每页的文本内容
    //   const totalPages = this.pdfDocu.pdfPageTotal;

    //   for (let i = 1; i <= totalPages; i++) {
    //     const page = await this.pdfDocu.getPage(i);
    //     const textContent = await page.getTextContent();

    //     // 获取每页的文本内容并拼接成字符串
    //     const pageText = textContent.items.map(item => item.str).join(" ");
    //     totalText.push(pageText);
    //   }

    //   // 将所有页的文本内容保存到 extractedPDFText 中
    //   this.extractedPDFText = totalText.join("\n\n"); // 将所有页的文本用换行分隔
    //   if(!this.extractedPDFText){
    //     console.log("OK!");
    //     console.log(this.extractedPDFText);
    //   }
    // },

    // extractTextFromPage(textContent, pageNumber) {
    //   const textLayer = document.getElementById(`text-layer${pageNumber}`);
    //   textLayer.innerHTML = ''; // 清空现有的文本图层

    //   textContent.items.forEach(item => {
    //     const span = document.createElement('span');
    //     span.textContent = item.str;
    //     span.style.left = `${item.transform[4]}px`;
    //     span.style.top = `${item.transform[5]}px`;
    //     span.style.fontSize = `${item.height}px`;
    //     textLayer.appendChild(span);
    //   });

    //   // 更新 extractedPDFText
    //   this.extractedPDFText += textContent.items.map(item => item.str).join(' ') + '\n';
    // },

    async renderPdfPage(pageNumber) {
      if (pageNumber < 1 || pageNumber > this.pdfParams.pdfPageTotal) {
        throw new Error(`Invalid page number: ${pageNumber}`);
      }
      const page = await this.pdfDocument.getPage(pageNumber);

      //获取默认的 viewport（缩放）
      const viewport = page.getViewport({
        scale: this.pdfParams.pdfScale * window.devicePixelRatio, // 根据设备像素比调整 scale
      });
      const canvas = document.getElementById(`pdf-render${pageNumber}`);
      if (!canvas) {
        console.error(`找不到 id 为 pdf-render${pageNumber} 的 canvas 元素`);
        throw new Error(`找不到 id 为 pdf-render${pageNumber} 的 canvas 元素`);
        // return reject('Canvas not found');
      }
      const context = canvas.getContext('2d');
      if (!context) {
        console.error('无法获取 2D 绘图上下文');
        throw new Error('无法获取 2D 绘图上下文');
      }

      //设置 Canvas 尺寸（根据 viewport 尺寸缩放）
      canvas.width = viewport.width;
      canvas.height = viewport.height;

      // 缩放 canvas 显示比例
      canvas.style.width = `${viewport.width / window.devicePixelRatio}px`;
      canvas.style.height = `${viewport.height / window.devicePixelRatio}px`;

      var renderContext = {
        canvasContext: context,
        viewport: viewport,
        // textLayer: {
        //   textContentStream: page.streamTextContent(),
        //   container: document.getElementById(`text-layer${pageNumber}`),
        //   viewport: viewport,
        //   enhanceTextSelection: true, // 选择文本时的优化
        //   textDivs: [] // 存储文本块的数组
        // },
        textLayerFactory: this.textLayerFactory,
        textLayerDiv: document.getElementById(`text-layer${pageNumber}`),
        textContent: await page.getTextContent(),
      };
      page.render(renderContext).promise.then(function () {
        console.log('Page rendered');
      });

      // await page.render({
      //   canvasContext: context,
      //   viewport: viewport,
      // }).promise;

      // 渲染成功后设置滚动条位置
      this.centerScroll();
      // 提取文本内容
      const textContent = await page.getTextContent();
      this.renderTextLayer(textContent);
    },

    // 清空所有 Canvas 内容
    clearCanvas() {
      const canvases = document.querySelectorAll(".pdf-viewer");
      canvases.forEach((canvas) => {
        const context = canvas.getContext("2d");
        if (context) {
          context.clearRect(0, 0, canvas.width, canvas.height);
        }
      });
    },

    // 上一页功能
    renderTextLayer(textContent) {
      // const textLayer = document.getElementById(`text-layer${pageNumber}`);
      // textLayer.innerHTML = ''; // Clear existing text layer

      // textContent.items.forEach(item => {
      //   const span = document.createElement('span');
      //   span.textContent = item.str;
      //   span.style.fontSize = `${item.height}px`;
      //   span.style.left = `${item.transform[4] * viewport.scale}px`;
      //   span.style.top = `${item.transform[5] * viewport.scale}px`;
      //   span.style.position = 'absolute';
      //   span.style.whiteSpace = 'pre'; // Preserve whitespace
      //   span.style.color = 'black'; // Ensure text is visible
      //   textLayer.appendChild(span);
      // });

      // Update extractedPDFText
      this.extractedPDFText += textContent.items.map(item => item.str).join(' ') + '\n';
    },

    prevPage() {
      if (this.pdfParams.currentPageNumber > 1) {
        this.pdfParams.currentPageNumber = this.pdfParams.currentPageNumber - 1;
        this.getPdfPage(this.pdfParams.currentPageNumber);
      }
    },

    // 下一页功能
    nextPage() {
      if (this.pdfParams.currentPageNumber < this.pdfParams.pdfPageTotal) {
        this.pdfParams.currentPageNumber = this.pdfParams.currentPageNumber + 1;
        console.log(this.pdfParams.currentPageNumber);
        this.getPdfPage(this.pdfParams.currentPageNumber);
      }
    },

    // 放大 PDF 页面
    async scaleUp() {
      const maxScale = window.screen.width > 1440 ? 1.4 : 1.2;
      if (this.pdfParams.pdfScale < maxScale) {
        this.pdfParams.pdfScale += 0.1;
        for (let pageNum = 1; pageNum <= this.pdfParams.pdfPageTotal; pageNum++) {
          await this.renderPdfPage(pageNum);
        }
        // await this.getPdfPage(this.pdfParams.currentPageNumber);
      }
    },

    // 缩小 PDF 页面
    async scaleDown() {
      const minScale = 0.5;
      if (this.pdfParams.pdfScale > minScale) {
        this.pdfParams.pdfScale -= 0.1;
        for (let pageNum = 1; pageNum <= this.pdfParams.pdfPageTotal; pageNum++) {
          await this.renderPdfPage(pageNum);
        }
        // await this.getPdfPage(this.pdfParams.currentPageNumber);
      }
    },

    // 设置横向滚动条居中
    centerScroll() {
      this.$nextTick(() => {
        const container = this.$refs.pdfContainer;
        if (container) {
          container.scrollLeft =
            container.scrollWidth / 2 - container.clientWidth / 2;
        }
      });
    },

    isImage() {
      // 判断预览的文件是否为图片
      return /\.(jpeg|jpg|gif|png|bmp|webp)$/i.test(this.fileName);
    },
    isPdf() {
      // 判断预览的文件是否为PDF
      return /\.(pdf)$/i.test(this.fileName);
    },
    isTxt() {
      // 判断预览的文件是否为Txt
      return /\.(txt)$/i.test(this.fileName);
    },

    triggerFileUpload() {
      if (!this.isDisabled) {
        // 触发隐藏的文件上传 input
        this.$refs.fileInput.click();
      }
    },

    // 向后端发送数据以提取关键词
    async sendDataToBackendForKeys(ContentFromFile, ContentFromSystem, question) {
      const url = 'http://localhost:8999/longcontext/uploadfile';
      const requestBody = {
        contents: [ContentFromFile],
        answer: ContentFromSystem,
        question: question,
      };

      try {
        const response = await fetch(url, {
          method: 'POST',
          // credentials: "include",
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestBody),
        });

        // 检查请求是否成功
        if (!response.ok) {
          ElMessage.error('HTTP error! status: ' + response.status);
          // throw new Error(`HTTP error! status: ${response.status}`);
        }

        // 解析JSON响应
        const responseData = await response.json();

        // 检查返回的 code 是否为 0
        if (responseData.code === 0) {
          // 处理成功返回的数据
          // console.log('Response:', responseData.data.response);
          this.keywords = responseData.data.response;
          console.log('Keywords:', this.keywords);
        } else {
          // 处理错误消息
          console.error('Error message:', responseData.message);
        }
      } catch (error) {
        // 捕获并处理错误
        console.error('Fetch error:', error);
      }
    },
    // 高亮匹配txt关键词的函数
    highlightedContent(rawTextContent) {
      let content = rawTextContent;

      console.log(this.keywords);
      // 如果没有提取到关键词，直接返回原始内容
      if (!this.keywords.length) {
        return content;
      }

      this.keywords.forEach((word) => {
        // 转义关键词中的特殊字符，并替换换行符为 \s*，以便匹配多行内容
        const escapedWord = word.replace(/\\([.*+?^${}()|[\]\\])/g, '\\$&');
        console.log('escapedWord: ' + escapedWord);
        const regex = new RegExp(`(${escapedWord})`, "gi");
        content = content.replace(regex, '<span class="highlight">$1</span>');
      });
      return content;
    },
    // 对特殊字符进行转义
    escapeRegExp(string) {
      return string.replace(/\\([.()?!,;])/g, "$1"); // 将正则表达式中的特殊字符进行转义
    },

    highlightKeySentences(htmlContent) {
      console.log(this.keywords);

      // 如果没有提取到关键词，直接返回原始内容
      if (!this.keywords.length) {
        return htmlContent;
      }
      let highlightedContent = htmlContent;

      for (const word of this.keywords) {
        const sentenceLength = word.length;
        const partLength = Math.ceil(sentenceLength / 2); // 计算每部分的长度
        const results = [];

        for (let i = 0; i < sentenceLength; i += partLength) {
          results.push(word.slice(i, i + partLength)); // 切割句子
        }

        for (const result of results) {
          // 创建正则表达式，使用 `g` 标志进行全局匹配
          const regex = new RegExp(`(${result})`, 'gi');
          // 使用 <span> 标签高亮匹配到的句子
          highlightedContent = highlightedContent.replace(regex, '<span class="highlight">$1</span>');
        }
      }
      return highlightedContent;
    },

    // 匹配pdf关键词的高亮函数
    async searchFile() {
      // 如果没有提取到关键词，直接返回原始内容
      if (!this.keywords.length) {
        return;
      }
      let iframe = document.getElementById('ifm')
      if (iframe && iframe.contentWindow && iframe.contentWindow.PDFViewerApplication) {
        console.log("pdf已加载");
        iframe.contentWindow.PDFViewerApplication.findBar.findField.click();
        iframe.contentWindow.PDFViewerApplication.findBar.findField.focus();

        for (const word of this.keywords) {
          const sentenceLength = word.length;
          const partLength = Math.ceil(sentenceLength / 2); // 计算每部分的长度
          const results = [];

          for (let i = 0; i < sentenceLength; i += partLength) {
            results.push(word.slice(i, i + partLength)); // 切割句子
          }

          for (const result of results) {
            // console.log(`Keywords: ${word}`);
            // 在每个关键词完成高亮后等待一小段时间，以确保渲染完成
            await new Promise(resolve => setTimeout(resolve, 400));  // 等待 500 毫秒
            await this.contentHighlighter(result, iframe);
          }
          // console.log(`Keywords: ${word}`);
          // await this.contentHighlighter(word, iframe);
          // // 在每个关键词完成高亮后等待一小段时间，以确保渲染完成
          // await new Promise(resolve => setTimeout(resolve, 500));  // 等待 500 毫秒
        }
        // iframe.contentWindow.PDFViewerApplication.findBar.dispatchEvent(new Event('highlightallchange'));
        // iframe.contentWindow.PDFViewerApplication.findBar.close();
      }
    },
    // 高亮pdf关键词的函数
    contentHighlighter(word, iframe) {
      // 转义关键词中的特殊字符，并替换换行符为 \s*，以便匹配多行内容
      const escapedWord = this.escapeRegExp(word).replace(/\r\n|\n|\r/g, "\\s*");
      console.log(escapedWord);
      // console.log('iframe.contentWindow:', iframe.contentWindow);
      // console.log('iframe.contentWindow.PDFViewerApplication:', iframe.contentWindow.PDFViewerApplication);
      // 模拟按下 Enter 键
      const enterEvent = new KeyboardEvent('keydown', {
        key: 'Enter',
        keyCode: 13,  // Enter 键的 keyCode 是 13
        code: 'Enter',
        which: 13,
        bubbles: true
      });
      return new Promise((resolve) => {
        iframe.contentWindow.PDFViewerApplication.findBar.findField.click();
        iframe.contentWindow.PDFViewerApplication.findBar.findField.focus();
        iframe.contentWindow.PDFViewerApplication.findBar.highlightAll.checked = true;
        iframe.contentWindow.PDFViewerApplication.findBar.findField.value = escapedWord;
        iframe.contentWindow.PDFViewerApplication.findBar.findField.dispatchEvent(enterEvent);
        iframe.contentWindow.PDFViewerApplication.findBar.dispatchEvent(new Event('highlightallchange'));
        // iframe.contentWindow.PDFViewerApplication.findBar.findNextButton.click();
        resolve();
        setTimeout(function () {
          console.log('等待完成，继续渲染');
        }, 200);
      });
    },
    cleanPdfText(text) {
      // 去除多余的空格，但保留单个英文空格和换行符
      return text
        .replace(/[^\S\r\n]+/g, ' ')  // 替换所有非换行的多余空白字符为一个空格
        .replace(/(?<!\s)-\s+/g, "")  // 左侧无空格右侧有空格删除
        .replace(/\s+-(?!\s)/g, "-")   // 左侧有空格右侧无空格删除
        .replace(/(\(|（)\s+/g, '$1') // 去除中英文前括号后的空格
        .replace(/\s+(?=[（])/g, '')
        .replace(/(?<=[）])\s+/g, '')
        .replace(/\s+(\)|）)/g, '$1') // 去除中英文后括号前的空格
        .replace(/\s+(:|：)/g, '$1')  // 去除中英文冒号前的空格
        .replace(/\s+(,|，)/g, "$1")  //去除中英文逗号前的空格
        .replace(/\s+\./g, ".")       // 去除句号前的空格
        .replace(/\s+。/g, "。")      // 去除句号前的空格
        .replace(/(\“|\“|\“|\‘)\s+/g, "$1") //去除中英文前冒号后的空格
        .replace(/\s+(\”|\”|\”|\’)/g, "$1") //去除中英文后冒号前的空格
        .replace(/(\{|\｛)\s+/g, "$1") //去除中英文前大括号后的空格
        .replace(/\s+(\}|\｝)/g, "$1") //去除中英文后大括号前的空格
        .replace(/†\s+/g, '†') //去除†后的空格
        .replace(/ +/g, ' ') // 将多个空格压缩为一个
        .replace(/(?<=\b[A-Z])\s+(?=[A-Z]{2,})/g, "")
        .replace(/([。？！])\s+/g, '$1') //去除，。？！之后的空格
        .replace(/([\u4e00-\u9fff])\s+([\u4e00-\u9fff])/g, '$1$2')  // 去除中文字符之间的空格 
        .trim(); // 去除文本开头和结尾的空格
    },
  },
}
</script>

<style>
/* 你可以根据需要自定义样式 */
.hljs {
  border-radius: 5px;
  /* 圆角边框 */
  border: 2px solid black;
  /* 黑框 */
}

/* 确保代码文本颜色高亮 */
.hljs-keyword,
.hljs-selector-tag,
.hljs-literal,
.hljs-section,
.hljs-link {
  color: #333;
  /* 设置文本颜色 */
}

#Total {
  display: flex;
  justify-content: center;
  text-align: center;
  width: 100%;
  height: 100%;
  margin-bottom: 0;
}

#SlideButtonDiv {
  display: inline-block;
  padding: 0;
  margin-top: 1%;
  width: 1.7%;
  height: 98%;
  margin-top: 1%;
  margin-bottom: 1%;
  margin-right: 0.3%;
  text-align: center;
  justify-content: center;
}

#slideBarButton {
  padding: 0;
  width: 100%;
  padding-top: 100%;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  background-image: url("../assets/green_icon.svg");
  /* 替换为点击后 SVG 图片路径 */
  background-size: 99% 99%;
  background-position: center;
  background-repeat: no-repeat;
  background-color: transparent;
}

/* 切换后的背景图片 */
#slideBarButton.active {
  background-image: url("../assets/red_x.svg");
  /* 替换为点击后 SVG 图片路径 */
}

#slideBarButton:hover {
  background-color: green;
}

#slideBarButton.active:hover {
  background-color: red;
}

#BarContainer {
  justify-content: center;
  align-items: center;
  display: inline-block;
  width: 10%;
  height: 95.5%;
  margin-top: 1%;
  margin-bottom: 1%;
  margin-right: 0.5%;
  padding: 0;
  text-align: center;
  background: rgba(255, 255, 255, 0.75);
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

#BarContainer.active {
  background: rgba(0, 0, 0, 0.5);
}

#BarContainer.active>p {
  color: white;
}

#Bar {
  position: relative;
  width: 100%;
  height: 90%;
  text-align: center;
  justify-content: center;
  align-items: center;
}

#sideBarOfDB {
  justify-content: center;
  align-items: center;
  display: inline-block;
  width: 10%;
  height: 95.5%;
  margin-top: 1%;
  margin-bottom: 1%;
  margin-right: 0.5%;
  padding: 0;
  text-align: center;
  background: rgba(255, 255, 255, 0.75);
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

#ChatContainer {
  display: inline-block;
  width: 70%;
  margin-top: 1%;
  margin-bottom: 1%;
  text-align: center;
  justify-content: center;
}

#container {
  /*background: rgba(255,255,255,0.75);*/
  display: flex;
  flex-direction: column;
  position: relative;
  background-color: transparent;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  height: 100%;
  text-align: center;
}

.Picture {
  position: absolute;
  top: 200px;
  left: 280px;
}

#palmLogo {
  width: 60%;
  aspect-ratio: 1 / 1;
  /* 设置宽高比为1:1，使宽度等于高度 */
  border-radius: 10px;
  border: none;
  background-color: rgba(255, 255, 255, 0.8);
  background-image: url("../assets/PALMLogo.png");
  background-size: auto 100%;
  background-position: center;
  background-repeat: no-repeat;
  cursor: pointer;
}

#palmLogo:hover {
  box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24), 0 17px 50px 0 rgba(0, 0, 0, 0.19);
}

#KnowledgeDBButton {
  width: 60%;
  aspect-ratio: 2 / 1;
  /* 设置宽高比为1:1，使宽度等于高度 */
  border-radius: 10px;
  border: none;
  background-color: rgba(255, 255, 255, 0.8);
  background-image: url("../assets/sharpicons_connection-points.svg");
  background-size: auto 100%;
  background-position: center;
  background-repeat: no-repeat;
  cursor: pointer;
}

#KnowledgeDBButton:hover {
  box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24), 0 17px 50px 0 rgba(0, 0, 0, 0.19);
}

#msg {
  background-color: thistle;
  opacity: 0.8;

  border-radius: 10px;
  height: 4%;
  text-align: center;
  justify-content: center;
  margin-bottom: 0.05%;
}

#msg p {
  font-size: 100%;
  text-size-adjust: 100%;
  margin-top: 0.5px;
  margin-bottom: 0.5px;
}

#msg.active {
  background-color: rgba(0, 0, 0, 0.5);
}

#chatbox {
  border: 1px solid transparent;
  border-radius: 10px;
  height: 85%;
  padding: 0.05%;
  overflow-y: scroll;
  margin-top: 0.15%;
  margin-bottom: 0.05%;
  overflow-y: auto;
  overflow-x: auto;
  background: rgba(255, 255, 255, 0.8);
}

#chatbox.active {
  background-color: rgba(0, 0, 0, 0.5);
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
  bottom: 0.05%;
  border-radius: 10px;
  height: 10%;
  width: 100%;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 1);
  box-sizing: border-box;
}

.custom-file-upload {
  margin-left: 1%;
  height: 80%;
  aspect-ratio: 1 / 1;
  /* 设置宽高比为1:1，使宽度等于高度 */
  border: none;
  background-color: transparent;
  background-image: url("../assets/attachment.svg");
  background-size: auto 70%;
  background-position: center;
  background-repeat: no-repeat;
  color: black;
  border-radius: 50%;
  cursor: pointer;
}

.custom-file-upload:hover {
  box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24), 0 17px 50px 0 rgba(0, 0, 0, 0.19);
}

.custom-file-upload.active {
  opacity: 0.5;
}

.custom-file-upload.active:hover {
  cursor: not-allowed;
}

.message {
  border-radius: 10px;
  margin-bottom: 10px;
}

.user {
  margin-left: auto;
  padding: 5px;
  text-align: left;
  background-color: rgb(136, 213, 185, 0.9);
}

.system {
  white-space: pre-wrap;
  text-align: left;
  padding: 5px;
  background-color: rgb(136, 213, 185, 0.9);
}

#userInput {
  flex-grow: 1;
  /* 第二个元素占据剩余的宽度 */
  margin-right: 1%;
  height: 100%;
  /* 设置最小高度 */
  overflow: hidden;
  /* 防止溢出显示 */
  resize: none;
  /* 禁止用户手动调整大小 */
  border: none;
  border-radius: 5px;
  opacity: 0.7;
  background-color: transparent;
}

#userInput:focus {
  outline: none;
  background-color: transparent;
  box-shadow: none;
  /* 防止出现阴影 */
}

#userInput.active {
  background-color: rgba(0, 0, 0, 0.5);
}

#userInput.active::placeholder {
  color: white;
}

#sendBtn {
  height: 100%;
  aspect-ratio: 1 / 1;
  /* 设置宽高比为1:1，使宽度等于高度 */
  border: none;
  background-color: transparent;
  background-image: url("../assets/button_gray_plane.svg");
  background-size: auto 70%;
  background-position: center;
  background-repeat: no-repeat;
  color: black;
  border-radius: 50%;
  cursor: pointer;

  /*position: absolute;
  right: 15px; /* 定位到容器的右侧 */
  /*top: 3px;*/
}

#sendBtn:hover {
  box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24), 0 17px 50px 0 rgba(0, 0, 0, 0.19);
}

#sendBtnStop {
  height: 100%;
  aspect-ratio: 1 / 1;
  /* 设置宽高比为1:1，使宽度等于高度 */
  border: none;
  background-color: transparent;
  background-image: url("../assets/Stop.svg");
  background-size: auto 70%;
  background-position: center;
  background-repeat: no-repeat;
  color: black;
  border-radius: 50%;
  cursor: pointer;
}

#sendBtnStop:hover {
  box-shadow: 0 12px 16px 0 rgba(0, 0, 0, 0.24), 0 17px 50px 0 rgba(0, 0, 0, 0.19);
}

/*dark mode*/
#mode {
  position: absolute;
  left: 30%;
  right: 30%;
  bottom: 10px;
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
  text-align: center;
  /* 文本居中对齐*/
  font-size: 13px;
  /* 设置字体大小*/
  width: 40px;
  height: 40px;
  cursor: pointer;
  background-image: url("../assets/white_mode.svg");
  /* 替换为默认 SVG 图片路径 */
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
  background-image: url("../assets/dark_mode.svg");
  /* 替换为点击后 SVG 图片路径 */
}

.fileContainer {
  position: relative;
  height: 540px;
}

.fileView {
  position: fixed;
  top: 2%;
  left: 15%;
  width: 70%;
  height: 95%;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 5px;
}

#fileViewButtonTwo {
  margin-top: 10px;
  margin-left: 10px;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  background-image: url("../assets/green_icon.svg");
  /* 替换为点击后 SVG 图片路径 */
  background-size: auto 70%;
  background-position: center;
  background-repeat: no-repeat;
  background-color: transparent;
}

#fileViewButtonTwo:hover {
  background-color: green;
}

#fileViewButton {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  background-image: url("../assets/red_x.svg");
  /* 替换为点击后 SVG 图片路径 */
  background-size: auto 70%;
  background-position: center;
  background-repeat: no-repeat;
  background-color: transparent;
}

#fileViewButton:hover {
  background-color: red;
}

#buttonDiv {
  position: relative;
  height: 100%;
}

#fileViewButton {
  position: absolute;
  top: 0;
}


.pdf-page {
  position: relative;
  margin-bottom: 20px;
}

.pdf-viewer {
  border: 1px solid black;
  z-index: 1;
}

.textLayer {
  position: absolute;
  pointer-events: visiblePainted;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 2999;
  color: red
}

.pdf_down {
  position: absolute;
  display: flex;
  z-index: 20;
  right: 0;
  bottom: 0;
  cursor: pointer;
  background: transparent;
  border: none;
}

.pdf_set_left,
.pdf_set_middle {
  width: 30px;
  height: 30px;
  color: #408fff;
  font-size: 15px;
  text-align: center;
  margin-right: 5px;
  padding-top: 2px;
  cursor: pointer;
  background: transparent;
  border: none;
}

.pdf-pre {
  position: fixed;
  z-index: 20;
  right: 160px;
  bottom: 9%;
  cursor: pointer;
}

.pdf-next {
  position: fixed;
  z-index: 20;
  right: 100px;
  bottom: 9%;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  /* 保持长宽比 */
}

.txtPage {
  width: 100%;
  height: 100%;
  background: white;
  overflow: auto;
  white-space: pre;
  /* 保留格式 */
  text-align: initial;
}

.txtPage::-webkit-scrollbar {
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

.docx-preview {
  margin-top: 20px;
  padding: 15px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  max-height: 500px;
  overflow-y: auto;
  text-align: initial;
}

.docx-preview::-webkit-scrollbar {
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

.highlight {
  background-color: yellow;
}

#knowledgeDBdiv {
  position: fixed;
  top: 2%;
  left: 15%;
  width: 70%;
  height: 95%;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  /*align-items: center;
  justify-content: center;*/
  border-radius: 5px;
}

#knowledgeDBPreviewDiv {
  position: fixed;
  top: 2%;
  left: 7%;
  width: 86%;
  height: 95%;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  /*align-items: center;
  justify-content: center;*/
  border-radius: 10px;
  padding: 0.5%;
}
</style>