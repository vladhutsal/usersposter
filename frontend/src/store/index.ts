import Vue from 'vue';
import Vuex, { ActionContext } from 'vuex';
import { MainState, IPost } from '@/interfaces';
import { getStoreAccessors } from "typesafe-vuex";

Vue.use(Vuex);

const State: MainState = {
  token: '',
  isLoggedIn: false,
  currentUser:  null,
  posts: [],
}

export default new Vuex.Store({
  state: State,
  getters: {
    
  },

  mutations: {
    addPost(state, post: IPost) {
      state.posts.push(post);
    }
  },

  actions: {
    addPost(context, post: IPost) {
      context.commit('addPost', post);
    }
  },

});
