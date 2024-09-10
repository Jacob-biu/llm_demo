<!--
 * @Author: Jacob-biu 2777245228@qq.com
 * @Date: 2024-09-06 09:31:35
 * @LastEditors: Jacob-biu 2777245228@qq.com
 * @LastEditTime: 2024-09-06 16:31:19
 * @FilePath: \llm-demo-0.2.1\llm_demo\src\components\knowledgeDBPreview.vue
 * @Description: 
 * Copyright (c) 2024 by Jacob John, All Rights Reserved. 
-->
<template>
  <!-- <el-card class="app-container"> -->
    <div class="sidebar">
      <div style="border-radius: 10px; background-color: white; width: 100%; text-align: left; ">
        <span style="margin-left: 4%;">全部文献  {{ totalFileCount }}</span>
      </div>
      <el-tree
        ref="tree"
        :data="fileTree"
        :props="defaultProps"
        node-key="id"
        :default-expanded-keys="defaultExpandedKeys"
        @node-click="handleNodeClick"
        @node-contextmenu="handleExpandToggle"
        :expand-on-click-node="true"
        style="border-radius: 10px;"
      >
        <template #default="{ node, data }">
          <div class="tree-node" @click="handleExpandToggle(node)">
            <el-tooltip class="item" effect="dark" :content=data.name placement="top">
              <span
                class="custom-node"
              >
                {{ data.name }}
                <span v-if="data.children" class="file-count">({{ data.fileCount }})</span>
              </span>
            </el-tooltip>
          </div>
        </template>
      </el-tree>
    </div>
    <div class="file-preview">
      <div v-show="showSen">
        请选择文件打开
      </div>
      <VueOfficeDocx v-if="isDocx" :src="fileUrl" v-show="isDocxShow" class="docx-preview" />
      <iframe
        v-else-if="!isDocx && selectedFile"
        :src="fileUrl"
        frameborder="0"
        width="100%"
        height="100%"
        v-show="isShow"
      ></iframe>
    </div>
  <!-- </el-card> -->
</template>

<script>
import axios from 'axios';
import { ElCard , ElTree , ElTooltip } from 'element-plus';
import 'element-plus/es/components/tooltip/style/css';  // 引入样式
import VueOfficeDocx from '@vue-office/docx';

export default {
  name: 'knowledgeDBPreview',
  data() {
    return {
      fileTree: [],
      selectedFile: null,
      defaultProps: {
        children: 'children',
        label: 'name',
      },
      totalFileCount: 0, // 用于保存所有文件的总数
      refreshInterval: null, // 定时器引用
      isShow: false,
      showSen: true,
      isDocxShow: false,
      isDocx: false,
    };
  },

  components: {
    ElCard,
    ElTree,
    ElTooltip,
    VueOfficeDocx,
  },

  methods: {
    // 计算文件树中所有文件的总数
    calculateTotalFileCount(treeData) {
      let count = 0;
      const traverse = (nodes) => {
        nodes.forEach((node) => {
          if (node.children && node.children.length > 0) {
            traverse(node.children);
          } else if (!node.children) {
            count += 1;
          }
        });
      };
      traverse(treeData);
      return count;
    },

    // 递归计算每个文件夹下所有子文件的数量
    calculateFileCounts(nodes) {
      nodes.forEach((node) => {
        node.fileCount = 0;
        if (node.children && node.children.length > 0) {
          node.fileCount = this.calculateTotalFileCount(node.children); // 递归计算子文件数量
          this.calculateFileCounts(node.children); // 继续遍历子节点
        }
      });
    },

    fetchFileTree() {
      axios
        .get('http://localhost:5000/allFiles')
        .then((response) => {
          this.fileTree = response.data;
          this.calculateFileCounts(this.fileTree); // 计算每个文件夹的子文件数量
          this.totalFileCount = this.calculateTotalFileCount(this.fileTree); // 计算所有文件的总数
        })
        .catch((error) => {
          console.error('获取文件树失败:', error);
        });
    },
    handleNodeClick(node) {
      if (!node.children) {
        this.selectedFile = node.filePath;
        console.log('selectedFile:' + this.selectedFile );
        this.previewFile(node.filePath);
        this.showSen = false;
        if(this.isDocx){
          this.isDocxShow = true;
        }else{
          this.isShow = true;
        }
      }
    },
    handleExpandToggle(node) {
      if (node.childNodes.length > 0) {
        if (node.expanded) {
          node.collapse();
        } else {
          node.expand();
        }
      }
    },

    previewFile(filePath) {
      const fileExtension = filePath.split('.').pop().toLowerCase();
      this.isDocx = false;

      if (fileExtension === 'docx') {
        this.isDocx = true;
      }
    },
  },

  created() {
    // 初始化时获取文件树
    this.fetchFileTree();

    // // 每隔 10 秒刷新文件树
    // this.refreshInterval = setInterval(() => {
    //   this.fetchFileTree();
    // }, 5000); // 每2秒刷新一次
  },

  beforeDestroy() {
    // 清除定时器
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  },

  computed: {
    fileUrl() {
      return this.selectedFile
        ? `http://localhost:5000/allFiles/${this.selectedFile}`
        : '';
    },
  },

  mounted(){
    this.fetchFileTree();
  }
};
</script>

<style>
.app-container {
  width: 100%;
  height: 100%;
  display: flex;
}

.sidebar {
  width: 20%;
  height: 100%;
  border-radius: 10px;
  overflow-y: auto;
}

.file-preview {
  width: 80%;
  height: 100%;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 控制文件名的显示，防止超长内容溢出 */
.custom-node {
  display: inline-block;
  max-width: 180px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  cursor: pointer;
}

/* 使用 Flexbox 布局让文件名和文件数量分布在左右两侧 */
.tree-node {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-right: 10px;
}

.file-count {
  color: #999;
  margin-left: 5px;
  flex-shrink: 0;
  text-align: right; /* 确保数字靠右 */
}

/* 工具提示样式 */
.el-tooltip {
  max-width: 300px;
  word-wrap: break-word;
}

.docx-preview {
  width: 90%;
  height: 90%;
  overflow: auto;
  max-height: 200px; /* 你可以根据需要调整这个值 */
}
.vue-office-docx.docx-preview{
  margin: 0;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
}
</style>
