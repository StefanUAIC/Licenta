<script lang="ts">
	import { onMount } from 'svelte';
	import { getUserClasses, getUserRole } from '$lib/users_api';
	import { getCookie, getUserIDFromJWT } from '$lib/utils';
	import type { ClassResponse, CreateClassPayload, JoinClassPayload } from '$lib/classes_api';
	import { createClass, joinClass } from '$lib/classes_api';
	import { goto } from '$app/navigation';

	let role: 'student' | 'teacher' | null = null;
	let error: string | null = null;
	let accessToken: string | null = null;
	let userClasses: ClassResponse[] = [];

	onMount(async () => {
		accessToken = getCookie('access');

		if (!accessToken) {
			error = 'User is not authenticated';
			return;
		}

		try {
			const user_id = getUserIDFromJWT(accessToken);
			const roleResponse = await getUserRole(user_id);
			role = roleResponse.role;

			userClasses = await getUserClasses(user_id);
			console.log(userClasses);
			console.log(userClasses[0].name);

			console.log('User role:', role);
			console.log('User classes:', userClasses);
		} catch (err) {
			error = 'Failed to fetch user role or classes';
			console.error(err);
		}
	});

	const handleJoinClass = async () => {
		try {
			const joinCode = prompt('Enter the join code:');
			if (!joinCode) return;

			const payload: JoinClassPayload = { join_code: joinCode };
			const classResponse = await joinClass(payload);
			alert(`Joined class: ${classResponse.name}`);
			await goto(`/classes/${classResponse.id}`);
		} catch (err) {
			error = err.message;
			console.error(err);
		}
	};

	const handleCreateClass = async () => {
		try {
			const className = prompt('Enter the class name:');
			if (!className) return;

			const payload: CreateClassPayload = { name: className };
			const classResponse = await createClass(payload);
			alert(`Created class: ${classResponse.name}`);
			await goto(`/classes/${classResponse.id}`);
		} catch (err) {
			error = err.message;
			console.error(err);
		}
	};

	const goToClass = (classId: number) => {
		goto(`/classes/${classId}`);
	};
</script>

<template>
	<div class="min-h-screen flex flex-col items-center justify-center bg-gray-100 py-6">
		<div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
			<h1 class="text-3xl font-bold text-center mb-4">Classes Page</h1>
			{#if error}
				<p class="text-red-500 text-center">{error}</p>
			{:else if role}
				<div class="text-center mb-6">
					<h2 class="text-2xl font-semibold">Welcome!</h2>
					<p class="text-lg mb-4">You are logged in as a {role}</p>
					{#if role === 'student'}
						<button on:click={handleJoinClass}
								class="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600">
							Join a class
						</button>
					{:else if role === 'teacher'}
						<button on:click={handleCreateClass}
								class="w-full bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600">
							Create a class
						</button>
					{/if}
				</div>
				<div class="mb-6">
					<h3 class="text-xl font-semibold mb-2">Your Classes</h3>
					<ul>
						{#each userClasses as classItem}
							<li class="mb-2">
								<button on:click={() => goToClass(classItem.id)}
										class="w-full bg-gray-200 text-gray-800 py-2 px-4 rounded hover:bg-gray-300">
									{classItem.name}
								</button>
							</li>
						{/each}
					</ul>
				</div>
			{:else}
				<p class="text-center">Loading...</p>
			{/if}
		</div>
	</div>
</template>

<style>
    .error {
        color: red;
    }
</style>
