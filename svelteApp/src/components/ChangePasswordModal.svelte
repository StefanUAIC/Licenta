<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { changePassword } from '$lib/auth_api';
	import { getCookie, getUserIDFromJWT } from '$lib/utils';
	import EyeIcon from './EyeIcon.svelte';
	import ClosedEyeIcon from './ClosedEyeIcon.svelte';

	export let showModal: boolean;

	const dispatch = createEventDispatcher();

	let oldPassword = '';
	let newPassword = '';
	let error = '';
	let success = '';
	let oldPasswordVisible = false;
	let newPasswordVisible = false;
	let validationErrors: string[] = [];

	function closeModal() {
		dispatch('close');
	}

	function validatePassword(password: string): string[] {
		const errors = [];
		if (password.length < 8 || password.length > 30) {
			errors.push('Password must be between 8 and 30 characters long');
		}
		if (!/[A-Z]/.test(password)) {
			errors.push('Password must contain at least one uppercase letter');
		}
		if (!/[a-z]/.test(password)) {
			errors.push('Password must contain at least one lowercase letter');
		}
		if (!/[0-9]/.test(password)) {
			errors.push('Password must contain at least one digit');
		}
		if (!/[@$!%*?&]/.test(password)) {
			errors.push('Password must contain at least one special character (@$!%*?&)');
		}
		if (!/^[a-zA-Z0-9_@$!%*?&]*$/.test(password)) {
			errors.push('Password can only contain letters, numbers, and special characters (@$!%*?&)');
		}
		return errors;
	}

	async function handleSubmit() {
		error = '';
		success = '';
		validationErrors = validatePassword(newPassword);

		if (validationErrors.length > 0) {
			return;
		}

		try {
			let access_token = getCookie('access');
			let user_id = getUserIDFromJWT(access_token);
			await changePassword(user_id, { old_password: oldPassword, new_password: newPassword });
			success = 'Password changed successfully';
			setTimeout(() => {
				success = '';
				closeModal();
			}, 2000);
		} catch (err) {
			if (Array.isArray(err)) {
				error = err[0].message || 'An error occurred';
			} else {
				error = 'An error occurred while changing the password';
			}
		}
	}

	const togglePasswordVisibility = (field: 'old' | 'new') => () => {
		if (field === 'old') {
			oldPasswordVisible = !oldPasswordVisible;
		} else {
			newPasswordVisible = !newPasswordVisible;
		}
	};

	$: {
		if (newPassword) {
			validationErrors = validatePassword(newPassword);
		} else {
			validationErrors = [];
		}
	}
</script>

{#if showModal}
	<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center modal">
		<div class="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
			<h2 class="text-2xl mb-4">Change Password</h2>
			<form on:submit|preventDefault={handleSubmit}>
				<div class="mb-4">
					<label class="block text-gray-700 text-sm font-bold mb-2" for="oldPassword">Old Password</label>
					<div class="relative">
						{#if oldPasswordVisible}
							<input
								class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
								id="oldPassword"
								type="text"
								placeholder="Old Password"
								bind:value={oldPassword}
								required
							>
						{:else}
							<input
								class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
								id="oldPassword"
								type="password"
								placeholder="Old Password"
								bind:value={oldPassword}
								required
							>
						{/if}
						<button
							type="button"
							on:click={togglePasswordVisibility('old')}
							class="absolute inset-y-0 right-0 flex items-center px-2 py-1 text-sm text-gray-600 hover:text-gray-800 focus:outline-none focus:ring-0">
							{#if oldPasswordVisible}
								<ClosedEyeIcon />
							{:else}
								<EyeIcon />
							{/if}
						</button>
					</div>
				</div>
				<div class="mb-4">
					<label class="block text-gray-700 text-sm font-bold mb-2" for="newPassword">New Password</label>
					<div class="relative">
						{#if newPasswordVisible}
							<input
								class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
								id="newPassword"
								type="text"
								placeholder="New Password"
								bind:value={newPassword}
								required
							>
						{:else}
							<input
								class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
								id="newPassword"
								type="password"
								placeholder="New Password"
								bind:value={newPassword}
								required
							>
						{/if}
						<button
							type="button"
							on:click={togglePasswordVisibility('new')}
							class="absolute inset-y-0 right-0 flex items-center px-2 py-1 text-sm text-gray-600 hover:text-gray-800 focus:outline-none focus:ring-0">
							{#if newPasswordVisible}
								<ClosedEyeIcon />
							{:else}
								<EyeIcon />
							{/if}
						</button>
					</div>
					{#if validationErrors.length > 0}
						<ul class="text-red-500 text-xs mt-1">
							{#each validationErrors as error}
								<li>{error}</li>
							{/each}
						</ul>
					{/if}
				</div>
				{#if error}
					<p class="text-red-500 text-xs italic mb-4">{error}</p>
				{/if}
				{#if success}
					<p class="text-green-500 text-xs italic mb-4">{success}</p>
				{/if}
				<div class="flex items-center justify-between">
					<button class="btn bg-indigo-custom" type="submit" disabled={validationErrors.length > 0}>Save
					</button>
					<button class="btn bg-gray-600 hover:bg-gray-700 rounded-md text-white" type="button"
							on:click={closeModal}>Cancel
					</button>
				</div>
			</form>
		</div>
	</div>
{/if}

<style lang="postcss">
    .modal {
        z-index: 3;
    }

    .btn.bg-indigo-custom {
        @apply bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded;
    }

    .btn:disabled {
        @apply opacity-50 cursor-not-allowed;
    }
</style>