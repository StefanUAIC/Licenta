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

export function isAuthenticated(accessToken: string | null): boolean {
	if (!accessToken) return false;

	try {
		const payload = JSON.parse(atob(accessToken.split('.')[1]));
		const currentTime = Date.now() / 1000;
		return payload.exp > currentTime;
	} catch (e) {
		return false;
	}
}

export const getUserIDFromJWT = (accessToken: string | null): number => {
	if (!accessToken) {
		console.log('No access token found');
		return 0;
	} else {
		const payload = JSON.parse(atob(accessToken.split('.')[1]));
		return payload.user_id;
	}
};
