import axios from 'axios';
import { getAuthHeaders } from './utils';

const API_POSTS_URL = import.meta.env.VITE_API_POSTS_URL;

export interface Post {
    id: number;
    title: string;
    content: string;
    author: string;
    created_at: string;
    author_id: number;
    likes_count: number;
    dislikes_count: number;
    is_liked: boolean;
    is_disliked: boolean;
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

export async function likePost(postId: number): Promise<Post> {
    const response = await axios.post<Post>(`${API_POSTS_URL}/${postId}/like`, {}, getAuthHeaders());
    return response.data;
}

export async function dislikePost(postId: number): Promise<Post> {
    const response = await axios.post<Post>(`${API_POSTS_URL}/${postId}/dislike`, {}, getAuthHeaders());
    return response.data;
}