<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import CodeEditor from '../../../components/CodeEditor.svelte';
    import { getProblemById, getTestCasesByProblemId, type ProblemSchema, type TestCase } from '$lib/problems_api';
    import { get, writable } from 'svelte/store';

    const API_CODE_SUBMISSION_URL = import.meta.env.VITE_API_SUBMISSIONS_URL;

    const problem = writable<ProblemSchema | null>(null);
    const error = writable<string | null>(null);
    const slug = $page.params.slug;
    let source_code = ``;
    let language_id = 54;
    let testCases = writable<TestCase[]>([]);
    let result = writable<TestCase[]>([]);
    let loading = writable(false);
    let passedCount = writable(0);

    const fetchProblem = async () => {
        try {
            const data = await getProblemById(Number(slug));
            problem.set(data);
        } catch (err) {
            console.error('Failed to load problem:', err);
            error.set('Failed to load problem');
        }
    };

    const fetchTestCases = async () => {
        try {
            const data = await getTestCasesByProblemId(Number(slug));
            testCases.set(data);
        } catch (err) {
            console.error('Failed to load test cases:', err);
            error.set('Failed to load test cases');
        }
    };

    onMount(() => {
        fetchProblem();
    });

    async function submitCode() {
        loading.set(true);
        await fetchTestCases();
        let passed = 0;
        const currentTestCases = get(testCases);

        for (const testCase of currentTestCases) {
            const body = JSON.stringify({
                source_code,
                language_id,
                stdin: testCase.stdin
            });

            const response = await fetch(`${API_CODE_SUBMISSION_URL}/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: body
            });

            const data = await response.json();
            testCase.actualOutput = data.stdout;
            testCase.status = data.status.description;
            testCase.passed = (testCase.actualOutput?.trim() || '') === testCase.expected_output.trim();

            if (testCase.passed) {
                passed += 1;
            }
        }

        passedCount.set(passed);
        result.set([...currentTestCases]);
        loading.set(false);
    }
</script>

<main class="min-h-screen bg-gray-100 py-10">
    <div class="max-w-6xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-2 gap-6">
        {#if $error}
            <p class="text-red-500 text-center mb-4">{$error}</p>
        {/if}

        {#if $problem}
            <div class="bg-white p-6 rounded-lg shadow-md">
                <h1 class="text-3xl font-bold mb-4">{$problem.title}</h1>
                <p class="text-gray-700 mb-4">{$problem.description}</p>
                <div class="mb-4">
                    <p><strong>Difficulty:</strong> {$problem.difficulty}</p>
                    <p><strong>Grade:</strong> {$problem.grade}</p>
                    <p><strong>Category:</strong> {$problem.category}</p>
                </div>
                <div class="mb-4">
                    <h2 class="text-xl font-semibold mb-2">Example Input</h2>
                    <pre class="bg-gray-200 p-2 rounded">{$problem.example_input}</pre>
                </div>
                <div>
                    <h2 class="text-xl font-semibold mb-2">Example Output</h2>
                    <pre class="bg-gray-200 p-2 rounded">{$problem.example_output}</pre>
                </div>
            </div>
        {/if}

        <div>
            {#if $problem}
                <CodeEditor bind:code={source_code} />
                <div class="mb-4">
                    <h2 class="text-xl font-semibold">Passed Test Cases: {$passedCount}</h2>
                </div>

                <button class="btn btn-primary mb-4" on:click={submitCode}>Submit Code</button>

                {#if $loading}
                    <p class="text-blue-500">Loading...</p>
                {/if}

                {#if $result}
                    <h2 class="text-2xl font-semibold mt-4">Results:</h2>
                    <div>
                        {#each $result as testCase, index}
                            <div class="p-4 bg-white border rounded-lg mb-4">
                                <h3 class="text-xl font-semibold">Test Case {index + 1}</h3>
                                <p><strong>Status:</strong> {testCase.status}</p>
                                <p><strong>Passed:</strong> {testCase.passed ? 'Yes' : 'No'}</p>
                            </div>
                        {/each}
                    </div>
                {/if}
            {/if}
        </div>
    </div>
</main>

<style>
    .btn {
        @apply px-4 py-2 rounded-lg;
    }

    .btn-primary {
        @apply bg-blue-500 text-white;
    }
</style>
