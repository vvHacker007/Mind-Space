"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Noise = void 0;
const NoiseDelay_1 = require("./NoiseDelay");
class Noise {
    constructor() {
        this.delay = new NoiseDelay_1.NoiseDelay();
        this.enable = false;
    }
    load(data) {
        if (data === undefined) {
            return;
        }
        this.delay.load(data.delay);
        if (data.enable !== undefined) {
            this.enable = data.enable;
        }
    }
}
exports.Noise = Noise;
