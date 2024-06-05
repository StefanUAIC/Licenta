import axios from 'axios';
import { getCookie } from '$lib/utils';

const API_AUTH_URL = import.meta.env.VITE_API_AUTH_URL;

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

export const login = async (username: string, password: string): Promise<TokenSchema> => {
	try {
		const response = await axios.post<TokenSchema>(`${API_AUTH_URL}/login`, { username, password });
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
		const response = await axios.post<TokenSchema>(`${API_AUTH_URL}/register`, user);
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


export function isAuthenticated(request: Request | null = null): boolean {
	let cookies = '';

	if (request) {
		// Server-side: read cookies from request headers
		cookies = request.headers.get('cookie') || '';
	}

	// Use getCookie function with the correct cookies context
	const accessToken = getCookie('access_token', cookies);
	if (!accessToken) return false;

	try {
		const payload = JSON.parse(atob(accessToken.split('.')[1]));
		const currentTime = Date.now() / 1000;
		return payload.exp > currentTime;
	} catch (e) {
		return false;
	}
}