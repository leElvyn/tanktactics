
import { persisted } from "$lib/stores/localStore";
export let messages = persisted<string[]>("logs", []);

export function addMessage(text: string) {
    messages.update((old: string[]) => [text, ...old])
}