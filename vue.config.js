// /$$
//  $ @Author: Jacob-biu 2777245228@qq.com
//  $ @Date: 2024-08-07 21:52:26
//  $ @LastEditors: Jacob-biu 2777245228@qq.com
//  $ @LastEditTime: 2024-08-08 09:43:37
//  $ @FilePath: \demo\llm_demo\vue.config.js
//  $ @Description: 
//  $ @Copyright (c) 2024 by Jacob John, All Rights Reserved. 
//  $/
const {
  defineConfig
} = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false, //关闭语法检查
  assetsDir: "static",
  devServer: {
    port: "8080",
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        pathRewrite: {
          '^/api': '/api'
        },
        changeOrigin: true,
        ws: true
      },
    },
  }
})
