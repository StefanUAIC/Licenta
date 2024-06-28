import axios from 'axios';
import { getAuthHeaders } from '$lib/utils';

const API_CODE_SUBMISSION_URL = import.meta.env.VITE_API_SUBMISSIONS_URL;

export interface CodeSubmissionResult {
    test_case_id: number;
    input: string;
    expected_output: string;
    actual_output: string;
    status: string;
    passed: boolean;
    memory_exceeded: boolean;
    time_exceeded: boolean;
    compile_output?: string | null;
    stderr?: string | null;
    message?: string | null;
}

export interface CodeSubmissionSchema {
	source_code: string;
	language_id: number;
	problem_id: number;
	homework_id?: number | null;
}

export interface TestCaseVerifySchema {
	stdin: string;
	expected_output: string;
}

export interface VerifyCodeSubmissionSchema {
	source_code: string;
	language_id: number;
	test_cases: TestCaseVerifySchema[];
	memory_limit: number;
	time_limit: number;
}

export const submitCode = async (submission: CodeSubmissionSchema): Promise<CodeSubmissionResult[]> => {
	try {
		const response = await axios.post<{ results: CodeSubmissionResult[] }>(
			`${API_CODE_SUBMISSION_URL}/submit_code`,
			submission,
			getAuthHeaders()
		);
		console.log('response.data', response.data.results);
		return response.data.results;
	} catch (error) {
		if (axios.isAxiosError(error) && error.response) {
			console.error(error.response.data);
			throw error.response.data;
		} else {
			throw new Error('An unexpected error occurred');
		}
	}
};

export const fetchLanguages = async (): Promise<{ id: number; name: string }[]> => {
	try {
		const response = await axios.get(`${API_CODE_SUBMISSION_URL}/languages`, getAuthHeaders());
		return response.data;
	} catch (error) {
		if (axios.isAxiosError(error) && error.response) {
			console.error(error.response.data);
			throw error.response.data;
		} else {
			throw new Error('An unexpected error occurred');
		}
	}
};

export const verifyTestCases = async (submission: VerifyCodeSubmissionSchema): Promise<CodeSubmissionResult[]> => {
	try {
		const response = await axios.post<{ results: CodeSubmissionResult[] }>(
			`${API_CODE_SUBMISSION_URL}/verify_test_cases`,
			submission,
			getAuthHeaders()
		);
		return response.data.results;
	} catch (error) {
		if (axios.isAxiosError(error) && error.response) {
			console.error(error.response.data);
			throw error.response.data;
		} else {
			throw new Error('An unexpected error occurred');
		}
	}
};
