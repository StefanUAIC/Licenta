<script lang="ts">
	import { type PaginationSettings, Paginator } from '@skeletonlabs/skeleton';
	import { faker } from '@faker-js/faker';

	export let activeTab: string;

	const sourceHeaders: string[] = ['', 'Problem Name', 'Difficulty', 'Date Solved', 'Score', 'Solutions'];
	const problemsHeaders: string[] = ['', 'Problem Name', 'Difficulty', 'Date Proposed', 'Status'];
	const classesHeaders: string[] = ['', 'Class Name', 'Date Joined', 'Instructor'];

	const sourceBody = Array(27).fill(undefined).map((_, index) => [
		index + 1,
		faker.hacker.phrase(),
		['Easy', 'Medium', 'Hard'][Math.floor(Math.random() * 3)],
		faker.date.past().toLocaleDateString(),
		Math.floor(Math.random() * 101),
		faker.string.uuid()
	]);

	const problemsBody = Array(15).fill(undefined).map((_, index) => [
		index + 1,
		faker.hacker.phrase(),
		['Easy', 'Medium', 'Hard'][Math.floor(Math.random() * 3)],
		faker.date.past().toLocaleDateString(),
		['Pending', 'Approved', 'Rejected'][Math.floor(Math.random() * 3)]
	]);

	const classesBody = Array(10).fill(undefined).map((_, index) => [
		index + 1,
		`${faker.word.adjective()} Class`,
		faker.date.past().toLocaleDateString(),
		faker.person.fullName()
	]);

	let paginationSettings = {
		page: 0,
		limit: 3,
		size: sourceBody.length,
		amounts: [1, 2, 3, 5, sourceBody.length]
	} satisfies PaginationSettings;

	let problemsPaginationSettings = {
		page: 0,
		limit: 3,
		size: problemsBody.length,
		amounts: [1, 2, 3, 5, problemsBody.length]
	} satisfies PaginationSettings;

	let classesPaginationSettings = {
		page: 0,
		limit: 3,
		size: classesBody.length,
		amounts: [1, 2, 3, 5, classesBody.length]
	} satisfies PaginationSettings;

	let state = {
		firstLast: false,
		previousNext: true
	};

	function onPageChange(e: CustomEvent): void {
		console.log('Paginator - event:page', e.detail);
	}

	function onAmountChange(e: CustomEvent): void {
		console.log('Paginator - event:amount', e.detail);
	}

	$: sourceBodySliced = sourceBody.slice(
		paginationSettings.page * paginationSettings.limit,
		paginationSettings.page * paginationSettings.limit + paginationSettings.limit
	);

	$: problemsBodySliced = problemsBody.slice(
		problemsPaginationSettings.page * problemsPaginationSettings.limit,
		problemsPaginationSettings.page * problemsPaginationSettings.limit + problemsPaginationSettings.limit
	);

	$: classesBodySliced = classesBody.slice(
		classesPaginationSettings.page * classesPaginationSettings.limit,
		classesPaginationSettings.page * classesPaginationSettings.limit + classesPaginationSettings.limit
	);

	function getDifficultyColor(difficulty: string): string {
		switch (difficulty) {
			case 'Easy':
				return 'text-green-600';
			case 'Medium':
				return 'text-yellow-600';
			case 'Hard':
				return 'text-blue-600';
			default:
				return '';
		}
	}

	function getScoreColor(score: number): string {
		if (score < 40) {
			return 'font-bold text-red-500';
		} else if (score < 80) {
			return 'font-bold text-yellow-500';
		} else {
			return 'font-bold text-green-500';
		}
	}
</script>

