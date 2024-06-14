import axios from 'axios';
import { getAuthHeaders, getCookie, getUserIDFromJWT } from './utils';
import { getUserRole } from '$lib/users_api';

const API_POSTS_URL = import.meta.env.VITE_API_POSTS_URL;

export interface Post {
	id: number;
	title: string;
	content: string;
	author: string;
	created_at: string;
}

export interface CreatePostData {
	title: string;
	content: string;
}

export const fetchPosts = async (): Promise<Post[]> => {
	const response = await axios.get<Post[]>(`${API_POSTS_URL}/`, getAuthHeaders());
	return response.data;
};

export const createPost = async (data: CreatePostData): Promise<Post> => {
	const response = await axios.post<Post>(`${API_POSTS_URL}/`, data, getAuthHeaders());
	return response.data;
};