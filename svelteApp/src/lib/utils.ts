export function getCookie(name: string, cookies: string = ''): string | null {
	console.log('getcookie', cookies);
	console.log(typeof document != 'undefined');
	console.log(typeof document);
	console.log(!cookies);
	if (!cookies && typeof document !== 'undefined') {
		console.log('document.cookie', document.cookie);
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