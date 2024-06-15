import axios from 'axios';
import { getAuthHeaders } from '$lib/utils';

const API_HOMEWORKS_URL = import.meta.env.VITE_API_HOMEWORKS_URL;

export interface Homework {
	id: number;
	class_instance_id: number;
	problem_id: number;
	due_date: string;
}

export interface HomeworkDetail {
	id: number;
	class_instance_id: number;
	problem_id: number;
	due_date: string;
	class_instance_name: string;
	problem_title: string;
}

export interface CreateHomeworkPayload {
	problem_id: number;
	class_instance_id: number;
	due_date: string;
}

export interface Solution {
	id: number;
	problem_id: number;
	user_id: number;
	code: string;
	language_id: number;
	created_at: string;
	percentage_passed: number;
}

export const createHomework = async (payload: CreateHomeworkPayload): Promise<Homework> => {
	try {
		const response = await axios.post<Homework>(`${API_HOMEWORKS_URL}/`, payload, getAuthHeaders());
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

export const deleteHomework = async (homeworkId: number): Promise<void> => {
	try {
		await axios.delete(`${API_HOMEWORKS_URL}/${homeworkId}`, getAuthHeaders());
	} catch (error) {
		if (axios.isAxiosError(error) && error.response) {
			console.log(error.response.data.error);
			throw new Error(error.response.data.error);
		} else {
			throw new Error('An unexpected error occurred');
		}
	}
};

export const getHomework = async (homeworkId: number): Promise<HomeworkDetail> => {
	try {
		const response = await axios.get<HomeworkDetail>(`${API_HOMEWORKS_URL}/${homeworkId}`, getAuthHeaders());
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

export const getClassHomeworks = async (classId: number): Promise<Homework[]> => {
	try {
		const response = await axios.get<Homework[]>(`${API_HOMEWORKS_URL}/class/${classId}`, getAuthHeaders());
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

export const getUserHomeworks = async (userId: number, problemId: number): Promise<HomeworkDetail[]> => {
	try {
		const response = await axios.get<HomeworkDetail[]>(`${API_HOMEWORKS_URL}/user/${userId}/problem/${problemId}`, getAuthHeaders());
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


export const getHomeworkSubmissions = async (homeworkId: number): Promise<Solution[]> => {
	try {
		const response = await axios.get<Solution[]>(`${API_HOMEWORKS_URL}/${homeworkId}/submissions`, getAuthHeaders());
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