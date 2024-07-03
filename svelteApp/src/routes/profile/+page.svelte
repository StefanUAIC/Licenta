<script lang="ts">
	import { type Writable, writable } from 'svelte/store';
	import { onMount } from 'svelte';
	import { getProfile, getUserSolutions, type ProfileSchema } from '$lib/users_api';
	import { type Solution } from '$lib/homeworks_api';
	import { getCookie, getUserIDFromJWT } from '$lib/utils';
	import ChangePasswordModal from '../../components/ChangePasswordModal.svelte';
	import EditProfileModal from '../../components/EditProfileModal.svelte';
	import ProfileTable from '../../components/ProfileTable.svelte';

	let profilePromise: Promise<ProfileSchema & { rank: string; level: number; points: number }> | null = null;
	let user_id: number;

	const error: Writable<string | null> = writable(null);

	function calculateRankAndLevel(solutions: Solution[]): { rank: string; level: number; points: number } {
		let points = solutions.filter(solution => solution.percentage_passed === 100).length;
		const level = Math.floor(points / 10) + 1;

		let rank;
		if (points < 50) rank = 'Bronze';
		else if (points < 100) rank = 'Silver';
		else if (points < 200) rank = 'Gold';
		else rank = 'Diamond';

		return { rank, level, points };
	}

	const fetchProfile = async (user_id: number) => {
		try {
			const profileData = await getProfile(user_id);
			const solutionsData = await getUserSolutions(user_id);
			const { rank, level, points } = calculateRankAndLevel(solutionsData);
			return {
				...profileData,
				rank,
				level,
				points
			};
		} catch (err) {
			console.error('Failed to load profile:', err);
			error.set('Failed to load profile');
			throw err;
		}
	};

	onMount(() => {
		let access_token = getCookie('access');
		if (access_token) {
			user_id = getUserIDFromJWT(access_token);
			profilePromise = fetchProfile(user_id);
		} else {
			profilePromise = Promise.reject(new Error('No access token found'));
		}
	});

	let showEditProfileModal = writable(false);
	let showChangePasswordModal = writable(false);

	function editProfile() {
		showEditProfileModal.set(true);
	}

	function closeEditProfileModal() {
		showEditProfileModal.set(false);
		profilePromise = fetchProfile(user_id);
	}

	function changePassword() {
		showChangePasswordModal.set(true);
	}

	function closeChangePasswordModal() {
		showChangePasswordModal.set(false);
	}

	function getRankColor(rank: string): string {
		switch (rank) {
			case 'Bronze':
				return 'text-amber-600';
			case 'Silver':
				return 'text-gray-400';
			case 'Gold':
				return 'text-yellow-400';
			case 'Diamond':
				return 'text-blue-400';
			default:
				return 'text-gray-700';
		}
	}

	function getProgressToNextLevel(level: number, experience: number): number {
		const expForCurrentLevel = (level - 1) * 10;
		const expToNextLevel = level * 10;
		const progressExp = experience - expForCurrentLevel;
		return (progressExp / (expToNextLevel - expForCurrentLevel)) * 100;
	}

	let activeTab = writable('sentSolutions');
</script>

