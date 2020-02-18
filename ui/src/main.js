import App from './App.svelte';
import Api from './api';

console.log(Api);

const app = new App({
	target: document.body,
	props: {
		name: 'world'
	}
});

app.api = new Api('');

export default app;