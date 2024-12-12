export interface Post {
  id: string;
  title: string;
  slug: string;
  content: string;
  excerpt: string;
  author: User;
  categories: Category[];
  tags: Tag[];
  createdAt: string;
  updatedAt: string;
  likes: number;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  postCount: number;
  color: string;
}

export interface Tag {
  id: string;
  name: string;
  slug: string;
  postCount: number;
  color: string;
}

export interface User {
  id: string;
  username: string;
  email: string;
  name: string;
  bio?: string;
  avatar?: string;
  isAdmin: boolean;
}

export interface AuthResponse {
  token: string;
  user: User;
} 