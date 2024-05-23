<script lang="ts">
    import { login } from '$lib/api';
    let username = '';
    let password = '';
    let error = '';

    const handleLogin = async () => {
        try {
            const response = await login(username, password);
            console.log('Logged in:', response);
        } catch (err) {
            if (err instanceof Error) {
                error = err.message;
            } else {
                error = 'An unexpected error occurred';
            }
        }
    };
</script>

<main class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md p-8 space-y-4 bg-white rounded-lg shadow-md">
        <h1 class="text-2xl font-bold text-center">Login</h1>
        {#if error}
            <p class="text-red-500 text-center">{error}</p>
        {/if}
        <form on:submit|preventDefault={handleLogin} class="space-y-4">
            <div>
                <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
                <input id="username" type="text" bind:value={username} class="w-full px-3 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>
            <div>
                <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
                <input id="password" type="password" bind:value={password} class="w-full px-3 py-2 mt-1 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>
            <button type="submit" class="w-full py-2 mt-4 text-white bg-indigo-600 rounded-md hover:bg-indigo-700">Login</button>
        </form>
    </div>
</main>
