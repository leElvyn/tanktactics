export async function registerGestures(mapDiv: HTMLElement) {
    map = mapDiv;
    mapcontainer = map.parentElement;
    dragElement(map);
    mobileDragElement(map);
    map.style.transform = "scale(1.01)";
    document.body.onwheel = wheelEvent;
    // @ts-ignore
    let mc = new Hammer(document.body);
    // @ts-ignore
    let pinch = new Hammer.Pinch();

    mc.add(pinch)

    mc.on("pinch", function(ev) { 
        //MOTHER FUCKING FUCK THIS SHIT
    })

}

var pz;
var scale = 1.01;
var realScale = 0.01;
var map: HTMLElement;
var mapcontainer: HTMLElement;

function dragElement(elmnt: HTMLElement) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    /* otherwise, move the DIV from anywhere inside the DIV:*/
    document.body.onmousedown = dragMouseDown;

    function dragMouseDown(e: MouseEvent) {
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }

    function elementDrag(e: MouseEvent) {
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        let rect = elmnt.getBoundingClientRect();

        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {

        // TO BE REWORKED
        /*var rect = elmnt.getBoundingClientRect();
        let bodyRect = document.body.getBoundingClientRect();
        if (rect.bottom < bodyRect.height / 2) {
            elmnt.style.top = 10 - rect.height + "px";
        }
        if (rect.right <  bodyRect.width / 2) {
            elmnt.style.left = 10 - rect.width + "px";
        }*/
        // TO BE REWORKED

        document.onmouseup = null;
        document.onmousemove = null;
    }
}

function mobileDragElement(elmnt: HTMLElement) {
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    /* otherwise, move the DIV from anywhere inside the DIV:*/
    document.body.addEventListener('touchstart', touchStart);
    document.body.addEventListener('touchmove', touchMove);

    function touchStart(e: TouchEvent) {
        e.preventDefault();
        // get the mouse cursor position at startup:
        var touchLocation = e.targetTouches[0];

        pos3 = touchLocation.clientX;
        pos4 = touchLocation.clientY;

    }

    function touchMove(e: TouchEvent) {
        e.preventDefault();
        // calculate the new cursor position:
        var touchLocation = e.targetTouches[0];

        pos1 = pos3 - touchLocation.clientX;
        pos2 = pos4 - touchLocation.clientY;
        pos3 = touchLocation.clientX;
        pos4 = touchLocation.clientY;
        // set the element's new position:
        let rect = elmnt.getBoundingClientRect();

        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    }
}

function wheelEvent(event: WheelEvent) {
    event.preventDefault();
    zoom(event.deltaY, event.clientX, event.clientY);
}

function zoom(deltaY: number, clientX: number, clientY:number) {
    realScale += deltaY * -0.003;
    realScale = Math.min(Math.max(-2,realScale), 3);
    // Restrict scale
    scale = Math.min(Math.max(0, Math.exp(realScale)), 20);
    let oldRect = map.getBoundingClientRect();
    
    let oldRelativeMousePositionX = clientX - oldRect.left;
    let posFromCenterX = (oldRect.width / 2) - oldRelativeMousePositionX 
    
    let oldRelativeMousePositionY = clientY - oldRect.top;
    let posFromCenterY = (oldRect.height / 2) - oldRelativeMousePositionY
    // Apply scale transform
    map.style.transform = `scale(${scale})`;

    let newRect = map.getBoundingClientRect();

    let scaleRatioX = newRect.width / oldRect.width
    let scaleRatioY = newRect.height / oldRect.height

    let newPositionOffsetX = posFromCenterX * scaleRatioX
    let newPositionOffsetY = posFromCenterY * scaleRatioY

    
    map.style.left = (parseInt(map.style.left) + newPositionOffsetX - posFromCenterX) + "px"
    map.style.top = (parseInt(map.style.top) + newPositionOffsetY - posFromCenterY) + "px"
}
