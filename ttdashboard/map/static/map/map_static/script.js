var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { registerGestures } from "./mapMouvement.js";
import { drawMap, fetchGame } from "./mapDrawing.js";
import { registerInteractions } from "./mapInteractions.js";
import { createSocket } from "./socket.js";
import { focusMap } from "./privateMap.js";
export const TILE_SIZE = 50;
var map = document.getElementById("map");
var game;
function main(map) {
    return __awaiter(this, void 0, void 0, function* () {
        registerGestures(map);
        game = yield fetchGame();
        yield drawMap(map, game);
        yield registerInteractions(map);
        // @ts-ignore
        if (is_public) {
            yield createSocket(game, map);
        }
        else {
            document.getElementById("background").style.background = "#333333";
        }
        // @ts-ignore
        if (is_focused) {
            focusMap(map, game.grid_size_x, game.grid_size_y);
        }
    });
}
main(map);
