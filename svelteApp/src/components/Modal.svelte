<script lang="ts">
    export let show: boolean;
    export let onClose: () => void;

    const closeModal = () => {
        onClose();
    };

    const stopPropagation = (event: MouseEvent) => {
        event.stopPropagation();
    };

    const handleKeydown = (event: KeyboardEvent) => {
        if (event.key === 'Escape') {
            closeModal();
        }
    };
</script>

<style>
    .modal-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .modal-content {
        background: white;
        padding: 20px;
        border-radius: 5px;
        width: 90%;
        max-width: 500px;
        position: relative;
    }

    .close-button {
        background: none;
        border: none;
        font-size: 1.5rem;
        position: absolute;
        top: 10px;
        right: 10px;
        cursor: pointer;
    }
</style>

{#if show}
    <div class="modal-background" role="dialog" aria-modal="true" tabindex="-1" on:click={closeModal} on:keydown={handleKeydown}>
        <div class="modal-content" on:click={stopPropagation}>
            <button class="close-button" on:click={closeModal} aria-label="Close">&times;</button>
            <slot></slot>
        </div>
    </div>
{/if}
