export async function loadTheories(){

  const res = await fetch('/artifacts/theory_graph.json',{cache:'no-store'})
  return await res.json()

}

export function applyTheoryOverlay(data){

  data.theories.forEach(t => {

    const node = document.querySelector(`[data-node="${t.source.origin_node}"]`)
    if(node){
      node.classList.add('overlay-theory')
    }

  })

}
