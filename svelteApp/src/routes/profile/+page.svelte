<script lang="ts">
    import {type PaginationSettings, Paginator} from '@skeletonlabs/skeleton';
    import {type Writable, writable} from 'svelte/store';
    import {faker} from '@faker-js/faker';
    import {onMount} from 'svelte';
    import type {ProfileSchema} from "$lib/profile_api";
    import {getProfile} from '$lib/profile_api';

    interface ExtendedProfileSchema extends ProfileSchema {
        rank: string;
        level: number;
        profilePicture: string;
    }

    let user: Writable<ExtendedProfileSchema | null> = writable(null);
    const error: Writable<string | null> = writable(null);

    const fetchProfile = async () => {
        try {
            const data = await getProfile(1);
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
        }
    };

    onMount(() => {
        fetchProfile().then(data => user.set(data));
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

    let activeTab = writable('sentSolutions');
</script>

<main>
    <div class="container mx-auto my-24">
        {#await fetchProfile() then profile}
            <div class="bg-white rounded-lg shadow-lg flex p-6 h-60">
                <img src={profile.profilePicture} alt="User profile picture" class="h-full w-auto object-cover mr-6">
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
        {:catch error}
            <p class="text-red-500">Error loading profile: {error.message}</p>
        {/await}

        {#if $showEditProfileModal}
            <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center modal">
                <div class="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
                    <h2 class="text-2xl mb-4">Edit Profile</h2>
                    <form class="z-50">
                        <div class="mb-4">
                            <label class="block text-gray-700 text-sm font-bold mb-2" for="firstname">First Name</label>
                            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                   id="firstname" type="text" placeholder="First Name">
                        </div>
                        <div class="mb-4">
                            <label class="block text-gray-700 text-sm font-bold mb-2" for="lastname">Last Name</label>
                            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                   id="lastname" type="text" placeholder="Last Name">
                        </div>
                        <div class="mb-4">
                            <label class="block text-gray-700 text-sm font-bold mb-2" for="profilePicture">Profile
                                Picture</label>
                            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                   id="profilePicture" type="file">
                        </div>
                        <div class="flex items-center justify-between">
                            <button class="btn bg-indigo-custom" type="button" on:click={closeModals}>Save</button>
                            <button class="btn bg-gray-600 hover:bg-gray-700 rounded-md text-white" type="button"
                                    on:click={closeModals}>Cancel
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        {/if}

        {#if $showChangePasswordModal}
            <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center modal">
                <div class="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
                    <h2 class="text-2xl mb-4">Change Password</h2>
                    <form>
                        <div class="mb-4">
                            <label class="block text-gray-700 text-sm font-bold mb-2" for="oldPassword">Old
                                Password</label>
                            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                   id="oldPassword" type="password" placeholder="Old Password">
                        </div>
                        <div class="mb-4">
                            <label class="block text-gray-700 text-sm font-bold mb-2" for="newPassword">New
                                Password</label>
                            <input class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                   id="newPassword" type="password" placeholder="New Password">
                        </div>
                        <div class="flex items-center justify-between">
                            <button class="btn bg-indigo-custom" type="button" on:click={closeModals}>Save</button>
                            <button class="btn bg-gray-600 hover:bg-gray-700 rounded-md text-white" type="button"
                                    on:click={closeModals}>Cancel
                            </button>
                        </div>
                    </form>
                </div>
            </div>
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

        {#if $activeTab === 'sentSolutions'}
            <div class="w-full space-y-4 text-token mt-4">
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
                                        <a href="/problem/{cell}"
                                           class="text-indigo-600 hover:text-indigo-900">{cell}</a>
                                    {:else if index === 2}
                                        <span class={getDifficultyColor(cell)}>{cell}</span>
                                    {:else if index === 4}
                                        <span class={getScoreColor(cell)}>{cell}</span>
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
                           select="variant-soft bg-white p-2 border rounded-md focus:outline-none focus:ring-indigo-500  focus:border-indigo-500"/>
            </div>
        {:else if $activeTab === 'problemsProposed'}
            <div class="w-full space-y-4 text-token mt-4">
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
                                        <a href="/problem/{cell}"
                                           class="text-indigo-600 hover:text-indigo-900">{cell}</a>
                                    {:else if index === 2}
                                        <span class={getDifficultyColor(cell)}>{cell}</span>
                                    {:else if index === 4}
                                        <span class={cell === 'Pending' ? 'text-yellow-500' : cell === 'Approved' ? 'text-green-500' : 'text-red-500'}>{cell}</span>
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
                           select="variant-soft bg-white p-2 border rounded-md focus:outline-none focus:ring-indigo-500  focus:border-indigo-500"/>
            </div>
        {:else if $activeTab === 'myClasses'}
            <div class="w-full space-y-4 text-token mt-4">
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
                           select="variant-soft bg-white p-2 border rounded-md focus:outline-none focus:ring-indigo-500  focus:border-indigo-500"/>
            </div>
        {/if}
    </div>
</main>

<style lang="postcss">
    table thead th {
        padding: 1.5rem;
    }

    table thead th:first-child {
        border-top-left-radius: 0.375rem;
    }

    table thead th:last-child {
        border-top-right-radius: 0.375rem;
    }

    table tbody tr:first-child td:first-child {
        border-bottom-left-radius: 0.375rem;
    }

    table tbody tr:first-child td:last-child {
        border-bottom-right-radius: 0.375rem;
    }

    .btn.bg-indigo-custom {
        @apply bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded;
    }

    .btn.bg-teal-custom {
        @apply bg-teal-500 hover:bg-teal-600 text-white font-bold py-2 px-4 rounded;
    }

    .btn.bg-solution-btn {
        @apply bg-none border-x-2 border-y-2 text-black hover:bg-indigo-600 hover:text-white hover:border-transparent py-2 px-4 rounded-md;
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

    .modal {
        z-index: 3;
    }
</style>
