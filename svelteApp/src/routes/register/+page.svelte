<script lang="ts">
	import { register } from '$lib/auth_api';
	import EyeIcon from '../../components/EyeIcon.svelte';
	import ClosedEyeIcon from '../../components/ClosedEyeIcon.svelte';
	import { goto } from '$app/navigation';

	let username = '';
	let password = '';
	let confirmPassword = '';
	let role = 'student';
	let email = '';
	let first_name = '';
	let last_name = '';
	let errors: string[] = [];
	let passwordVisible = false;
	let confirmPasswordVisible = false;
	let passwordFocused = false;
	let confirmPasswordFocused = false;

	const validateUsername = (username: string): string | null => {
		const usernamePattern = /^[a-zA-Z0-9_]*$/;
		if (username.length < 5 || username.length > 30) {
			return 'Username must be between 5 and 30 characters long';
		}
		if (!usernamePattern.test(username)) {
			return 'Username can only contain letters, numbers, and underscores';
		}
		return null;
	};

	const validatePassword = (password: string): string | null => {
		const passwordPattern = /^[a-zA-Z0-9_@$!%*?&]*$/;
		if (password.length < 8 || password.length > 30) {
			return 'Password must be between 8 and 30 characters long';
		}
		if (!passwordPattern.test(password)) {
			return 'Password can only contain letters, numbers, and special characters (@$!%*?&)';
		}
		if (!/[A-Z]/.test(password)) {
			return 'Password must contain at least one uppercase letter';
		}
		if (!/[a-z]/.test(password)) {
			return 'Password must contain at least one lowercase letter';
		}
		if (!/[0-9]/.test(password)) {
			return 'Password must contain at least one digit';
		}
		if (!/[@$!%*?&]/.test(password)) {
			return 'Password must contain at least one special character (@$!%*?&)';
		}
		return null;
	};

	const validateName = (name: string): string | null => {
		const namePattern = /^[a-zA-Z]*$/;
		if (name.length < 1 || name.length > 30) {
			return 'Name must be between 1 and 30 characters long';
		}
		if (!namePattern.test(name)) {
			return 'Name can only contain letters';
		}
		return null;
	};

	const validateEmail = (email: string): string | null => {
		const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
		if (!emailPattern.test(email)) {
			return 'Email must contain a valid format (e.g., example@example.com)';
		}
		return null;
	};

	const handleRegister = async () => {
		errors = [];

		let validationError = validateUsername(username);
		if (validationError) {
			errors = [...errors, validationError];
		}

		validationError = validatePassword(password);
		if (validationError) {
			errors = [...errors, validationError];
		}

		if (password !== confirmPassword) {
			errors = [...errors, 'Passwords do not match'];
		}

		validationError = validateEmail(email);
		if (validationError) {
			errors = [...errors, validationError];
		}

		validationError = validateName(first_name);
		if (validationError) {
			errors = [...errors, validationError];
		}

		validationError = validateName(last_name);
		if (validationError) {
			errors = [...errors, validationError];
		}

		if (errors.length > 0) {
			return;
		}

		try {
			const user = { username, password, role, email, first_name, last_name };
			const response = await register(user);

			document.cookie = `access=${response.access}; path=/; SameSite=Strict`;
			document.cookie = `refresh=${response.refresh}; path=/; SameSite=Strict`;

			console.log('Registered:', response);

			await goto('/posts');
		} catch (err) {
			console.log('Registration error:', err);
			if (Array.isArray(err)) {
				err.forEach((error: { field: string; message: string }) => {
					errors = [...errors, `${error.message}`];
				});
			} else {
				errors = [...errors, 'An unexpected error occurred'];
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

	const handleLogin = () => {
		goto('/login');
	};
</script>

<main class="flex justify-center items-center h-full background-pattern">
	<div class="w-full max-w-md p-8 space-y-4 bg-white rounded-lg shadow-md">
		<h1 class="text-2xl font-bold text-center">Înregistrare</h1>
		{#if errors.length > 0}
			<div class="text-red-500 text-center space-y-1">
				{#each errors as error}
					<p>{error}</p>
				{/each}
			</div>
		{/if}
		<form on:submit|preventDefault={handleRegister} class="space-y-4">
			<div>
				<label for="username" class="block text-sm font-medium text-gray-700">Nume de utilizator</label>
				<input id="username" type="text" bind:value={username} required
							 class="w-full px-3 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" />
			</div>
			<div>
				<label for="password" class="block text-sm font-medium text-gray-700">Parolă</label>
				<div class="relative">
					<input
						id="password"
						type="password"
						bind:value={password}
						required
						minlength="8"
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
				<label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirmă Parola</label>
				<div class="relative">
					<input
						id="confirmPassword"
						type="password"
						bind:value={confirmPassword}
						required
						minlength="8"
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
				<input id="email" type="email" bind:value={email} required
							 class="w-full px-3 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" />
			</div>
			<div>
				<label for="first_name" class="block text-sm font-medium text-gray-700">Prenume</label>
				<input id="first_name" type="text" bind:value={first_name} required minlength="1"
							 class="w-full px-3 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" />
			</div>
			<div>
				<label for="last_name" class="block text-sm font-medium text-gray-700">Nume de familie</label>
				<input id="last_name" type="text" bind:value={last_name} required minlength="1"
							 class="w-full px-3 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" />
			</div>
			<fieldset class="mt-4">
				<legend class="block text-sm font-medium text-gray-700">Alege tipul de cont</legend>
				<div class="flex justify-around mt-2 space-x-4">
					<label class="flex items-center space-x-2">
						<input type="radio" bind:group={role} value="student" class="form-radio h-4 w-4 text-indigo-600"
									 required />
						<span class="text-sm text-gray-700">Elev</span>
					</label>
					<label class="flex items-center space-x-2">
						<input type="radio" bind:group={role} value="teacher"
									 class="form-radio h-4 w-4 text-indigo-600" />
						<span class="text-sm text-gray-700">Profesor</span>
					</label>
				</div>
			</fieldset>
			<button type="submit"
							class="w-full py-2 mt-4 text-white bg-indigo-600 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500">
				Înregistrează-te
			</button>
		</form>
		<div class="text-center">
			<p class="text-sm text-gray-600">Deja ești înregistrat?
				<button
					type="button"
					on:click={handleLogin}
					class="text-indigo-600 hover:underline">
					Loghează-te
				</button>
			</p>
		</div>
	</div>
</main>

<style lang="postcss">
    .background-pattern {
        background-color: #DFDBE5;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 304 304' width='304' height='304'%3E%3Cpath fill='%234f46e5' fill-opacity='0.25' d='M44.1 224a5 5 0 1 1 0 2H0v-2h44.1zm160 48a5 5 0 1 1 0 2H82v-2h122.1zm57.8-46a5 5 0 1 1 0-2H304v2h-42.1zm0 16a5 5 0 1 1 0-2H304v2h-42.1zm6.2-114a5 5 0 1 1 0 2h-86.2a5 5 0 1 1 0-2h86.2zm-256-48a5 5 0 1 1 0 2H0v-2h12.1zm185.8 34a5 5 0 1 1 0-2h86.2a5 5 0 1 1 0 2h-86.2zM258 12.1a5 5 0 1 1-2 0V0h2v12.1zm-64 208a5 5 0 1 1-2 0v-54.2a5 5 0 1 1 2 0v54.2zm48-198.2V80h62v2h-64V21.9a5 5 0 1 1 2 0zm16 16V64h46v2h-48V37.9a5 5 0 1 1 2 0zm-128 96V208h16v12.1a5 5 0 1 1-2 0V210h-16v-76.1a5 5 0 1 1 2 0zm-5.9-21.9a5 5 0 1 1 0 2H114v48H85.9a5 5 0 1 1 0-2H112v-48h12.1zm-6.2 130a5 5 0 1 1 0-2H176v-74.1a5 5 0 1 1 2 0V242h-60.1zm-16-64a5 5 0 1 1 0-2H114v48h10.1a5 5 0 1 1 0 2H112v-48h-10.1zM66 284.1a5 5 0 1 1-2 0V274H50v30h-2v-32h18v12.1zM236.1 176a5 5 0 1 1 0 2H226v94h48v32h-2v-30h-48v-98h12.1zm25.8-30a5 5 0 1 1 0-2H274v44.1a5 5 0 1 1-2 0V146h-10.1zm-64 96a5 5 0 1 1 0-2H208v-80h16v-14h-42.1a5 5 0 1 1 0-2H226v18h-16v80h-12.1zm86.2-210a5 5 0 1 1 0 2H272V0h2v32h10.1zM98 101.9V146H53.9a5 5 0 1 1 0-2H96v-42.1a5 5 0 1 1 2 0zM53.9 34a5 5 0 1 1 0-2H80V0h2v34H53.9zm60.1 3.9V66H82v64H69.9a5 5 0 1 1 0-2H80V64h32V37.9a5 5 0 1 1 2 0zM101.9 82a5 5 0 1 1 0-2H128V37.9a5 5 0 1 1 2 0V82h-28.1zm16-64a5 5 0 1 1 0-2H146v44.1a5 5 0 1 1-2 0V18h-26.1zm102.2 270a5 5 0 1 1 0 2H98v14h-2v-16h124.1zM242 149.9V160h16v34h-16v62h48v48h-2v-46h-48v-66h16v-30h-16v-12.1a5 5 0 1 1 2 0zM53.9 18a5 5 0 1 1 0-2H64V2H48V0h18v18H53.9zm112 32a5 5 0 1 1 0-2H192V0h50v2h-48v48h-28.1zm-48-48a5 5 0 0 1-9.8-2h2.07a3 3 0 1 0 5.66 0H178v34h-18V21.9a5 5 0 1 1 2 0V32h14V2h-58.1zm0 96a5 5 0 1 1 0-2H137l32-32h39V21.9a5 5 0 1 1 2 0V66h-40.17l-32 32H117.9zm28.1 90.1a5 5 0 1 1-2 0v-76.51L175.59 80H224V21.9a5 5 0 1 1 2 0V82h-49.59L146 112.41v75.69zm16 32a5 5 0 1 1-2 0v-99.51L184.59 96H300.1a5 5 0 0 1 3.9-3.9v2.07a3 3 0 0 0 0 5.66v2.07a5 5 0 0 1-3.9-3.9H185.41L162 121.41v98.69zm-144-64a5 5 0 1 1-2 0v-3.51l48-48V48h32V0h2v50H66v55.41l-48 48v2.69zM50 53.9v43.51l-48 48V208h26.1a5 5 0 1 1 0 2H0v-65.41l48-48V53.9a5 5 0 1 1 2 0zm-16 16V89.41l-34 34v-2.82l32-32V69.9a5 5 0 1 1 2 0zM12.1 32a5 5 0 1 1 0 2H9.41L0 43.41V40.6L8.59 32h3.51zm265.8 18a5 5 0 1 1 0-2h18.69l7.41-7.41v2.82L297.41 50H277.9zm-16 160a5 5 0 1 1 0-2H288v-71.41l16-16v2.82l-14 14V210h-28.1zm-208 32a5 5 0 1 1 0-2H64v-22.59L40.59 194H21.9a5 5 0 1 1 0-2H41.41L66 216.59V242H53.9zm150.2 14a5 5 0 1 1 0 2H96v-56.6L56.6 162H37.9a5 5 0 1 1 0-2h19.5L98 200.6V256h106.1zm-150.2 2a5 5 0 1 1 0-2H80v-46.59L48.59 178H21.9a5 5 0 1 1 0-2H49.41L82 208.59V258H53.9zM34 39.8v1.61L9.41 66H0v-2h8.59L32 40.59V0h2v39.8zM2 300.1a5 5 0 0 1 3.9 3.9H3.83A3 3 0 0 0 0 302.17V256h18v48h-2v-46H2v42.1zM34 241v63h-2v-62H0v-2h34v1zM17 18H0v-2h16V0h2v18h-1zm273-2h14v2h-16V0h2v16zm-32 273v15h-2v-14h-14v14h-2v-16h18v1zM0 92.1A5.02 5.02 0 0 1 6 97a5 5 0 0 1-6 4.9v-2.07a3 3 0 1 0 0-5.66V92.1zM80 272h2v32h-2v-32zm37.9 32h-2.07a3 3 0 0 0-5.66 0h-2.07a5 5 0 0 1 9.8 0zM5.9 0A5.02 5.02 0 0 1 0 5.9V3.83A3 3 0 0 0 3.83 0H5.9zm294.2 0h2.07A3 3 0 0 0 304 3.83V5.9a5 5 0 0 1-3.9-5.9zm3.9 300.1v2.07a3 3 0 0 0-1.83 1.83h-2.07a5 5 0 0 1 3.9-3.9zM97 100a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-48 32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm32 48a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm32-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0-32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm32 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16-64a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 96a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16-144a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16-32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-96 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16-32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm96 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16-64a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-32 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM49 36a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-32 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm32 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM33 68a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16-48a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 240a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16-64a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16-32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm80-176a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm32 48a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0-32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm112 176a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-16 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM17 180a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0 16a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm0-32a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM17 84a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm32 64a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm16-16a3 3 0 1 0 0-6 3 3 0 0 0 0 6z'%3E%3C/path%3E%3C/svg%3E");
    }
</style>