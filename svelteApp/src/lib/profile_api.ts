import axios from 'axios';
import { getAuthHeaders } from '$lib/utils';

const API_AUTH_URL = import.meta.env.VITE_API_AUTH_URL;

interface ProfileSchema{
    username: string;
    role: string;
    email: string;
    first_name: string;
    last_name: string;
}

export const getProfile = async (user_id: number): Promise<ProfileSchema> => {
    try {
        const response = await axios.get<ProfileSchema>(`${API_AUTH_URL}/${user_id}`, getAuthHeaders());
        console.log('response.data', response.data)
        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            console.log(error.response.data.errors);
            throw error.response.data.errors;
        } else {
            throw new Error('An unexpected error occurred');
        }
    }
}

