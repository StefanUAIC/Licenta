<script>
	import { AppShell } from '@skeletonlabs/skeleton';
	// import UserPosts from '../components/UserPosts.svelte';
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
        padding-top: 50px; /* Ajustează în funcție de dimensiunea SVG-ului */
        margin-top: -1px; /* Ajustează pentru a elimina eventualele spații */
    }
</style>

<AppShell>
	<div class="container mx-auto pt-8">
		<div class="flex flex-col md:flex-row items-center justify-between">
			<div class="md:w-2/3 text-center">
				<h1 class="text-5xl font-bold mb-8 text-indigo-600">Bine ai venit pe site-ul nostru de probleme pentru
					informatică!</h1>
				<p class="text-2xl mb-12 text-gray-600">Explorează o colecție vastă de probleme și îmbunătățește-ți
					abilitățile de programare.</p>
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
		<div class="background-custom">
<!--			<div class="container mx-auto pb-8">-->
<!--				<h2 class="text-3xl font-bold mb-12 text-white">Postări ale utilizatorilor</h2>-->
<!--				<UserPosts />-->
<!--			</div>-->

		</div>
	</div>

</AppShell>
