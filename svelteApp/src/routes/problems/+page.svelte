<script lang="ts">
	import { onMount } from 'svelte';
	import { derived, writable, type Writable } from 'svelte/store';
	import type { ProblemSchema } from '$lib/problems_api';
	import { getAllProblems } from '$lib/problems_api';
	import { goto } from '$app/navigation';
	import { getUserRole } from '$lib/users_api';
	import { getCookie, getUserIDFromJWT } from '$lib/utils';

	const search: Writable<string> = writable('');
	const difficulty: Writable<string> = writable('');
	const grade: Writable<string> = writable('');
	const category: Writable<string> = writable('');

	const problems: Writable<ProblemSchema[]> = writable([]);
	const error: Writable<string | null> = writable(null);
	const userRole: Writable<'student' | 'teacher' | null> = writable(null);

	const difficultyLabels: Record<string, string> = {
		'easy': 'Easy',
		'medium': 'Medium',
		'hard': 'Hard'
	};

	const gradeLabels: Record<number, string> = {
		9: '9th',
		10: '10th',
		11: '11th',
		12: '12th'
	};

	const categoryLabels: Record<string, string> = {
		'arrays': 'Arrays',
		'linked_lists': 'Linked Lists',
		'sorting': 'Sorting',
		'searching': 'Searching',
		'trees': 'Trees',
		'graphs': 'Graphs',
		'dynamic_programming': 'Dynamic Programming',
		'recursion': 'Recursion',
		'backtracking': 'Backtracking',
		'bit_manipulation': 'Bit Manipulation',
		'greedy': 'Greedy',
		'math': 'Math',
		'geometry': 'Geometry',
		'combinatorics': 'Combinatorics',
		'probability': 'Probability',
		'game_theory': 'Game Theory',
		'puzzles': 'Puzzles',
		'miscellaneous': 'Miscellaneous'
	};

	const fetchProblems = async () => {
		try {
			const data = await getAllProblems();
			problems.set(data);
		} catch (err) {
			console.error('Failed to load problems:', err);
			error.set('Failed to load problems');
		}
	};

	onMount(async () => {
		await fetchProblems();
		let accessToken = getCookie('access');
		const user_id = getUserIDFromJWT(accessToken);
		const roleResponse = await getUserRole(user_id);
		userRole.set(roleResponse.role);
	});

	const filteredProblems = derived(
		[problems, search, difficulty, grade, category],
		([$problems, $search, $difficulty, $grade, $category]) => {
			if (!$problems) return [];
			return $problems.filter(problem => {
				return (
					(!$search || problem.title.toLowerCase().includes($search.toLowerCase())) &&
					(!$difficulty || problem.difficulty === $difficulty) &&
					(!$grade || problem.grade === Number($grade)) &&
					(!$category || problem.category === $category)
				);
			});
		}
	);

	function handleCreateProblem() {
		goto('/problems/create');
	}

	function truncateText(text: string, limit: number): string {
		return text.length > limit ? text.slice(0, limit) + '...' : text;
	}

	function toRomanNumeral(num: number): string {
		const romanNumerals: [number, string][] = [
			[10, 'X'],
			[9, 'IX'],
			[5, 'V'],
			[4, 'IV'],
			[1, 'I']
		];
		let result = '';
		for (const [value, symbol] of romanNumerals) {
			while (num >= value) {
				result += symbol;
				num -= value;
			}
		}
		return result;
	}
</script>

<main class="min-h-screen bg-gray-100 py-16 px-4">
	<div class="max-w-7xl mx-auto flex flex-col md:flex-row gap-8">
		<aside class="w-full md:w-1/3 space-y-4">
			{#if $error}
				<p class="text-red-500 mb-4">{$error}</p>
			{/if}
			<form on:submit|preventDefault class="space-y-4">
				<input type="text" placeholder="Search" bind:value={$search}
							 class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500" />
				<select bind:value={$difficulty}
								class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
					<option value="">All Difficulties</option>
					<option value="easy">Easy</option>
					<option value="medium">Medium</option>
					<option value="hard">Hard</option>
				</select>
				<select bind:value={$grade}
								class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
					<option value="">All Grades</option>
					<option value="9">9th</option>
					<option value="10">10th</option>
					<option value="11">11th</option>
					<option value="12">12th</option>
				</select>
				<select bind:value={$category}
								class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
					<option value="">All Categories</option>
					{#each Object.entries(categoryLabels) as [key, value]}
						<option value={key}>{value}</option>
					{/each}
				</select>
			</form>
			{#if $userRole === 'teacher'}
				<button on:click={handleCreateProblem} class="w-full btn btn-primary">Create Problem</button>
			{/if}

			<img src="problems_vector.png" alt="laptop" class="my-16">
		</aside>

		<section class="w-full md:w-3/4">
			<ul class="space-y-6">
				{#each $filteredProblems as problem}
					<li>
						<a href={`problems/${problem.id}`} class="block bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300">
							<h2 class="text-2xl font-bold mb-2">{problem.title}</h2>
							<div class="border-b border-gray-200 mb-4"></div>
							<p class="text-gray-700 mb-4">{truncateText(problem.description, 100)}</p>
							<div class="flex flex-wrap items-center gap-4 text-sm">
								<span class="px-3 py-1 rounded-full font-semibold
									{problem.difficulty === 'easy' ? 'bg-green-600 text-white' :
									problem.difficulty === 'medium' ? 'bg-yellow-600 text-white' :
									'bg-blue-600 text-white'}">
									{difficultyLabels[problem.difficulty]}
								</span>
								<span class="text-gray-600">Grade: {toRomanNumeral(problem.grade)}</span>
								<span class="text-gray-600">{categoryLabels[problem.category]}</span>
							</div>
						</a>
					</li>
				{/each}
			</ul>
		</section>
	</div>
</main>

<style lang="postcss">
    .btn {
        @apply px-4 py-2 rounded-lg font-semibold transition-colors duration-300;
    }

    .btn-primary {
        @apply bg-indigo-600 text-white hover:bg-indigo-700;
    }
</style>