import axios from 'axios';
import { getAuthHeaders } from './utils';

const API_NOTIFICATIONS_URL = import.meta.env.VITE_API_NOTIFICATIONS_URL

export const fetchNotifications = async () => {
    const response = await axios.get(API_NOTIFICATIONS_URL, getAuthHeaders());
    return response.data;
};

export const markNotificationAsRead = async (notificationId: number) => {
    const response = await axios.post(`${API_NOTIFICATIONS_URL}/${notificationId}/read`, {}, getAuthHeaders());
    return response.data;
};

export const checkUnreadNotifications = async () => {
    const response = await axios.get(`${API_NOTIFICATIONS_URL}?unread=true`, getAuthHeaders());
    return response.data.length > 0;
}