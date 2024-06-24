<script lang="ts">
	import { onMount } from 'svelte';
	import { AppShell } from '@skeletonlabs/skeleton';
	import HomeBackgroundImage from '../components/HomeBackgroundImage.svelte';
	import Waves_1 from '../components/Waves_1.svelte';

	function setCustomHeight(): void {
		const targetDiv = document.getElementById('target') as HTMLElement;
		const targetHeight = targetDiv.offsetHeight;

		document.documentElement.style.setProperty('--custom-height', `${targetHeight}px`);
	}

	onMount(() => {
		setCustomHeight();
		window.addEventListener('resize', setCustomHeight);

		return () => {
			window.removeEventListener('resize', setCustomHeight);
		};
	});
</script>

<style>
    .imagine-container {
        width: 100%;
        max-width: 750px;
    }

    .waves-container {
        position: relative;
        width: 100%;
    }

    .background-custom {
        background-color: #4f46e5;
        margin-top: -1px;
        position: relative;
    }

    #result {
        height: calc(100vh - var(--custom-height));
    }

    :root {
        --custom-height: 0px;
    }
</style>

<AppShell>
	<div id="target">
		<div class="container mx-auto pt-8">
			<div class="flex flex-col md:flex-row items-center justify-between">
				<div class="md:w-2/3 text-center">
					<h1 class="text-5xl font-bold mb-8 text-indigo-600">Bun venit pe platforma CodeLegends</h1>
					<p class="text-2xl mb-12 text-gray-600">Înscrie-te pentru a rezolva probleme de programare</p>
					<div class="flex flex-col md:flex-row justify-center space-y-4 md:space-x-8 md:space-y-0">
						<a href="/register"
						   class="bg-indigo-600 text-white px-14 py-6 rounded-lg hover:bg-indigo-700 text-lg">Înregistrare</a>
						<a href="/login" class="bg-teal-500 text-white px-14 py-6 rounded-lg hover:bg-teal-600 text-lg">Logare</a>
					</div>
				</div>
				<div class="imagine-container">
					<svelte:component this={HomeBackgroundImage} />
				</div>
			</div>
		</div>

		<div class="waves-container">
			<Waves_1 />
		</div>

	</div>
	<div id="result" class="background-custom"></div>
</AppShell>
