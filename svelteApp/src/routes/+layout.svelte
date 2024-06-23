<script lang="ts">
	import '../app.css';
	import { AppShell } from '@skeletonlabs/skeleton';
	import { page } from '$app/stores';
	import Footer from '../components/Footer.svelte';
	import NotificationsModal from '../components/NotificationsModal.svelte';
	import { writable } from 'svelte/store';
	import { fetchNotifications } from '$lib/notifications_api';
	import { onMount } from 'svelte';

	let sidebarVisible = false;
	let currentPage = '';
	let isNotificationsModalOpen = writable(false);
	let hasUnreadNotifications = writable(false);

	function toggleSidebar() {
		sidebarVisible = !sidebarVisible;
	}

	function toggleNotificationsModal() {
		isNotificationsModalOpen.update(open => !open);
		if ($isNotificationsModalOpen) {
			hasUnreadNotifications.set(false);
		}
	}

	$: currentPage = $page.url.pathname;

	function updateCurrentPage(path: string) {
		currentPage = path;
	}

	function logout(event: Event) {
		event.preventDefault();
		document.cookie = 'access=; Max-Age=0; path=/';
		document.cookie = 'refresh=; Max-Age=0; path=/';
		window.location.href = '/';
	}

	onMount(async () => {
		if (currentPage === '/' || currentPage === '/login' || currentPage === '/register') {
			return;
		}
		const notifications = await fetchNotifications();
		hasUnreadNotifications.set(notifications.length > 0);
	});
</script>

