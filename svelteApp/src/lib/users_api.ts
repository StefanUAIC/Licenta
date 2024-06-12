import axios from 'axios';
import { getAuthHeaders } from '$lib/utils';
import type { RoleResponse } from '$lib/auth_api';
import type { ClassResponse } from '$lib/classes_api';

const API_USERS_URL = import.meta.env.VITE_API_USERS_URL;

export interface ProfileSchema {
	username: string;
	role: string;
	email: string;
	first_name: string;
	last_name: string;
}

export const getProfile = async (user_id: number): Promise<ProfileSchema> => {
	try {
		const response = await axios.get<ProfileSchema>(`${API_USERS_URL}/${user_id}`, getAuthHeaders());
		return response.data;
	} catch (error) {
		if (axios.isAxiosError(error) && error.response) {
			console.log(error.response.data.errors);
			throw error.response.data.errors;
		} else {
			throw new Error('An unexpected error occurred');
		}
	}
};

export const getUserRole = async (user_id: number): Promise<RoleResponse> => {
	try {
		const response = await axios.get<RoleResponse>(`${API_USERS_URL}/${user_id}/role`, getAuthHeaders());
		return response.data;
	} catch (error) {
		if (axios.isAxiosError(error) && error.response) {
			console.log(error.response.data.errors);
			throw error.response.data.errors;
		} else {
			throw new Error('An unexpected error occurred');
		}
	}
};

export const getUserClasses = async (userId: number): Promise<ClassResponse[]> => {
	try {
		const response = await axios.get<ClassResponse[]>(`${API_USERS_URL}/${userId}/classes`, getAuthHeaders());
		return response.data;
	} catch (error) {
		if (axios.isAxiosError(error) && error.response) {
			console.log(error.response.data.error);
			throw new Error(error.response.data.error);
		} else {
			throw new Error('An unexpected error occurred');
		}
	}
};