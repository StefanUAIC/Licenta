<script lang="ts">
	import { register } from '$lib/api';
	import EyeIcon from '../../components/EyeIcon.svelte';
	import ClosedEyeIcon from '../../components/ClosedEyeIcon.svelte';

	let username = '';
	let password = '';
	let confirmPassword = '';
	let role = 'student';
	let email = '';
	let first_name = '';
	let last_name = '';
	let error = '';
	let passwordVisible = false;
	let confirmPasswordVisible = false;
	let passwordFocused = false;
	let confirmPasswordFocused = false;

	const handleRegister = async () => {
		if (password !== confirmPassword) {
			error = 'Passwords do not match';
			return;
		}

		try {
			const user = { username, password, role, email, first_name, last_name };
			const response = await register(user);
			console.log('Registered:', response);
			// Redirect or perform any post-registration actions
		} catch (err) {
			if (err instanceof Error) {
				error = err.message;
			} else {
				error = 'An unexpected error occurred';
			}
		}
	};

	const togglePasswordVisibility = (event: MouseEvent, inputId: string) => {
		event.preventDefault();
		const passwordInput = document.getElementById(inputId) as HTMLInputElement;
		if (passwordInput) {
			const start = passwordInput.selectionStart;
			const end = passwordInput.selectionEnd;
			if (inputId === 'password') {
				passwordVisible = !passwordVisible;
				passwordInput.type = passwordVisible ? 'text' : 'password';
			} else if (inputId === 'confirmPassword') {
				confirmPasswordVisible = !confirmPasswordVisible;
				passwordInput.type = confirmPasswordVisible ? 'text' : 'password';
			}
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

<main class="flex items-center justify-center min-h-screen bg-gray-100">
	<div class="w-full max-w-md p-8 space-y-4 bg-white rounded-lg shadow-md">
		<h1 class="text-2xl font-bold text-center">Register</h1>
		{#if error}
			<p class="text-red-500 text-center">{error}</p>
		{/if}
		<form on:submit|preventDefault={handleRegister} class="space-y-4">
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
							on:click={(event) => togglePasswordVisibility(event, 'password')}
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
			<div>
				<label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirm Password</label>
				<div class="relative">
					<input
						id="confirmPassword"
						type="password"
						bind:value={confirmPassword}
						class="w-full px-3 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
						on:focus={() => confirmPasswordFocused = true}
						on:blur={() => confirmPasswordFocused = false}
					/>
					{#if confirmPasswordFocused}
						<button
							type="button"
							on:mousedown={handleMouseDown}
							on:click={(event) => togglePasswordVisibility(event, 'confirmPassword')}
							class="absolute inset-y-0 right-0 flex items-center px-2 py-1 text-sm text-gray-600 hover:text-gray-800 focus:outline-none focus:ring-0">
							{#if confirmPasswordVisible}
								<ClosedEyeIcon />
							{:else}
								<EyeIcon />
							{/if}
						</button>
					{/if}
				</div>
			</div>
			<div>
				<label for="email" class="block text-sm font-medium text-gray-700">Email</label>
				<input id="email" type="email" bind:value={email}
					   class="w-full px-3 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" />
			</div>
			<div>
				<label for="first_name" class="block text-sm font-medium text-gray-700">First Name</label>
				<input id="first_name" type="text" bind:value={first_name}
					   class="w-full px-3 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" />
			</div>
			<div>
				<label for="last_name" class="block text-sm font-medium text-gray-700">Last Name</label>
				<input id="last_name" type="text" bind:value={last_name}
					   class="w-full px-3 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" />
			</div>
			<fieldset class="mt-4">
				<legend class="block text-sm font-medium text-gray-700">Select account type</legend>
				<div class="flex justify-around mt-2 space-x-4">
					<label class="flex items-center space-x-2">
						<input type="radio" bind:group={role} value="student" class="form-radio h-4 w-4 text-indigo-600" />
						<span class="text-sm text-gray-700">Student</span>
					</label>
					<label class="flex items-center space-x-2">
						<input type="radio" bind:group={role} value="teacher" class="form-radio h-4 w-4 text-indigo-600" />
						<span class="text-sm text-gray-700">Teacher</span>
					</label>
				</div>
			</fieldset>
			<button type="submit"
					class="w-full py-2 mt-4 text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500">
				Register
			</button>
		</form>
	</div>
</main>
