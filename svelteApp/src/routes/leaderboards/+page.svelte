<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import axios from 'axios';
	import { getAuthHeaders } from '$lib/utils';
	import { getUserSolutions } from '$lib/users_api';

	const API_USERS_URL = import.meta.env.VITE_API_USERS_URL;

	interface UserProfile {
		id: number;
		username: string;
		role: string;
		email: string;
		first_name: string;
		last_name: string;
		profile_picture: {
			type: string;
			data: string;
		} | null;
		points: number;
		rank: string;
		level: number;
	}

	const users = writable<UserProfile[]>([]);
	const error = writable<string | null>(null);
	const loading = writable<boolean>(true);

	onMount(async () => {
		await fetchLeaderboard();
	});

	async function fetchLeaderboard() {
		try {
			const response = await axios.get<number[]>(`${API_USERS_URL}/`, getAuthHeaders());
			const userIds = response.data;
			const userProfiles: UserProfile[] = [];

			for (const userId of userIds) {
				const profile = await fetchProfile(userId);
				const solutions = await fetchSolutions(userId);
				const { rank, level, points } = calculateRankAndLevel(solutions);

				userProfiles.push({ ...profile, rank, level, points });
			}

			userProfiles.sort((a, b) => b.points - a.points);
			users.set(userProfiles);
		} catch (err) {
			error.set('Failed to load leaderboard');
			console.error(err);
		} finally {
			loading.set(false);
		}
	}

	async function fetchProfile(userId: number): Promise<UserProfile> {
		const response = await axios.get<UserProfile>(`${API_USERS_URL}/${userId}`, getAuthHeaders());
		return response.data;
	}

	async function fetchSolutions(userId: number): Promise<Solution[]> {
		try {
			const solutions = await getUserSolutions(userId);
			console.log(`Solutions for user ${userId}:`, solutions);
			return solutions;
		} catch (err: any) {
			console.error(`Error fetching solutions for user ${userId}:`, err.response?.data || err.message || err);
			return [];
		}
	}

	interface Solution {
		percentage_passed: number;
	}

	function calculateRankAndLevel(solutions: Solution[]): { rank: string; level: number; points: number } {
		let points = solutions.filter(solution => solution.percentage_passed === 100).length;
		const level = Math.floor(points / 10) + 1;

		let rank;
		if (points < 50) rank = 'Bronze';
		else if (points < 100) rank = 'Silver';
		else if (points < 200) rank = 'Gold';
		else rank = 'Platinum';

		return { rank, level, points };
	}
</script>

<style>
	.table {
		width: 100%;
		border-collapse: collapse;
		margin: 20px 0;
		font-size: 1.2em;
		text-align: left;
	}
	.table thead tr {
		background-color: #009879;
		color: #ffffff;
		text-align: left;
	}
	.table th {
		padding: 12px 15px;
		font-size: 1rem;
		text-align: center;
	}
	.table td {
		padding: 12px 15px;
		font-size: 1.5rem;
		text-align: center
	}
	.table tbody tr {
		border-bottom: 1px solid #dddddd;
	}
	.table tbody tr:nth-of-type(even) {
		background-color: #f3f3f3;
	}
	.table tbody tr:last-of-type {
		border-bottom: 2px solid #009879;
	}
	.profile-picture {
		width: 50px;
		height: 50px;
		border-radius: 50%;
		object-fit: cover;
		display: block;
		margin: 0 auto;
	}
</style>

<main class="max-w-8xl mx-auto p-8">
	<h1 class="text-4xl font-bold mb-8 text-center">Clasamente</h1>

	{#if $loading}
		<p class="text-center">Se încarcă clasamentele</p>
	{:else if $error}
		<p class="text-red-500 text-center">{$error}</p>
	{:else}
		<table class="table">
			<thead>
				<tr>
					<th>Poziție</th>
					<th>Poză de profil</th>
					<th>Nume de utilizator</th>
					<th>Prenume</th>
					<th>Nume</th>
					<th>Puncte</th>
					<th>Nivel</th>
					<th>Rang</th>
				</tr>
			</thead>
			<tbody>
				{#each $users as user, index}
					<tr>
						<td>{index + 1}</td>
						<td>
							{#if user.profile_picture}
								<img src={`data:${user.profile_picture.type};base64,${user.profile_picture.data}`} alt="Profile" class="profile-picture" />
							{:else}
								<img src="/default-profile-picture.png" alt="Profile" class="profile-picture" />
							{/if}
						</td>
						<td>{user.username}</td>
						<td>{user.first_name}</td>
						<td>{user.last_name}</td>
						<td>{user.points}</td>
						<td>{user.level}</td>
						<td>{user.rank}</td>
					</tr>
				{/each}
			</tbody>
		</table>
	{/if}
</main>
