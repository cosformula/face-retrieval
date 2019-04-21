<template lang="pug">
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
</template>
<script>
export default {

}
</script>
<style scoped>

</style>
