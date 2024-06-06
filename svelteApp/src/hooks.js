// @ts-nocheck
// noinspection JSUnusedGlobalSymbols

import { redirect } from '@sveltejs/kit';
import { isAuthenticated } from '$lib/auth_api';
import { accessToken } from '$lib/stores';

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
	const { url } = event;
	let access_token = event.cookies.get('access');
	accessToken.set(access_token);
	const unprotectedRoutes = ['/', '/login', '/register'];

	if (!unprotectedRoutes.includes(url.pathname)) {
		if (!isAuthenticated(access_token)) {
			console.log('User is not authenticated, redirecting to /login');
			throw redirect(302, '/login');
		}
	}

	return await resolve(event);
}
