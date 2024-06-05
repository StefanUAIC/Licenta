<script lang="ts">
	import { type PaginationSettings, Paginator } from '@skeletonlabs/skeleton';
	import { writable } from 'svelte/store';
	import { faker } from '@faker-js/faker';

	interface User {
		name: string;
		email: string;
		rank: string;
		level: number;
		profilePicture: string;
	}

	const user = writable<User>({
		name: 'John Doe',
		email: 'john.doe@example.com',
		rank: 'Gold',
		level: 42,
		profilePicture: 'default-profile-picture.png'
	});

	let showEditProfileModal = writable(false);
	let showChangePasswordModal = writable(false);

	function editProfile() {
		showEditProfileModal.set(true);
	}

	function changePassword() {
		showChangePasswordModal.set(true);
	}

	function closeModals() {
		showEditProfileModal.set(false);
		showChangePasswordModal.set(false);
	}

	const sourceHeaders: string[] = ['Index', 'Problem Name', 'Difficulty', 'Date Solved', 'Score', 'Solutions'];
	const sourceBody = Array(27).fill(undefined).map((_, index) => [
		index + 1,
		faker.hacker.phrase(),
		['Easy', 'Medium', 'Hard'][Math.floor(Math.random() * 3)],
		faker.date.past().toLocaleDateString(),
		Math.floor(Math.random() * 101),  // Random score between 0 and 100
		faker.datatype.uuid()
	]);

	let paginationSettings = {
		page: 0,
		limit: 3,
		size: sourceBody.length,
		amounts: [1, 2, 3, 5, sourceBody.length]
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

<div class="container mx-auto my-24">
	<div class="bg-white rounded-lg shadow-lg flex p-6 h-60"> <!-- Increase the height -->
		<img src={$user.profilePicture} alt="User profile picture" class="h-full w-auto object-cover mr-6">
		<!-- Image same height as container -->
		<div class="flex-1 flex flex-col justify-center text-2xl"> <!-- Increase text size and center content -->
			<h2 class="text-4xl font-bold">{$user.name}</h2> <!-- Larger font size for name -->
			<p class="text-xl">{$user.email}</p> <!-- Increase font size for details -->
			<p class="text-xl">Rank: {$user.rank}</p>
			<p class="text-xl">Level: {$user.level}</p>
			<div class="flex justify-end mt-4 space-x-2"> <!-- Right align buttons and add space between them -->
				<button class="btn flex items-center space-x-1 bg-indigo-custom" on:click={editProfile}>
					<i class="fas fa-edit w-5 h-5"></i> <!-- Font Awesome Icon -->
					<span>Edit Profile</span>
				</button>
				<button class="btn flex items-center space-x-1 bg-teal-custom" on:click={changePassword}>
					<i class="fas fa-key w-5 h-5"></i> <!-- Font Awesome Icon -->
					<span>Change Password</span>
				</button>
			</div>
		</div>
	</div>
	<div class="mt-8">
		<h3 class="text-2xl font-bold">Sent Solutions</h3>
		<div class="w-full space-y-4 text-token mt-4">
			<table class="min-w-full divide-y divide-gray-200">
				<thead class="bg-gradient-to-br from-indigo-600 to-teal-300 text-white">
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
									<span class={getDifficultyColor(cell)}>{cell}</span>
								{:else if index === 4}
									<span class={getScoreColor(cell)}>{cell}</span>
								{:else if index === 5}
									<a href="/solution/{cell}" class="btn bg-teal-500 hover:bg-teal-700">View
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
			<Paginator
				bind:settings={paginationSettings}
				on:page={onPageChange}
				on:amount={onAmountChange}
				showFirstLastButtons={state.firstLast}
				showPreviousNextButtons={state.previousNext}
				controlVariant="variant-ghost-secondary"
				class="paginator-custom"
				select="bg-red-500"
			/>
		</div>
	</div>
</div>

{#if $showEditProfileModal}
	<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
		<div class="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
			<h2 class="text-2xl mb-4">Edit Profile</h2>
			<form>
				<div class="mb-4">
					<label class="block text-gray-700 text-sm font-bold mb-2" for="name">Name</label>
					<input
						class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
						id="name" type="text" placeholder="Name">
				</div>
				<div class="mb-4">
					<label class="block text-gray-700 text-sm font-bold mb-2" for="profilePicture">Profile
						Picture</label>
					<input
						class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
						id="profilePicture" type="file">
				</div>
				<div class="flex items-center justify-between">
					<button class="btn bg-indigo-600 hover:bg-indigo-700" type="button" on:click={closeModals}>Save
					</button>
					<button class="btn bg-gray-600 hover:bg-gray-700" type="button" on:click={closeModals}>Cancel
					</button>
				</div>
			</form>
		</div>
	</div>
{/if}

{#if $showChangePasswordModal}
	<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
		<div class="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
			<h2 class="text-2xl mb-4">Change Password</h2>
			<form>
				<div class="mb-4">
					<label class="block text-gray-700 text-sm font-bold mb-2" for="oldPassword">Old Password</label>
					<input
						class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
						id="oldPassword" type="password" placeholder="Old Password">
				</div>
				<div class="mb-4">
					<label class="block text-gray-700 text-sm font-bold mb-2" for="newPassword">New Password</label>
					<input
						class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
						id="newPassword" type="password" placeholder="New Password">
				</div>
				<div class="flex items-center justify-between">
					<button class="btn bg-indigo-600 hover:bg-indigo-700" type="button" on:click={closeModals}>Save
					</button>
					<button class="btn bg-gray-600 hover:bg-gray-700" type="button" on:click={closeModals}>Cancel
					</button>
				</div>
			</form>
		</div>
	</div>
{/if}

<style lang="postcss">
    table thead th {
        padding: 1.5rem;
    }

    table thead th:first-child {
        border-top-left-radius: 0.375rem; /* Rounded top-left corner */
    }

    table thead th:last-child {
        border-top-right-radius: 0.375rem; /* Rounded top-right corner */
    }

    table tbody tr:first-child td:first-child {
        border-bottom-left-radius: 0.375rem; /* Rounded bottom-left corner of the first row */
    }

    table tbody tr:first-child td:last-child {
        border-bottom-right-radius: 0.375rem; /* Rounded bottom-right corner of the first row */
    }


    .btn.bg-indigo-custom {
        @apply bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded;
    }

    .btn.bg-teal-custom {
        @apply bg-teal-500 hover:bg-teal-700 text-white font-bold py-2 px-4 rounded;
    }

    .paginator-custom .select.paginator-select.select.mi {
        background-color: red !important; /* Custom background color */
        color: red !important; /* Custom text color */
        border-color: red !important; /* Custom border color */
    }


</style>
