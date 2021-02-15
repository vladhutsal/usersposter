<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <p>{{ posts }}</p>
    
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { readPosts } from '@/store';

@Component({})
export default class Home extends Vue {
  public newPost: string = '';

  get posts() {
    return readPosts(this.$store)
  }
}
</script>
