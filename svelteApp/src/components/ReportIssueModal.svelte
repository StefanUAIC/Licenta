<script lang="ts">
	import { reportIssue } from '$lib/issues_api';
	import { writable } from 'svelte/store';

	export let isOpen = false;
	export let onClose: () => void;

	let title = '';
	let description = '';
	let titleError = writable('');
	let descriptionError = writable('');

	const validate = () => {
		let isValid = true;
		if (title.length < 3) {
			titleError.set('Title must be at least 3 characters long.');
			isValid = false;
		} else {
			titleError.set('');
		}

		if (description.length < 5) {
			descriptionError.set('Description must be at least 5 characters long.');
			isValid = false;
		} else {
			descriptionError.set('');
		}

		return isValid;
	};

	const handleSubmit = async () => {
		if (!validate()) {
			return;
		}
		try {
			await reportIssue({ title, description });
			alert('You have successfully sent the issue to the admin.');
			title = '';
			description = '';
			onClose();
		} catch (error) {
			console.error('Error submitting issue:', error);
			alert('There was an error submitting your issue. Please try again.');
		}
	};
</script>

<div class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50 z-50" class:hidden={!isOpen}>
	<div class="relative bg-white rounded-lg shadow-lg p-6 w-full max-w-md mx-auto max-h-full overflow-y-auto"
		 class:hidden={!isOpen}>
		<div class="flex justify-between items-center mb-4">
			<h2 class="text-xl font-bold">Report an Issue</h2>
			<button class="text-white bg-red-500 hover:bg-red-700 rounded-full w-8 h-8 flex items-center justify-center"
					on:click={onClose}>
				✖
			</button>
		</div>
		<div class="mb-4">
			<label for="title" class="block text-sm font-medium text-gray-700">Title</label>
			<input type="text" id="title" bind:value={title}
				   class="px-1 py-1 mt-1 block w-full rounded-md border border-gray-300 shadow-sm">
			{#if $titleError}
				<p class="text-red-500 text-sm">{$titleError}</p>
			{/if}
		</div>
		<div class="mb-4">
			<label for="description" class="block text-sm font-medium text-gray-700">Description</label>
			<textarea id="description" bind:value={description}
					  class="px-1 py-1 mt-1 block w-full rounded-md border border-gray-300 shadow-sm"></textarea>
			{#if $descriptionError}
				<p class="text-red-500 text-sm">{$descriptionError}</p>
			{/if}
		</div>
		<button on:click={handleSubmit}
				class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded justify-center">
			Send
		</button>
	</div>
</div>

<style>
    .hidden {
        display: none;
    }
</style>
