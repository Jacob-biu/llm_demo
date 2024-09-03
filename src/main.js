// /$$
//  $ @Author: Jacob-biu 2777245228@qq.com
//  $ @Date: 2024-08-07 21:52:26
//  $ @LastEditors: Jacob-biu 2777245228@qq.com
//  $ @LastEditTime: 2024-08-08 11:27:13
//  $ @FilePath: \demo\llm_demo\src\main.js
//  $ @Description: 
//  $ @Copyright (c) 2024 by Jacob John, All Rights Reserved. 
//  $/
import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App);
app.use(ElementPlus);

// 配置全局错误处理函数
app.config.errorHandler = (err, vm, info) => {
  // err: 错误对象
  // vm: 发生错误的 Vue 实例
  // info: Vue 特定的错误类型信息，如生命周期钩子中的错误

  // 在控制台输出错误信息（开发环境）
  console.error('Error:', err);
  console.error('Error Info:', info);

  // 你还可以将错误发送到日志服务
  // logErrorToService(err, vm, info);
};

// 挂载 Vue 应用
app.mount('#app');
