<script lang="ts">
    import { toast } from "svelte-sonner";

    type Execution = {
        input: string;
        stdout: string;
        stderr: string;
        exitCode: number;
        index: number;
    };

    let code = `print('Hello from the bundled Python runtime!')`;
    let history: Execution[] = [];
    let isRunning = $state(false);
    let executionCount = $state(1);

    const runCode = async () => {
        if (!code.trim()) {
            toast.error("Enter some Python code to execute.");
            return;
        }

        isRunning = true;
        try {
            const result = await window.electronAPI.runPython(code);
            history = [
                {
                    input: code,
                    stdout: result?.stdout || "",
                    stderr: result?.stderr || "",
                    exitCode: result?.exitCode ?? 0,
                    index: executionCount,
                },
                ...history,
            ];
            executionCount += 1;
        } catch (error) {
            console.error("Failed to execute Python code", error);
            toast.error(error?.message ?? "Failed to run Python code.");
        } finally {
            isRunning = false;
        }
    };

    const clearHistory = () => {
        history = [];
        executionCount = 1;
    };
</script>

<div class="flex flex-col space-y-3">
    <div class="flex flex-col space-y-2">
        <div class="flex flex-row items-center justify-between">
            <div class="text-sm font-medium">Python REPL</div>
            <div class="flex flex-row space-x-2">
                <button
                    class="px-2 py-1 rounded-lg bg-gray-200 dark:bg-gray-850 text-xs cursor-pointer disabled:opacity-50"
                    type="button"
                    disabled={isRunning}
                    on:click={clearHistory}
                >
                    Clear
                </button>
                <button
                    class="px-2 py-1 rounded-lg bg-blue-600 text-white text-xs cursor-pointer disabled:opacity-50"
                    type="button"
                    disabled={isRunning}
                    on:click={runCode}
                >
                    {isRunning ? "Running..." : "Run"}
                </button>
            </div>
        </div>
        <div class="text-xs text-gray-500 dark:text-gray-400">
            Execute Python 3 code locally using the bundled runtime (optimized for
            macOS). Output is captured similar to an IPython session without
            leaving the desktop app.
        </div>
        <textarea
            class="w-full min-h-28 p-3 rounded-lg bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 text-sm font-mono focus:outline-none"
            bind:value={code}
            placeholder="Type Python commands here..."
        />
    </div>

    <div class="flex flex-col space-y-2">
        <div class="flex flex-row items-center justify-between text-sm font-medium">
            <div>Session Output</div>
            <div class="text-xs text-gray-500 dark:text-gray-400">
                {history.length} entr{history.length === 1 ? "y" : "ies"}
            </div>
        </div>
        {#if history.length === 0}
            <div class="text-xs text-gray-500 dark:text-gray-400 bg-gray-50 dark:bg-gray-900 border border-dashed border-gray-200 dark:border-gray-800 rounded-lg p-3">
                Run code to see results rendered here.
            </div>
        {:else}
            <div class="flex flex-col space-y-3">
                {#each history as entry (entry.index)}
                    <div class="rounded-lg bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 p-3 space-y-2">
                        <div class="flex flex-row items-center justify-between text-xs text-gray-500 dark:text-gray-400">
                            <div class="font-semibold text-gray-700 dark:text-gray-200">In [{entry.index}]</div>
                            <div>Exit {entry.exitCode}</div>
                        </div>
                        <pre class="whitespace-pre-wrap break-words text-sm font-mono text-gray-800 dark:text-gray-100 bg-white/70 dark:bg-gray-950/40 rounded-md p-2 border border-gray-200 dark:border-gray-800">
{entry.input}
                        </pre>
                        <div class="text-xs text-gray-500 dark:text-gray-400 font-semibold">
                            Out[{entry.index}]
                        </div>
                        {#if entry.stdout}
                            <pre class="whitespace-pre-wrap break-words text-sm font-mono text-gray-800 dark:text-green-200 bg-white/70 dark:bg-gray-950/40 rounded-md p-2 border border-gray-200 dark:border-gray-800">
{entry.stdout}
                            </pre>
                        {:else}
                            <div class="text-xs text-gray-500 dark:text-gray-400">(no stdout)</div>
                        {/if}
                        {#if entry.stderr}
                            <div>
                                <div class="text-xs text-gray-500 dark:text-gray-400 font-semibold">Errors</div>
                                <pre class="whitespace-pre-wrap break-words text-sm font-mono text-red-700 dark:text-red-300 bg-red-50/80 dark:bg-red-950/40 rounded-md p-2 border border-red-200 dark:border-red-700/60">
{entry.stderr}
                                </pre>
                            </div>
                        {/if}
                    </div>
                {/each}
            </div>
        {/if}
    </div>
</div>
