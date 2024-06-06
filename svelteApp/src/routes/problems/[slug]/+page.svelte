<script lang="ts">
    import { onMount } from 'svelte';
    import { page } from '$app/stores';
    import CodeEditor from '../../../components/CodeEditor.svelte';
    import { getProblemById, type ProblemSchema } from '$lib/problems_api';
    import { type CodeSubmissionResult, type CodeSubmissionSchema, submitCode, fetchLanguages } from '$lib/code_submission_api';
    import { writable } from 'svelte/store';

    const problem = writable<ProblemSchema | null>(null);
    const error = writable<string | null>(null);
    const slug = $page.params.slug;
    let source_code = ``;
    let language_id = writable(54);
    let result = writable<CodeSubmissionResult[]>([]);
    let loading = writable(false);
    let passedCount = writable(0);
    let languages = writable<{ id: number; name: string }[]>([]);

    const fetchProblem = async () => {
        try {
            const data = await getProblemById(Number(slug));
            problem.set(data);
        } catch (err) {
            console.error('Failed to load problem:', err);
            error.set('Failed to load problem');
        }
    };

    onMount(() => {
        fetchProblem();
        fetchLanguagesData();
    });

    const fetchLanguagesData = async () => {
        try {
            const data = await fetchLanguages();
            languages.set(data);
        } catch (err) {
            console.error('Failed to load languages:', err);
            error.set('Failed to load languages');
        }
    };

    async function submitCodeHandler() {
        loading.set(true);

        const submission: CodeSubmissionSchema = {
            source_code,
            language_id: $language_id,
            problem_id: Number(slug)
        };

        try {
            const results = await submitCode(submission);
            let passed = 0;
            results.forEach(testCase => {
                if (testCase.passed) {
                    passed += 1;
                }
            });

            passedCount.set(passed);
            result.set(results);
            console.log('Results:', results);
        } catch (err) {
            console.error('Failed to submit code:', err);
            error.set('Failed to submit code');
        } finally {
            loading.set(false);
        }
    }
</script>

<main class="min-h-screen bg-gray-100 py-10">
    <div class="max-w-6xl mx-auto px-4 grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="col-span-1 lg:col-span-2">
            <div class="h-8">
                {#if $error}
                    <p class="text-red-500 text-center">{$error}</p>
                {/if}
            </div>
        </div>

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
                <div class="mb-4">
                    <label for="language" class="block text-lg font-medium text-gray-700 mb-2">Select Language</label>
                    <select id="language" class="block w-full p-2 border border-gray-300 rounded-lg" bind:value={$language_id}>
                        {#each $languages as language}
                            <option value={language.id}>{language.name}</option>
                        {/each}
                    </select>
                </div>
                <CodeEditor bind:code={source_code} />
                <div class="mb-4">
                    <h2 class="text-xl font-semibold">Passed Test Cases: {$passedCount}</h2>
                </div>

                <button class="btn btn-primary mb-4" on:click={submitCodeHandler}>Submit Code</button>

                {#if $loading}
                    <p class="text-blue-500">Loading...</p>
                {/if}

                {#if $result}
                    <h2 class="text-2xl font-semibold mt-4">Results:</h2>
                    <div>
                        {#each $result as testCase, index}
                            <div class="p-4 bg-white border rounded-lg mb-4">
                                <h3 class="text-xl font-semibold">Test Case {index + 1}</h3>
                                <p><strong>Status:</strong> {testCase.status || 'Rejected'}</p>
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
