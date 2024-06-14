<!-- src/components/NotificationsModal.svelte -->
<script lang="ts">
	import { fetchNotifications, markNotificationAsRead } from '$lib/notifications_api';
	import { writable } from 'svelte/store';

	interface Notification {
		id: number;
		message: string;
	}

	export let isOpen = false;
	export let onClose: () => void;
	export let hasUnreadNotifications = writable(false);

	let notifications = writable<Notification[]>([]);

	$: if (isOpen) {
		(async () => {
			const data = await fetchNotifications();
			notifications.set(data);
			hasUnreadNotifications.set(data.length > 0);
		})();
	}

	const handleMarkAsRead = async (notificationId: number) => {
		await markNotificationAsRead(notificationId);
		notifications.update(n => {
			const updatedNotifications = n.filter(notif => notif.id !== notificationId);
			hasUnreadNotifications.set(updatedNotifications.length > 0);
			return updatedNotifications;
		});
	};
</script>

<div class="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50 z-50" class:hidden={!isOpen}>
	<div class="relative bg-white rounded-lg shadow-lg p-6 w-full max-w-md mx-auto" class:hidden={!isOpen}>
		<div class="flex justify-between items-center mb-4">
			<h2 class="text-xl font-bold">Notifications</h2>
			<button class="text-white bg-red-500 hover:bg-red-700 rounded-full w-8 h-8 flex items-center justify-center" on:click={onClose}>
				✖
			</button>
		</div>
		{#if $notifications.length === 0}
			<p>There are no new notifications available for you</p>
		{:else}
			{#each $notifications as notification (notification.id)}
				<div class="flex justify-between items-center bg-yellow-200 p-3 mb-2 rounded">
					<p>{notification.message}</p>
					<button class="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-700" on:click={() => handleMarkAsRead(notification.id)}>
						Mark as read
					</button>
				</div>
			{/each}
		{/if}
	</div>
</div>

<style>
	.hidden {
		display: none;
	}
</style>