<div class="w-full space-y-4 text-token mt-4">
	{#if activeTab === 'sentSolutions'}
		<table class="min-w-full divide-y divide-gray-200 shadow-lg">
			<thead class="bg-gradient-to-tr from-teal-300 to-indigo-600 text-white">
			<tr>
				{#each sourceHeaders as header}
					<th class="px-6 py-4 text-left text-xs font-medium uppercase tracking-wider first:rounded-tl-md last:rounded-tr-md">{header}</th>
				{/each}
			</tr>
			</thead>
			<tbody class="bg-white divide-y divide-gray-200">
			{#each sourceBodySliced as row}
				<tr class="rounded-md">
					{#each row as cell, index}
						<td class="px-6 py-4 whitespace-nowrap {index === 0 ? 'rounded-l-md' : ''} {index === row.length - 1 ? 'rounded-r-md' : ''}">
							{#if index === 1}
								<a href="/problem/{cell}" class="text-indigo-600 hover:text-indigo-900">{cell}</a>
							{:else if index === 2}
								{#if typeof cell === 'string'}
									<span class={getDifficultyColor(cell)}>{cell}</span>
								{:else}
									{cell}
								{/if}
							{:else if index === 4}
								{#if typeof cell === 'number'}
									<span class={getScoreColor(cell)}>{cell}</span>
								{:else}
									{cell}
								{/if}
							{:else if index === 5}
								<a href="/solution/{cell}" class="btn bg-solution-btn hover:bg-teal-700">View
									Solution</a>
							{:else}
								{cell}
							{/if}
						</td>
					{/each}
				</tr>
			{/each}
			</tbody>
		</table>
		<Paginator bind:settings={paginationSettings} on:page={onPageChange} on:amount={onAmountChange}
				   showFirstLastButtons={state.firstLast} showPreviousNextButtons={state.previousNext}
				   controlVariant="variant-soft bg-white"
				   select="variant-soft bg-white p-2 border rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" />
	{:else if activeTab === 'problemsProposed'}
		<table class="min-w-full divide-y divide-gray-200 shadow-lg">
			<thead class="bg-gradient-to-tr from-teal-300 to-indigo-600 text-white">
			<tr>
				{#each problemsHeaders as header}
					<th class="px-6 py-4 text-left text-xs font-medium uppercase tracking-wider first:rounded-tl-md last:rounded-tr-md">{header}</th>
				{/each}
			</tr>
			</thead>
			<tbody class="bg-white divide-y divide-gray-200">
			{#each problemsBodySliced as row}
				<tr class="rounded-md">
					{#each row as cell, index}
						<td class="px-6 py-4 whitespace-nowrap {index === 0 ? 'rounded-l-md' : ''} {index === row.length - 1 ? 'rounded-r-md' : ''}">
							{#if index === 1}
								<a href="/problem/{cell}" class="text-indigo-600 hover:text-indigo-900">{cell}</a>
							{:else if index === 2}
								{#if typeof cell === 'string'}
									<span class={getDifficultyColor(cell)}>{cell}</span>
								{:else}
									{cell}
								{/if}
							{:else if index === 4}
								<span
									class={cell === 'Pending' ? 'text-yellow-500' : cell === 'Approved' ? 'text-green-500' : 'text-red-500'}>{cell}</span>
							{:else}
								{cell}
							{/if}
						</td>
					{/each}
				</tr>
			{/each}
			</tbody>
		</table>
		<Paginator bind:settings={problemsPaginationSettings} on:page={onPageChange} on:amount={onAmountChange}
				   showFirstLastButtons={state.firstLast} showPreviousNextButtons={state.previousNext}
				   controlVariant="variant-soft bg-white"
				   select="variant-soft bg-white p-2 border rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" />
	{:else if activeTab === 'myClasses'}
		<table class="min-w-full divide-y divide-gray-200 shadow-lg">
			<thead class="bg-gradient-to-tr from-teal-300 to-indigo-600 text-white">
			<tr>
				{#each classesHeaders as header}
					<th class="px-6 py-4 text-left text-xs font-medium uppercase tracking-wider first:rounded-tl-md last:rounded-tr-md">{header}</th>
				{/each}
			</tr>
			</thead>
			<tbody class="bg-white divide-y divide-gray-200">
			{#each classesBodySliced as row}
				<tr class="rounded-md">
					{#each row as cell, index}
						<td class="px-6 py-4 whitespace-nowrap {index === 0 ? 'rounded-l-md' : ''} {index === row.length - 1 ? 'rounded-r-md' : ''}">
							{#if index === 1}
								<a href="/class/{cell}" class="text-indigo-600 hover:text-indigo-900">{cell}</a>
							{:else}
								{cell}
							{/if}
						</td>
					{/each}
				</tr>
			{/each}
			</tbody>
		</table>
		<Paginator bind:settings={classesPaginationSettings} on:page={onPageChange} on:amount={onAmountChange}
				   showFirstLastButtons={state.firstLast} showPreviousNextButtons={state.previousNext}
				   controlVariant="variant-soft bg-white"
				   select="variant-soft bg-white p-2 border rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500" />
	{/if}
</div>

<style lang="postcss">
    table thead th {
        padding: 1.5rem;
    }

    table thead th:first-child {
        border-top-left-radius: 0.375rem;
        border-bottom-left-radius: 0.375rem;
    }

    table thead th:last-child {
        border-top-right-radius: 0.375rem;
        border-bottom-right-radius: 0.375rem;
    }

    table tbody tr:first-child td:first-child {
        border-bottom-left-radius: 0.375rem;
    }

    table tbody tr:first-child td:last-child {
        border-bottom-right-radius: 0.375rem;
    }

    .btn.bg-solution-btn {
        @apply bg-none border-x-2 border-y-2 text-black hover:bg-indigo-600 hover:text-white hover:border-transparent py-2 px-4 rounded-md;
    }
</style>