<script lang="ts">
  import { writable } from 'svelte/store';
  import { get } from 'svelte/store';
  import AceEditor from '../components/CodeEditor.svelte';

  const API_URL = import.meta.env.VITE_API_BASE_URL;

  interface TestCase {
    input: string;
    expectedOutput: string;
    actualOutput?: string;
    status?: string;
    passed?: boolean;
  }

  let source_code: string = `printf("Hello, World!")`;
  let language_id: number = 54;
  let testCases = writable<TestCase[]>([{ input: '', expectedOutput: '' }]);
  let result = writable<null | TestCase[]>(null);
  let loading = writable<boolean>(false);
  let passedCount = writable<number>(0);

  function addTestCase() {
    testCases.update(tcs => {
      tcs.push({ input: '', expectedOutput: '' });
      return tcs;
    });
  }

  async function submitCode(): Promise<void> {
    loading.set(true);
    let passed = 0;
    let currentTestCases = get(testCases);

    for (const testCase of currentTestCases) {
      let body = JSON.stringify({
        source_code,
        language_id,
        stdin: testCase.input
      });

      const response = await fetch(`${API_URL}/code_submission/submit/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: body
      });

      const data = await response.json();
	  console.log(data);
      testCase.actualOutput = data.stdout;
      testCase.status = data.status.description;
      testCase.passed = (testCase.actualOutput?.trim() || '') === testCase.expectedOutput.trim();

      if (testCase.passed) {
        passed += 1;
      }
    }

    passedCount.set(passed);
    result.set([...currentTestCases]);
    loading.set(false);
  }
</script>

<main class="p-8 bg-gray-100 min-h-screen">
  <h1 class="text-3xl font-bold mb-4">Judge0 Code Submission</h1>
  <AceEditor bind:code={source_code} />

  <div class="mb-4">
    <h2 class="text-xl font-semibold">
      Passed Test Cases: {$passedCount} / {$testCases.length}
    </h2>
  </div>

  {#each $testCases as testCase, index}
    <div class="mb-4">
      <h2 class="text-xl font-semibold">Test Case {index + 1}</h2>
      <textarea
        class="w-full p-2 mb-2 border rounded-lg"
        bind:value={testCase.input}
        rows="3"
        placeholder="Input"
      ></textarea>
      <textarea
        class="w-full p-2 mb-2 border rounded-lg"
        bind:value={testCase.expectedOutput}
        rows="3"
        placeholder="Expected Output"
      ></textarea>
    </div>
  {/each}

  <button class="btn btn-secondary mb-4" on:click={addTestCase}>Add Test Case</button>
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
          <p><strong>Input:</strong> {testCase.input}</p>
          <p><strong>Expected Output:</strong> {testCase.expectedOutput}</p>
          <p><strong>Actual Output:</strong> {testCase.actualOutput}</p>
          <p><strong>Status:</strong> {testCase.status}</p>
          <p><strong>Passed:</strong> {testCase.passed ? 'Yes' : 'No'}</p>
        </div>
      {/each}
    </div>
  {/if}
</main>

<style>
  .btn {
    @apply px-4 py-2 rounded-lg;
  }

  .btn-primary {
    @apply bg-blue-500 text-white;
  }

  .btn-secondary {
    @apply bg-gray-500 text-white;
  }
</style>
