<template lang="pug">
  div(style="padding:20px;display:flex;flex-direction:column;height:calc(100vh - 50px);overflow:scroll;justify-content:center;")
    //- <el-progress :percentage="100*iterationPointer/retrieval.maxIteration" :text-inside="true" :stroke-width="18" style="margin-bottom:20px;"></el-progress>
    el-row.info(:gutter="20" type="flex")
      el-col(:span="6" :xs="{span: 24}")
        el-card(shadow="hover" style="height:200px;" v-loading="!retrieval.library")
          div(slot="header" class="clearfix")
            span 基本信息
            //- <!-- <el-button style="float: right; padding: 3px 0" type="text">操作按钮</el-button> -->
          table(v-if="retrieval.library")
            tbody
              tr
                th 人脸库：
                td {{ retrieval.library.name }}
              tr
                th 距离：
                td {{ retrieval.distance.name }}
              tr
                th 策略：
                td {{ retrieval.strategy }}
              tr
                th 容量：
                td {{ retrieval.library.name }}
      el-col(:span="6" :xs="{span: 24}")
        //- style="text-align:center;vertical-align:middle;height:100%;margin:auto;display:flex;align-items:center;justify-content:center;"
        //- el-progress(type="circle" :percentage="100*iterationPointer/retrieval.maxIteration")
        el-card(shadow="hover" style="height:200px;")
          div(slot="header" class="clearfix")
            span 进度
            //- el-progress(:width="60" :percentage="100*iterationPointer/retrieval.maxIteration")
          table
            tbody
              tr
                th 迭代次数
                td {{ iterationPointer-1 }} / {{retrieval.maxIteration}}
              //- tr
                th 距离：
                <td>{{ retrieval.distance.name }}</td>
              //- tr
                th 策略：
                <td>{{ retrieval.strategy }}</td>
              //- tr
                th 容量：
                <td>{{ retrieval.library.name }}</td>
          div(style="text-align:center;")
            el-progress(:width="60" :percentage="Math.round(100*(iterationPointer-1)/retrieval.maxIteration)")
      el-col(:span="6" :xs="{span: 24}")
        el-card(shadow="hover" style="height:200px;position:relative;")
          div(slot="header" class="clearfix" style="display:flex;justify-content:space-between;")
            div 目标
            //- div(style="position:absolute;right:10px;top:6px;")
              el-input(style="width:80px;margin-right:0px;")
              el-button(type="primary" @click="next" ) 上 传

          div(style="text-align:center;display:flex;justify-content:space-around;align-items:center;")
            div(style="width:40%;")
              el-input(style="width:100%;margin-bottom:10px;")
              el-button() 指 定
              //- el-button(type="primary" ) 指 定

            el-upload(:action="`/api/retrieves/${retrieval.id}/targets`" list-type="picture-card" :on-preview="handlePictureCardPreview" :file-list="fileList")
              i(class="el-icon-plus")
            el-dialog(:visible.sync="dialogVisible")
              img(width="100%" :src="dialogImageUrl" alt="")
          //- el-upload(class="avatar-uploader" action="https://jsonplaceholder.typicode.com/posts/" :show-file-list="false" :on-success="handleAvatarSuccess" :before-upload="beforeAvatarUpload")
            img(v-if="imageUrl" :src="imageUrl" class="avatar")
            i(v-else class="el-icon-plus avatar-uploader-icon")
          //- photo-card(:photo-name="retrievalID" library-name="target")

      el-col(:span="6" :xs="{span: 24}")
        history-card(:selected-history="selectedHistory" :library-name="libraryName")

    //- div(style="flex:1;display:flex;align-items:center;")
    el-row.photos(:gutter="10" style="flex:1;" v-loading="loadingPhotos")
      //- div(style="flex:1;box-sizing:border-box;padding:20px;display:flex;flex-wrap:wrap;justify-content:center;align-items:center;")
      el-col(v-for="(photo,index) in photos" :span="photoSpan" :key="index" :style="{marginBottom:'0px',height:`${100/(photos.length/(24/photoSpan))}%`}")
        //- div(style="position:relative;height:40%;padding-left:10%;margin:0 7.5%;" v-for="(photoName,index) in photos" )
        photo-card(style="height:100%;" :photo="photo"  @click.native="getNextIteration(photo)")
          //- divstyle="height:20px">{{ photoName }}</div>
    el-row.operation(:gutter="12" style="" type="flex" justify="center")
      el-col(:span="4" :xs="{span: 8}")
        el-button(:disabled="iterationPointer <= 1" @click="back") 上一步
      el-col(:span="4" :xs="{span: 8}" )
        el-button(type="primary" ) 结束选择
      el-col(:span="4" :xs="{span: 8}")
        el-button(:disabled="iterationPointer <= 1" @click="next" ) 下一步
        //- <!-- <el-row :gutter="12">
        //-   <el-col style="margin-top:10px;" :span="photoSpan" v-for="(photoName,index) in photos" :key="index">
        //-     <photo-card :libraryName="libraryName" :photoName="photoName" @click.native="getNextIteration(photoName)"></photo-card>
        //-   </el-col>
        //- </el-row> -->
    el-dialog(title="迭代结果" :visible.sync="resultDialogVisible" center)
      //- el-col(:span="6" :xs="{span: 24}")
      history-card(:selected-history="selectedHistory" :library-name="libraryName")
      span(slot="footer" class="dialog-footer" style="text-align:center;")
        el-button(@click="resultDialogVisible = false") 重 开
        el-button(type="primary" @click="resultDialogVisible = false") 确 定

