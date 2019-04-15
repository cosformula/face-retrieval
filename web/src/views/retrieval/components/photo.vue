<template lang="pug">
  el-card(v-loading="loading"
    shadow="none"
    :body-style="{ padding:0,height:'100%', width: '100%', display:'flex', flexDirection:'column' }"
    style="margin: auto;text-align:center;cursor:pointer;border-radius:0;width:auto;border:none;position:relative;display:flex;align-items:center;")
    //- div(style="padding-bottom:5px;") {{photoName}}
    img(v-if="photo.url" :src="photo.url" class="image" @load="loading=false")
    div(v-else) 暂无图片
    div
      | {{(photo.status.prob * 100).toFixed(2)}}%
      | {{(photo.status.lastProb * 100).toFixed(2)}}%
      | {{ ((photo.status.prob - photo.status.lastProb)*100).toFixed(5) }}%
</template>
<script>
export default {
  props: {
    photo: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      loading: true
    }
  },
  watch: {
    photo: function(oldVal, newVal) {
      this.loading = true
    }
  }
}
</script>
<style scoped>
.image {
  object-fit: contain;
  height: 80%;
  left: 0;
  right: 0;
  top: 0;
  right: 0;
  margin: auto;
  /* height:80%; */
  /* width:100%; */
  /* margin: auto; */
  /* width: auto; */
  /* height: auto; */
  /* flex: 1; */
  display: block;
}
@media (max-width: 700px) {
  .image {
    height: 50%;
  }
}
</style>
