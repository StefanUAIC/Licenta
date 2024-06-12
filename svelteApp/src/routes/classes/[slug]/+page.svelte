<script lang="ts">
	import { onMount } from 'svelte';
	import { type ClassInfoResponse, getClassInfo } from '$lib/classes_api';
	import { getCookie } from '$lib/utils';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { get } from 'svelte/store';
	import { format } from 'date-fns';

	let classId: number;
	let classInfo: ClassInfoResponse | null = null;
	let error: string | null = null;
	let accessToken: string | null = null;

	onMount(async () => {
		const urlParams = get(page).params;
		classId = Number(urlParams.slug);

		accessToken = getCookie('access');

		if (!accessToken) {
			error = 'User is not authenticated';
			return;
		}

		try {
			classInfo = await getClassInfo(classId);
			console.log('Class info:', classInfo);
		} catch (err) {
			error = err.message;
			console.error(err);
		}
	});

	const goBack = () => {
		goto('/classes');
	};

	const copyToClipboard = async (text: string) => {
		try {
			await navigator.clipboard.writeText(text);
			alert('Join code copied to clipboard!');
		} catch (err) {
			console.error('Failed to copy join code: ', err);
		}
	};

	const formatDate = (dateString: string) => {
		return format(new Date(dateString), 'MMMM d, yyyy h:mm a');
	};
</script>

<template>
	<div class="min-h-screen flex flex-col items-center justify-center bg-gray-100 py-12">
		<div class="bg-white p-10 rounded-lg shadow-lg w-full max-w-2xl relative">
			{#if error}
				<p class="text-red-500 text-center text-xl">{error}</p>
			{:else if classInfo}
				<h1 class="text-4xl font-bold text-center mb-6">{classInfo.name}</h1>
				<div class="absolute top-4 right-4 text-gray-600">
					<p><strong>Teacher ID:</strong> {classInfo.teacher_id}</p>
				</div>
				<div class="mb-8 text-lg">
					<p class="mb-4"><strong>Created At:</strong> {formatDate(classInfo.created_at)}</p>
					<p class="flex items-center">
						<strong>Join Code:</strong>
						<button on:click={() => copyToClipboard(classInfo.join_code)} class="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 ml-2">
							Copy
						</button>
					</p>
				</div>
				<button on:click={goBack} class="w-full bg-gray-300 text-gray-800 py-3 px-4 rounded hover:bg-gray-400 text-lg">
					Go Back
				</button>
			{:else}
				<p class="text-center text-xl">Loading...</p>
			{/if}
		</div>
	</div>
</template>

<style>
    .error {
        color: red;
    }
</style>
