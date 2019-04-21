<template lang="pug">
  .app-container
    .filter-container
      //- el-input(:placeholder="$t('table.title')"
        v-model="listQuery.title"
        style="width: 200px;"
        class="filter-item"
        @keyup.enter.native="handleFilter")
      //- el-button(class="filter-item"
        type="primary"
        icon="el-icon-search"
        @click="handleFilter") {{ $t('table.search') }}
      el-button( :loading="downloadLoading" class="filter-item" type="primary" icon="el-icon-search" @click="handleCreate") 导入照片库
      //- el-button(
        :loading="downloadLoading"
        class="filter-item"
        type="primary"
        icon="el-icon-download"
        @click="handleDownload") {{ $t('table.export') }}
    el-table.table(v-loading='listLoading', :key='tableKey', :data='list', border='', fit='', highlight-current-row='')
      el-table-column(:label="'序号'", align='center', width='65')
        template(slot-scope='scope')
          span {{ scope.row.id }}
      el-table-column(:label="'例图'", align='center' width='100')
        template(slot-scope='scope')
          img.cover(:src="`/api/${scope.row.cover}`")
          //- span {{ scope.row.detail }}
      el-table-column(:label="'名称'", align='center' width='150')
        template(slot-scope='scope')
          span {{ scope.row.name }}
      el-table-column(:label="'容量'", align='center' width='150')
        template(slot-scope='scope')
          span {{ scope.row.count }}
      //- el-table-column(:label="'状态'", align='center')
        template(slot-scope='scope')
          span {{ scope.row.status }}
      //- el-table-column(:label="'策略'", align='center')
        template(slot-scope='scope')
          span {{ scope.row.strategy }}
      el-table-column(:label="'可用'", align='center'  width=50)
        template(slot-scope='scope')
          // span {{ scope.row.isAvailable }}
          i(v-if="scope.row.isAvailable" class="el-icon-success" style="color:green;")
          i(v-else class="el-icon-error"  style="color:red;")
      el-table-column(:label="'状态'", align='center' width=100)
        template(slot-scope='scope')
          span {{ scope.row.status }}
      el-table-column(:label="'备注'", align='center')
        template(slot-scope='scope')
          span {{ scope.row.detail }}
      el-table-column(:label="'操作'" align='center')
        template(slot-scope='scope' )
          //- el-button(size="mini" @click="handleEdit(scope.$index, scope.row)") 图片浏览
          //- el-button(size="mini" @click="$router.push(`/feature/index?libraryId=${scope.row.id}`)") 特征管理
          el-button(size="mini" @click="$router.push(`/distance/index?libraryId=${scope.row.id}`)") 距离管理
          el-button(size="mini" type="danger" @click="handleDelete(scope.$index, scope.row)") 删除照片库
      //- el-table-column(:label="'图像库'", align='center')
      //-   template(slot-scope='scope')
      //-     span {{ scope.row.library.name }}
      //- el-table-column(:label="'状态'", align='center')
      //-   template(slot-scope='scope')
      //-     span {{ scope.row.status }}
      //- el-table-column(:label="'策略'", align='center')
      //-   template(slot-scope='scope')
      //-     span {{ scope.row.strategy }}
      //- el-table-column(:label="'备注'", align='center')
      //-   template(slot-scope='scope')
      //-     span {{ scope.row.strategy }}
    //- el-row.content(:gutter="20")
      el-col(v-for="library in list" span="4" style="margin-bottom:10px;" :key="library.id")
        el-card(style="text-align:center;" shadow="hover")
          div(slot="header" class="clearfix")
            span {{ library.name }}
          img.cover(:src="`/api/${library.cover}`")
          table(style="width:100%;margin-bottom:5px;")
            <tbody>
              <tr>
                <th>ID</th>
                <td>{{ library.id }}</td>
              </tr>
              <tr>
                <th>容量</th>
                <td>{{ library.count }}</td>
              </tr>
              <tr>
                <th>时间</th>
                <td>{{ library.detail }}</td>
              </tr>
              <tr>
                <th>详情</th>
                <td>{{ library.detail }}</td>
              </tr>
              //- tr
                th 例图
                td
                  img.cover(:src="`/api/${library.cover}`")
            </tbody>
          el-row(style="text-align:center;")
            el-col(:span="12")
              <el-button>图片浏览</el-button>
            el-col(:span="12")
              <el-button>特征管理</el-button>
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
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="70px"
        style="width: 400px; margin-left:50px;")
        el-form-item(:label="'图片库'" prop="title")
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
            div(slot="tip" class="el-upload__tip") 只能上传zip文件
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
    el-dialog(:visible.sync="dialogPvVisible" title="Reading statistics")
      <el-table :data="pvData" border fit highlight-current-row style="width: 100%">
        <el-table-column prop="key" label="Channel"/>
        <el-table-column prop="pv" label="Pv"/>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogPvVisible = false"> {{ $t('table.confirm') }}</el-button>
      </span>
</template>

<script>
// import { fetchList, fetchPv, createArticle, updateArticle } from '@/api/article'
import { fetchLibraries, createLibrary, deleteLibrary } from '@/api'

// import waves from '@/directive/waves' // 水波纹指令
// import { parseTime } from '@/utils'

const calendarTypeOptions = [
  { key: 'CN', display_name: 'China' },
  { key: 'US', display_name: 'USA' },
  { key: 'JP', display_name: 'Japan' },
  { key: 'EU', display_name: 'Eurozone' }
]

