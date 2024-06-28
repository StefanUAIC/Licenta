<script lang="ts">
	import { type Writable, writable } from 'svelte/store';
	import { onMount } from 'svelte';
	import { getProfile, type ProfileSchema } from '$lib/users_api';
	import { getCookie, getUserIDFromJWT } from '$lib/utils';
	import ChangePasswordModal from '../../components/ChangePasswordModal.svelte';
	import EditProfileModal from '../../components/EditProfileModal.svelte';
	import ProfileTable from '../../components/ProfileTable.svelte';

	let profilePromise: Promise<ExtendedProfileSchema> | null = null;
	let user_id: number;
	let loading = true;

	interface ExtendedProfileSchema extends ProfileSchema {
		rank: string;
		level: number;
		profilePicture: string;
	}

	const error: Writable<string | null> = writable(null);

	const fetchProfile = async (user_id: number) => {
		try {
			const data = await getProfile(user_id);
			return {
				...data,
				rank: 'Gold',
				level: 42,
				profilePicture: 'https://randomuser.me/api/portraits/men/1.jpg'
			};
		} catch (err) {
			console.error('Failed to load profile:', err);
			error.set('Failed to load profile');
			throw err;
		} finally {
			loading = false;
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
	}

	function changePassword() {
		showChangePasswordModal.set(true);
	}

	function closeChangePasswordModal() {
		showChangePasswordModal.set(false);
	}

	let activeTab = writable('sentSolutions');
</script>

<main>
	<div class="container mx-auto my-24">
		{#if loading}
			<p class="text-center text-2xl">Loading profile...</p>
		{/if}
		{#await profilePromise then profile}
			{#if profile}
				<div class="bg-white rounded-lg shadow-lg flex p-6 h-60">
					<img src={profile.profilePicture}
						 alt={'Profile picture of ' + profile.first_name + ' ' + profile.last_name}
						 class="h-full w-auto object-cover mr-6">
					<div class="flex-1 flex flex-col justify-center text-2xl">
						<h2 class="text-4xl font-bold">{profile.first_name} {profile.last_name}</h2>
						<p class="text-xl">{profile.email}</p>
						<p class="text-xl">Rank: {profile.rank}</p>
						<p class="text-xl">Level: {profile.level}</p>
						<p class="text-xl">Role: {profile.role}</p>
						<div class="flex justify-end mt-4 space-x-2">
							<button class="btn flex items-center space-x-1 bg-indigo-custom" on:click={editProfile}>
								<i class="fas fa-edit w-5 h-5"></i>
								<span>Edit Profile</span>
							</button>
							<button class="btn flex items-center space-x-1 bg-teal-custom" on:click={changePassword}>
								<i class="fas fa-key w-5 h-5"></i>
								<span>Change Password</span>
							</button>
						</div>
					</div>
				</div>
			{/if}
		{:catch error}
			<p class="text-red-500">Error loading profile: {error.message}</p>
		{/await}

		{#if $showEditProfileModal}
			<EditProfileModal
				showModal={$showEditProfileModal}
				on:close={closeEditProfileModal}
			/>
		{/if}

		{#if $showChangePasswordModal}
			<ChangePasswordModal
				showModal={$showChangePasswordModal}
				on:close={closeChangePasswordModal}
			/>
		{/if}

		<div class="nav-container mt-8 pt-8">
			<div class="flex space-x-4 mb-4">
				<button class="cursor-pointer text-lg" class:active={$activeTab === 'sentSolutions'}
						on:click={() => activeTab.set('sentSolutions')}>Sent Solutions
				</button>
				<button class="cursor-pointer text-lg" class:active={$activeTab === 'problemsProposed'}
						on:click={() => activeTab.set('problemsProposed')}>Problems Proposed
				</button>
				<button class="cursor-pointer text-lg" class:active={$activeTab === 'myClasses'}
						on:click={() => activeTab.set('myClasses')}>My Classes
				</button>
			</div>
		</div>

		<ProfileTable activeTab={$activeTab} />
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
</style>