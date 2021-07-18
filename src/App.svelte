<script>
	let lines = []
	let hovering = -1;
	let mousedown = false;
	let remaining = 0;
	async function getMoreLines(){
		let req = await fetch('http://localhost:5004/lineset')
		let data = await req.json()
		lines = data.lines.map(line=>({
			text:line,
			isLyric:false
		}))
		remaining = data.remaining
	}
	getMoreLines()
	let lastIndex = -1
	let lastState = true
	$: {
		if(!mousedown){
			lastIndex = -1
		}
		if(mousedown && hovering>-1){
			if(lastIndex == -1){
				lastIndex = hovering
				lastState = !lines[hovering].isLyric
			} 
			for(let i = 0; i<=Math.abs(lastIndex-hovering); i++){
				lines[Math.min(hovering, lastIndex)+i].isLyric = lastState
			}
		}
	}
	async function send(){
		await fetch('http://localhost:5004/save', {method:'post', body:JSON.stringify(lines)})
		await getMoreLines()
	}
</script>

<main on:mousedown={_=>mousedown=true} on:mouseup={_=>mousedown=false} on:mouseleave={_=>hovering=-1}>
	<p style="background-color: #222; position: sticky; flex-shrink: 0; top:0; left:0; margin:0;" on:mouseover={_=>hovering=-1}>
		<button on:click={_=>lines = lines.map(line=>({...line, isLyric:false}))}>Clear</button>
		<button on:click={send}>Send</button>
		<button>Skip</button>
		<br>
		<span style=" background-color: #222;">
			{lines.reduce((count, item)=>count+(item.isLyric?1:0), 0)} lines selected <br> {remaining} linesets remaining
		</span>
	</p>
	<div style="flex: 1;">
		{#each lines as line, i}
			<pre class={`${line.isLyric ? 'selected' : null}`} on:mouseenter={_=>hovering=i}>{i}	{line.text}</pre>
		{/each}
	</div>
</main>

<style>
	pre{
		margin: 0;
	}

	.selected {
		background-color: rgb(46, 61, 66);
	}

	main {
		/* text-align: center; */
		user-select: none;
		padding: 1em;
		box-sizing: border-box;
		margin: 0;
		display: flex;
		gap: 2em;
		position: relative;
		height: 100vh;
		overflow: auto;
		align-items: flex-start;
		justify-content: flex-start;
	}
</style>