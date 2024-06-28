<script lang="ts">
	import UserPosts from '../../components/UserPosts.svelte';
	import Waves_2 from '../../components/Waves_2.svelte';
	import { AppShell } from '@skeletonlabs/skeleton';
</script>

<style>
    .waves-container {
        background-color: #4f46e5;
    }

</style>

<AppShell>
	<div class="waves-container h-full">
		<Waves_2 />
		<div class="container mx-auto pb-8 ">
			<h2 class="text-3xl font-bold mb-12 text-white">Postările Utilizatorilor</h2>
			<UserPosts />
		</div>
	</div>
</AppShell>
