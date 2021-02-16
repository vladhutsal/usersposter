<template>
<v-card class="ma-3 pa-3">
    <v-card-title primary-title>
      <div class="headline primary--text">Додати ачівку</div>
    </v-card-title>
    <v-card-text>
      <v-form
        @submit.prevent="submit"
      >
        <v-text-field 
          v-model="title" 
          label="Title" 
        >
        </v-text-field>
        <v-card-actions>
          <v-layout row align-center>
            <v-btn type="submit">Create post</v-btn>
          </v-layout>
        </v-card-actions>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { readPosts, dispatchAddPost } from '@/store';

@Component({})
export default class Posts extends Vue {
  public title: string = '';

  public async submit() {

    await dispatchAddPost(this.$store, {
      owner_id: this.$store.state.currentUser.id,
      title: this.title
    })
  }

  get posts() {
    return readPosts(this.$store)
  }
}
</script>