// arr to obj ,such as { CN : "China", US : "USA" }
const calendarTypeKeyValue = calendarTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'ComplexTable',
  directives: {
    // waves
  },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    typeFilter(type) {
      return calendarTypeKeyValue[type]
    }
  },
  data() {
    return {
      tableKey: 0,
      list: null,
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
      importanceOptions: [1, 2, 3],
      calendarTypeOptions,
      sortOptions: [
        { label: 'ID Ascending', key: '+id' },
        { label: 'ID Descending', key: '-id' }
      ],
      statusOptions: ['published', 'draft', 'deleted'],
      showReviewer: false,
      temp: {
        id: undefined,
        importance: 1,
        file: '',
        name: '',
        detail: '',
        timestamp: new Date(),
        title: '',
        type: '',
        status: 'published',
        fileId: ''
      },
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: 'Edit',
        create: 'Create'
      },
      dialogPvVisible: false,
      pvData: [],
      rules: {
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
        timestamp: [
          {
            type: 'date',
            required: true,
            message: 'timestamp is required',
            trigger: 'blur'
          }
        ],
        detail: [
          { required: true, message: 'remark is required', trigger: 'blur' }
        ]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    handleFileUploaded(response) {
      this.temp.file = response.file
    },

    handleFileChange(file, fileList) {
      this.temp.name = this.temp.name || file.name
    },

    handleRemove(file, fileList) {
      console.log(file, fileList)
    },
    handlePreview(file) {
      console.log(file)
    },
    handleExceed(files, fileList) {
      this.$message.warning(
        `当前限制选择 3 个文件，本次选择了 ${
          files.length
        } 个文件，共选择了 ${files.length + fileList.length} 个文件`
      )
    },
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`)
    },
    getList() {
      this.listLoading = true
      fetchLibraries(this.listQuery).then(response => {
        this.list = response.data.items
        this.total = response.data.total
        this.listLoading = false
        console.log(this.list)
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.getList()
    },
    handleCurrentChange(val) {
      this.listQuery.page = val
      this.getList()
    },
    handleModifyStatus(row, status) {
      this.$message({
        message: '操作成功',
        type: 'success'
      })
      row.status = status
    },
    resetTemp() {
      this.temp = {
        id: undefined,
        importance: 1,
        remark: '',
        file: '',
        name: '',
        timestamp: new Date(),
        title: '',
        status: 'published',
        type: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    handleDelete(index, row) {
      this.$confirm(
        '此操作将永久删除该人脸库，与之关联的所有记录也将删除, 是否继续?',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
        .then(() => {
          deleteLibrary(row.id).then(() => {
            this.$notify({
              title: '成功',
              message: '删除成功',
              type: 'success',
              duration: 2000
            })
            this.list.splice(index, 1)
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    createData() {
      this.$refs['dataForm'].validate(valid => {
        if (valid) {
          this.temp.id = parseInt(Math.random() * 100) + 1024 // mock a id
          this.temp.author = 'vue-element-admin'
          createLibrary(this.temp).then(resp => {
            this.dialogFormVisible = false
            this.$notify({
              title: '成功',
              message: '创建成功',
              type: 'success',
              duration: 2000
            })
            // console.log(data)
            this.list.unshift(resp.data)
          })
          // createArticle(this.temp).then(() => {
          //   this.list.unshift(this.temp)
        }
      })
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row) // copy obj
      this.temp.timestamp = new Date(this.temp.timestamp)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate(valid => {
        if (valid) {
          const tempData = Object.assign({}, this.temp)
          tempData.timestamp = +new Date(tempData.timestamp) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
          // updateArticle(tempData).then(() => {
          //   for (const v of this.list) {
          //     if (v.id === this.temp.id) {
          //       const index = this.list.indexOf(v)
          //       this.list.splice(index, 1, this.temp)
          //       break
          //     }
          //   }
          //   this.dialogFormVisible = false
          //   this.$notify({
          //     title: '成功',
          //     message: '更新成功',
          //     type: 'success',
          //     duration: 2000
          //   })
          // })
        }
      })
    },
    // handleDelete(row) {
    //   this.$notify({
    //     title: '成功',
    //     message: '删除成功',
    //     type: 'success',
    //     duration: 2000
    //   })
    //   const index = this.list.indexOf(row)
    //   this.list.splice(index, 1)
    // },
    handleFetchPv(pv) {
      // fetchPv(pv).then(response => {
      //   this.pvData = response.data.pvData
      //   this.dialogPvVisible = true
      // })
    },
    handleDownload() {
      this.downloadLoading = true
      // import('@/vendor/Export2Excel').then(excel => {
      //   const tHeader = ['timestamp', 'title', 'type', 'importance', 'status']
      //   const filterVal = ['timestamp', 'title', 'type', 'importance', 'status']
      //   const data = this.formatJson(filterVal, this.list)
      //   excel.export_json_to_excel({
      //     header: tHeader,
      //     data,
      //     filename: 'table-list'
      //   })
      //   this.downloadLoading = false
      // })
    },
    formatJson(filterVal, jsonData) {
      return jsonData.map(v =>
        filterVal.map(j => {
          if (j === 'timestamp') {
            // return parseTime(v[j])
          } else {
            return v[j]
          }
        })
      )
    }
  }
}
</script>
<style lang="stylus" scoped>
.table
  margin 20px 0

.cover
  height 50px
</style>
