<script lang="ts">
	import { login } from '$lib/auth_api';
	import EyeIcon from '../../components/EyeIcon.svelte';
	import ClosedEyeIcon from '../../components/ClosedEyeIcon.svelte';
	import { goto } from '$app/navigation';

	let username = '';
	let password = '';
	let errors = '';
	let passwordVisible = false;
	let passwordFocused = false;

	const handleLogin = async () => {
		try {
			const response = await login(username, password);
			console.log('Response:', response);
			document.cookie = `access=${response.access}; path=/; SameSite=Strict`;
			document.cookie = `refresh=${response.refresh}; path=/; SameSite=Strict`;

			errors = '';
			await goto('/posts');
		} catch (err) {
			console.log('Error:', err);
			if (Array.isArray(err)) {
				err.forEach((error: { field: string; message: string }) => {
					errors = `${error.message}`;
				});
			} else {
				errors = `An unexpected error occurred`;
			}
		}
	};

	const togglePasswordVisibility = (event: MouseEvent) => {
		event.preventDefault();
		const passwordInput = document.getElementById('password') as HTMLInputElement;
		if (passwordInput) {
			const start = passwordInput.selectionStart;
			const end = passwordInput.selectionEnd;
			passwordVisible = !passwordVisible;
			passwordInput.type = passwordVisible ? 'text' : 'password';
			requestAnimationFrame(() => {
				passwordInput.setSelectionRange(start, end);
				passwordInput.focus();
			});
		}
	};

	const handleMouseDown = (event: MouseEvent) => {
		event.preventDefault();
	};
</script>

<main class="flex justify-center items-center h-full bg-gray-100">
	<div class="w-full max-w-md p-8 space-y-4 bg-white rounded-lg shadow-md">
		<h1 class="text-2xl font-bold text-center">Login</h1>
		{#if errors}
			<p class="text-red-500 text-center">{errors}</p>
		{/if}
		<form on:submit|preventDefault={handleLogin} class="space-y-4">
			<div>
				<label for="username" class="block text-sm font-medium text-gray-700">Username</label>
				<input id="username" type="text" bind:value={username}
					   class="w-full px-3 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" />
			</div>
			<div>
				<label for="password" class="block text-sm font-medium text-gray-700">Password</label>
				<div class="relative">
					<input
						id="password"
						type="password"
						bind:value={password}
						class="w-full px-3 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
						on:focus={() => passwordFocused = true}
						on:blur={() => passwordFocused = false}
					/>
					{#if passwordFocused}
						<button
							type="button"
							on:mousedown={handleMouseDown}
							on:click={togglePasswordVisibility}
							class="absolute inset-y-0 right-0 flex items-center px-2 py-1 text-sm text-gray-600 hover:text-gray-800 focus:outline-none focus:ring-0">
							{#if passwordVisible}
								<ClosedEyeIcon />
							{:else}
								<EyeIcon />
							{/if}
						</button>
					{/if}
				</div>
			</div>
			<button type="submit" class="w-full py-2 mt-4 text-white bg-indigo-600 rounded-md hover:bg-indigo-700">
				Login
			</button>
		</form>
	</div>
</main>