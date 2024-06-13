<script lang="ts">
	import { onMount } from 'svelte';
	import UserPosts from '../../components/UserPosts.svelte';
	import Waves_2 from '../../components/Waves_2.svelte';
	import { getCookie, getUserIDFromJWT } from '$lib/utils';
	import { getUserRole } from '$lib/users_api';
	import { writable } from 'svelte/store';
	import { AppShell } from '@skeletonlabs/skeleton';

	let userIsTeacher = false;
	let isTeacher = writable(false);

	onMount(async () => {
		const token = getCookie('access');
		const userId = getUserIDFromJWT(token);
		const UserRole = await getUserRole(userId);
		userIsTeacher = UserRole.role === 'teacher';
		isTeacher.set(userIsTeacher);
	});
</script>

<style>
    .waves-container {
        position: relative;
        width: 100%;
        background-color: #4f46e5;
    }

    .container {
        max-width: 800px;
        margin: 0 auto;
    }
</style>

<AppShell>
	<div class="waves-container">
		<Waves_2 />
		<div class="container mx-auto pb-8">
			<h2 class="text-3xl font-bold mb-12 text-white">Users posts</h2>
			<UserPosts {userIsTeacher} />
		</div>
	</div>
</AppShell>
