//入口组件，components里的组件会被插入此组件中，此组件再插入 index.html 文件里，形成单页面应用；
<template >
  <div id="app">
    <div id = "middle" v-bind:class="{home: homeActive, reg: regActive, ver: verActive, iden: idenActive}">
      <div class = "head">
        <ul id = "daohang">
          <li v-on:click="changebacground('home')"><router-link to="/">首页</router-link></li>
          <li v-on:click="changebacground('reg')"><router-link to="/reg">注册</router-link></li>
          <li v-on:click="changebacground('ver')"><router-link to="/ver">验证</router-link></li>
          <li v-on:click="changebacground('iden')"><router-link to="/iden">识别</router-link></li>
        </ul>
      </div>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
export default {
  name: 'app',
  data() {
        return {
            homeActive: true,
            regActive: false,
            verActive: false,
            idenActive: false,
        }
      },
    methods:{
      changebacground(s){
        if (s == 'home'){
          this.homeActive = true
          this.regActive = false
          this.verActive = false
          this.idenActive = false
        }else if(s == 'reg'){
          this.homeActive = true
          this.regActive = true
          this.verActive = false
          this.idenActive = false
        }else if(s == 'ver'){
          this.homeActive = true
          this.regActive = true
          this.verActive = true
          this.idenActive = false
        }else if(s == 'iden'){
          this.homeActive = true
          this.regActive = true
          this.verActive = true
          this.idenActive = true
        }
        }
    }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
  
}
#daohang {
    list-style-type: none;
    margin:0px;
    padding: 0px;
    /*overflow: hidden;*/
}
#middle {
  height: 1000px;
  /*background-image:url('assets/0424594360.jpg');*/
}
/*样式绑定*/
.home {
  height: 1000px;
  background-image:url('assets/0424594360.jpg')
}
.reg {
  height: 1000px;
  background-image:url('assets/0424058625.jpg')
}
.ver {
  height: 1000px;
  background-image:url('assets/1044395137.jpg')
}
.iden {
  height: 1000px;
  background-image:url('assets/0351114624.jpg')
}

.head {
  margin-left: auto;
  margin-right: auto;
  width: 260px;
  height:40px; 
  /*background-color:#00AA00;*/
}

ul > li {
    float: left;
}

li a {
    display: block;
    color: white;
    text-align: center;
    padding: 14px 16px;
    text-decoration: none;
}

li a:hover:not(.active) {
    background-color: #111;
}

</style>