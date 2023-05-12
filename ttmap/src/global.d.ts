
declare interface Window {
	map: HTMLElement;
	game: Game;
	gamePromise: Promise<Game>;
	gamePromiseResolve: (value: Game | PromiseLike<Game>) => void;
}