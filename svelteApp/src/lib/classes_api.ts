// src/lib/classes_api.ts
import axios from 'axios';
import { getAuthHeaders } from '$lib/utils';

const API_CLASSES_URL = import.meta.env.VITE_API_CLASSES_URL;

export interface CreateClassPayload {
	name: string;
}

export interface JoinClassPayload {
	join_code: string;
}

export interface ClassResponse {
	id: number;
	name: string;
	teacher_id: number;
}

export interface ClassInfoResponse {
	id: number;
	name: string;
	teacher_id: number;
	created_at: string;
	updated_at: string;
	join_code: string;
}

export const createClass = async (payload: CreateClassPayload): Promise<ClassResponse> => {
	try {
		const response = await axios.post<ClassResponse>(`${API_CLASSES_URL}/create`, payload, getAuthHeaders());
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

export const joinClass = async (payload: JoinClassPayload): Promise<ClassResponse> => {
	try {
		const response = await axios.post<ClassResponse>(`${API_CLASSES_URL}/join`, payload, getAuthHeaders());
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

export const getClassInfo = async (classId: number): Promise<ClassInfoResponse> => {
	try {
		const response = await axios.get<ClassInfoResponse>(`${API_CLASSES_URL}/${classId}`, getAuthHeaders());
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