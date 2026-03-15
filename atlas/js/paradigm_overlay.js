export async function loadParadigmEvents(){

  const res = await fetch('/artifacts/paradigm_shift_events.json',{cache:'no-store'})
  return await res.json()

}

export function applyParadigmOverlay(data){

  data.events.forEach(e => {

    if(e.event === 'paradigm_shift'){

      const node = document.querySelector(`[data-node="${e.node}"]`)
      if(node){
        node.classList.add('overlay-rupture')
      }

    }

  })

}
