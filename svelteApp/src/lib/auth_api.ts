import axios from 'axios';
import { getAuthHeaders } from '$lib/utils';

const API_USERS_URL = import.meta.env.VITE_API_USERS_URL;

interface UserSchema {
	username: string;
	password: string;
	role: string;
	email: string;
	first_name: string;
	last_name: string;
}

interface TokenSchema {
	access: string;
	refresh: string;
	user_id: number;
	username: string;
	role: string;
}

interface AccessTokenSchema {
	access: string;
}

export interface RoleResponse {
	role: 'student' | 'teacher';
}

interface ChangePasswordData {
	old_password: string;
	new_password: string;
}

export const login = async (username: string, password: string): Promise<TokenSchema> => {
	try {
		const response = await axios.post<TokenSchema>(`${API_USERS_URL}/login`, { username, password });
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

export const register = async (user: UserSchema): Promise<TokenSchema> => {
	try {
		const response = await axios.post<TokenSchema>(`${API_USERS_URL}/register`, user);
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

export const refreshAccessToken = async (refreshToken: string): Promise<AccessTokenSchema> => {
	try {
		const response = await axios.post<AccessTokenSchema>(`${API_USERS_URL}/refresh`, { refresh: refreshToken });
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

export const changePassword = async (userId: number, passwordData: ChangePasswordData): Promise<void> => {
	try {
		await axios.post(`${API_USERS_URL}/${userId}/change-password`, passwordData, getAuthHeaders());
	} catch (error) {
		if (axios.isAxiosError(error) && error.response) {
			console.log(error.response.data.errors);
			throw error.response.data.errors;
		} else {
			throw new Error('An unexpected error occurred');
		}
	}
};