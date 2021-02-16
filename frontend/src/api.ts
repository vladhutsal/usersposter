import axios from 'axios';
import { IPostCreate, IUserCreate } from '@/interfaces';

const API_URL = 'localhost/api';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

const api = {
  async logInGetToken(payload: IUserCreate) {
    const params = new URLSearchParams();
    params.append('username', payload.username);
    params.append('password', payload.password);
    return axios.post(`${API_URL}/api/login/access-token`, params);
  },
  async createPost(payload: IPostCreate, token: string) {
    return axios.post(`${API_URL}/post/create`, payload, authHeaders(token));
  },
  async signUp(payload: IUserCreate) {
    return axios.post(`${API_URL}/users/signup`, {
      username: payload.username,
      password: payload.password,
    });
  },
}

export default api;
