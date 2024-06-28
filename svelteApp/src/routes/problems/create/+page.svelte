<script lang="ts">
    import {writable} from 'svelte/store';
    import CodeEditor from '../../../components/CodeEditor.svelte';
    import type {CreateProblemPayload} from '$lib/problems_api';
    import {createProblem, createTestCase} from '$lib/problems_api';
    import {verifyTestCases} from '$lib/code_submission_api';
    import {goto} from '$app/navigation';

    let title = '';
    let description = '';
    let difficulty = 'easy';
    let example_input = '';
    let example_output = '';
    let solution_code = '';
    let grade = 9;
    let category = 'arrays';
    let error = writable<string | null>(null);
    let testCases = writable<{ stdin: string; expected_output: string }[]>([{stdin: '', expected_output: ''}]);
    let memory_limit = 256;
    let time_limit = 1;
    let restrictions = '';
    let activeTestCase = writable<number>(0);
    let verificationResults = writable<{ passed: boolean; message: string }[]>([]);

    const difficultyOptions = ['easy', 'medium', 'hard'];
    const gradeOptions = [9, 10, 11, 12];
    const categoryOptions = [
        'arrays', 'linked_lists', 'sorting', 'searching', 'trees', 'graphs',
        'dynamic_programming', 'recursion', 'backtracking', 'bit_manipulation',
        'greedy', 'math', 'geometry', 'combinatorics', 'probability',
        'game_theory', 'puzzles', 'miscellaneous'
    ];

    async function handleSubmit() {
        const problem: CreateProblemPayload = {
            title,
            description,
            difficulty,
            example_input,
            example_output,
            solution_code,
            grade,
            category,
            memory_limit,
            time_limit,
            restrictions
        };

        try {
            const createdProblem = await createProblem(problem);
            const problemId = createdProblem.id;

            for (const testCase of $testCases) {
                await createTestCase(problemId, testCase);
            }

            alert('Problemă creată cu succes! Acum așteaptă să fie verificată de administrator.');
            await goto(`/problems`);
        } catch (err) {
            error.set('Failed to create problem or test cases');
            console.error('Failed to create problem or test cases:', err);
        }
    }

    function addTestCase() {
        testCases.update(cases => {
            const newCases = [...cases, { stdin: '', expected_output: '' }];
            activeTestCase.set(newCases.length - 1);
            return newCases;
        });
    }

    function removeTestCase(index: number) {
        if ($testCases.length === 1) {
            alert('You must have at least one test case');
            return;
        }
        testCases.update(cases => cases.filter((_, i) => i !== index));
        if ($activeTestCase === index) {
            activeTestCase.set(Math.max(0, index - 1));
        } else if ($activeTestCase > index) {
            activeTestCase.update(current => current - 1);
        }
    }

    function toggleTestCase(index: number) {
        activeTestCase.set(index);
    }

    function getTestCaseColor(index: number): string {
        return index === $activeTestCase
            ? 'bg-blue-200 text-blue-800'
            : 'bg-gray-200 text-gray-800';
    }

    async function handleVerifyTestCases() {
        try {
            const results = await verifyTestCases(solution_code, $testCases);
            verificationResults.set(results);
        } catch (err) {
            error.set('Failed to verify test cases');
            console.error('Failed to verify test cases:', err);
        }
    }

    function getVerificationColor(passed: boolean): string {
        return passed
            ? 'bg-green-200 text-green-800'
            : 'bg-red-200 text-red-800';
    }
</script>

