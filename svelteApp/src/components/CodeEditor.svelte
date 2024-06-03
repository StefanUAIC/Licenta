<script lang="ts">
  import { onMount } from 'svelte';
  import ace from 'ace-builds';
  import 'ace-builds/src-noconflict/mode-python';
  import 'ace-builds/src-noconflict/theme-github';

  export let code: string;
  let editorElement: HTMLDivElement;

  onMount(() => {
    const editor = ace.edit(editorElement, {
      mode: 'ace/mode/text',
      theme: 'ace/theme/github',
      value: code,
      tabSize: 4,
      useSoftTabs: true,
      showLineNumbers: true,
      showGutter: true,
      highlightActiveLine: true,
      wrap: true,
      fontSize: 16
    });

    editor.setOption('printMargin', false);

    editor.session.on('change', () => {
      code = editor.getValue();
    });
  });
</script>

<style>
  .editor {
    width: 100%;
    height: 400px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
</style>

<div bind:this={editorElement} class="editor"></div>
