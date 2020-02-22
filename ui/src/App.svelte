<script>
	import { Router, Route, Link } from 'yrv';

	import Index from './views/Index.svelte';
	import NotFound from './views/NotFound.svelte';

	import Dashboard from './views/Dashboard.svelte';
	import Query from './views/Query.svelte';
	import Export from './views/Export.svelte';
	import Modify from './views/Modify.svelte';
	import Swiper from './views/Swiper.svelte';

	export let name;

	// Router.hashchange = true;
</script>

<nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
	<Link href="/" class="navbar-brand">Dora&nbsp;<small>the DNS explorer</small></Link>
	<button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
		<span class="navbar-toggler-icon"></span>
	</button>
	<div class="collapse navbar-collapse" id="navbarCollapse">
		<ul class="navbar-nav mr-auto">
			<li class="nav-item">
				<Link href="/dashboard" class="nav-link">Dashboard</Link>
			</li>
			<li class="nav-item">
				<Link href="/query" class="nav-link">Query</Link>
			</li>
			<li class="nav-item">
				<Link href="/swiper" class="nav-link">Swiper</Link>
			</li>
		</ul>
		<!--		<form class="form-inline mt-2 mt-md-0">-->
		<!--			<input class="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search">-->
		<!--			<button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>-->
		<!--		</form>-->
	</div>
</nav>

<main role="main" class="content d-flex flex-column">
<!--	<div class="jumbotron">-->
<!--		<h1>Navbar example</h1>-->
<!--		<p class="lead">This example is a quick exercise to illustrate how fixed to top navbar works. As you scroll, it will remain fixed to the top of your browser's viewport.</p>-->
<!--		<a class="btn btn-lg btn-primary" href="../../components/navbar/" role="button">View navbar docs &raquo;</a>-->
<!--	</div>-->
	<div class="container flex-grow-1 d-flex flex-column">
		<Router nofallback>
			<Route path="/" exact component={Index} />
			<Route path="/dashboard" component={Dashboard} />
			<Route path="/query" exact component={Query} />
			<Route path="/query/:context" exact component={Query} />
			<Route path="/export/:context" exact component={Export} />
			<Route path="/modify/:context/:line" exact component={Modify} />
			<Route path="/swiper" component={Swiper} />
			<Route fallback component={NotFound} />
		</Router>
	</div>
</main>

<footer class="footer mt-auto">
	<div class="container-fluid p-3 p-md-5 text-muted">
		<ul class="">
			<li><a href="https://github.com/hnzlmnn/dora">GitHub</a></li>
			<li><a href="https://twitter.com/hnzlmnn">Twitter</a></li>
		</ul>
		<p>Dora the DNS explorer was built by <a href="mailto:malte@cybaer.ninja">Malte Heinzelmann</a> licensed under <a href="https://opensource.org/licenses/BSD-3-Clause">BSD 3 Clause</a>.</p>
	</div>
</footer>

<style>
	nav small {
		font-size: 50%;
	}

	main {
		text-align: left;
		width: 100%;
		margin: 0 auto;
		flex: 1 0 auto;
	}

	footer {
		flex-shrink: 0;
		font-size: .875rem;
	}

	footer p {
		margin-bottom: 0;
	}

	footer ul {
		padding-left: 0;
    	margin-bottom: 1rem;
	}

	footer ul li {
		display: inline-block;
	}

	footer a {
		font-weight: 600;
		color: #495057;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	.jumbotron {
		border-radius: 0;
	}

	/*@media (min-width: 640px) {*/
	/*	main {*/
	/*		max-width: none;*/
	/*	}*/
	/*}*/
</style>