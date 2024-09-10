<!--
 * @Author: Jacob-biu 2777245228@qq.com
 * @Date: 2024-09-09 13:29:56
 * @LastEditors: Jacob-biu 2777245228@qq.com
 * @LastEditTime: 2024-09-09 17:51:52
 * @FilePath: \llm_demo\src\components\sidebarOfDB.vue
 * @Description: 
 * Copyright (c) 2024 by Jacob John, All Rights Reserved. 
-->
<template>
  <div class="scroll-container">
    <span class="scroll-text">当前知识库：{{this.selectedDB.label}}</span>
  </div>
  <div style="height:1.5%"></div>
  <div id="knowledgeDBHistory">
    <div v-for="(item, index) in buttonList" :key="index" class="DB_List">
      <button @click="handleClick(item)" class="DB_ListButton" :class="{ active: activeButton === item.value }">
        {{ item.label }}
      </button>
    </div>
  </div>
</template>

<script>
import { EventBusOne } from '../event-bus.js';
import axios from 'axios';

export default{
  data(){
    return{
      buttonList: [],
      options: [ // 下拉框的选项，模拟接口返回的值，包含显示的标签和实际的值
        { label: '不使用知识库', value: 'null' , description: ''},
      ],
      selectedDB: { label: '不使用知识库', value: 'null' , description: ''},
      activeButton: 'null',
      textFromServer: '', //后端返回的rag参考文字
      filePath: [],
    }
  },

  methods: {
    initButtonList(){
      this.buttonList = this.options
        .map(option => ({
          label: option.label,
          value: option.value,
          description: option.description,
        }));
    },

    // 点击事件的处理函数
    async handleClick(item) {
      this.selectedDB = item;
      this.activeButton = item.value;
      this.$emit('selectedDB-sent-from-side', this.selectedDB);
      await this.getFilesPath();
      console.log(this.filePath);
      this.$emit('filePaths-sent-from-side', this.filePath);
      console.log('selectedDB-sent-from-side:', this.selectedDB);
    },

    updateOptions(options) {
      this.options = options;
      console.log('options-received:', options);
      this.initButtonList(); // 更新 options 后重新初始化 buttonList
    },

    async getFilesPath() {
      try {
        const getFilesResponse = await axios.post('http://localhost:5000/get_files', 
        { 
          dataset: this.selectedDB.value,
        });
        this.filePath = getFilesResponse.data.files;
      } catch (error) {
        console.error('Error:', error);
        this.response = { error: '请求失败，请检查控制台获取更多信息。' };
      }
    },
  },

  mounted() {
    this.updateOptions(EventBusOne.getOptions()); // 主动获取当前状态
    EventBusOne.on('options-sent', this.updateOptions);
    this.initButtonList(); // 在组件挂载后初始化 buttonList
  },
}
</script>

<style>
.scroll-container {
  width: 100%; /* 设置容器的宽度 */
  overflow: hidden; /* 隐藏超出容器的内容 */
  white-space: nowrap; /* 防止文本换行 */
  position: relative;
}

.scroll-text {
  display: inline-block;
  padding-left: 100%; /* 确保文本从容器外部开始 */
  animation: scroll 5s linear infinite; /* 设置动画 */
}

@keyframes scroll {
  0% {
    transform: translateX(0); /* 从容器外部开始 */
  }
  100% {
    transform: translateX(-100%); /* 滚动到容器的另一端 */
  }
}

#knowledgeDBHistory{
  width: 90%;
  height: 92%;
  background-color:transparent;
  border-radius:10px;
  margin-top: 2%;
  margin-bottom: 1%;
  margin-left: 5%;
  margin-right: 5%;
  font-size: 15px;
  font-weight: bold;
  color: #000000;
  border: 0px;
  outline: none;
  transition: all 0.3s;
  padding:2%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 阴影效果增加立体感 */
  overflow-y: auto;
}
::-webkit-scrollbar {
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
.DB_ListButton{
  width:90%;
  aspect-ratio: 5 / 2; /* 设置宽高比为1:1，使宽度等于高度 */
  background-color:white;
  border-radius: 10px;
  border: none;
}
.DB_ListButton:hover {
  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
}
.DB_ListButton.active{
  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
}
.DB_List{
  width:95%;
  margin-left: 2.5%;
  margin-right: 2.5%;
}
</style>