"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.EmitterRate = void 0;
class EmitterRate {
    constructor() {
        this.quantity = 1;
        this.delay = 0.1;
    }
    load(data) {
        if (data === undefined) {
            return;
        }
        if (data.quantity !== undefined) {
            this.quantity = data.quantity;
        }
        if (data.delay !== undefined) {
            this.delay = data.delay;
        }
    }
}
exports.EmitterRate = EmitterRate;
