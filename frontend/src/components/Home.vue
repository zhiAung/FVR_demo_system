<template>
  <div id="main">
    <div class="title">
      <h1>欢迎体验指静脉识别系统</h1>
    </div>
    <div class="bacimg">
        <img src="../assets/0107025130 (1).png" height="500" width="400">
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
    data () {
        return {
            active: '主页'
        }
      },
      methods: {
        makeActive (item) {
          this.active = item;
        }
      },
      created () {
        this.makeActive()
      }
    }
</script>

<style scoped>
h1 {
  margin-left: auto;
  margin-right: auto;
  height: 80px;
  color:#FFFFFF;
  font-weight:bold;
  /*background-color: #00FF00*/
}
#bacimg {
background-color: #FF0000;
}

  
</style>
