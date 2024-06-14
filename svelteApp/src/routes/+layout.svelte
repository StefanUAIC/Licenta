<!-- src/routes/__layout.svelte -->
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

	onMount(async () => {
		const notifications = await fetchNotifications();
		hasUnreadNotifications.set(notifications.length > 0);
	});
</script>

<style>
    .hamburger {
        cursor: pointer;
        padding: 10px;
        position: fixed;
        top: 10px;
        left: 10px;
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
        min-height: 24px;
        transition: transform 0.3s ease-in-out;
    }

    svg line {
        stroke: currentColor;
        stroke-width: 3;
        transition: transform 0.3s ease-in-out;
    }

    .open svg {
        transform: scale(0.7);
    }

    .open #top {
        transform: translate(6px, 0px) rotate(45deg);
        stroke: white;
    }

    .open #middle {
        opacity: 0;
    }

    .open #bottom {
        transform: translate(-12px, 9px) rotate(-45deg);
        stroke: white;
    }

    .list-nav {
        padding-top: 60px;
    }

    .active-page::before {
        content: '';
        position: absolute;
        left: -1rem;
        top: 0;
        bottom: 0;
        width: 4px;
        background-color: white;
    }

    .nav-link {
        color: white;
        padding: 1rem;
        font-size: 1.2rem;
        display: flex;
        align-items: center;
    }

    .nav-link:hover {
        background-color: rgba(255, 255, 255, 0.3);
        color: rgb(255, 255, 255) !important;
    }

    .content-wrapper {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }

    .main-content {
        flex: 1;
    }

    .notifications-button {
        cursor: pointer;
        padding: 10px;
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 20;
        background-color: white;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .notifications-button svg {
        width: 24px;
        height: 24px;
        color: #4f46e5;
    }

    .notification-indicator {
        position: absolute;
        top: 2px;
        right: 2px;
        width: 10px;
        height: 10px;
        background-color: red;
        border-radius: 50%;
    }
</style>

<AppShell slotSidebarLeft="w-56 p-4">
    {#if !['/', '/login', '/register'].includes(currentPage)}
        <button class="hamburger" class:open={sidebarVisible} on:click={toggleSidebar}>
            <svg width="32" height="24">
                <line id="top" x1="0" y1="2" x2="32" y2="2" />
                <line id="middle" x1="0" y1="12" x2="24" y2="12" />
                <line id="bottom" x1="0" y1="22" x2="32" y2="22" />
            </svg>
        </button>

        <button class="notifications-button" on:click={toggleNotificationsModal}>
            {#if $hasUnreadNotifications}
                <div class="notification-indicator"></div>
            {/if}
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.003 6.003 0 00-4-5.659V4a2 2 0 10-4 0v1.341C7.67 6.165 6 8.388 6 11v3.159c0 .417-.162.82-.451 1.13L4 17h11z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 19a1 1 0 11-2 0h2z" />
            </svg>
        </button>

        <nav class="list-nav fixed top-0 left-0 w-56 h-full bg-indigo-600 z-10 p-4 sidebar {sidebarVisible ? 'visible' : ''}">
            <ul>
                <li class="relative mb-2">
                    <a href="/posts" on:click={() => updateCurrentPage('/posts')}
                       class={`nav-link block rounded-md px-4 py-2 ${currentPage === '/posts' ? 'active-page' : ''}`}>
                        <i class="fas fa-blog mr-2"></i> Posts
                    </a>
                </li>
                <li class="relative mb-2">
                    <a href="/problems" on:click={() => updateCurrentPage('/problems')}
                       class={`nav-link block rounded-md px-4 py-2 ${currentPage === '/problems' ? 'active-page' : ''}`}>
                        <i class="fas fa-tasks mr-2"></i> Problems
                    </a>
                </li>
                <li class="relative mb-2">
                    <a href="/compiler" on:click={() => updateCurrentPage('/compiler')}
                       class={`nav-link block rounded-md px-4 py-2 ${currentPage === '/compiler' ? 'active-page' : ''}`}>
                        <i class="fas fa-code mr-2"></i> Compiler
                    </a>
                </li>
                <li class="relative mb-2">
                    <a href="/profile" on:click={() => updateCurrentPage('/profile')}
                       class={`nav-link block rounded-md px-4 py-2 ${currentPage === '/profile' ? 'active-page' : ''}`}>
                        <i class="fas fa-user mr-2"></i> Profile
                    </a>
                </li>
            </ul>
        </nav>
    {/if}

    <NotificationsModal bind:isOpen={$isNotificationsModalOpen} {hasUnreadNotifications} onClose={() => isNotificationsModalOpen.set(false)} />

    <div class="content-wrapper">
        <main class="main-content">
            <slot />
        </main>
        <Footer />
    </div>
</AppShell>
