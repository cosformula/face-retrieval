<template lang="pug">
  div.app-container
    el-form(ref="form" :model="form" :rules="rules" label-width="120px" label-position="left" size="medium")
      el-form-item(required label="图片库" prop="libID")
        el-select(@change="updateDistances" v-model="form.libID" placeholder="请选择图片库" style="width: 100%;")
          el-option(v-for="lib in libraries" :label="lib.name" :key="lib.id" :value="lib.id")
      el-form-item(required label="特征距离" prop="distance")
        el-select(v-model="form.distance" placeholder="请特征距离" style="width: 100%;" )
          el-option(v-for="dis in distances" :label="dis.name" :value="dis.id" :key="dis.id")
      el-form-item(required label="选择策略" prop="strategy")
        el-select(v-model="form.strategy" placeholder="请选择策略" style="width: 100%;")
          el-option(v-for="strategy in strategies" :label="strategy.label" :value="strategy.value" :key="strategy.label")
      el-form-item(required label="供选人像数" prop="maxIterationFaces")
        el-select(v-model="form.maxIterationFaces" placeholder="请选择人像数" style="width: 100%;")
          el-option(v-for="option in facesOptions" :label="option.label" :value="option.value" :key="option.label")
      el-form-item(required label="反馈次数上限" prop="maxIteration")
        el-input-number(v-model="form.maxIteration" :min="1" :max="10" label="描述文字" style="width: 100%;")
      el-form-item(label="备注" prop="remark")
        el-input(type="textarea" v-model="form.remark")
      el-form-item
        el-button(type="primary" @click="submitForm('form')" :loading="loading") 立即创建
        el-button(@click="resetForm('form')") 重置
</template>

<script>
import { fetchLibraries, fetchDistances, createRetrieval } from '@/api'
export default {
  data() {
    return {
      loading: false,
      libraries: [],
      distances: [],
      facesOptions: [
        { label: 8, value: 8 },
        { label: 12, value: 12 },
        { label: 18, value: 18 },
        { label: 24, value: 24 }
      ],
      strategies: [
        { label: '随机', value: 'random' },
        { label: '最相似', value: 'similarity' },
        { label: '墒算法', value: 'entropy' }
      ],
      form: {
        libID: '',
        distance: '',
        strategy: 'random',
        maxIterationFaces: 8,
        maxIteration: 8,
        remark: ''
      },
      rules: {
        libID: [{ required: true, message: '请选择图片库', trigger: 'change' }],
        distance: [
          { required: true, message: '请选择特征距离', trigger: 'change' }
        ],
        maxIterationFaces: [
          {
            type: 'number',
            required: true,
            message: '请输入供选人像数',
            trigger: 'change'
          }
        ]
      }
    }
  },
  mounted() {
    // console.log('mounted', fetchLibraries())
    fetchLibraries({ limit: 1000 }).then(resp => {
      this.libraries = resp.data.items
    })
  },
  methods: {
    submitForm(formName) {
      this.loading = true
      this.$refs[formName].validate(valid => {
        if (valid) {
          createRetrieval(
            this.form.libID,
            this.form.distance,
            this.form.maxIterationFaces,
            this.form.maxIteration,
            this.form.strategy,
            this.form.remark
          ).then(resp => {
            const retrievalID = resp.data.id
            this.$router.push(`/retrieval/${retrievalID}/start`)
            console.log(resp.data)
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    updateDistances() {
      fetchDistances(this.form.libID).then(resp => {
        this.distances = resp.data.items
      })
    }
  }
}
</script>

<style scoped>
.line {
  text-align: center;
}
.app-container {
  max-width: 600px;
  /* width: 30vw; */
}
</style>

