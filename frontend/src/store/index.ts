import Vue from 'vue';
import Vuex, { ActionContext } from 'vuex';
import { getStoreAccessors } from "typesafe-vuex";

import { getLocalToken, removeLocalToken, saveLocalToken } from '@/utils';
import { MainState, IPost, IPostCreate, IUserCreate, ICurrentUser } from '@/interfaces';
import api from '@/api';

Vue.use(Vuex);

type MainContext = ActionContext<MainState, MainState>

const State: MainState = {
  token: '',
  isLoggedIn: false,
  currentUser:  null,
  posts: [],
}

export const options = {
  state: State,
  getters: {
    getPosts: (state: MainState) => state.posts,
  },

  mutations: {
    addPost(state: MainState, post: IPost) {
      state.posts.push(post);
    },
    setLogIn(state: MainState, payload: { token: string, user: ICurrentUser }) {
      state.token = payload.token;
      state.isLoggedIn = true;
      state.currentUser = payload.user;
    },
  },

  actions: {
    async actionAddPost(context: MainContext, payload: IPostCreate) {
      const response = await api.createPost(payload, context.rootState.token);
      commitAddPost(context, response.data);
    },
    async actionSignUp(context: MainContext, payload: IUserCreate) {
      try {
        const signUpResponse = await api.signUp(payload);
        const signUpData = signUpResponse.data;
        const tokenResponse = await api.logInGetToken(payload);
        const token = tokenResponse.data.access_token;
        if (token) {
          saveLocalToken(token);
          const user: ICurrentUser = {
            id: signUpData.id,
            name: signUpData.username,
            last_login: signUpData.last_login,
            last_active: signUpData.last_active,
            posts: signUpData.posts,
          };
          commitLogIn(context, { token, user } );
        }
      } catch (e) {
        console.log(e)
      }
    }
  },

};

export const store = new Vuex.Store<MainState>(options);

const { commit, read, dispatch } = getStoreAccessors<MainState, MainState>(''); 

export const readPosts = read(options.getters.getPosts);

export const dispatchAddPost = dispatch(options.actions.actionAddPost);

export const commitAddPost = commit(options.mutations.addPost);
export const commitLogIn = commit(options.mutations.setLogIn);
