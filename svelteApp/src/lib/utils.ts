export function getCookie(name: string): string | null {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()!.split(';').shift()!;
    return null;
}

export function getAuthHeaders() {
    const accessToken = getCookie('access');
    if (!accessToken) {
        throw new Error('No access token found');
    }
    return {
        headers: {
            Authorization: `Bearer ${accessToken}`,
        },
    };
}