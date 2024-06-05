// @ts-nocheck
// noinspection JSUnusedGlobalSymbols

import { redirect } from '@sveltejs/kit';
import { isAuthenticated } from '$lib/auth_api'; // Adjust this import path as needed

export async function handle({ event, resolve }) {
  const { url } = event;

  const unprotectedRoutes = ['/', '/login', '/register'];

  if (!unprotectedRoutes.includes(url.pathname)) {
    if (!isAuthenticated()) {
      console.log('User is not authenticated, redirecting to /login');
      throw redirect(302, '/login');
    }
  }

  return await resolve(event);
}
