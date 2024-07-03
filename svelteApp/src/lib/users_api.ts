import axios from 'axios';
import { getAuthHeaders } from '$lib/utils';
import type { RoleResponse } from '$lib/auth_api';
import type { ClassResponse } from '$lib/classes_api';
import type { HomeworkDetail, Solution } from '$lib/homeworks_api';
import type { ProblemSchema } from '$lib/problems_api';

const API_USERS_URL = import.meta.env.VITE_API_USERS_URL;

export interface ProfileSchema {
	username: string;
	role: string;
	email: string;
	first_name: string;
	last_name: string;
	profile_picture: {
		type: string;
		data: string;
	} | null;
}

export interface UpdateProfileSchema {
	first_name: string;
	last_name: string;
	profile_picture?: string | null;
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


export const getUserCount = async (role: string): Promise<number> => {
	try {
		const response = await axios.get<number>(`${API_USERS_URL}/count/${role}`, getAuthHeaders());
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

export const getUserSolutions = async (user_id: number): Promise<Solution[]> => {
	try {
		const response = await axios.get<Solution[]>(`${API_USERS_URL}/${user_id}/solutions`, getAuthHeaders());
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

export const getAllUserHomeworks = async (user_id: number): Promise<HomeworkDetail[]> => {
    try {
        const response = await axios.get<HomeworkDetail[]>(`${API_USERS_URL}/${user_id}/homeworks`, getAuthHeaders());
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

export const getTeacherProblems = async (user_id: number): Promise<ProblemSchema[]> => {
	try {
		const response = await axios.get<ProblemSchema[]>(`${API_USERS_URL}/${user_id}/problems`, getAuthHeaders());
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

export const updateProfile = async (user_id: number, profileData: UpdateProfileSchema): Promise<ProfileSchema> => {
	try {
		console.log('profileData', profileData);
		console.log('profile picture', profileData.profile_picture);
		const response = await axios.put<ProfileSchema>(`${API_USERS_URL}/${user_id}/profile`, profileData, getAuthHeaders());
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