var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { movePlayer } from "./actions.js";
export function createSocket(game, map) {
    return __awaiter(this, void 0, void 0, function* () {
        const socket = new WebSocket('ws://'
            + window.location.host
            + '/ws/game/'
            + game.guild_id
            + '/');
        socket.onmessage = function (e) {
            const message = JSON.parse(e.data);
            const event = message.event;
            const data = message.data;
            game = message.new_game_data;
            switch (event) {
                case 'move':
                    let event = data;
                    movePlayer(event);
                    break;
            }
            ;
        };
        socket.onclose = function (e) {
            console.error('Chat socket closed unexpectedly');
        };
    });
}
