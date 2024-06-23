import { getAuthHeaders } from '$lib/utils';
import axios from 'axios';

const API_ISSUES_URL = import.meta.env.VITE_API_ISSUES_URL;

export interface IssueSchema {
	title: string;
	description: string;
}

export interface IssueResponse {
	id: number;
	title: string;
	description: string;
	created_at: string;
}

export const reportIssue = async (payload: IssueSchema): Promise<IssueResponse> => {
	const response = await axios.post<IssueResponse>(`${API_ISSUES_URL}/`, payload, getAuthHeaders());
	return response.data;
};