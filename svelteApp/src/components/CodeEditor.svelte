<script lang="ts">
	import { afterUpdate, onMount } from 'svelte';
	import ace from 'ace-builds';
	import 'ace-builds/src-noconflict/theme-dreamweaver';

	import 'ace-builds/src-noconflict/mode-c_cpp';
	import 'ace-builds/src-noconflict/mode-python';
	import 'ace-builds/src-noconflict/mode-javascript';
	import 'ace-builds/src-noconflict/mode-java';
	import 'ace-builds/src-noconflict/mode-assembly_x86';
	import 'ace-builds/src-noconflict/mode-sh';
	import 'ace-builds/src-noconflict/mode-vbscript';
	import 'ace-builds/src-noconflict/mode-clojure';
	import 'ace-builds/src-noconflict/mode-csharp';
	import 'ace-builds/src-noconflict/mode-cobol';
	import 'ace-builds/src-noconflict/mode-lisp';
	import 'ace-builds/src-noconflict/mode-d';
	import 'ace-builds/src-noconflict/mode-elixir';
	import 'ace-builds/src-noconflict/mode-erlang';
	import 'ace-builds/src-noconflict/mode-fsharp';
	import 'ace-builds/src-noconflict/mode-fortran';
	import 'ace-builds/src-noconflict/mode-golang';
	import 'ace-builds/src-noconflict/mode-groovy';
	import 'ace-builds/src-noconflict/mode-haskell';
	import 'ace-builds/src-noconflict/mode-kotlin';
	import 'ace-builds/src-noconflict/mode-lua';
	import 'ace-builds/src-noconflict/mode-objectivec';
	import 'ace-builds/src-noconflict/mode-ocaml';
	import 'ace-builds/src-noconflict/mode-pascal';
	import 'ace-builds/src-noconflict/mode-perl';
	import 'ace-builds/src-noconflict/mode-php';
	import 'ace-builds/src-noconflict/mode-prolog';
	import 'ace-builds/src-noconflict/mode-r';
	import 'ace-builds/src-noconflict/mode-ruby';
	import 'ace-builds/src-noconflict/mode-rust';
	import 'ace-builds/src-noconflict/mode-scala';
	import 'ace-builds/src-noconflict/mode-sql';
	import 'ace-builds/src-noconflict/mode-swift';
	import 'ace-builds/src-noconflict/mode-typescript';

	export let code: string;
	export let languageId: number;
	let editorElement: HTMLDivElement;
	let editor: ace.Ace.Editor;

	const languageIdToMode: { [key: number]: string } = {
		45: 'assembly_x86',
		46: 'sh',
		47: 'vbscript',
		75: 'c_cpp',
		76: 'c_cpp',
		48: 'c_cpp',
		52: 'c_cpp',
		49: 'c_cpp',
		53: 'c_cpp',
		50: 'c_cpp',
		54: 'c_cpp',
		86: 'clojure',
		51: 'csharp',
		77: 'cobol',
		55: 'lisp',
		56: 'd',
		57: 'elixir',
		58: 'erlang',
		44: 'text',
		87: 'fsharp',
		59: 'fortran',
		60: 'golang',
		88: 'groovy',
		61: 'haskell',
		62: 'java',
		63: 'javascript',
		78: 'kotlin',
		64: 'lua',
		89: 'text',
		79: 'objectivec',
		65: 'ocaml',
		66: 'matlab',
		67: 'pascal',
		85: 'perl',
		68: 'php',
		43: 'text',
		69: 'prolog',
		70: 'python',
		71: 'python',
		80: 'r',
		72: 'ruby',
		73: 'rust',
		81: 'scala',
		82: 'sql',
		83: 'swift',
		74: 'typescript',
		84: 'vbscript'
	};

	function getMode(langId: number): string {
		return languageIdToMode[langId] || 'text';
	}

	onMount(() => {
		editor = ace.edit(editorElement, {
			mode: `ace/mode/text`,
			theme: 'ace/theme/dreamweaver',
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

		const initialMode = getMode(languageId);
		editor.session.setMode(`ace/mode/${initialMode}`);
	});

	afterUpdate(() => {
		if (editor) {
			const mode = getMode(languageId);
			editor.session.setMode(`ace/mode/${mode}`);
		}
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