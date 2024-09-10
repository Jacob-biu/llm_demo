<!--
 * @Author: Jacob-biu 2777245228@qq.com
 * @Date: 2024-09-02 15:11:44
 * @LastEditors: Jacob-biu 2777245228@qq.com
 * @LastEditTime: 2024-09-09 21:30:36
 * @FilePath: \llm_demo\src\components\knowledgeDB.vue
 * @Description: 
 * Copyright (c) 2024 by Jacob John, All Rights Reserved. 
-->
<template>
  <div id="knowledgeDBElement" style="width:100%; height:100%;">
    <el-dialog title="新建知识库" v-model="dialogVisible" @close="handleCancel" width="480px">
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <!-- 其他表单项 -->
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="4"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </span>
    </el-dialog>
    <!-- <el-card id="topBar">
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
    </el-card> -->
    <el-card id="topBar">
      <span>当前知识库：{{ options.find(option => option.value === selectedOption) ? options.find(option => option.value === selectedOption).label : '未找到匹配的选项' }}</span>
    </el-card>
    <div id="majorBar">
      <div id="leftBar">
        <button id="createKnowledgeDB" @click="this.dialogVisible = true; this.handleCancel();">➕ 新建知识库</button>
        <div id="knowledgeDBHistory">
          <div v-for="(item, index) in buttonList" :key="index" class="DB_List">
            <button @click="handleClick(item)" class="DB_ListButton" :class="{ active: activeButton === item.value }">
              {{ item.label }}
            </button>
          </div>
        </div>
      </div>
      <div id="rightBox">
        <!-- 右侧表单内容 -->
        <div  v-show="isRightBox" style="position:relative; width: 99%; height:98%; margin:0.5%; border-radius:10px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); ">
          <div style="position: absolute; top: 0; left: 0; z-index: 10; height: 5%;">
            <button class="custom-btn btn-8" @click="changeCardStateOne">
              <span>知识库</span>
            </button>
            <button class="custom-btn btn-8" @click="changeCardStateTwo">
              <span>配置</span>
            </button>
          </div>
          <el-card class="box-card" style="height:100%; width:100%;" v-show="isCardOne">
            <div style="border-top: 1px solid #ccc; margin-top:1.5%"></div>
            <div slot="header" class="clearfix" style="text-align:left; margin-bottom: 5%; display:flex;flex-direction: column; /* 设置主轴为垂直方向 */">
              <h3 style="margin-bottom:1%; margin-top: 1%;">知识库 {{dataset.label}}</h3>
              <el-tooltip class="item" effect="dark" content="解析成功后才能问答哦。" placement="top">
                <span style="font-size:15px">😊解析成功后才能问答哦。</span>
              </el-tooltip>
            </div>
  
            <el-row :gutter="20" style="margin-bottom: 8%;">
              <el-col :span="12" style="position: absolute; left:0;">
                <!-- 使用 el-dropdown 实现下拉菜单 -->
                <el-dropdown :disabled="isDisabled">
                  <el-button type="primary"  style="z-index:10;" :disabled="isDisabled">
                    批量<i class="el-icon-arrow-down el-icon--right"></i>
                  </el-button>
                  <!-- 下拉菜单 -->
                  <template #dropdown>
                    <el-dropdown-menu slot="dropdown" :disabled="isDisabled">
                      <el-dropdown-item @click.native="handleEnable" style="display: flex; align-items: center;" :disabled="isDisabled">
                        <i class="el-icon-check" style="color: green; margin-right: 8px;">启用</i>
                      </el-dropdown-item>
                      <el-dropdown-item @click.native="handleCancelEnable" style="display: flex; align-items: center;" :disabled="isDisabled">
                        <i class="el-icon-close" style="color: red; margin-right: 8px;">取消</i>
                      </el-dropdown-item>
                      <el-dropdown-item @click.native="handleDeleteDataset" style="display: flex; align-items: center;" :disabled="isDisabled">
                        <i class="el-icon-delete" style="margin-right: 8px;">删除</i>
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </el-col>
              <el-col :span="12" style="text-align: right;position: absolute;right:0;">
                <el-input v-model="searchQuery" placeholder="搜索文件" suffix-icon="el-icon-search" style="width: 70%;margin-right:0.5%;"></el-input>
                <el-button type="primary" @click="triggerFileSelect">新增文件</el-button>
                  <!-- 隐藏的文件选择框 -->
                <input
                  type="file"
                  ref="fileInput"
                  style="display: none"
                  @change="handleFileChange"
                  accept=".jpg,.png,.txt,.pdf,.docx"
                />
              </el-col>
            </el-row>
            <div style="border-top: 1px solid #ccc; margin: 10px 0;"></div>
  
            <!-- 绑定 v-loading，当 isLoading 为 true 时显示加载状态 -->
            <el-table :data="filteredDatasets" v-loading="isLoading" style="width: 100%;" ref="table"  @selection-change="handleSelectionChange">
              <el-table-column type="selection" width="55"></el-table-column>
              <el-table-column prop="name" label="名称" width="180"></el-table-column>
              <!-- <el-table-column prop="chunks" label="分块数" width="100"></el-table-column> -->
              <el-table-column prop="uploadDate" label="上传日期" width="180"></el-table-column>
              <!-- <el-table-column prop="parseMethod" label="解析方法" width="150"></el-table-column> -->
              <el-table-column prop="enabled" label="启用" width="100">
                <template v-slot="scope">
                  <el-switch v-model="scope.row.enabled"></el-switch>
                </template>
              </el-table-column>
              <el-table-column prop="parseStatus" label="解析状态" width="180"></el-table-column>
              <el-table-column label="动作" width="240"  style="display: flex;">
                <!-- 自定义动作列 -->
                <template v-slot="scope">
                  <el-button @click="deleteAction(scope.row)" style="width:15px; border:none;">删除</el-button>
                  <!--<el-button @click="changeNameAction(scope.row)" style="border:none; ">更改文件名</el-button>-->
                  <el-button @click="downloadAction(scope.row)" style="width: 15px; size:10; border:none;">下载</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>

          <el-card class="box-card" style="height:100%; width:100%;" v-show="isCardTwo">
            <div style="border-top: 1px solid #ccc; margin-top:1.5%"></div>
            <div slot="header" class="clearfix" style="text-align:left; margin-top: 2.5%; margin-bottom: 2.5%; display:flex;flex-direction: column; /* 设置主轴为垂直方向 */">
              <h3 style="margin-bottom:1%;">配置</h3>
              <el-tooltip class="item" effect="dark" content="在这里更新您的知识库详细信息。" placement="top">
                <span style="font-size:15px">😊在这里更新您的知识库详细信息</span>
              </el-tooltip>
            </div>
            <div style="border-top: 1px solid #ccc; margin-top:1.5%; margin-bottom: 2.5%;"></div>
            
            <el-card class="box-card" style="height:50%; width:50%;">
              <el-form :model="form" :rules="rules" ref="formRef">
                <el-form-item label="名称" prop="name">
                  <el-input v-model="formTwo.name"></el-input>
                </el-form-item>
                <!-- 其他表单项 -->
                <el-form-item label="描述" prop="description">
                  <el-input v-model="formTwo.description" type="textarea" :rows="4"></el-input>
                </el-form-item>
              </el-form>
              <span slot="footer" class="dialog-footer">
                <el-button type="primary" @click="submitChange">提交修改</el-button>
              </span>
            </el-card>
            <el-card style="margin-top: 1%;">
              <el-button type="danger" @click="deleteKnowledgeDB">删除数据集</el-button>
            </el-card>
          </el-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ElButton, ElDialog , ElForm , ElFormItem , ElInput , ElSelect, ElOption , ElUpload , ElTable , ElTableColumn , ElMessage , ElDropdown, ElDropdownMenu, ElDropdownItem } from 'element-plus';
