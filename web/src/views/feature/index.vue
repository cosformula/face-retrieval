<template lang="pug">
  .app-container
    .filter-container
      //- el-button( :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-search" @click="handleImport") 导入距离
      el-button( :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-search" @click="handleCreate") 新建特征

    el-table.table(v-loading='listLoading', :key='tableKey', :data='list', border='', fit='', highlight-current-row='')
      el-table-column(:label="'序号'", align='center', width='65')
        template(slot-scope='scope')
          span {{ scope.row.id }}
      el-table-column(:label="'名称'", align='center' width='250')
        template(slot-scope='scope')
          span {{ scope.row.name }}
      el-table-column(:label="'图像库'", align='center' width='250')
        template(slot-scope='scope')
          span {{ scope.row.library.name }}
      el-table-column(:label="'可用'", align='center')
        template(slot-scope='scope')
          i(v-if="scope.row.available" class="el-icon-success" style="color:green;")
          i(v-else class="el-icon-error"  style="color:red;")
      el-table-column(:label="'状态'", align='center')
        template(slot-scope='scope')
          pulse-loader(v-if="scope.row.status === 'initializing'")
          span(v-else) {{ scope.row.status }}
      el-table-column(:label="'操作'" align='center')
        template(slot-scope='scope' )
          //- el-button(size="mini" @click="handleEdit(scope.$index, scope.row)") 图片浏览
          //- el-button(size="mini" @click="$router.push(`/feature/index?libraryId=${scope.row.id}`)") 特征管理
          //- el-button(size="mini" @click="$router.push(`/distance/index?libraryId=${scope.row.id}`)") 距离管理
          el-button(size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)") 删除特征
    div(class="pagination-container")
      el-pagination(
        :current-page="listQuery.page"
        :page-sizes="[10,20,30, 50]"
        :page-size="listQuery.limit"
        :total="total"
        background
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange")
    el-dialog(:title="textMap[dialogStatus]" :visible.sync="dialogFormVisible")
      el-form(
        ref="dataForm"
        :rules="temp.local? localRules: uploadRules"
        :model="temp"
        label-position="left"
        label-width="100px"
        style="width: 400px; margin-left:50px;")
        el-form-item(required label="图片库" prop="libraryId")
          el-select(@change="updateDistances" v-model="temp.libraryId" placeholder="请选择图片库" style="width: 100%;")
            el-option(v-for="lib in libraries" :label="lib.name" :key="lib.id" :value="lib.id")
        el-form-item
          el-switch(v-model="temp.local" active-text="本地生成特征" inactive-text="导入特征文件")
        template(v-if="temp.local")
          el-form-item(:label="'特征算法'" prop="feature" )
            // el-input(v-model="temp.feature" disabled)
            el-select(v-model="temp.feature" placeholder="请选择" style="width:100%;")
              el-option(v-for="item in featureOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value")
          //- el-form-item(:label="'特征算法'" prop="title")
            el-input(v-model="temp.feature" disabled)
        template(v-else)
          el-form-item(:label="'距离文件'" prop="title")
            el-upload(class="upload-demo"
              action="/api/files"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :on-change="handleFileChange"
              :on-success="handleFileUploaded"
              :before-remove="beforeRemove"
              :limit="1"
              :on-exceed="handleExceed")
              el-button(size="small" type="primary") 点击上传
              div(slot="tip" class="el-upload__tip") 只能上传csv文件
          el-form-item(:label="'文件ID'" prop="file")
            el-input(v-model="temp.file" disabled)
        el-form-item(:label="'名称'" prop="name")
          el-input(v-model="temp.name")
        el-form-item(:label="'备注'" prop="detail")
          el-input(v-model="temp.detail")
      div(slot="footer" class="dialog-footer")
        <el-button @click="dialogFormVisible = false"> {{ $t('table.cancel') }}</el-button>
        el-button(
          v-if="dialogStatus=='create'"
          type="primary"
          @click="createData") {{ $t('table.confirm') }}</el-button>
        <el-button v-else type="primary" @click="updateData"> {{ $t('table.confirm') }}</el-button>

</template>
<script>
import { featureService, fetchLibraries, fetchDistances } from '@/api'
import PulseLoader from 'vue-spinner/src/PulseLoader.vue'
export default {
  components: {
    PulseLoader
  },
  data() {
    return {
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      list: [],
      total: null,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        importance: undefined,
        title: undefined,
        type: undefined,
        sort: '+id'
      },
      dialogFormVisible: false,
      dialogStatus: '',
      libraries: [],
      temp: {
        libraryId: '',
        file: '',
        name: '22',
        detail: '22',
        algorithm: 'resnet50'
      },
      featureOptions: [
        {
          label: 'resnet50',
          value: 'resnet50'
        },
        {
          label: 'vggface',
          value: 'vggface'
        }
      ],
      localRules: {
        name: [
          {
            // type: 'string',
            required: true,
            message: 'name is required',
            trigger: 'blur'
          }
        ],
        feature: [
          { required: true, message: 'remark is required', trigger: 'blur' }
        ],
        detail: [
          { required: true, message: 'remark is required', trigger: 'blur' }
        ]
      },
      uploadRules: {
        name: [
          {
            // type: 'string',
            required: true,
            message: 'name is required',
            trigger: 'blur'
          }
        ],
        file: [
          {
            // type: 'string',
            required: true,
            message: 'name is required',
            trigger: 'blur'
          }
        ],
        detail: [
          { required: true, message: 'remark is required', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    this.getList()
    fetchLibraries().then(res => {
      this.libraries = res.data.items
    })
  },
  methods: {
    getList() {
      this.listLoading = true
      featureService.get(this.listQuery).then(res => {
        this.list = res.data.items
        this.total = res.data.total
        this.listLoading = false
      })
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.getList()
    },
    handleCurrentChange(val) {
      this.listQuery.page = val
      this.getList()
    },
    createData() {
      featureService.create(this.temp).then(res => {
        this.dialogFormVisible = false
        this.list.unshift(res.data)
        console.log(res)
      })
    },
    handleImport() {},
    handleCreate() {
      this.dialogFormVisible = true
      this.dialogStatus = 'create'
    },
    updateDistances() {
      fetchDistances(this.form.libID).then(resp => {
        this.distances = resp.data
      })
    }
  }
}
</script>
<style lang="stylus" scoped>
.table
  margin 20px 0
</style>
