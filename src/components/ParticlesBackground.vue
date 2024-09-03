<template>
  <canvas ref="canvas"></canvas>
</template>

<script>
export default {
  name: 'ParticleCanvas',
  data() {
    return {
      canvas: null,
      ctx: null,
      particlesArray: [],
      count: 0,
      DISTANCE_THRESHOLD: 100, // 控制连线的最大距离
      mouse: {
        x: 0,
        y: 0
      }
    };
  },
  mounted() {
    this.canvas = this.$refs.canvas;
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    this.ctx = this.canvas.getContext('2d');
    this.count = Math.floor(this.canvas.height / 100 * this.canvas.width / 100 / 2);
    this.addEventListeners();
    this.animate();
    window.addEventListener('resize', this.handleResize);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    addEventListeners() {
      window.addEventListener('mousemove', this.handleMouseMove);
    },
    handleMouseMove(event) {
      this.mouse.x = event.x;
      this.mouse.y = event.y;
    },
    createParticle() {
      const x = Math.random() * this.canvas.width;
      const y = Math.random() * this.canvas.height;
      this.particlesArray.push(new Particle(x, y, this.mouse));
    },
    handleParticle() {
      for (let i = 0; i < this.particlesArray.length; i++) {
        const particle = this.particlesArray[i];
        particle.update(this.mouse, this.canvas);
        particle.draw(this.ctx);
        if (particle.x < 0 || particle.x > this.canvas.width || particle.y < 0 || particle.y > this.canvas.height) {
          this.particlesArray.splice(i, 1);
        }
        for (let j = i + 1; j < this.particlesArray.length; j++) {
          const dx = this.particlesArray[i].x - this.particlesArray[j].x;
          const dy = this.particlesArray[i].y - this.particlesArray[j].y;
          const long = Math.sqrt(dx * dx + dy * dy);
          if (long < this.DISTANCE_THRESHOLD) {
            this.ctx.beginPath();
            this.ctx.strokeStyle = `rgba(255,255,255,${1 - long / this.DISTANCE_THRESHOLD})`;
            this.ctx.moveTo(this.particlesArray[i].x, this.particlesArray[i].y);
            this.ctx.lineTo(this.particlesArray[j].x, this.particlesArray[j].y);
            this.ctx.lineWidth = 1;
            this.ctx.stroke();
          }
        }
      }
    },
    draw() {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      if (this.particlesArray.length < this.count) {
        this.createParticle();
      }
      this.handleParticle();
    },
    animate() {
      this.draw();
      requestAnimationFrame(this.animate);
    },
    handleResize() {
      this.canvas.width = window.innerWidth;
      this.canvas.height = window.innerHeight;
      this.count = Math.floor(this.canvas.height / 100 * this.canvas.width / 100 / 2);
    }
  }
};

// 修改后的 Particle 类
class Particle {
  constructor(x, y, mouse) {
    this.x = x;
    this.y = y;
    this.directionY = 0.5 - Math.random();
    this.directionX = 0.5 - Math.random();
    this.size = 2;
    this.speed = 5; // 控制粒子向鼠标移动的速度
    this.mouse = mouse;
  }
  update(mouse, canvas) {
    // 计算鼠标与粒子之间的距离
    const dx = mouse.x - this.x;
    const dy = mouse.y - this.y;
    const distance = Math.sqrt(dx * dx + dy * dy);

    // 调整速度使粒子朝向鼠标移动
    if (distance < 100) {
      this.x += (dx / distance) * this.speed;
      this.y += (dy / distance) * this.speed;
    } else {
      this.x += this.directionX;
      this.y += this.directionY;
    }

    // 边界处理
    if (this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height) {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
    }
  }
  draw(ctx) {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fillStyle = 'white';
    ctx.fill();
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
}
body {
  background: #333;
  overflow: hidden;
}
canvas {
  position: fixed;
  left: 0;
  top: 0;
}
</style>
