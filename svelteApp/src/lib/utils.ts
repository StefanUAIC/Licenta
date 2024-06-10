export function getCookie(name: string, cookies: string = ''): string | null {
	if (!cookies && typeof document !== 'undefined') {
		cookies = document.cookie;
	}

	const value = `; ${cookies}`;
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
			Authorization: `Bearer ${accessToken}`
		}
	};
}