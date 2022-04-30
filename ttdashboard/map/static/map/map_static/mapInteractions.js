var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
export function registerInteractions(map) {
    return __awaiter(this, void 0, void 0, function* () {
        let players = document.getElementsByClassName("player-canvas");
        for (let player of players) {
            player.addEventListener("mouseenter", canvasMouseEnter);
            player.addEventListener("mouseout", canvasMouseOut);
        }
    });
}
function canvasMouseEnter(event) {
    // @ts-ignore
    let element = event.target;
    let range = document.getElementById("range_" + element.getAttribute("coordinate"));
    range.style.backgroundColor = range.style.backgroundColor.replace(/[^,]+(?=\))/, '0.8');
    //range.style.border = "7px solid rgb(5, 5, 5)";
    range.style.zIndex = "2";
}
function canvasMouseOut(event) {
    // @ts-ignore
    let element = event.target;
    let range = document.getElementById("range_" + element.getAttribute("coordinate"));
    range.style.backgroundColor = range.style.backgroundColor.replace(/[^,]+(?=\))/, '0.2');
    //range.style.border = "3px solid rgb(5,5,5)";
    range.style.zIndex = "1";
}
