<script>
	import { AppShell } from '@skeletonlabs/skeleton';
	import HomeBackgroundImage from '../components/HomeBackgroundImage.svelte';
	import Waves_1 from '../components/Waves_1.svelte';
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
        padding-top: 50px;
        margin-top: -1px;
    }
</style>

<AppShell>
	<div class="container mx-auto pt-8">
		<div class="flex flex-col md:flex-row items-center justify-between">
			<div class="md:w-2/3 text-center">
				<h1 class="text-5xl font-bold mb-8 text-indigo-600">Welcome to my website</h1>
				<p class="text-2xl mb-12 text-gray-600">Go and look around, you'll find cool stuff</p>
				<div class="flex flex-col md:flex-row justify-center space-y-4 md:space-x-8 md:space-y-0">
					<a href="/register"
					   class="bg-indigo-600 text-white px-14 py-6 rounded-lg hover:bg-indigo-700 text-lg">Register</a>
					<a href="/login" class="bg-teal-500 text-white px-14 py-6 rounded-lg hover:bg-teal-600 text-lg">Login</a>

				</div>
			</div>
			<div class="imagine-container">
				<svelte:component this={HomeBackgroundImage} />
			</div>
		</div>
	</div>
	<div class="waves-container">
		<Waves_1 />
		<div class="background-custom">
		</div>
	</div>

</AppShell>
