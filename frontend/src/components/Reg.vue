<template>
  <div class="main">
    <div class="part1">
      <div class="upload_image">
          <h3 id = 'h3'><font color="white">第二步：请上传图片</font></h3>
          <div class="upload">
            <div class="upload_warp">
              <div class="upload_warp_left" @click="fileClick">
                <img src="../assets/upload.png">
              </div>
              <div class="upload_warp_right" @drop="drop($event)" @dragenter="dragenter($event)" @dragover="dragover($event)">
                或者将文件拖到此处
              </div>
            </div>
            <!--选中统计-->
            <div class="upload_warp_text">
              选中{{imgList.length}}张文件，共{{bytesToSize(this.size)}}
            </div>
            <input @change="fileChange($event)" type="file" id="upload_file" multiple style="display: none"/>
            <!--图片列表-->
            <div class="upload_warp_img" v-show="imgList.length!=0">
              <div class="upload_warp_img_div" v-for="(item,index) in imgList"
                   v-dragging="{ item: item, list: imgList, group: 'color' }"
                   :key="index"
                   >
                <div class="upload_warp_img_div_top">
                  <div class="upload_warp_img_div_text">
                    {{item.file.name}}
                  </div>
                  <img src="../assets/del.png" class="upload_warp_img_div_del" @click="fileDel(index)">
                </div>
                <img :src="item.file.src">
              </div>
            </div>
          </div>
          <!--底部文件名字列表 -->
          <div v-for="(item,index) in imgList" style="text-align: left">
            <font color="white">{{index}}：{{item.file.name}}</font>
          </div>
      </div>
      <!--输入表单-->
      <div class="input_id">
          <h3 id = 'h3'><font color="white">第一步：请输入ID、姓名</font></h3>
          <form action="" method="">
            <div>
              <label for="name">ID:</label>
              <input type="text" id="name" v-model.trim="my_id" placeholder="唯一ID" >
            </div>
            <div>
              <label for="mail">姓名:</label>
              <input type="email" id="mail" v-model.trim="my_name" placeholder="姓名" >
            </div>
          </form>
      </div>
      <div class="button">
        <button v-on:click="register" type="submit">注册</button>
      </div>
      <div class="error">
        <p><font color="white">{{error}}</font></p>
      </div>
      <div class="result1" v-if = "resultNumber === '1'">
        <p><font color="white">注册成功</font></p>
      </div>
      <div class="result2" v-else-if = "resultNumber === '-1'">
        <p><font color="white">注册失败,该ID已存在</font></p>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  export default {
    name: 'hello',
    data() {
      return {
        imgList: [],
        my_id: "",
        my_name: "",
        size: 0,
        limit: 5,
        error: "",
        resultNumber: "0"
      }
    },
    methods: {
      //设置
      fileClick() {
        document.getElementById('upload_file').click()
      },
      fileChange(el) {
        if (!el.target.files[0].size) return
        this.fileList(el.target)
        el.target.value = ''
      },
      fileList(fileList) {
        let files = fileList.files
        for (let i = 0; i < files.length; i++) {
          //判断是否为文件夹
          if (files[i].type != '') {
            this.fileAdd(files[i])
          } else {
            //文件夹处理
            this.folders(fileList.items[i])
          }
        }
      },
      //文件夹处理
      folders(files) {
        let _this = this
        //判断是否为原生file
        if (files.kind) {
          files = files.webkitGetAsEntry()
        }
        files.createReader().readEntries(function (file) {
          for (let i = 0; i < file.length; i++) {
            if (file[i].isFile) {
              _this.foldersAdd(file[i])
            } else {
              _this.folders(file[i])
            }
          }
        })
      },
      foldersAdd(entry) {
        let _this = this
        entry.file(function (file) {
          _this.fileAdd(file)
        })
      },
      fileAdd(file) {
        if (this.limit !== undefined) this.limit--
        if (this.limit !== undefined && this.limit < 0) return
        //总大小
        this.size = this.size + file.size
        //判断是否为图片文件
        if (file.type.indexOf('image') == -1) {
          file.src = 'wenjian.png'
          this.imgList.push({
            file
          })
        } else {
          let reader = new FileReader()
          let image = new Image()
          let _this = this // this 在后面的代码执行之后会变成 
          reader.readAsDataURL(file)
          reader.onload = function () {
            file.src = this.result// this 变为reader
            image.onload=function(){
              let width = image.width
              let height = image.height
              //file.width=width;
              //file.height=height;
              _this.imgList.push({file}) // 注意这里又将file封装成对象了
              console.log( _this.imgList[0].file)
            }
            image.src= file.src
          }
        }
      },
      fileDel(index) {
        this.size = this.size - this.imgList[index].file.size//总大小
        this.imgList.splice(index, 1)
        if (this.limit !== undefined) this.limit = this.imgList.length
      },
      bytesToSize(bytes) {
        if (bytes === 0) return '0 B'
        let k = 1000, // or 1024
          sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
          i = Math.floor(Math.log(bytes) / Math.log(k))
        return (bytes / Math.pow(k, i)).toPrecision(3) + ' ' + sizes[i]
      },
      dragenter(el) {
        el.stopPropagation()
        el.preventDefault()
      },
      dragover(el) {
        el.stopPropagation()
        el.preventDefault()
      },
      drop(el) {
        el.stopPropagation()
        el.preventDefault()
        this.fileList(el.dataTransfer)
      },
      register: function() {
        if (this.my_id== "") {
          this.error = "ERROR:ID不为空"
        }
        else if (this.my_name== "") {
          this.error = "ERROR:姓名不为空"
        }
        else if (this.imgList.length == 0) {
          this.error = "ERROR:图片不为空"
        }
        else{
          let formData = new FormData()

          console.log(this.imgList.length)
          for (let i = 0;i < this.imgList.length; i++) {
            formData.append("files", this.imgList[i].file)
          }
          console.log(formData.getAll("files"))
          formData.append("id", this.my_id)
          formData.append("name", this.my_name)
          //append方法 formData重复的往一个值添加数据并不会被覆盖掉，可以全部接收到，可以通过formData.getAll('files')来查看所有插入的数据
          let url = 'http://10.108.246.53:5000/api/register'
          let headers = {
            'Content-Type': 'multipart/form-data'
          }
          axios.post(url, formData, {headers: headers})
          .then(response => {
            this.resultNumber = response.data.resultNumber
            console.log(this.resultNumber)
          })
          .catch(error => {
            console.log(error)
          })
           
        }
      }
    }
  }

