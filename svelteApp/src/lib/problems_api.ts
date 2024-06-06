import axios from 'axios';
import { getAuthHeaders } from '$lib/utils';

const API_PROBLEMS_URL = import.meta.env.VITE_API_PROBLEMS_URL;

export interface ProblemSchema {
	id: number;
	title: string;
	description: string;
	difficulty: string;
	example_input: string;
	example_output: string;
	created_at: string;
	updated_at: string;
	created_by: string;
	grade: number;
	category: string;
}

export interface TestCase {
    id: number;
    problem_id: number;
    stdin: string;
    expected_output: string;
    actualOutput?: string;
    status?: string;
    passed?: boolean;
}

export const getAllProblems = async (): Promise<ProblemSchema[]> => {
	try {
		const response = await axios.get<ProblemSchema[]>(API_PROBLEMS_URL, getAuthHeaders());
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

export const getProblemById = async (problemId: number): Promise<ProblemSchema> => {
	try {
		const response = await axios.get<ProblemSchema>(`${API_PROBLEMS_URL}/${problemId}`, getAuthHeaders());
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

export const createProblem = async (problem: ProblemSchema): Promise<ProblemSchema> => {
	try {
		const response = await axios.post<ProblemSchema>(`${API_PROBLEMS_URL}/`, problem, getAuthHeaders());
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

export const createTestCase = async (problemId: number, testCase: { stdin: string; expected_output: string }): Promise<TestCase> => {
	try {
		const response = await axios.post<TestCase>(`${API_PROBLEMS_URL}/${problemId}/test_cases/`, testCase, getAuthHeaders());
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

export const getTestCasesByProblemId = async (problemId: number): Promise<TestCase[]> => {
	try {
		const response = await axios.get<TestCase[]>(`${API_PROBLEMS_URL}/${problemId}/test_cases`, getAuthHeaders());
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
