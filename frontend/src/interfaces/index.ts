export interface MainState {
  token: string;
  isLoggedIn: boolean;
  currentUser: ICurrentUser | null;
  posts: Array<IPost>;
}

export interface ICurrentUser {
  id: number;
  name: string;
  last_login: string;
  last_active: string;
  posts: Array<IPost>;
}

export interface IUserCreate {
  username: string;
  password: string;
}

export interface IPost {
  id: number;
  title: string;
  owner_id: number;
  post_likes: Array<ILike>;
}

export interface IPostCreate {
  title: string;
  owner_id: number;
}

interface ILike {
  id: number;
  post_id: number;
  user_id: number;
  when_liked: string;
}
