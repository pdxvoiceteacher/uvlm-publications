export async function loadHypotheses(){

  const res = await fetch('/artifacts/hypothesis_candidates.json',{cache:'no-store'})
  return await res.json()

}

export function applyHypothesisOverlay(data){

  data.hypotheses.forEach(h => {

    const node = document.querySelector(`[data-node="${h.origin_node}"]`)
    if(node){
      node.classList.add('overlay-hypothesis')
    }

  })

}