<main class="min-h-screen bg-gray-100">
	<div class="container mx-auto py-24 px-4">
		<div class="bg-white rounded-lg shadow-lg p-6 mb-8">
			{#await profilePromise}
				<p class="text-center text-2xl">Loading profile...</p>
			{:then profile}
				{#if profile}
					<div class="flex h-60">
						<div class="w-1/4 mr-6">
							<img
								src={profile.profile_picture ? `data:image/${profile.profile_picture.type};base64,${profile.profile_picture.data}` : '/default-profile-picture.png'}
								alt={'Profile picture of ' + profile.first_name + ' ' + profile.last_name}
								class="w-full h-full object-cover rounded-lg shadow-md">
						</div>
						<div class="w-1/2 flex flex-col justify-between">
							<div>
								<p class="text-xl mb-2"><span
									class="font-semibold">Name:</span> {profile.first_name} {profile.last_name}</p>
								<p class="text-xl mb-4"><span class="font-semibold">Email:</span> {profile.email}</p>
								<div class="mb-2">
									<span class="text-2xl font-semibold mr-2">Level {profile.level}</span>
									<div class="w-full bg-gray-200 rounded-full h-4">
										<div
											class="bg-green-500 h-4 rounded-full"
											style="width: {getProgressToNextLevel(profile.level, profile.points)}%"
										></div>
									</div>
								</div>
								<p class="text-lg">Experience: <span class="font-semibold">{profile.points}</span></p>
							</div>
							<div
								class="text-center py-1 px-3 bg-indigo-100 rounded-lg text-indigo-800 text-xl font-semibold w-1/5">
								{profile.role === 'teacher' ? '👨‍🏫 Teacher' : '👨‍🎓 Student'}
							</div>
							<div class="flex mt-2 space-x-2">
								<button class="btn flex items-center space-x-1 bg-indigo-custom" on:click={editProfile}>
									<i class="fas fa-edit w-5 h-5"></i>
									<span>Edit Profile</span>
								</button>
								<button class="btn flex items-center space-x-1 bg-teal-custom"
										on:click={changePassword}>
									<i class="fas fa-key w-5 h-5"></i>
									<span>Change Password</span>
								</button>
							</div>
						</div>
						<div class="w-1/4 flex flex-col items-center justify-center">
							<div class="text-center mb-4">
								<span class={`text-3xl font-bold ${getRankColor(profile.rank)}`}>{profile.rank}</span>
							</div>
							<img
								src="{profile.rank.toLowerCase()}.png"
								alt="{profile.rank} rank"
								class="w-56 h-56 object-contain"
							>
						</div>
					</div>

					{#if $showEditProfileModal}
						<EditProfileModal
							showModal={$showEditProfileModal}
							firstName={profile.first_name}
							lastName={profile.last_name}
							userId={user_id}
							on:close={closeEditProfileModal}
						/>
					{/if}
				{/if}
			{:catch error}
				<p class="text-red-500">Error loading profile: {error.message}</p>
			{/await}
		</div>
		{#if $showChangePasswordModal}
			<ChangePasswordModal
				showModal={$showChangePasswordModal}
				on:close={closeChangePasswordModal}
			/>
		{/if}

		<div class="bg-white rounded-lg shadow-lg p-6">
			<div class="nav-container mb-8">
				<div class="flex space-x-4 mb-4">
					<button class="cursor-pointer text-lg" class:active={$activeTab === 'sentSolutions'}
							on:click={() => activeTab.set('sentSolutions')}>Sent Solutions
					</button>
					{#await profilePromise}
						<!-- Loading profile -->
					{:then profile}
						{#if profile && profile.role === 'teacher'}
							<button class="cursor-pointer text-lg" class:active={$activeTab === 'problemsProposed'}
									on:click={() => activeTab.set('problemsProposed')}>Problems Proposed
							</button>
						{:else}
							<button class="cursor-pointer text-lg" class:active={$activeTab === 'myHomeworks'}
									on:click={() => activeTab.set('myHomeworks')}>My Homeworks
							</button>
						{/if}
					{/await}
					<button class="cursor-pointer text-lg" class:active={$activeTab === 'myClasses'}
							on:click={() => activeTab.set('myClasses')}>My Classes
					</button>
				</div>
			</div>

			<ProfileTable activeTab={$activeTab} />
		</div>
	</div>
</main>
<style lang="postcss">
    .btn.bg-indigo-custom {
        @apply bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded;
    }

    .btn.bg-teal-custom {
        @apply bg-teal-500 hover:bg-teal-600 text-white font-bold py-2 px-4 rounded;
    }

    .nav-container {
        position: relative;
        z-index: 1;
    }

    .nav-container::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 2px;
        z-index: 0;
        background-color: rgb(55, 65, 81, 0.2);
    }

    .cursor-pointer {
        cursor: pointer;
        padding: 0.5rem 1rem;
        position: relative;
        color: rgb(55, 65, 81, 0.5);
        z-index: 2;
    }

    .cursor-pointer.active {
        color: rgb(55, 65, 81, 1);
        z-index: 1;
    }

    .cursor-pointer.active::after {
        content: '';
        position: absolute;
        bottom: 1px;
        left: 0;
        width: 100%;
        height: 4px;
        background-color: #5699dc;
    }

    .bg-indigo-custom {
        @apply bg-indigo-600 hover:bg-indigo-700 text-white;
    }

    .bg-teal-custom {
        @apply bg-teal-500 hover:bg-teal-600 text-white;
    }
</style>