<script lang="ts">
	import '../app.css';
	import { AppShell } from '@skeletonlabs/skeleton';
	import { page } from '$app/stores';
	import Footer from '../components/Footer.svelte';

	let sidebarVisible = false;
	let currentPage = '';

	function toggleSidebar() {
		sidebarVisible = !sidebarVisible;
	}

	$: {
		currentPage = $page.url.pathname;
	}

	function updateCurrentPage(path: string) {
		currentPage = path;
	}
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
        padding-top: 60px; /* Adjust to create space for the logo */
    }

    .active-page::before {
        content: '';
        position: absolute;
        left: -1rem;
        top: 0;
        bottom: 0;
        width: 4px;
        background-color: white; /* Vertical line color */
    }

    .nav-link {
        color: white;
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

    /*.footer {*/
    /*    background-color: #4f46e5;*/
    /*    color: white;*/
    /*    padding: 20px;*/
    /*    text-align: center;*/
    /*}*/
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

		<nav
			class="list-nav fixed top-0 left-0 w-56 h-full bg-indigo-600 z-10 p-4 sidebar {sidebarVisible ? 'visible' : ''}">
			<ul>
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
				<li class="relative mb-2">
					<a href="/problems" on:click={() => updateCurrentPage('/problems')}
					   class={`nav-link block rounded-md px-4 py-2 ${currentPage === '/problems' ? 'active-page' : ''}`}>
						<i class="fas fa-tasks mr-2"></i> Problems
					</a>
				</li>
				<li class="relative mb-2">
					<a href="/posts" on:click={() => updateCurrentPage('/about')}
					   class={`nav-link block rounded-md px-4 py-2 ${currentPage === '/posts' ? 'active-page' : ''}`}>
						<i class="fas fa-blog mr-2"></i> Posts
					</a>
				</li>
			</ul>
		</nav>
	{/if}

	<div class="content-wrapper">
		<main class="main-content">
			<slot />
		</main>
		<Footer />
	</div>
</AppShell>
