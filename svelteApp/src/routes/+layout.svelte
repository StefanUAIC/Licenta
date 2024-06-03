<script>
	import '../app.css';
	import { AppShell } from '@skeletonlabs/skeleton';
	import { onMount } from 'svelte';

	let sidebarVisible = false;
	let currentPage = '';

	function toggleSidebar() {
		sidebarVisible = !sidebarVisible;
	}

	function updateCurrentPage(path) {
		currentPage = path;
	}

	onMount(() => {
		currentPage = window.location.pathname; // Get the current path
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
        background-color: white;
        color: rgb(79 70 229) !important;

    }

    .nav-link:focus {
        background-color: white;
        color: rgb(79 70 229);
    }

    .nav-link:active {
        background-color: white;
        color: rgb(79 70 229);
    }

    .nav-link:visited {
        color: white;
    }


</style>

<AppShell slotSidebarLeft="w-56 p-4">
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
				<a href="/" on:click={() => updateCurrentPage('/')}
				   class={`nav-link block rounded-md px-4 py-2 ${currentPage === '/' ? 'active-page' : ''}`}>
					<i class="fas fa-home mr-2"></i> Home
				</a>
			</li>
			<li class="relative mb-2">
				<a href="/login" on:click={() => updateCurrentPage('/login')}
				   class={`nav-link block rounded-md px-4 py-2 ${currentPage === '/login' ? 'active-page' : ''}`}>
					<i class="fas fa-sign-in-alt mr-2"></i> Login
				</a>
			</li>
			<li class="relative mb-2">
				<a href="/register" on:click={() => updateCurrentPage('/register')}
				   class={`nav-link block rounded-md px-4 py-2 ${currentPage === '/register' ? 'active-page' : ''}`}>
					<i class="fas fa-user-plus mr-2"></i> Register
				</a>
			</li>
			<li class="relative mb-2">
				<a href="/compiler" on:click={() => updateCurrentPage('/compiler')}
				   class={`nav-link block rounded-md px-4 py-2 ${currentPage === '/compiler' ? 'active-page' : ''}`}>
					<i class="fas fa-code mr-2"></i> Compiler
				</a>
			</li>
		</ul>
	</nav>

	<slot></slot>
</AppShell>