</template>

<script>
import { createIteration, fetchRetrieval } from '@/api'
import photoCard from './components/photo'
import historyCard from './components/historyCard'

export default {
  components: { photoCard, historyCard },
  props: {
    retrievalID: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      iterations: [],
      retrieval: {},
      iterationPointer: 0,
      selectedHistory: [],
      libraryName: '',
      loadingPhotos: false,
      imageUrl: '',
      dialogImageUrl: '',
      dialogVisible: false,
      resultDialogVisible: false,
      library: {},
      fileList: []
    }
  },
  computed: {
    photos: function() {
      if (this.iterationPointer === 0) {
        return []
      } else {
        return this.iterations[this.iterationPointer - 1]
      }
    },
    photoSpan: function() {
      if (this.photos.length === 8) {
        return 6
      } else if (this.photos.length === 12) {
        return 6
      } else if (this.photos.length === 18) {
        return 4
      } else if (this.photos.length === 24) {
        return 3
      }
      return 4
    }
  },
  mounted: function() {
    fetchRetrieval(this.retrievalID).then(resp => {
      this.retrieval = resp.data
      this.libraryName = resp.data.library.name
      if (resp.data.targetUrl) {
        this.imageUrl = resp.data.targetUrl
        this.fileList = [
          {
            name: 'target',
            url: resp.data.targetUrl
          }
        ]
      }
      this.getNextIteration('0')
    })
  },
  methods: {
    handleRemove(file, fileList) {
      console.log(file, fileList)
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url
      this.dialogVisible = true
    },
    handleAvatarSuccess(res, file) {
      this.imageUrl = URL.createObjectURL(file.raw)
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg'
      const isLt2M = file.size / 1024 / 1024 < 2

      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!')
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!')
      }
      return isJPG && isLt2M
    },
    getNextIteration(selectedPhoto) {
      if (this.iterations.length > this.retrieval.maxIteration) {
        this.resultDialogVisible = true
        return
      }
      this.loadingPhotos = true
      createIteration(
        this.retrievalID,
        this.iterationPointer,
        selectedPhoto.name
      ).then(resp => {
        if (this.iterations.length === this.retrieval.maxIteration) {
          this.resultDialogVisible = true
        }
        this.iterations.push(resp.data)
        this.iterationPointer && this.selectedHistory.unshift(selectedPhoto)
        this.iterationPointer += 1
        this.loadingPhotos = false
      })
    },
    back() {
      this.iterationPointer -= 1
      this.selectedHistory.shift()
      this.iterations.pop()
    },
    next() {}
  }
}
</script>
<style scoped>
.info {
}
.photos {
  padding: 20px;
}
.operation {
  padding-top: 5vh;
  padding-bottom: 5vh;
  text-align: center;
}
@media (max-width: 700px) {
  .info {
    flex-wrap: nowrap;
    width: 100%;
    overflow: scroll;
  }
  .info .el-card {
    width: 80vw;
  }
  .photos {
    padding: 0;
  }
  .operation {
    padding-top: 10px;
    padding-bottom: 10px;
    text-align: center;
  }
}
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  height: 100px;
  margin: auto;
}
.avatar-uploader .el-upload:hover {
  border-color: #409eff;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  line-height: 100px;
  text-align: center;
}
.avatar {
  width: 100px;
  height: 100px;
  display: block;
}
.el-upload-list--picture-card:not(:empty) + .el-upload--picture-card {
  display: none;
}
.el-upload-list__item {
  width: 100px !important;
  height: 100px !important;
}
.el-upload--picture-card {
  width: 100px !important;
  height: 100px !important;
  line-height: 100px !important;
}
.el-icon-plus {
  line-height: 100px !important;
}
.el-upload-list--picture-card .el-upload-list__item-status-label i {
  margin-top: 6px;
}
</style>
