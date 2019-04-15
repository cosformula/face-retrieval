<template lang="pug">
  el-card(shadow="hover" style="height:200px;")
    div(slot="header" class="clearfix") 历史
    div(style="white-space:nowrap;overflow:scroll;height:100%;")
      photo-card(v-for="photo in selectedHistory"
        :key="photo.name"
        :photo="photo"
        style="display:inline-block;width:100px;height:100px;")
</template>
<script>
import photoCard from './photo'

export default {
  components: { photoCard },
  props: {
    selectedHistory: {
      type: Array,
      default: () => []
    },
    libraryName: {
      type: String,
      default: ''
    }
  },
  data() {
    return {}
  }
}
</script>

