<!--
 * @Author: Jacob-biu 2777245228@qq.com
 * @Date: 2024-08-15 14:25:11
 * @LastEditors: Jacob-biu 2777245228@qq.com
 * @LastEditTime: 2024-08-15 22:30:51
 * @FilePath: \llm-demo-0.1.1\llm_demo\src\components\pdfViewer.vue
 * @Description: 
 * Copyright (c) 2024 by Jacob John, All Rights Reserved. 
-->
<template>
  <div class="pdf-preview-box">
    <!-- <div class="pdf_down">
            <div class="pdf_set_left" @click="scaleD()">➕</div>
            <div class="pdf_set_middle" @click="scaleX()">➖</div>
            <div class="pdf-pre" @click="prePage">上一页</div>
            <div class="pdf-next" @click="nextPage">下一页</div>
        </div> -->
    <canvas
      class="pdf-viewer"
      v-for="i in pdfParams.pdfPageTotal"
      :key="i"
      :id="'pdf-render' + i"
    ></canvas>
  </div>
</template>

<script setup>
import { onMounted, ref, reactive } from "vue";

const props = defineProps({
  pdfUrl: {
    type: String,
    default: "/testPdf.pdf",
    required: true,
  },
  containerWidth: {
    type: Number,
    default: 700,
    required: true,
  },
});

const pdfParams = reactive({
  currentPageNumber: 1,
  pdfScale: 1.0,
  pdfPageTotal: 0, // 总页数
});

// 不要定义为ref或reactive格式，就定义为普通的变量
let pdfDoc = null;

onMounted(async () => {
  await loadFile();
});

// 这里必须使用异步去引用pdf文件，直接去import会报错，也不知道为什么
const loadFile = async () => {
  let pdfjs = await import("pdfjs-dist/build/pdf");
  let pdfjsWorker = await import("pdfjs-dist/build/pdf.worker.entry");
  pdfjs.GlobalWorkerOptions.workerSrc = pdfjsWorker;
  // 此文件位于public/testPdf.pdf
  pdfjs.getDocument(props.pdfUrl).promise.then(async (doc) => {
    pdfDoc = doc;
    pdfParams.pdfPageTotal = doc.numPages;
    // // 仅加载第一页  注释  取消页码切换
    // await getPdfPage(pdfParams.currentPageNumber)
    // 加载pdf所有页
    for (let pageNum = 1; pageNum <= doc.numPages; pageNum++) {
      await getPdfPage(pageNum);
    }
  });
};

// 加载pdf的某一页
const getPdfPage = (number) => {
  return new Promise((resolve, reject) => {
    pdfDoc
      .getPage(number)
      .then((page) => {
        const canvas = document.getElementById(`pdf-render${number}`);
        const context = canvas.getContext("2d");
        const scale = 1; // 缩放比例
        const dpr = window.devicePixelRatio || 1;
        const bsr =
          context.webkitBackingStorePixelRatio ||
          context.mozBackingStorePixelRatio ||
          context.msBackingStorePixelRatio ||
          context.oBackingStorePixelRatio ||
          context.backingStorePixelRatio ||
          1;
        const ratio = dpr / bsr;
        const viewport = page.getViewport({ scale: pdfParams.pdfScale }); // 获取窗口大小
        const canvasWidth = Math.floor(viewport.width * ratio);
        const canvasHeight = Math.floor(viewport.height * ratio);
        // const canvasWidth = props.containerWidth;
        // const canvasHeight = Math.floor(viewport.height * ratio) * (props.containerWidth / Math.floor(viewport.width * ratio));
        canvas.width = canvasWidth;
        canvas.height = canvasHeight;
        // canvas.style.width = Math.floor(viewport.width) + 'px'
        // canvas.style.height = Math.floor(viewport.height) + 'px'
        canvas.style.width = Math.floor(props.containerWidth) + "px";
        canvas.style.height =
          Math.floor(
            (viewport.height * props.containerWidth) / viewport.width
          ) + "px";

        let renderContext = {
          canvasContext: context,
          viewport: viewport,
          // 这里transform的六个参数，使用的是transform中的Matrix(矩阵)
          // transform: [1, 0, 0, -1, 0, viewport.height]
          transform: [ratio, 0, 0, ratio, 0, 0],
        };

        // 进行渲染
        page
          .render(renderContext)
          .promise.then(() => {
            resolve();
          })
          .catch((error) => {
            reject(error);
          });
      })
      .catch((error) => {
        reject(error);
      });
  });
};

// // 下一页功能
// const prevPage = () => {
//     if (pdfParams.currentPageNumber > 1) {
//         pdfParams.currentPageNumber -= 1
//     } else {
//         pdfParams.currentPageNumber = 1
//     }
//     getPdfPage(pdfParams.currentPageNumber)
// }
// // 上一页功能
// const nextPage = () => {
//     if (pdfParams.currentPageNumber < pdfParams.pdfPageTotal) {
//         pdfParams.currentPageNumber += 1
//     } else {
//         pdfParams.currentPageNumber = pdfParams.pdfPageTotal
//     }
//     getPdfPage(pdfParams.currentPageNumber)
// }

// //放大
// const scaleD = async () => {
//     let max = 0;
//     if (window.screen.width > 1440) {
//         max = 1.4;
//     } else {
//         max = 1.2;
//     }
//     if (pdfParams.pdfScale >= max) {
//         return;
//     }
//     pdfParams.pdfScale = pdfParams.pdfScale + 0.1;
//     await loadFile();
// }
// //缩小
// const scaleX = async () => {
//     let min = 1.0;
//     if (pdfParams.pdfScale <= min) {
//         return;
//     }
//     pdfParams.pdfScale = pdfParams.pdfScale - 0.1;
//     await loadFile();
// }
</script>

<style scoped lang="scss">
.pdf-preview-box {
  width: 100%;
  position: relative;

  // .pdf_down {
  //     position: fixed;
  //     display: flex;
  //     z-index: 20;
  //     right: 26px;
  //     bottom: 7%;
  //     cursor: pointer;

  //     .pdf_set_left {
  //         width: 30px;
  //         height: 40px;
  //         color: #408fff;
  //         font-size: 15px;
  //         padding-top: 25px;
  //         text-align: center;
  //         margin-right: 5px;
  //         cursor: pointer;
  //     }

  //     .pdf_set_middle {
  //         width: 30px;
  //         height: 40px;
  //         color: #408fff;
  //         font-size: 15px;
  //         padding-top: 25px;
  //         text-align: center;
  //         margin-right: 5px;
  //         cursor: pointer;
  //     }

  //     .pdf-pre {
  //         position: fixed;
  //         display: flex;
  //         z-index: 20;
  //         right: 160px;
  //         bottom: 9%;
  //         cursor: pointer;
  //     }

  //     .pdf-next {
  //         position: fixed;
  //         display: flex;
  //         z-index: 20;
  //         right: 100px;
  //         bottom: 9%;
  //     }
  // }
}
</style>
