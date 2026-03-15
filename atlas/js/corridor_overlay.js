export async function loadCorridors() {

  const res = await fetch('/artifacts/discovery_corridors.json', {cache:'no-store'})
  return await res.json()

}

export function applyCorridorOverlay(data){

  data.corridors.forEach(c => {

    const node = document.querySelector(`[data-node="${c.node}"]`)
    if(node){
      node.classList.add('overlay-corridor')
    }

  })

}