</script>

<style scoped>
  .upload_warp_img_div_del {
    position: absolute;
    top: 6px;
    width: 16px;
    right: 4px;
  }
  .upload_warp_img_div_top {
    position: absolute;
    top: 0;
    width: 100%;
    height: 30px;
    background-color: rgba(0, 0, 0, 0.4);
    line-height: 30px;
    text-align: left;
    color: #fff;
    font-size: 12px;
    text-indent: 4px;
  }
  .upload_warp_img_div_text {
    white-space: nowrap;
    width: 80%;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .upload_warp_img_div img {
    max-width: 100%;
    max-height: 100%;
    vertical-align: middle;
  }
  .upload_warp_img_div {
    position: relative;
    height: 100px;
    width: 120px;
    border: 1px solid #ccc;
    margin: 0px 30px 10px 0px;
    float: left;
    line-height: 100px;
    display: table-cell;
    text-align: center;
    background-color: #eee;
    cursor: pointer;
  }
  .upload_warp_img {
    border-top: 1px solid #D2D2D2;
    padding: 14px 0 0 14px;
    overflow: hidden;
  }
  .upload_warp_text {
    text-align: left;
    margin-bottom: 10px;
    padding-top: 10px;
    text-indent: 14px;
    border-top: 1px solid #ccc;
    font-size: 14px;
  }
  .upload_warp_right {
    float: left;
    width: 57%;
    margin-left: 2%;
    height: 100%;
    border: 1px dashed #999;
    border-radius: 4px;
    line-height: 130px;
    color: #999;
  }
  .upload_warp_left img {
    margin-top: 32px;
  }
  .upload_warp_left {
    float: left;
    width: 40%;
    height: 100%;
    border: 1px dashed #999;
    border-radius: 4px;
    cursor: pointer;
  }
  .upload_warp {
    margin: 14px;
    height: 130px;
  }
  .upload {
    border: 1px solid #ccc;
    background-color: #fff;
    width: 800px;
    box-shadow: 0px 1px 0px #ccc;
    border-radius: 4px;
  }
  .upload_image {
    width: 800px;
    float: right;
  }
  form {
    /* 居中表单 */
    margin: 0 auto;
    width: 400px;
    /* 显示表单的轮廓 */
    padding: 1em;
    border: 1px solid #CCC;
    border-radius: 1em;
  }
  form div + div {
    margin-top: 1em;
  }
  label {
    /* 确保所有label大小相同并正确对齐 */
    display: inline-block;
    width: 90px;
    text-align: right;
    color: #FFFFFF;
  }

  input{
    /* 确保所有文本输入框字体相同
       textarea默认是等宽字体 */
    font: 1em sans-serif;
    /* 使所有文本输入框大小相同 */
    width: 300px;
    box-sizing: border-box;
    /* 调整文本输入框的边框样式 */
    border: 1px solid #999;
  }
  input:focus {
    /* 给激活的元素一点高亮效果 */
    border-color: #000;
  }
  .input_id {
    height: 300px;
    width: 500px;
    float: left;
  }
  .button {
    width: 300px;
  }
  .part1 {
    margin-left: auto;
    margin-right: auto;
    height: 500px;
    width: 1300px;
    
  }
  .main {
    height: auto;
    width: auto;
    height: 1000px;
    background-image:url('../assets/0424058625.jpg');
  }
</style>