<script lang="ts">
    import { createEventDispatcher } from 'svelte';

    export let showModal: boolean;

    const dispatch = createEventDispatcher();

    function closeModal() {
        dispatch('close');
    }

    function handleSubmit() {
        closeModal();
    }
</script>

{#if showModal}
<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center modal">
    <div class="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <h2 class="text-2xl mb-4">Change Password</h2>
        <form on:submit|preventDefault={handleSubmit}>
            <div class="mb-4">
                <label class="block text-gray-700 text-sm font-bold mb-2" for="oldPassword">Old Password</label>
                <input
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    id="oldPassword"
                    type="password"
                    placeholder="Old Password"
                    required
                >
            </div>
            <div class="mb-4">
                <label class="block text-gray-700 text-sm font-bold mb-2" for="newPassword">New Password</label>
                <input
                    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                    id="newPassword"
                    type="password"
                    placeholder="New Password"
                    required
                >
            </div>
            <div class="flex items-center justify-between">
                <button class="btn bg-indigo-custom" type="submit">Save</button>
                <button class="btn bg-gray-600 hover:bg-gray-700 rounded-md text-white" type="button" on:click={closeModal}>Cancel</button>
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
</style>