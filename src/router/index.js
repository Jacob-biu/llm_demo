// /$$
//  $ @Author: Jacob-biu 2777245228@qq.com
//  $ @Date: 2024-08-08 11:25:16
//  $ @LastEditors: Jacob-biu 2777245228@qq.com
//  $ @LastEditTime: 2024-08-08 11:25:31
//  $ @FilePath: \demo\llm_demo\src\router\index.js
//  $ @Description: 
//  $ @Copyright (c) 2024 by Jacob John, All Rights Reserved. 
//  $/
import { createRouter, createWebHistory } from "vue-router";  //导入路由
const routes = [
    {
        path:'/home', // 要路由到的url路径
        name:'home',
        component:()=>import('../components/ChatDialog.vue'), //导入路由页面的路径
    }
];

const router = createRouter({    // 定义一个路由器
    history:createWebHistory(),
    routes
});

export default router;