<style>
    .hamburger {
        cursor: pointer;
        padding: 1rem;
        position: fixed;
        top: 1rem;
        left: 1rem;
        z-index: 20;
    }

    .sidebar {
        transition: transform 0.8s ease;
        transform: translateX(-100%);
    }

    .sidebar.visible {
        transform: translateX(0);
    }

    svg {
        min-height: 1.5rem;
        transition: transform 0.3s ease-in-out;
    }

    svg line {
        stroke: currentColor;
        stroke-width: 0.1875rem;
        transition: transform 0.3s ease-in-out;
    }

    .open svg {
        transform: scale(0.7);
    }

    .open #top {
        transform: translate(0.375rem, 0) rotate(45deg);
        stroke: white;
    }

    .open #middle {
        opacity: 0;
    }

    .open #bottom {
        transform: translate(-0.75rem, 0.5625rem) rotate(-45deg);
        stroke: white;
    }

    .list-nav {
        padding-top: 3.75rem;
    }

    .active-page::before {
        content: '';
        position: absolute;
        left: -1rem;
        top: 0;
        bottom: 0;
        width: 0.25rem;
        background-color: white;
    }

    .nav-link {
        color: white;
        padding: 1rem;
        font-size: 1.3rem;
        display: flex;
        align-items: center;
    }

    .nav-link:hover {
        background-color: rgba(255, 255, 255, 0.3);
        color: rgb(255, 255, 255) !important;
    }

    .main-content {
        flex: 1;
    }

    .notifications-button {
        cursor: pointer;
        padding: 0.75rem;
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 20;
        background-color: white;
        border: none;
        border-radius: 50%;
        width: 3rem;
        height: 3rem;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .notifications-button svg {
        width: 1.5rem;
        height: 1.5rem;
        color: #4f46e5;
    }

    .notification-indicator {
        position: absolute;
        top: 0;
        left: 0;
        width: 0.75rem;
        height: 0.75rem;
        background-color: red;
        border-radius: 50%;
    }

    .color-nav {
        background-color: #009fff !important;
    }

    .app-logo {
        display: flex;
        flex-direction: column;
        align-items: center;
		margin-bottom: 2rem;
    }

    .app-logo img {
        width: 10rem;
        height: 10rem;
        margin-bottom: 1rem;
    }

    .separator {
        height: 2px;
        background-color: rgba(255, 255, 255, 0.5);
        margin: 1rem 0;
    }
</style>

<AppShell slotSidebarLeft="w-56 p-4">
	{#if !['/', '/login', '/register'].includes(currentPage)}
		<button class="hamburger" class:open={sidebarVisible} on:click={toggleSidebar}>
			<svg width="2rem" height="1.5rem">
				<line id="top" x1="0" y1="0.125rem" x2="2rem" y2="0.125rem" />
				<line id="middle" x1="0" y1="0.75rem" x2="1.5rem" y2="0.75rem" />
				<line id="bottom" x1="0" y1="1.375rem" x2="2rem" y2="1.375rem" />
			</svg>
		</button>

		<button class="notifications-button" on:click={toggleNotificationsModal}>
			{#if $hasUnreadNotifications}
				<div class="notification-indicator"></div>
			{/if}
			<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
					  d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.003 6.003 0 00-4-5.659V4a2 2 0 10-4 0v1.341C7.67 6.165 6 8.388 6 11v3.159c0 .417-.162.82-.451 1.13L4 17h11z" />
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 19a1 1 0 11-2 0h2z" />
			</svg>
		</button>

		<nav
			class="list-nav fixed top-0 left-0 w-56 h-full color-nav z-10 p-4 sidebar {sidebarVisible ? 'visible' : ''}">
			<div class="app-logo">
				<img src="/logo.png" alt="Logo">
				<h1 class="bg-white text-blue-500 rounded-tr-lg rounded-bl-lg px-4 py-2 text-2xl font-semibold">CodeLegends</h1>
			</div>
			<ul>
				<li class="relative mb-2">
					<a href="/posts" on:click={() => updateCurrentPage('/posts')}
					   class={`nav-link block rounded-md px-4 py-2 ${currentPage === '/posts' ? 'active-page' : ''}`}>
						<i class="fas fa-blog mr-2 w-8"></i> Posts
					</a>
				</li>
				<li class="relative mb-2">
					<a href="/problems" on:click={() => updateCurrentPage('/problems')}
					   class={`nav-link block rounded-md px-4 py-2 ${currentPage === '/problems' ? 'active-page' : ''}`}>
						<i class="fas fa-tasks mr-2 w-8"></i> Problems
					</a>
				</li>
				<li class="relative mb-2">
					<a href="/compiler" on:click={() => updateCurrentPage('/compiler')}
					   class={`nav-link block rounded-md px-4 py-2 ${currentPage === '/compiler' ? 'active-page' : ''}`}>
						<i class="fas fa-code mr-2 w-8"></i> Compiler
					</a>
				</li>
				<li class="relative mb-2">
					<a href="/classes" on:click={() => updateCurrentPage('/classes')}
					   class={`nav-link block rounded-md px-4 py-2 ${currentPage === '/classes' ? 'active-page' : ''}`}>
						<i class="fas fa-users mr-2 w-8"></i> Classes
					</a>
				</li>
				<div class="separator"></div>
				<li class="relative mb-2">
					<a href="/profile" on:click={() => updateCurrentPage('/profile')}
					   class={`nav-link block rounded-md px-4 py-2 ${currentPage === '/profile' ? 'active-page' : ''}`}>
						<i class="fas fa-user mr-2 w-8"></i> Profile
					</a>
				</li>
				<li class="relative mb-2">
					<a href="/" on:click={logout}
					   class="nav-link block rounded-md px-4 py-2">
						<i class="fas fa-sign-out-alt mr-2 w-8"></i> Logout
					</a>
				</li>
			</ul>
		</nav>
	{/if}

	<NotificationsModal bind:isOpen={$isNotificationsModalOpen} {hasUnreadNotifications}
						onClose={() => isNotificationsModalOpen.set(false)} />

	<div class="flex flex-col bg-gray-100 h-screen">
		<main class="main-content">
			<slot />
		</main>
		<Footer />
	</div>

</AppShell>