import { ref } from 'vue';
import axios from 'axios';
import moment from 'moment'; // 用于格式化日期
import { Check, Close, Delete } from '@element-plus/icons-vue'; // 引入图标
import { EventBusOne } from '../event-bus.js';


export default {
  data() {
    const validateName = (rule, value, callback) => {
      const regex = /^(?!_)[a-z0-9_\u4e00-\u9fa5]+$/;
      if (!value) {
        callback(new Error('名称不能为空'));
      } else if (!regex.test(value)) {
        callback(new Error('名称只能包含小写字母、数字、中文字符和下划线，且不能以下划线开头'));
      } else {
        callback();
      }
    };

    return {
      isRightBox: false,
      isCardOne: true,
      isCardTwo: false,
      selectedOption: 'null', // 用于接口调用的实际值
      options: [ // 下拉框的选项，模拟接口返回的值，包含显示的标签和实际的值
        { label: '不使用知识库', value: 'null' , description: ''},
        // { label: 'DB', value: 'DB' , description: 'DB'},
        // { label: 'DB2', value: 'DB2' , description: 'DB2'},
        // { label: 'DB3', value: 'DB3' , description: 'DB3'},
      ],
      dialogVisible: false,
      form: {
        name: '',
        description: '',
        // 其他字段
      },
      formTwo: {
        name: '',
        description: '',
        // 其他字段
      },
      // 按钮数据数组
      buttonList: [],
      rules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { validator: validateName, trigger: 'blur' }
        ],
        description: [
          { required: false }
        ]
      },
      searchQuery: '', // 搜索框内容
      selectedFiles: [], // 选择的文件，用于批量操作
      dataset: { label: '不使用知识库', value: 'null' , description: ''} ,  //当前数据集信息（和button绑定）
      datasetsFile: [],  // 数据集文件列表
      isLoading: false, // 加载状态
      selectedRows: [],
      activeButton: 'null',
    };
  },

  components: {
    ElButton,
    ElDialog,
    ElForm,
    ElFormItem,
    ElInput,
    ElSelect,
    ElOption,
    ElUpload,
    ElTable,
    ElTableColumn,
    ElDropdown,
    ElDropdownMenu,
    ElDropdownItem,
    Check, // 启用图标
    Close, // 取消图标
    Delete // 删除图标
  },

  created(){
  },

  methods: {
    //初始化options
    fetchKnowledgeBases() {
      this.options = [];
      axios.post('http://localhost:8999/es/indeces', {
          headers: {
            'Content-Type': 'application/json'
          }
        })
        .then(response => {
          const data = response.data;
          this.options.push({ label: '不使用知识库', value: 'null' , description: ''});

          for (const [key, value] of Object.entries(data)) {
            this.options.push({ label: key, value: key, description: value });
            this.buttonList.push({ label: key, value: key, description: value });
          }
        })
        .catch(error => {
          console.error('Error fetching knowledge bases:', error);
        });
        // this.initButtonList();
        this.sendOptions();
    },

    // 你可以在这里添加一个方法来处理选项选择后的操作，例如调用接口
    handleChange() {
      this.$emit('selectedOption', this.selectedOption);
      // 使用 this.selectedValue 作为调用接口的参数
      // console.log("Selected value for API call:", this.selectedOption);
      // 这里添加调用接口的代码
    },

    handleSubmit() {
      this.$refs.formRef.validate((valid) => {
        if (valid) {
          // 验证通过，执行提交逻辑
          console.log('Form submitted:', this.form);
          
          var option = { label: this.form.name, value: this.form.name , description: this.form.description };
          this.options.push(option);
          this.initButtonList();
          // 提交表单逻辑
          this.dialogVisible = false;
          document.getElementById('knowledgeDBHistory').scrollTop = document.getElementById('knowledgeDBHistory').scrollHeight;
          this.handleClick(option);

          //向数据库提交新建知识库的信息
          this.createIndex(this.form.name);
        } else {
          console.log('Form validation failed');
          return false;
        }
      });
    },
    //向数据库发出新增索引要求
    async createIndex(name) {
      try {
        const response = await axios.post('http://localhost:8999/es/create_index', {
          datasetName: name
        }, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        console.log(response.data); // { code: 1 }
        ElMessage.success('知识库创建成功！');
      } catch (error) {
        console.error('Error creating index:', error);
      }
    },

    handleCancel() {
      // 取消表单时的逻辑
      // 可以选择重置表单
      this.form = {
        name: '',
        description: '',
        value: '',
        // 其他字段
      };
    },
    initButtonList(){
      this.buttonList = this.options
        .filter(option => option.value !== 'null')
        .map(option => ({
          label: option.label,
          value: option.value,
          description: option.description,
        }));
      this.sendOptions();
    },
    // 点击事件的处理函数
    handleClick(item) {
      this.activeButton = item.value;
      this.isRightBox = true;
      this.dataset = item;
      this.formTwo.name = item.label;
      this.formTwo.description = item.description;
      this.formTwo.value = item.value;
      console.log(`Clicked on ${item.label}`);
      this.datasetsFile=[];
      this.fetchFiles();
      // 在这里执行与button相关的通用操作
    },

    changeCardStateOne() {
      this.isCardOne = true;
      this.isCardTwo = false;
    },
    changeCardStateTwo() {
      this.isCardOne = false;
      this.isCardTwo = true;
    },

    submitChange(){
      console.log('Form submitted:', this.formTwo);
      // 提交表单逻辑

      // 更新 options 数组中的项
      this.options = this.options.map(option => {
        if (option.value === this.formTwo.value) {
          // 返回更新后的 option
          return {
            ...option,
            label: this.formTwo.name,
            description: this.formTwo.description
          };
        }
        // 返回未修改的 option
        return option;
      });
      this.initButtonList();
    },

    deleteKnowledgeDB(){
      this.isRightBox = false;
      //删除options中label为this.dataset.label的项
      this.options = this.options.filter(option => option.label !== this.dataset.label);
      this.initButtonList();
      this.deleteDataset();
      this.dataset = null;
    },



    
    //以下实现文件上传逻辑
    // 触发文件选择框
    triggerFileSelect() {
      this.$refs.fileInput.click();
    },
    // 处理文件选择
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        // 校验文件类型
        const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf', 'text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        if (!allowedTypes.includes(file.type)) {
          ElMessage.error( '不支持的文件类型，请上传 JPG、PNG、PDF、TXT 或 DOCX 格式的文件');
          // 清除文件选择框中的文件
          this.$refs.fileInput.value = '';
          return;
        }
        this.uploadFile(file);
      }
    },
    // 上传文件
    async uploadFile(file) {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("datasetName", this.dataset.label);

      try {
        const response = await axios.post("http://localhost:5000/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        console.log("文件上传成功", response);
        console.log(response.data.file_path); // 文件路径
        this.uploadFileToDataBase(this.dataset.label,response.data.file_path);
        ElMessage.success( '文件上传成功！');
        this.fetchFiles();
      } catch (error) {
        console.error("文件上传失败", error);
        ElMessage.error( '文件上传失败！');
      }
    },
    //向数据库发出新增索引要求
    async uploadFileToDataBase(name,path) {
      try {
        const response = await axios.post('http://localhost:8999/es/uploadfile', {
          datasetName: name,
          file_abs_paths: [path,]
        }, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        console.log(response.data); // { code: 1 }
      } catch (error) {
        console.error('Error upload file:', error);
      }
    },



    //以下实现文件展示逻辑
    // 请求后端 API 获取文件列表
    async fetchFiles() {
      this.isLoading = true; // 开始加载状态

      try {
        const response = await axios.get('http://localhost:5000/files',{
          params: {
            datasetName: this.dataset.label,
          },
        });
        // 处理文件数据，例如格式化日期
        this.datasetsFile = response.data.map(file => ({
          ...file,
          name: file.name,
          uploadDate: moment(file.uploadDate * 1000).format('YYYY-MM-DD HH:mm:ss'),
          enabled: file.enabled,
          parseStatus: file.parseStatus,
        }));
      } catch (error) {
        console.error('获取文件列表失败:', error);
        // ElMessage.error( 'PDF上传成功！');
      }
      finally{
        ElMessage.success( '文件列表刷新成功');
        this.isLoading = false; // 加载完毕后关闭加载状态
      }
    },



    // 自定义的动作方法，例如处理文件
    // 删除文件
    async deleteAction(row) {
      try {
        const response = await axios.delete(`http://localhost:5000/delete/${this.dataset.label}/${row.name}`);
        console.log(response.data.message);
        console.log(response.data.file_path);

        this.deleteFileFromDataBase(this.dataset.label,response.data.file_path);
        ElMessage.success( '删除文件成功');
        this.fetchFiles(); // 刷新文件列表
      } catch (error) {
        console.error('删除文件失败:', error);
        ElMessage.error( '删除文件失败');
      }
    },
    //向数据库发出新增索引要求
    async deleteFileFromDataBase(name,path) {
      try {
        const response = await axios.post('http://localhost:8999/es/deletefile', {
          datasetName: name,
          file_abs_paths: [path,]
        }, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        console.log(response.data); // { code: 1 }
      } catch (error) {
        console.error('Error upload file:', error);
      }
    },



    // 更改文件名
    async changeNameAction(row) {
      const newFilename = prompt('请输入新的文件名', row.name);
      if (newFilename && newFilename !== row.name) {
        try {
          const response = await axios.post('http://localhost:5000/rename', {
            datasetName: this.dataset.label,
            oldFilename: row.name,
            newFilename: newFilename
          });
          ElMessage.success('文件名更改成功');
          console.log(response.data.message);
          this.fetchFiles(); // 刷新文件列表
        } catch (error) {
          console.error('更改文件名失败:', error);
          ElMessage.error( '文件名更改失败');
        }
      }
    },
    // 下载文件
    downloadAction(row) {
      window.open(`http://localhost:5000/download/${this.dataset.label}/${row.name}`);
    },


    // 删除数据集
    async deleteDataset() {
      try {
        this.deleteIndex(this.dataset.label);
        const response = await axios.delete(`http://localhost:5000/delete_dataset/${this.dataset.label}`);
        console.log(response.data.message);
        this.datasetsFile = []; // 清空当前文件列表
        ElMessage.success( '文件名更改成功');
      } catch (error) {
        console.error('删除数据集失败:', error);
      }
    },
    //向数据库发出新增索引要求
    async deleteIndex(name) {
      try {
        const response = await axios.post('http://localhost:8999/es/delete_index', {
          datasetName: name
        }, {
          headers: {
            'Content-Type': 'application/json'
          }
        });
        console.log(response.data); // { code: 1 }
        ElMessage.success( '知识库删除成功！');
      } catch (error) {
        console.error('Error deleting index:', error);
      }
    },


    
    handleSelectionChange(selected) {
      this.selectedRows = selected;
    },
    handleEnable() {
      console.log("启用操作");
      this.selectedRows.forEach(row => {
        row.enabled = true;
      });
    },
    handleCancelEnable() {
      console.log("取消操作");
      this.selectedRows.forEach(row => {
        row.enabled = false;
      });
    },
    handleDeleteDataset() {
      console.log("删除操作");
      this.selectedRows.forEach(row => {
        this.deleteAction(row);
      });
    },

    sendOptions() {
      EventBusOne.setOptions(this.options);
      console.log('Options sent:', this.options);
    },
  },

  mounted() {
    this.fetchKnowledgeBases();
  },

  computed: {
    // 根据搜索框输入内容过滤表格数据
    filteredDatasets() {
      // 如果没有输入内容，直接返回所有数据
      if (!this.searchQuery) {
        return this.datasetsFile;
      }
      
      // 根据 name 字段进行过滤，判断是否包含搜索框输入的内容
      return this.datasetsFile.filter(item => {
        return item.name.toLowerCase().includes(this.searchQuery.toLowerCase());
      });
    },
    isDisabled() {
      return this.datasetsFile.length === 0;
    }
  },
  // created() {
  //   // 组件加载时获取文件列表
  //   this.fetchFiles();
  // },
};
</script>

<style>
#topBar{
  width:99.5%;
  height:10%;
  border-radius:10px;
  margin-top: 1%;
  margin-bottom: 0.5%;
  padding: 0;
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
.DB_ListButton.active{
  box-shadow: 0 12px 16px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
}
.DB_List{
  width:95%;
  margin-left: 2.5%;
  margin-right: 2.5%;
  margin-top: 10px;
}

.custom-btn {
  width: 55px;
  height: 20px;
  color: #fff;
  border-radius: 5px;
  padding: 10px 25px;
  font-family: Lato,sans-serif;
  font-weight: 500;
  margin: 0 3px;
  background: transparent;
  cursor: pointer;
  transition: all .3s ease;
  position: relative;
  display: inline-block;
  box-shadow: inset 2px 2px 2px 0 hsla(0,0%,100%,.5),7px 7px 20px 0 rgba(0,0,0,.1),4px 4px 5px 0 rgba(0,0,0,.1);
  outline: none;
  margin-bottom: 50px;
}

.custom-btn.btn-8 {
  background-color: #f0ecfc;
  background-image: linear-gradient(315deg,#f0ecfc,#c797eb 74%);
  line-height: 20px;
  padding: 0;
  border: none
}

.custom-btn.btn-8 span {
  position: relative;
  display: block;
  width: 100%;
  height: 100%
}

.custom-btn.btn-8:after,.custom-btn.btn-8:before {
  position: absolute;
  content: "";
  right: 0;
  bottom: 0;
  background: #c797eb;
  transition: all .3s ease
}

.custom-btn.btn-8:before {
  height: 0%;
  width: 2px
}

.custom-btn.btn-8:after {
  width: 0;
  height: 2px
}

.custom-btn.btn-8:hover:before {
  height: 100%
}

.custom-btn.btn-8:hover:after {
  width: 100%
}

.custom-btn.btn-8:hover {
  background: transparent
}

.custom-btn.btn-8 span:hover {
  color: #c797eb
}

.custom-btn.btn-8 span:after,.custom-btn.btn-8 span:before {
  position: absolute;
  content: "";
  left: 0;
  top: 0;
  background: #c797eb;
  transition: all .3s ease
}

.custom-btn.btn-8 span:before {
  width: 2px;
  height: 0%
}

.custom-btn.btn-8 span:after {
  height: 2px;
  width: 0
}

.custom-btn.btn-8 span:hover:before {
  height: 100%
}

.custom-btn.btn-8 span:hover:after {
  width: 100%
}

</style>
