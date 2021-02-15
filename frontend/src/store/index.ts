import Vue from 'vue';
import Vuex, { ActionContext } from 'vuex';
import { MainState, IPost } from '@/interfaces';
import { getStoreAccessors } from "typesafe-vuex";

Vue.use(Vuex);

type MainContext = ActionContext<MainState, MainState>

const State: MainState = {
  token: '',
  isLoggedIn: false,
  currentUser:  null,
  posts: ['kek', 'cheburek'],
}

export const options = {
  state: State,
  getters: {
    getPost: (state: MainState) => state.posts,
  },

  mutations: {
    addPost(state: MainState, post: string) {
      state.posts.push(post);
    }
  },

  actions: {
    async actionAddPost(context: MainContext, post: IPost) {
      context.commit('addPost', post);
    }
  },

};

export const store = new Vuex.Store<MainState>(options);

const { commit, read, dispatch } = 
  getStoreAccessors<MainState, MainState>(''); 

export const readPosts = read(options.getters.getPost);
export const dispatchAddPost = dispatch(options.actions.actionAddPost);
export const commitAppendPost = commit(options.mutations.addPost);
