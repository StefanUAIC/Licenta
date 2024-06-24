// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck
// noinspection JSUnusedGlobalSymbols

import { redirect } from '@sveltejs/kit';
import { isAuthenticated } from '$lib/utils';
import { refreshAccessToken } from '$lib/auth_api';

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
	const { url } = event;
	let access_token = event.cookies.get('access');
	const unprotectedRoutes = ['/', '/login', '/register'];
	if (!unprotectedRoutes.includes(url.pathname)) {
		if (!isAuthenticated(access_token)) {
			let refresh_token = event.cookies.get('refresh');
			if (refresh_token) {
				try {
					access_token = await refreshAccessToken(refresh_token);
					event.cookies.set('access', access_token.access, {
						httpOnly: false,
						maxAge: 3600,
						sameSite: 'strict',
						path: '/'
					});
				} catch (e) {
					console.log('Error refreshing access token:', e);
					throw redirect(302, '/login');
				}
			} else {
				console.log('User is not authenticated, redirecting to /login');
				throw redirect(302, '/login');
			}
		}
	}

	return await resolve(event);
}
