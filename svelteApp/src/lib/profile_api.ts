import axios from 'axios';
import {getAuthHeaders} from '$lib/utils';

const API_AUTH_URL = import.meta.env.VITE_API_AUTH_URL;

export interface ProfileSchema {
    username: string;
    role: string;
    email: string;
    first_name: string;
    last_name: string;
}

export const getProfile = async (user_id: number): Promise<ProfileSchema> => {
    try {
        console.log(API_AUTH_URL, user_id)
        const response = await axios.get<ProfileSchema>(`${API_AUTH_URL}/${user_id}`, getAuthHeaders());
        console.log('response.data', response.data);
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

export const getUserIDFromJWT = (accessToken: string | null): number => {
    if (!accessToken) {
        console.log('No access token found');
        return 0;
    } else {
        const payload = JSON.parse(atob(accessToken.split('.')[1]));
        return payload.user_id;
    }
};