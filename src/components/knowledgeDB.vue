<!--
 * @Author: Jacob-biu 2777245228@qq.com
 * @Date: 2024-09-02 15:11:44
 * @LastEditors: Jacob-biu 2777245228@qq.com
 * @LastEditTime: 2024-09-02 22:33:34
 * @FilePath: \llm-demo-0.2.1\llm_demo\src\components\knowledgeDB.vue
 * @Description: 
 * Copyright (c) 2024 by Jacob John, All Rights Reserved. 
-->
<template>
  <div id="knowledgeDBElement" style="width:100%; height:100%;">
    <el-dialog title="新建知识库" v-model="dialogVisible" @close="handleCancel" width="300px">
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <!-- 其他表单项 -->
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </span>
    </el-dialog>
    <div id="topBar">
      <span>当前知识库：</span>
      <el-select v-model="selectedOption" placeholder="请选择知识库" @change="handleChange" style="width: 200px;">
        <el-option
          v-for="option in options"
          :key="option.value"
          :label="option.label"
          :value="option.value">
        </el-option>
      </el-select>
      <span>（默认不使用）</span>
    </div>
    <div id="majorBar">
      <div id="leftBar">
        <button id="createKnowledgeDB" @click="this.dialogVisible = true">➕ 新建知识库</button>
        <div id="knowledgeDBHistory">
          <div v-for="(item, index) in buttonList" :key="index" class="DB_List">
            <button @click="handleClick(item)" class="DB_ListButton">
              {{ item.text }}
            </button>
          </div>
        </div>
      </div>
      <div id="rightBox"></div>
    </div>
  </div>
</template>

<script>
import { ElButton, ElDialog } from 'element-plus';
import { ref } from 'vue';


export default {
  data() {
    return {
      selectedOption: null, // 用于接口调用的实际值
      options: [ // 下拉框的选项，模拟接口返回的值，包含显示的标签和实际的值
        { label: '不使用知识库', value: null },
        { label: 'DB', value: 'DB' },
        { label: 'DB2', value: 'DB2' },
      ],
      dialogVisible: false,
      form: {
        name: '',
        // 其他字段
      },
      // 按钮数据数组
      buttonList: [],
      rules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' }
        ]
      },
    };
  },

  components: {
    ElButton,
    ElDialog
  },

  methods: {
    // 你可以在这里添加一个方法来处理选项选择后的操作，例如调用接口
    handleChange() {
      this.$emit('knowledgeDBContent', this.selectedOption);
      // 使用 this.selectedValue 作为调用接口的参数
      console.log("Selected value for API call:", this.selectedOption);
      // 这里添加调用接口的代码
    },

    handleSubmit() {
      this.$refs.formRef.validate((valid) => {
        if (valid) {
          // 验证通过，执行提交逻辑
          console.log('Form submitted:', this.form);
          
          var listButton = document.createElement('BUTTON');
          listButton.id = this.form.name;
          listButton.className = 'DB_ListButton';
          var t=document.createTextNode(this.form.name);
          listButton.appendChild(t);
          var listDiv = document.createElement('div');
          listDiv.id = this.form.name;
          listDiv.className = 'DB_List';
          listDiv.appendChild(listButton);
          document.getElementById('knowledgeDBHistory').appendChild(listDiv);
          document.getElementById('knowledgeDBHistory').scrollTop = document.getElementById('knowledgeDBHistory').scrollHeight;
          var option = { label: this.form.name, value: this.form.name };
          this.options.push(option);
          // 提交表单逻辑
          this.dialogVisible = false;

        } else {
          console.log('Form validation failed');
          return false;
        }
      });
    },
    handleCancel() {
      // 取消表单时的逻辑
      // 可以选择重置表单
      this.form = {
        name: '',
        // 其他字段
      };
    },
    initButtonList(){
      this.buttonList = this.options
        .filter(option => option.value !== null)
        .map(option => ({
          text: option.label,
          value: option.value
        }));
    },
    // 点击事件的处理函数
    handleClick(item) {
      console.log(`Clicked on ${item.text}`);
      // 在这里执行与button相关的通用操作
    },
  },

  mounted() {
    this.initButtonList(); // 在组件挂载后初始化 buttonList
  }
};
</script>

<style>
#topBar{
  width:99.5%;
  height:10%;
  background-color: #f0f0f0;
  border-radius:10px;
  margin-top: 1%;
  margin-bottom: 0.5%;
}
#majorBar{
  width:100%;
  height:87%;
  background: transparent;
  border-radius:10px;
  margin-bottom: 1%;
  display: flex;
}
#leftBar{
  width:20%;
  height:99%;
  background-color: #f0f0f0;
  border-radius:10px;
  margin-bottom: 0.5%;
  margin-right: 0.5%;
}
#rightBox{
  width:79%;
  height:99%;
  background-color: #f0f0f0;
  border-radius:10px;
  margin-bottom: 0.5%;
}

#createKnowledgeDB{
  width: 90%;
  height: 10%;
  background-color:white;
  border-radius:10px;
  margin-top: 3%;
  margin-bottom: 1%;
  margin-left: 5%;
  margin-right: 5%;
  font-size: 15px;
  font-weight: bold;
  color: #000000;
  border: 0px;
  cursor: pointer;
  outline: none;
  transition: all 0.3s;
}
#createKnowledgeDB:hover {
  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
}
#knowledgeDBHistory{
  width: 90%;
  height: 87%;
  background-color:transparent;
  border-radius:10px;
  margin-top: 1%;
  margin-bottom: 1%;
  margin-left: 5%;
  margin-right: 5%;
  font-size: 15px;
  font-weight: bold;
  color: #000000;
  border: 0px;
  outline: none;
  transition: all 0.3s;
  padding:0.1%;
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
  width:80%;
  height: 40px;
  background-color:white;
  border-radius: 10px;
  border: none;
}
.DB_ListButton:hover {
  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
}
.DB_List{
  width:95%;
  margin-left: 2.5%;
  margin-right: 2.5%;
  margin-top: 10px;
}
</style>
