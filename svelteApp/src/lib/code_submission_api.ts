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
	compile_output: string;
	runtime_error: string;
	message: string;
}

export interface CodeSubmissionSchema {
	source_code: string;
	language_id: number;
	problem_id: number;
}

export const submitCode = async (submission: CodeSubmissionSchema): Promise<CodeSubmissionResult[]> => {
	try {
		console.log('submission', submission);
		console.log(API_CODE_SUBMISSION_URL);
		const response = await axios.post<{ results: CodeSubmissionResult[] }>(
			`${API_CODE_SUBMISSION_URL}/submit_code`,
			submission,
			getAuthHeaders()
		);
		console.log('response.data', response.data.results)
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
