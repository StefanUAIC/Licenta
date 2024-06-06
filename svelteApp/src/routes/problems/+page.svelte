<script lang="ts">
	import { onMount } from 'svelte';
	import { derived, writable, type Writable } from 'svelte/store';
	import type { ProblemSchema } from '$lib/problems_api';
	import { getAllProblems } from '$lib/problems_api';
	import { goto } from '$app/navigation';

	const search: Writable<string> = writable('');
	const difficulty: Writable<string> = writable('');
	const grade: Writable<string> = writable('');
	const category: Writable<string> = writable('');

	const problems: Writable<ProblemSchema[]> = writable([]);
	const error: Writable<string | null> = writable(null);

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

	onMount(() => {
		fetchProblems();
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
</script>

<main class="min-h-screen bg-gray-100 py-10">
	<div class="max-w-4xl mx-auto px-4">
		<h1 class="text-3xl font-bold text-center mb-6">Problem Selector</h1>
		{#if $error}
			<p class="text-red-500 text-center mb-4">{$error}</p>
		{/if}
		<form on:submit|preventDefault class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4 mb-6">
			<input type="text" placeholder="Search" bind:value={$search}
				   class="px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500" />
			<select bind:value={$difficulty}
					class="px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500">
				<option value="">All Difficulties</option>
				<option value="easy">Easy</option>
				<option value="medium">Medium</option>
				<option value="hard">Hard</option>
			</select>
			<select bind:value={$grade}
					class="px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500">
				<option value="">All Grades</option>
				<option value="9">9th</option>
				<option value="10">10th</option>
				<option value="11">11th</option>
				<option value="12">12th</option>
			</select>
			<select bind:value={$category}
					class="px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500">
				<option value="">All Categories</option>
				{#each Object.entries(categoryLabels) as [key, value]}
					<option value={key}>{value}</option>
				{/each}
			</select>
		</form>

		<div class="text-right mb-6">
			<button on:click={handleCreateProblem} class="btn btn-primary">Create Problem</button>
		</div>

		<ul class="space-y-4">
			{#each $filteredProblems as problem}
				<li>
					<a href={`problems/${problem.id}`} class="block bg-white p-4 rounded-lg shadow-md hover:bg-gray-50">
						<h2 class="text-xl font-bold">{problem.title}</h2>
						<p class="text-gray-700">{problem.description}</p>
						<p class="text-gray-600">Difficulty: {difficultyLabels[problem.difficulty]}</p>
						<p class="text-gray-600">Grade: {gradeLabels[problem.grade]}</p>
						<p class="text-gray-600">Category: {categoryLabels[problem.category]}</p>
					</a>
				</li>
			{/each}
		</ul>
	</div>
</main>

<style>
	.btn {
		@apply px-4 py-2 rounded-lg;
	}

	.btn-primary {
		@apply bg-blue-500 text-white;
	}

	.error {
		color: red;
	}
</style>
