"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Attract = void 0;
class Attract {
    constructor() {
        this.distance = 200;
        this.duration = 0.4;
        this.speed = 1;
    }
    load(data) {
        if (data === undefined) {
            return;
        }
        if (data.distance !== undefined) {
            this.distance = data.distance;
        }
        if (data.duration !== undefined) {
            this.duration = data.duration;
        }
        if (data.speed !== undefined) {
            this.speed = data.speed;
        }
    }
}
exports.Attract = Attract;