<main class="min-h-screen bg-gray-100 py-10">
    <div class="max-w-7xl mx-auto px-4">
        <h1 class="text-3xl font-bold mb-6 text-center">Create Problem</h1>

        {#if $error}
            <p class="text-red-500 text-center mb-4">{$error}</p>
        {/if}

        <form on:submit|preventDefault={handleSubmit} class="space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="space-y-6">
                    <div>
                        <label class="block font-bold text-xl mb-2" for="title">Problem Title</label>
                        <input id="title" type="text" bind:value={title} required
                               class="w-full px-3 py-2 border rounded-md"/>
                    </div>

                    <div>
                        <label class="block font-bold text-xl mb-2" for="description">Problem Description</label>
                        <textarea id="description" bind:value={description} required
                                  class="w-full px-3 py-2 border rounded-md" rows="8"></textarea>
                    </div>

                    <div>
                        <label class="block font-bold text-xl mb-2" for="restrictions">Restrictions</label>
                        <textarea id="restrictions" bind:value={restrictions} required
                                  class="w-full px-3 py-2 border rounded-md" rows="4"></textarea>
                    </div>

                    <div>
                        <label class="block font-bold text-xl mb-2" for="example_input">Example Input</label>
                        <textarea id="example_input" bind:value={example_input} required
                                  class="w-full px-3 py-2 border rounded-md" rows="4"></textarea>
                    </div>

                    <div>
                        <label class="block font-bold text-xl mb-2" for="example_output">Example Output</label>
                        <textarea id="example_output" bind:value={example_output} required
                                  class="w-full px-3 py-2 border rounded-md" rows="4"></textarea>
                    </div>

                     <div>
                        <label class="block font-bold text-xl mb-2" for="difficulty">Difficulty</label>
                        <select id="difficulty" bind:value={difficulty} required class="w-full px-3 py-2 border rounded-md">
                            {#each difficultyOptions as option}
                                <option value={option}>{option.charAt(0).toUpperCase() + option.slice(1)}</option>
                            {/each}
                        </select>
                    </div>

                    <div>
                        <label class="block font-bold text-xl mb-2" for="grade">Grade</label>
                        <select id="grade" bind:value={grade} required class="w-full px-3 py-2 border rounded-md">
                            {#each gradeOptions as option}
                                <option value={option}>{option}th</option>
                            {/each}
                        </select>
                    </div>

                    <div>
                        <label class="block font-bold text-xl mb-2" for="category">Category</label>
                        <select id="category" bind:value={category} required class="w-full px-3 py-2 border rounded-md">
                            {#each categoryOptions as option}
                                <option value={option}>{option.replace('_', ' ').charAt(0).toUpperCase() + option.replace('_', ' ').slice(1)}</option>
                            {/each}
                        </select>
                    </div>

                </div>

                <div class="space-y-6">
                    <div>
                        <label class="block font-bold text-xl mb-2" for="memory_limit">Memory Limit (KB)</label>
                        <input id="memory_limit" type="number" bind:value={memory_limit} required
                               class="w-full px-3 py-2 border rounded-md"/>
                    </div>

                    <div>
                        <label class="block font-bold text-xl mb-2" for="time_limit">Time Limit (seconds)</label>
                        <input id="time_limit" type="number" bind:value={time_limit} required
                               class="w-full px-3 py-2 border rounded-md"/>
                    </div>

                    <div>
                        <label class="block font-bold text-xl mb-2" for="solution_code">Solution Code</label>
                        <CodeEditor bind:code={solution_code}/>
                    </div>

                    <div>
                        <h2 class="text-2xl font-bold mb-4">Test Cases</h2>
                        <div class="flex flex-wrap gap-2 mb-4">
                            {#each $testCases as _, index}
                                <button
                                        type="button"
                                        class={`px-4 py-2 text-lg rounded-md ${getTestCaseColor(index)} hover:opacity-80 transition-opacity`}
                                        on:click={() => toggleTestCase(index)}
                                >
                                    Test {index + 1}
                                </button>
                            {/each}
                            <button
                                    type="button"
                                    class="px-4 py-2 text-lg rounded-md bg-green-200 text-green-800 hover:opacity-80 transition-opacity"
                                    on:click={addTestCase}
                            >
                                + Add Test Case
                            </button>
                        </div>

                        {#if $activeTestCase !== null}
                            <div class="mt-4 p-4 bg-gray-100 rounded-lg">
                                <h3 class="text-xl font-semibold mb-2">Test Case {$activeTestCase + 1} Details</h3>
                                <div class="mb-4">
                                    <label class="block font-medium mb-1" for="test_case_input">Input</label>
                                    <textarea
                                            id="test_case_input"
                                            bind:value={$testCases[$activeTestCase].stdin}
                                            class="w-full px-3 py-2 border rounded-md"
                                            rows="4"
                                    ></textarea>
                                </div>
                                <div class="mb-4">
                                    <label class="block font-medium mb-1" for="test_case_output">Expected Output</label>
                                    <textarea
                                            id="test_case_output"
                                            bind:value={$testCases[$activeTestCase].expected_output}
                                            class="w-full px-3 py-2 border rounded-md"
                                            rows="4"
                                    ></textarea>
                                </div>
                                <button
                                        type="button"
                                        class="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
                                        on:click={() => removeTestCase($activeTestCase)}
                                >
                                    Remove Test Case
                                </button>
                            </div>
                        {/if}
                    </div>

                    <button type="button" class="btn btn-secondary w-full mb-4" on:click={handleVerifyTestCases}>
                        Verify Test Cases
                    </button>

                    {#if $verificationResults.length > 0}
                        <div class="mt-4">
                            <h3 class="text-xl font-semibold mb-2">Verification Results</h3>
                            <div class="flex flex-wrap gap-2">
                                {#each $verificationResults as result, index}
                                    <button
                                            type="button"
                                            class={`px-3 py-1 rounded-full ${getVerificationColor(result.passed)} hover:opacity-80 transition-opacity`}
                                    >
                                        Test {index + 1}: {result.passed ? 'Passed' : 'Failed'}
                                    </button>
                                {/each}
                            </div>
                        </div>
                    {/if}
                </div>
            </div>

            <div class="flex justify-center mt-8">
                <button type="submit" class="btn btn-primary px-8 py-3 text-lg">Create Problem</button>
            </div>
        </form>
    </div>
</main>

<style lang="postcss">
    .btn {
        @apply px-4 py-2 rounded-lg;
    }

    .btn-primary {
        @apply bg-blue-500 text-white hover:bg-blue-600 transition-colors;
    }

    .btn-secondary {
        @apply bg-gray-500 text-white hover:bg-gray-600 transition-colors;
    }
</style>